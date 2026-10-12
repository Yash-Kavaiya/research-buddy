#!/usr/bin/env python3
"""Chase citations backward and forward from one or more seed papers (OpenAlex).

Seeds are DOIs or OpenAlex work ids. With two or more seeds, references shared
by several seeds are reported as seminal-paper candidates.

Examples:
    python citation_graph.py 10.48550/arXiv.1706.03762
    python citation_graph.py 10.18653/v1/N19-1423 W2963403868 --top 15 --format md
"""

from __future__ import annotations

import argparse
import json
import sys
import time

sys.dont_write_bytecode = True  # keep the skill folder free of __pycache__

import _scholarly_api as api  # noqa: E402

BATCH = 50


def fetch_works(ids: list[str]) -> list[dict]:
    """Fetch OpenAlex works by id, in batches."""
    works: list[dict] = []
    for start in range(0, len(ids), BATCH):
        chunk = ids[start:start + BATCH]
        data = api.openalex_get("works", {"filter": "openalex_id:" + "|".join(chunk), "per-page": BATCH})
        works.extend(api.parse_openalex(data))
        time.sleep(0.15)
    return works


def fetch_citing(work_id: str, limit: int) -> list[dict]:
    data = api.openalex_get("works", {
        "filter": f"cites:{work_id}", "sort": "cited_by_count:desc", "per-page": min(limit, 200),
    })
    return api.parse_openalex(data)


def rank_seminal(references_by_seed: dict[str, list[dict]], top: int = 10) -> list[dict]:
    """Rank references by how many seeds cite them, then by citation count.

    A paper cited by most of the seeds is a shared foundation of the area.
    With a single seed this reduces to its most-cited references.
    """
    seen: dict[str, dict] = {}
    for seed, references in references_by_seed.items():
        for paper in references:
            entry = seen.setdefault(paper["id"], {**paper, "cited_by_seeds": []})
            if seed not in entry["cited_by_seeds"]:
                entry["cited_by_seeds"].append(seed)
    ranked = sorted(seen.values(), key=lambda p: (len(p["cited_by_seeds"]), p.get("citations") or 0), reverse=True)
    return ranked[:top]


def top_cited(papers: list[dict], top: int) -> list[dict]:
    return sorted(papers, key=lambda p: p.get("citations") or 0, reverse=True)[:top]


def explore(seed_ids: list[str], top: int, max_refs: int) -> dict:
    result = {"seeds": [], "seminal_candidates": []}
    references_by_seed: dict[str, list[dict]] = {}
    for raw in seed_ids:
        seed = api.openalex_work(raw)
        backward = fetch_works(seed.get("referenced_works", [])[:max_refs])
        forward = fetch_citing(seed["id"], top)
        references_by_seed[seed["id"]] = backward
        result["seeds"].append({
            "seed": {k: seed[k] for k in ("id", "title", "authors", "year", "venue", "doi", "citations")},
            "reference_count": len(seed.get("referenced_works", [])),
            "backward_top": top_cited(backward, top),
            "forward_top": forward,
        })
    result["seminal_candidates"] = rank_seminal(references_by_seed, top)
    return result


def to_markdown(result: dict) -> str:
    lines = []
    for block in result["seeds"]:
        seed = block["seed"]
        lines += [f"## Seed: {seed['title']} ({seed['year']})",
                  f"OpenAlex {seed['id']}, {seed['citations']} citations, {block['reference_count']} references", "",
                  "### Backward: most-cited references", api.to_markdown(block["backward_top"]), "",
                  "### Forward: most-cited citing papers", api.to_markdown(block["forward_top"]), ""]
    lines.append("## Seminal-paper candidates")
    for number, paper in enumerate(result["seminal_candidates"], 1):
        lines.append(f"{number}. **{paper['title']}** ({paper['year']}). {api.short_authors(paper['authors'])}. "
                     f"Cited by {len(paper['cited_by_seeds'])} of {len(result['seeds'])} seeds, "
                     f"{paper['citations']} citations overall. {paper['url']}")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("seeds", nargs="+", help="DOIs or OpenAlex work ids")
    parser.add_argument("--top", type=int, default=10, help="papers to list in each direction")
    parser.add_argument("--max-refs", type=int, default=200, help="references fetched per seed")
    parser.add_argument("--format", choices=("json", "md"), default="md")
    args = parser.parse_args()
    api.utf8_stdout()
    try:
        result = explore(args.seeds, args.top, args.max_refs)
    except api.ApiError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    print(to_markdown(result) if args.format == "md" else json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
