#!/usr/bin/env python3
"""Search arXiv, Semantic Scholar, OpenAlex, PubMed, and Crossref in one call.

Examples:
    python search_papers.py "retrieval augmented generation" --limit 10
    python search_papers.py "CRISPR off-target" --sources pubmed,openalex --year-from 2021 --format md --abstracts 300
    python search_papers.py "graph neural networks" --sort citations --out results.json
"""

from __future__ import annotations

import argparse
import json
import sys

sys.dont_write_bytecode = True  # keep the skill folder free of __pycache__

import _scholarly_api as api  # noqa: E402


def sort_papers(papers: list[dict], key: str) -> list[dict]:
    if key == "citations":
        return sorted(papers, key=lambda p: p.get("citations") or 0, reverse=True)
    if key == "year":
        return sorted(papers, key=lambda p: p.get("year") or 0, reverse=True)
    # relevance: papers found by more sources first, original order otherwise
    return sorted(papers, key=lambda p: len(p.get("sources") or []), reverse=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("query")
    parser.add_argument("--sources", default=",".join(api.SOURCES),
                        help=f"comma-separated subset of: {', '.join(api.SOURCES)}")
    parser.add_argument("--limit", type=int, default=10, help="results requested from each source")
    parser.add_argument("--year-from", type=int)
    parser.add_argument("--year-to", type=int)
    parser.add_argument("--sort", choices=("relevance", "citations", "year"), default="relevance")
    parser.add_argument("--format", choices=("json", "md"), default="json")
    parser.add_argument("--abstracts", type=int, default=0, help="md only: characters of abstract to show")
    parser.add_argument("--out", help="write to this file instead of stdout")
    args = parser.parse_args()
    api.utf8_stdout()

    sources = [s.strip() for s in args.sources.split(",") if s.strip()]
    papers, errors = api.search_all(args.query, sources=sources, limit=args.limit)
    papers = sort_papers(api.filter_years(papers, args.year_from, args.year_to), args.sort)

    if args.format == "md":
        text = api.to_markdown(papers, abstract_chars=args.abstracts)
        if errors:
            text += "\n\nSources that failed: " + "; ".join(f"{k} ({v})" for k, v in errors.items())
    else:
        text = json.dumps({"query": args.query, "count": len(papers), "errors": errors, "papers": papers},
                          indent=2, ensure_ascii=False)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as handle:
            handle.write(text + "\n")
        print(f"wrote {len(papers)} papers to {args.out}")
    else:
        print(text)
    for source, message in errors.items():
        print(f"warning: {source} failed: {message}", file=sys.stderr)
    return 0 if papers or not errors else 1


if __name__ == "__main__":
    sys.exit(main())
