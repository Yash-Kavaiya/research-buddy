#!/usr/bin/env python3
"""Mechanical pre-submission checks on a paper PDF.

Checks page count against a limit, page size, font embedding (Type 3 and
non-embedded fonts), document metadata, and, with --anonymous, signs of author
identity for double-blind review.

Examples:
    python check_pdf.py paper.pdf --max-pages 9 --paper letter
    python check_pdf.py paper.pdf --max-pages 8 --anonymous --names "Jane Doe,Example University,janedoe"

Needs pypdf. It does not judge margins, template compliance, or content; see SKILL.md for those.
"""

from __future__ import annotations

import argparse
import json
import re
import sys

PAPER_SIZES = {"letter": (612, 792), "a4": (595.28, 841.89)}
REFERENCES_RE = re.compile(r"^\s*(?:\d+\.?\s+)?(references|bibliography)\s*$", re.I | re.M)
ACK_RE = re.compile(r"^\s*(?:\d+\.?\s+)?acknowledge?ments?\s*$", re.I | re.M)
EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
REPO_RE = re.compile(r"(?:github\.com|gitlab\.com|bitbucket\.org|huggingface\.co)/[\w.-]+(?:/[\w.-]+)?", re.I)
SELF_REFERENCE_RE = re.compile(r"\b(?:our|my) (?:previous|prior|earlier|recent) (?:work|paper|study|results?)\b"
                               r"|\bwe (?:previously|have previously|recently) (?:showed|proposed|introduced|reported)\b", re.I)
ANONYMOUS_HOSTS = ("anonymous.4open.science", "anonymous.github")


def page_size_name(width: float, height: float, tolerance: float = 2.0) -> str:
    for name, (w, h) in PAPER_SIZES.items():
        if abs(width - w) <= tolerance and abs(height - h) <= tolerance:
            return name
    return f"custom ({width:.0f} x {height:.0f} pt)"


def find_references_page(page_texts: list[str]) -> int | None:
    """1-based number of the first page with a References or Bibliography heading on its own line."""
    for number, text in enumerate(page_texts, 1):
        if REFERENCES_RE.search(text):
            return number
    return None


def anonymity_findings(page_texts: list[str], metadata: dict, names: list[str]) -> list[dict]:
    """Things that may reveal author identity. Each finding has page (0 for metadata), kind, and text."""
    findings = []
    author = (metadata.get("author") or "").strip()
    if author and author.lower() not in ("anonymous", "anonymous authors", "anonymous author(s)"):
        findings.append({"page": 0, "kind": "metadata author", "text": author})
    for number, text in enumerate(page_texts, 1):
        for name in names:
            if name and re.search(re.escape(name), text, re.I):
                findings.append({"page": number, "kind": "listed name", "text": name})
        if ACK_RE.search(text):
            findings.append({"page": number, "kind": "acknowledgements section", "text": "Acknowledgements heading"})
        for email in sorted(set(EMAIL_RE.findall(text))):
            findings.append({"page": number, "kind": "email address", "text": email})
        for repo in sorted(set(REPO_RE.findall(text))):
            if not any(host in repo.lower() for host in ANONYMOUS_HOSTS):
                findings.append({"page": number, "kind": "repository link", "text": repo})
        for match in SELF_REFERENCE_RE.finditer(text):
            findings.append({"page": number, "kind": "first-person self-reference", "text": match.group(0)})
    for name in names:
        for field, value in metadata.items():
            if name and value and re.search(re.escape(name), str(value), re.I):
                findings.append({"page": 0, "kind": f"listed name in metadata {field}", "text": name})
    return findings


def font_report(reader) -> list[dict]:
    """Every font used, with its subtype and whether a font program is embedded."""
    fonts: dict[str, dict] = {}

    def embedded(font) -> bool:
        if font.get("/Subtype") == "/Type3":
            return True  # Type 3 glyphs are defined inline; flagged separately
        descriptor = font.get("/FontDescriptor")
        if descriptor is None and "/DescendantFonts" in font:
            descendant = font["/DescendantFonts"][0].get_object()
            descriptor = descendant.get("/FontDescriptor")
        if descriptor is None:
            return False
        descriptor = descriptor.get_object()
        return any(key in descriptor for key in ("/FontFile", "/FontFile2", "/FontFile3"))

    def walk(resources, depth=0):
        if resources is None or depth > 4:
            return
        resources = resources.get_object()
        for font_ref in (resources.get("/Font") or {}).values():
            font = font_ref.get_object()
            name = str(font.get("/BaseFont", "/unnamed")).lstrip("/")
            fonts[name] = {"name": name, "subtype": str(font.get("/Subtype", "")).lstrip("/"),
                           "embedded": embedded(font)}
        for xobject in (resources.get("/XObject") or {}).values():
            xobject = xobject.get_object()
            if xobject.get("/Subtype") == "/Form":
                walk(xobject.get("/Resources"), depth + 1)

    for page in reader.pages:
        walk(page.get("/Resources"))
    return sorted(fonts.values(), key=lambda f: f["name"])


def check(path: str, max_pages: int | None = None, paper: str | None = None, anonymous: bool = False,
          names: list[str] | None = None) -> dict:
    from pypdf import PdfReader

    reader = PdfReader(path)
    page_texts = [(page.extract_text() or "") for page in reader.pages]
    info = reader.metadata or {}
    metadata = {"title": info.get("/Title"), "author": info.get("/Author"), "creator": info.get("/Creator"),
                "producer": info.get("/Producer"), "subject": info.get("/Subject"), "keywords": info.get("/Keywords")}
    sizes = sorted({page_size_name(float(p.mediabox.width), float(p.mediabox.height)) for p in reader.pages})
    fonts = font_report(reader)
    references_page = find_references_page(page_texts)

    problems, warnings = [], []
    pages = len(reader.pages)
    if max_pages is not None:
        content_pages = references_page if references_page else pages
        if references_page is None:
            warnings.append("no References heading found; the page limit was compared with the total page count")
        if content_pages > max_pages:
            problems.append(f"content runs to page {content_pages}, over the limit of {max_pages} "
                            f"(references start on page {references_page})" if references_page else
                            f"{pages} pages, over the limit of {max_pages}")
        elif references_page == max_pages:
            warnings.append(f"references start on page {references_page}, the last allowed content page; "
                            "confirm whether the limit excludes references")
    if paper and sizes != [paper]:
        problems.append(f"page size is {', '.join(sizes)}; expected {paper}")
    type3 = [f["name"] for f in fonts if f["subtype"] == "Type3"]
    missing = [f["name"] for f in fonts if not f["embedded"]]
    if type3:
        problems.append(f"Type 3 fonts present ({', '.join(type3)}); usually from matplotlib figures, "
                        "set pdf.fonttype to 42 and regenerate")
    if missing:
        problems.append(f"fonts not embedded: {', '.join(missing)}")
    if not any(text.strip() for text in page_texts):
        warnings.append("no extractable text; the PDF may be scanned or image-only, so text checks were skipped")

    identity = anonymity_findings(page_texts, metadata, names or []) if anonymous else []
    if identity:
        problems.append(f"{len(identity)} possible identity leaks for double-blind review (see anonymity)")
    if not anonymous and not (metadata.get("title") or "").strip():
        warnings.append("PDF metadata has no title; camera-ready versions should set title and authors")

    return {"file": path, "pages": pages, "references_start_page": references_page, "page_sizes": sizes,
            "metadata": metadata, "fonts": fonts, "anonymity": identity, "problems": problems,
            "warnings": warnings, "passed": not problems}


def to_text(result: dict) -> str:
    lines = [f"{result['file']}: {'PASS' if result['passed'] else 'FAIL'}",
             f"  pages: {result['pages']} (references start on page {result['references_start_page'] or 'not found'})",
             f"  page size: {', '.join(result['page_sizes'])}",
             f"  fonts: {len(result['fonts'])} "
             f"({sum(1 for f in result['fonts'] if f['embedded'])} embedded, "
             f"{sum(1 for f in result['fonts'] if f['subtype'] == 'Type3')} Type 3)",
             "  metadata: " + ", ".join(f"{k}={v!r}" for k, v in result["metadata"].items() if v)]
    lines += [f"  PROBLEM: {p}" for p in result["problems"]]
    lines += [f"  warning: {w}" for w in result["warnings"]]
    lines += [f"  anonymity (page {f['page'] or 'metadata'}): {f['kind']}: {f['text']}" for f in result["anonymity"]]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("pdf")
    parser.add_argument("--max-pages", type=int, help="page limit for content (references are treated as excluded)")
    parser.add_argument("--paper", choices=sorted(PAPER_SIZES), help="required page size")
    parser.add_argument("--anonymous", action="store_true", help="check for identity leaks (double-blind review)")
    parser.add_argument("--names", default="", help="comma-separated author names, institutions, and usernames to search for")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args()
    for stream in (sys.stdout, sys.stderr):
        stream.reconfigure(encoding="utf-8", errors="replace")
    result = check(args.pdf, args.max_pages, args.paper, args.anonymous,
                   [n.strip() for n in args.names.split(",") if n.strip()])
    print(json.dumps(result, indent=2, ensure_ascii=False) if args.format == "json" else to_text(result))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
