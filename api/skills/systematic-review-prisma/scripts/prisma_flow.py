#!/usr/bin/env python3
"""Record handling and flow-diagram numbers for a PRISMA 2020 systematic review.

Subcommands:
    dedupe   merge database exports (CSV or RIS), remove duplicates, write a screening sheet
    tally    count decisions in a completed screening sheet and build the flow counts
    diagram  check the flow counts add up and draw the PRISMA flow diagram (Mermaid or TikZ)

Examples:
    python prisma_flow.py dedupe pubmed.ris scopus.csv wos.csv --out screening.csv --counts counts.json
    python prisma_flow.py tally screening.csv --counts counts.json
    python prisma_flow.py diagram counts.json --format mermaid
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path

SHEET_COLUMNS = ["id", "title", "authors", "year", "venue", "doi", "source", "abstract",
                 "title_abstract_decision", "fulltext_decision", "exclusion_reason", "notes"]
ALIASES = {
    "title": ("title", "article title", "ti", "document title"),
    "authors": ("authors", "author", "au", "author names"),
    "year": ("year", "publication year", "py", "pubyear"),
    "venue": ("venue", "journal", "source title", "publication name", "so", "jo"),
    "doi": ("doi", "di", "do"),
    "abstract": ("abstract", "ab"),
}


def normalize_title(title: str) -> str:
    text = unicodedata.normalize("NFKD", title or "")
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    return " ".join(re.sub(r"[^a-z0-9]+", " ", text.lower()).split())


def normalize_doi(doi: str) -> str:
    doi = re.sub(r"^(https?://(dx\.)?doi\.org/|doi:\s*)", "", (doi or "").strip().lower())
    return doi.rstrip(".,; ")


def read_csv_records(path: Path) -> list[dict]:
    with open(path, newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))
    records = []
    for row in rows:
        lowered = {(k or "").strip().lower(): (v or "").strip() for k, v in row.items()}
        record = {field: next((lowered[a] for a in names if lowered.get(a)), "") for field, names in ALIASES.items()}
        record["source"] = lowered.get("source") or lowered.get("database") or path.stem
        records.append(record)
    return records


def read_ris_records(path: Path) -> list[dict]:
    tags = {"TI": "title", "T1": "title", "PY": "year", "Y1": "year", "DO": "doi", "AB": "abstract",
            "JO": "venue", "JF": "venue", "T2": "venue"}
    records, current, authors = [], {}, []
    for line in path.read_text(encoding="utf-8-sig", errors="replace").splitlines():
        match = re.match(r"^([A-Z][A-Z0-9])\s{2}-\s?(.*)$", line)
        if not match:
            continue
        tag, value = match.group(1), match.group(2).strip()
        if tag == "ER":
            if current or authors:
                current["authors"] = "; ".join(authors)
                current["source"] = path.stem
                current["year"] = (re.findall(r"\d{4}", current.get("year", "")) or [""])[0]
                records.append({field: current.get(field, "") for field in (*ALIASES, "source")})
            current, authors = {}, []
        elif tag in ("AU", "A1"):
            authors.append(value)
        elif tag in tags and not current.get(tags[tag]):
            current[tags[tag]] = value
    return records


def read_records(path: Path) -> list[dict]:
    return read_ris_records(path) if path.suffix.lower() in (".ris", ".txt") else read_csv_records(path)


def dedupe_records(records: list[dict]) -> tuple[list[dict], int]:
    """Drop later records that share a DOI or a normalized title with an earlier one."""
    seen: set[str] = set()
    kept = []
    for record in records:
        keys = set()
        if normalize_doi(record.get("doi", "")):
            keys.add("doi:" + normalize_doi(record["doi"]))
        if normalize_title(record.get("title", "")):
            keys.add("title:" + normalize_title(record["title"]))
        if keys & seen:
            continue
        seen |= keys
        kept.append(record)
    return kept, len(records) - len(kept)


def tally_decisions(rows: list[dict]) -> dict:
    """Count screening decisions. Decisions are include, exclude, or (full text only) not_retrieved."""
    def decision(row: dict, column: str) -> str:
        return (row.get(column) or "").strip().lower().replace(" ", "_")

    undecided = [r.get("id", "?") for r in rows if decision(r, "title_abstract_decision") not in ("include", "exclude")]
    if undecided:
        raise ValueError(f"{len(undecided)} records have no title/abstract decision (first ids: {undecided[:5]})")
    passed = [r for r in rows if decision(r, "title_abstract_decision") == "include"]
    pending = [r.get("id", "?") for r in passed
               if decision(r, "fulltext_decision") not in ("include", "exclude", "not_retrieved")]
    if pending:
        raise ValueError(f"{len(pending)} records passed screening but have no full-text decision "
                         f"(first ids: {pending[:5]})")
    excluded = [r for r in passed if decision(r, "fulltext_decision") == "exclude"]
    no_reason = [r.get("id", "?") for r in excluded if not (r.get("exclusion_reason") or "").strip()]
    if no_reason:
        raise ValueError(f"{len(no_reason)} full-text exclusions have no exclusion_reason (first ids: {no_reason[:5]})")
    not_retrieved = sum(1 for r in passed if decision(r, "fulltext_decision") == "not_retrieved")
    reasons = Counter((r["exclusion_reason"]).strip() for r in excluded)
    return {
        "screened": len(rows),
        "excluded_screening": len(rows) - len(passed),
        "sought_retrieval": len(passed),
        "not_retrieved": not_retrieved,
        "assessed_eligibility": len(passed) - not_retrieved,
        "excluded_fulltext": dict(reasons.most_common()),
        "included": sum(1 for r in passed if decision(r, "fulltext_decision") == "include"),
    }


def check_counts(counts: dict) -> list[str]:
    """Return a list of arithmetic inconsistencies in the flow counts (empty when consistent)."""
    problems = []
    identified = sum(counts.get("identified", {}).values())
    removed = counts.get("duplicates_removed", 0) + counts.get("removed_other", 0)
    checks = [
        ("screened", identified - removed, "identified minus records removed before screening"),
        ("sought_retrieval", counts.get("screened", 0) - counts.get("excluded_screening", 0),
         "screened minus excluded at screening"),
        ("assessed_eligibility", counts.get("sought_retrieval", 0) - counts.get("not_retrieved", 0),
         "sought for retrieval minus not retrieved"),
        ("included", counts.get("assessed_eligibility", 0) - sum(counts.get("excluded_fulltext", {}).values()),
         "assessed minus full-text exclusions"),
    ]
    for key, expected, rule in checks:
        if key not in counts:
            problems.append(f"missing count: {key}")
        elif counts[key] != expected:
            problems.append(f"{key} is {counts[key]} but {rule} gives {expected}")
    return problems


def _boxes(counts: dict) -> dict[str, str]:
    identified = counts.get("identified", {})
    databases = "; ".join(f"{name} (n = {n})" for name, n in identified.items())
    reasons = "; ".join(f"{reason} (n = {n})" for reason, n in counts.get("excluded_fulltext", {}).items())
    removed_other = counts.get("removed_other", 0)
    return {
        "identified": f"Records identified (n = {sum(identified.values())}): {databases}",
        "removed": f"Records removed before screening: duplicates (n = {counts.get('duplicates_removed', 0)})"
                   + (f"; other reasons (n = {removed_other})" if removed_other else ""),
        "screened": f"Records screened (n = {counts['screened']})",
        "excluded": f"Records excluded (n = {counts['excluded_screening']})",
        "sought": f"Reports sought for retrieval (n = {counts['sought_retrieval']})",
        "not_retrieved": f"Reports not retrieved (n = {counts['not_retrieved']})",
        "assessed": f"Reports assessed for eligibility (n = {counts['assessed_eligibility']})",
        "ft_excluded": f"Reports excluded (n = {sum(counts.get('excluded_fulltext', {}).values())})"
                       + (f": {reasons}" if reasons else ""),
        "included": f"Studies included in review (n = {counts['included']})",
    }


def to_mermaid(counts: dict) -> str:
    b = _boxes(counts)
    q = lambda text: '"' + text.replace('"', "'") + '"'  # noqa: E731
    return "\n".join([
        "flowchart TD",
        f"    A[{q(b['identified'])}] --> B[{q(b['screened'])}]",
        f"    A --> A2[{q(b['removed'])}]",
        f"    B --> C[{q(b['sought'])}]",
        f"    B --> B2[{q(b['excluded'])}]",
        f"    C --> D[{q(b['assessed'])}]",
        f"    C --> C2[{q(b['not_retrieved'])}]",
        f"    D --> E[{q(b['included'])}]",
        f"    D --> D2[{q(b['ft_excluded'])}]",
    ])


def to_tikz(counts: dict) -> str:
    b = {key: text.replace("&", r"\&").replace("%", r"\%").replace("_", r"\_") for key, text in _boxes(counts).items()}
    return "\n".join([
        r"% Requires \usepackage{tikz} and \usetikzlibrary{positioning,arrows.meta}",
        r"\begin{tikzpicture}[node distance=8mm and 12mm,",
        r"  box/.style={draw, rounded corners=2pt, align=left, text width=62mm, font=\small, inner sep=5pt},",
        r"  side/.style={box, text width=55mm}, arrow/.style={-{Latex[length=2mm]}}]",
        rf"  \node[box] (identified) {{{b['identified']}}};",
        rf"  \node[side, right=of identified] (removed) {{{b['removed']}}};",
        rf"  \node[box, below=of identified] (screened) {{{b['screened']}}};",
        rf"  \node[side, right=of screened] (excluded) {{{b['excluded']}}};",
        rf"  \node[box, below=of screened] (sought) {{{b['sought']}}};",
        rf"  \node[side, right=of sought] (notretrieved) {{{b['not_retrieved']}}};",
        rf"  \node[box, below=of sought] (assessed) {{{b['assessed']}}};",
        rf"  \node[side, right=of assessed] (ftexcluded) {{{b['ft_excluded']}}};",
        rf"  \node[box, below=of assessed] (included) {{{b['included']}}};",
        r"  \draw[arrow] (identified) -- (screened);  \draw[arrow] (identified) -- (removed);",
        r"  \draw[arrow] (screened) -- (sought);      \draw[arrow] (screened) -- (excluded);",
        r"  \draw[arrow] (sought) -- (assessed);      \draw[arrow] (sought) -- (notretrieved);",
        r"  \draw[arrow] (assessed) -- (included);    \draw[arrow] (assessed) -- (ftexcluded);",
        r"\end{tikzpicture}",
    ])


def cmd_dedupe(args) -> int:
    records, per_source = [], {}
    for name in args.files:
        found = read_records(Path(name))
        per_source[found[0]["source"] if found else Path(name).stem] = len(found)
        records.extend(found)
    kept, duplicates = dedupe_records(records)
    with open(args.out, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=SHEET_COLUMNS)
        writer.writeheader()
        for number, record in enumerate(kept, 1):
            writer.writerow({**{c: "" for c in SHEET_COLUMNS}, **record, "id": number})
    counts = {"identified": per_source, "duplicates_removed": duplicates}
    if args.counts:
        Path(args.counts).write_text(json.dumps(counts, indent=2), encoding="utf-8")
    print(json.dumps({**counts, "records_to_screen": len(kept), "screening_sheet": args.out}, indent=2))
    return 0


def cmd_tally(args) -> int:
    with open(args.sheet, newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))
    try:
        tallied = tally_decisions(rows)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    counts = json.loads(Path(args.counts).read_text(encoding="utf-8")) if args.counts and Path(args.counts).exists() else {}
    counts.update(tallied)
    if args.counts:
        Path(args.counts).write_text(json.dumps(counts, indent=2), encoding="utf-8")
    print(json.dumps(counts, indent=2))
    return 0


def cmd_diagram(args) -> int:
    counts = json.loads(Path(args.counts).read_text(encoding="utf-8"))
    problems = check_counts(counts)
    if problems:
        for problem in problems:
            print(f"error: {problem}", file=sys.stderr)
        return 1
    print(to_tikz(counts) if args.format == "tikz" else to_mermaid(counts))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("dedupe", help="merge exports and remove duplicates")
    p.add_argument("files", nargs="+", help="CSV or RIS exports, one per database")
    p.add_argument("--out", default="screening.csv")
    p.add_argument("--counts", help="write identification counts to this JSON file")
    p.set_defaults(func=cmd_dedupe)
    p = sub.add_parser("tally", help="count decisions in the screening sheet")
    p.add_argument("sheet")
    p.add_argument("--counts", help="JSON file from dedupe; updated in place with screening counts")
    p.set_defaults(func=cmd_tally)
    p = sub.add_parser("diagram", help="validate counts and draw the flow diagram")
    p.add_argument("counts")
    p.add_argument("--format", choices=("mermaid", "tikz"), default="mermaid")
    p.set_defaults(func=cmd_diagram)
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
