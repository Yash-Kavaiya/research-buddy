#!/usr/bin/env python3
"""Find the prior work closest to a research idea.

Runs several query phrasings across the scholarly APIs, merges the results,
and ranks them by term overlap with the idea and by how many phrasings found
them. The ranking is a shortlist for reading, not a verdict on novelty.

Example:
    python closest_work.py --idea "Use contrastive pretraining on ECG signals to detect arrhythmia with few labels" \
        --query "contrastive learning ECG" --query "self-supervised arrhythmia detection" \
        --query "few-shot ECG classification" --top 15
"""

from __future__ import annotations

import argparse
import json
import math
import re
import sys

sys.dont_write_bytecode = True  # keep the skill folder free of __pycache__

import _scholarly_api as api  # noqa: E402

STOPWORDS = set("""a an and are as at be by can do for from has have how in into is it its more most of on or our
that the their this to using use used via we with which while what when where new novel approach method methods
based paper study propose proposed results show towards toward""".split())


def content_terms(text: str) -> list[str]:
    return [w for w in re.findall(r"[a-z0-9]+", (text or "").lower()) if len(w) > 2 and w not in STOPWORDS]


def overlap_score(idea_terms: set[str], paper: dict) -> tuple[float, list[str]]:
    """Share of the idea's terms found in the paper's title or abstract (title counts double)."""
    if not idea_terms:
        return 0.0, []
    title = set(content_terms(paper.get("title", "")))
    abstract = set(content_terms(paper.get("abstract", "")))
    matched = idea_terms & (title | abstract)
    weight = sum(2 if term in title else 1 for term in matched)
    return weight / (2 * len(idea_terms)), sorted(matched)


def rank_closest(idea: str, papers_by_query: dict[str, list[dict]], top: int = 15) -> list[dict]:
    idea_terms = set(content_terms(idea))
    hits: dict[int, list[str]] = {}
    merged = api.dedupe([paper for papers in papers_by_query.values() for paper in papers])
    # dedupe keeps the first record, so recover which queries found each paper
    for paper in merged:
        keys = {api.normalize_doi(paper["doi"]), api.normalize_title(paper["title"])} - {""}
        found = []
        for query, papers in papers_by_query.items():
            if any({api.normalize_doi(p["doi"]), api.normalize_title(p["title"])} & keys for p in papers):
                found.append(query)
        hits[id(paper)] = found

    ranked = []
    for paper in merged:
        overlap, matched = overlap_score(idea_terms, paper)
        queries = hits[id(paper)]
        score = overlap * (1 + math.log(len(queries))) if queries else overlap
        ranked.append({**paper, "overlap": round(overlap, 3), "matched_terms": matched,
                       "found_by_queries": queries, "score": round(score, 3)})
    ranked.sort(key=lambda p: (p["score"], p.get("citations") or 0), reverse=True)
    return ranked[:top]


def to_markdown(idea: str, ranked: list[dict]) -> str:
    lines = [f"Idea: {idea}", ""]
    for number, paper in enumerate(ranked, 1):
        lines.append(f"{number}. **{paper['title']}** ({paper.get('year') or 'n.d.'}). "
                     f"{api.short_authors(paper['authors'])}. {paper.get('url', '')}")
        lines.append(f"   overlap {paper['overlap']:.0%}, found by {len(paper['found_by_queries'])} "
                     f"quer{'y' if len(paper['found_by_queries']) == 1 else 'ies'}; "
                     f"shared terms: {', '.join(paper['matched_terms']) or 'none'}")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--idea", required=True, help="one or two sentences stating the idea")
    parser.add_argument("--query", action="append", required=True, help="a search phrasing; repeat 3 to 6 times")
    parser.add_argument("--sources", default="arxiv,openalex,semantic_scholar,crossref")
    parser.add_argument("--limit", type=int, default=15, help="results per source per query")
    parser.add_argument("--top", type=int, default=15)
    parser.add_argument("--format", choices=("json", "md"), default="md")
    args = parser.parse_args()
    api.utf8_stdout()

    sources = [s.strip() for s in args.sources.split(",") if s.strip()]
    papers_by_query, failures = {}, {}
    for query in args.query:
        papers, errors = api.search_all(query, sources=sources, limit=args.limit)
        papers_by_query[query] = papers
        for source, message in errors.items():
            failures.setdefault(source, message)
    ranked = rank_closest(args.idea, papers_by_query, args.top)
    if args.format == "md":
        print(to_markdown(args.idea, ranked))
    else:
        print(json.dumps({"idea": args.idea, "errors": failures, "closest": ranked}, indent=2, ensure_ascii=False))
    for source, message in failures.items():
        print(f"warning: {source} failed for at least one query: {message}", file=sys.stderr)
    return 0 if ranked else 1


if __name__ == "__main__":
    sys.exit(main())
