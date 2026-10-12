#!/usr/bin/env python3
"""Clean, de-duplicate, and check a BibTeX file.

What it does:
  - normalizes entry types, field names, whitespace, DOIs, and page ranges (123-130 becomes 123--130)
  - protects acronyms and mixed-case words in titles with braces ({BERT}, {ImageNet})
  - removes empty fields and bulky fields (abstract, file, keywords by default)
  - merges duplicate entries (same DOI, or same title and year) and reports the key mapping
  - reports missing required fields and preprints that may have a published version
  - optionally fills missing DOIs from Crossref (--fill-doi) and regenerates keys (--rekey)

Examples:
    python clean_bibtex.py refs.bib --out refs.clean.bib
    python clean_bibtex.py refs.bib --out refs.clean.bib --fill-doi --report report.json
    python clean_bibtex.py refs.bib --out refs.clean.bib --rekey --sort
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time

sys.dont_write_bytecode = True  # keep the skill folder free of __pycache__

import _scholarly_api as api  # noqa: E402

REQUIRED = {
    "article": ["author", "title", "journal", "year"],
    "inproceedings": ["author", "title", "booktitle", "year"],
    "conference": ["author", "title", "booktitle", "year"],
    "book": ["title", "publisher", "year"],
    "incollection": ["author", "title", "booktitle", "publisher", "year"],
    "phdthesis": ["author", "title", "school", "year"],
    "mastersthesis": ["author", "title", "school", "year"],
    "techreport": ["author", "title", "institution", "year"],
    "misc": ["title"],
}
DEFAULT_STRIP = "abstract,file,keywords"
SKIP_WORDS = {"a", "an", "the", "on", "of", "in", "for", "to", "and", "with", "from", "towards", "toward", "is", "are"}


def protect_title(title: str) -> str:
    """Brace words whose capitalisation BibTeX styles would otherwise lowercase.

    A word is protected when it has a capital after its first letter (BERT,
    ImageNet, mRNA) and is not already inside braces. A leading capital alone
    is left for the style to handle.
    """
    out, depth = [], 0
    for token in re.split(r"(\s+)", title):
        if depth == 0 and not token.isspace() and "{" not in token and "\\" not in token and "$" not in token:
            core = token.strip(".,:;!?()[]\"'`")
            if core and re.search(r"[A-Z]", core[1:]) and re.search(r"[A-Za-z]", core):
                token = token.replace(core, "{" + core + "}", 1)
        depth += token.count("{") - token.count("}")
        out.append(token)
    return "".join(out)


def clean_entry(entry: dict, strip: set[str]) -> dict:
    fields = {}
    for name, value in entry["fields"].items():
        value = " ".join(value.split())
        if not value or name in strip:
            continue
        fields[name] = value
    if "doi" in fields:
        fields["doi"] = api.normalize_doi(fields["doi"])
        if api.normalize_doi(fields.get("url", "")) == fields["doi"]:
            del fields["url"]  # the URL only repeats the DOI
    if "pages" in fields:
        fields["pages"] = re.sub(r"\s*[-–—]+\s*", "--", fields["pages"])
    if "title" in fields:
        fields["title"] = protect_title(fields["title"])
    if "year" in fields:
        year = re.search(r"\d{4}", fields["year"])
        fields["year"] = year.group(0) if year else fields["year"]
    return {"type": entry["type"], "key": entry["key"], "fields": fields}


def duplicate_key(entry: dict) -> list[str]:
    keys = []
    fields = entry["fields"]
    if fields.get("doi"):
        keys.append("doi:" + fields["doi"])
    if fields.get("title"):
        keys.append("title:" + api.normalize_title(fields["title"]) + "|" + fields.get("year", ""))
    return keys


def merge_duplicates(entries: list[dict]) -> tuple[list[dict], dict[str, str]]:
    """Keep one entry per work. Returns (entries, {removed key: kept key}).

    The entry with more fields is kept (a published version beats a preprint
    only if it is the fuller record), and fields it lacks are copied from the duplicate.
    """
    kept: list[dict] = []
    index: dict[str, dict] = {}
    mapping: dict[str, str] = {}
    for entry in entries:
        keys = duplicate_key(entry)
        existing = next((index[k] for k in keys if k in index), None)
        if existing is None:
            kept.append(entry)
            target = entry
        else:
            if len(entry["fields"]) > len(existing["fields"]):
                existing["fields"], entry["fields"] = entry["fields"], existing["fields"]
                existing["type"] = entry["type"]
            for name, value in entry["fields"].items():
                existing["fields"].setdefault(name, value)
            if entry["key"] != existing["key"]:
                mapping[entry["key"]] = existing["key"]
            target = existing
        for key in keys + duplicate_key(target):
            index[key] = target
    return kept, mapping


def make_key(entry: dict) -> str:
    """authorYEARfirstword, e.g. vaswani2017attention."""
    fields = entry["fields"]
    people = api.bib_authors(fields.get("author") or fields.get("editor") or "")
    author = api.surname(people[0]).replace(" ", "") if people else "anon"
    words = [w for w in api.normalize_title(fields.get("title", "")).split() if w not in SKIP_WORDS]
    return f"{author}{fields.get('year', '')}{words[0] if words else ''}"


def rekey(entries: list[dict]) -> dict[str, str]:
    """Assign generated keys in place; collisions get a, b, c. Returns {old key: new key} for changed keys."""
    used: dict[str, int] = {}
    mapping = {}
    for entry in entries:
        base = make_key(entry)
        count = used.get(base, 0)
        used[base] = count + 1
        new = base if count == 0 else base + "abcdefghijklmnopqrstuvwxyz"[min(count, 25)]
        if new != entry["key"]:
            mapping[entry["key"]] = new
        entry["key"] = new
    return mapping


def check_entry(entry: dict) -> list[str]:
    problems = []
    fields = entry["fields"]
    for name in REQUIRED.get(entry["type"], []):
        if name not in fields and not (name == "author" and "editor" in fields):
            problems.append(f"missing {name}")
    venue = (fields.get("journal", "") + " " + fields.get("howpublished", "") + " " + fields.get("booktitle", "")).lower()
    if "arxiv" in venue or fields.get("archiveprefix", "").lower() == "arxiv" or "arxiv" in fields.get("doi", ""):
        problems.append("preprint: check whether a published version exists and cite that instead")
    if re.search(r"\bet al\b", fields.get("author", "")):
        problems.append("author list contains 'et al'; list all authors")
    if "year" in fields and not re.fullmatch(r"\d{4}", fields["year"]):
        problems.append(f"unusual year: {fields['year']}")
    return problems


def fill_doi(entry: dict) -> str | None:
    """Look the title up in Crossref; accept a DOI only on a near-exact title and matching year."""
    fields = entry["fields"]
    if fields.get("doi") or not fields.get("title"):
        return None
    people = api.bib_authors(fields.get("author", ""))
    query = fields["title"] + (" " + api.surname(people[0]) if people else "")
    for candidate in api.search_crossref(query, limit=3):
        same_title = api.title_similarity(candidate["title"], fields["title"]) >= 0.9
        year = fields.get("year", "")
        same_year = not year.isdigit() or candidate["year"] is None or abs(candidate["year"] - int(year)) <= 1
        if same_title and same_year and candidate["doi"]:
            return candidate["doi"]
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("bibfile")
    parser.add_argument("--out", required=True, help="cleaned file to write (never the input file)")
    parser.add_argument("--strip", default=DEFAULT_STRIP, help=f"fields to drop (default {DEFAULT_STRIP}); '' keeps all")
    parser.add_argument("--fill-doi", action="store_true", help="look up missing DOIs in Crossref (network)")
    parser.add_argument("--rekey", action="store_true", help="regenerate keys as authorYEARword (changes \\cite keys)")
    parser.add_argument("--sort", action="store_true", help="sort entries by key")
    parser.add_argument("--report", help="write the JSON report here")
    args = parser.parse_args()
    api.utf8_stdout()
    if args.out == args.bibfile:
        print("error: --out must differ from the input so the original is kept", file=sys.stderr)
        return 1

    with open(args.bibfile, encoding="utf-8-sig") as handle:
        parsed = api.parse_bibtex(handle.read())
    strip = {s.strip().lower() for s in args.strip.split(",") if s.strip()}
    entries = [clean_entry(e, strip) for e in parsed]
    entries, merged = merge_duplicates(entries)

    filled = {}
    if args.fill_doi:
        for entry in entries:
            try:
                doi = fill_doi(entry)
            except api.ApiError as exc:
                print(f"warning: Crossref lookup failed for {entry['key']}: {exc}", file=sys.stderr)
                continue
            if doi:
                entry["fields"]["doi"] = doi
                filled[entry["key"]] = doi
            time.sleep(0.2)

    rekeyed = rekey(entries) if args.rekey else {}
    if args.sort:
        entries.sort(key=lambda e: e["key"].lower())
    problems = {e["key"]: check_entry(e) for e in entries if check_entry(e)}

    with open(args.out, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(api.format_bibtex(entries))
    report = {"entries_in": len(parsed), "entries_out": len(entries), "duplicates_merged": merged,
              "dois_filled": filled, "keys_changed": rekeyed, "problems": problems}
    text = json.dumps(report, indent=2, ensure_ascii=False)
    if args.report:
        with open(args.report, "w", encoding="utf-8") as handle:
            handle.write(text + "\n")
    print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
