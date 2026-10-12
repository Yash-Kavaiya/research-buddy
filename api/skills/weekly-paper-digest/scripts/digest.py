#!/usr/bin/env python3
"""Build a digest of new papers for saved search queries.

Queries arXiv (newest submissions) and OpenAlex (by publication date), keeps
papers from the last N days, drops papers already reported in earlier digests
(tracked in a state file), and writes a Markdown digest.

Examples:
    python digest.py --query "retrieval augmented generation" --query "cat:cs.CL AND all:hallucination" --days 7
    python digest.py --config digest.json --out digests/2026-03-09.md

Config file (JSON):
    {"queries": ["retrieval augmented generation", "cat:cs.CL AND all:hallucination"],
     "days": 7, "sources": ["arxiv", "openalex"], "max_per_query": 15,
     "boost": ["benchmark", "survey"], "state": "digest-seen.json"}
"""

from __future__ import annotations

import argparse
import datetime
import json
import sys
import time
from pathlib import Path

sys.dont_write_bytecode = True  # keep the skill folder free of __pycache__

import _scholarly_api as api  # noqa: E402


def paper_key(paper: dict) -> str:
    return paper.get("doi") or (f"{paper['source']}:{paper['id']}" if paper.get("id") else
                                "title:" + api.normalize_title(paper.get("title")))


def is_recent(paper: dict, cutoff: datetime.date, today: datetime.date | None = None) -> bool:
    """True when the publication date is between the cutoff and today.

    Undated papers are dropped, and so are future-dated records, which are
    indexing errors or advance listings.
    """
    published = (paper.get("published") or "")[:10]
    try:
        date = datetime.date.fromisoformat(published)
    except ValueError:
        return False
    return cutoff <= date <= (today or datetime.date.today())


def fetch(query: str, source: str, cutoff: datetime.date, limit: int) -> list[dict]:
    if source == "arxiv":
        return api.search_arxiv(query, limit=limit, sort_by="submittedDate")
    if source == "openalex":
        plain = " ".join(part.split(":", 1)[-1] for part in query.replace(" AND ", " ").replace(" OR ", " ").split()
                         if not part.lower().startswith("cat:"))
        # Phrase match in title or abstract, articles and preprints only: full-text search by date returns noise.
        filters = (f'title_and_abstract.search:"{plain}",from_publication_date:{cutoff.isoformat()},'
                   f"to_publication_date:{datetime.date.today().isoformat()},type:article|preprint")
        return api.search_openalex("", limit=limit, filters=filters, sort="publication_date:desc")
    raise ValueError(f"unknown source: {source}")


def select_new(papers_by_query: dict[str, list[dict]], seen: set[str], cutoff: datetime.date,
               boost: list[str] | None = None, today: datetime.date | None = None) -> list[dict]:
    """Merge results across queries, keep recent unseen papers, and rank them.

    Rank: number of queries that found the paper, then number of boost terms in
    its title or abstract, then newest first.
    """
    merged: dict[str, dict] = {}
    for query, papers in papers_by_query.items():
        for paper in api.dedupe(papers):
            key = paper_key(paper)
            title_key = "title:" + api.normalize_title(paper.get("title"))
            if not is_recent(paper, cutoff, today) or key in seen or title_key in seen:
                continue
            entry = next((e for e in merged.values() if e["_title"] == title_key), None) or merged.get(key)
            if entry is None:
                entry = merged[key] = {**paper, "key": key, "_title": title_key, "queries": []}
            if query not in entry["queries"]:
                entry["queries"].append(query)
    terms = [t.lower() for t in boost or []]
    for entry in merged.values():
        text = (entry.get("title", "") + " " + entry.get("abstract", "")).lower()
        entry["boost_hits"] = [t for t in terms if t in text]
    ranked = sorted(merged.values(), key=lambda e: (len(e["queries"]), len(e["boost_hits"]), e.get("published", "")),
                    reverse=True)
    return ranked


def render(papers: list[dict], queries: list[str], days: int, today: datetime.date, errors: dict[str, str],
           abstract_chars: int = 400) -> str:
    start = today - datetime.timedelta(days=days)
    lines = [f"# Paper digest: {start.isoformat()} to {today.isoformat()}", "",
             f"{len(papers)} new papers for {len(queries)} queries: " + "; ".join(f"`{q}`" for q in queries), ""]
    if errors:
        lines += ["Sources that failed (not covered in this digest): "
                  + "; ".join(f"{name}: {message}" for name, message in errors.items()), ""]
    if not papers:
        lines.append("No new papers in this period.")
    for number, paper in enumerate(papers, 1):
        tags = [f"matched {len(paper['queries'])} queries"] if len(paper["queries"]) > 1 else []
        tags += paper["boost_hits"]
        lines += [f"## {number}. {paper['title']}",
                  f"{api.short_authors(paper['authors'])} · {paper.get('published') or paper.get('year')} · "
                  f"{paper.get('venue') or paper['source']} · {paper.get('url', '')}"
                  + (f" · {', '.join(tags)}" if tags else ""), ""]
        abstract = paper.get("abstract") or ""
        if abstract:
            lines += [abstract[:abstract_chars].rstrip() + ("…" if len(abstract) > abstract_chars else ""), ""]
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--config", help="JSON config file; command-line options override it")
    parser.add_argument("--query", action="append", help="search query; repeatable (arXiv field syntax allowed)")
    parser.add_argument("--days", type=int)
    parser.add_argument("--sources", help="comma-separated: arxiv,openalex")
    parser.add_argument("--max-per-query", type=int)
    parser.add_argument("--boost", help="comma-separated terms that raise a paper's rank")
    parser.add_argument("--state", help="JSON file remembering reported papers (default digest-seen.json)")
    parser.add_argument("--no-state", action="store_true", help="do not read or update the state file")
    parser.add_argument("--out", help="write the digest here instead of stdout")
    args = parser.parse_args()
    api.utf8_stdout()

    config = json.loads(Path(args.config).read_text(encoding="utf-8")) if args.config else {}
    queries = args.query or config.get("queries") or []
    if not queries:
        print("error: give at least one --query or a config with queries", file=sys.stderr)
        return 1
    days = args.days or config.get("days", 7)
    sources = args.sources.split(",") if args.sources else config.get("sources", ["arxiv", "openalex"])
    limit = args.max_per_query or config.get("max_per_query", 15)
    boost = args.boost.split(",") if args.boost else config.get("boost", [])
    state_path = Path(args.state or config.get("state", "digest-seen.json"))

    today = datetime.date.today()
    cutoff = today - datetime.timedelta(days=days)
    seen = set(json.loads(state_path.read_text(encoding="utf-8"))) if state_path.exists() and not args.no_state else set()

    papers_by_query: dict[str, list[dict]] = {}
    errors: dict[str, str] = {}
    for query in queries:
        found = []
        for source in sources:
            try:
                found.extend(fetch(query, source.strip(), cutoff, limit))
            except (api.ApiError, ValueError) as exc:
                errors[source.strip()] = str(exc)
            time.sleep(3 if source.strip() == "arxiv" else 0.3)  # arXiv asks for 3 seconds between calls
        papers_by_query[query] = found

    papers = select_new(papers_by_query, seen, cutoff, boost, today)
    text = render(papers, queries, days, today, errors)
    if args.out:
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.out).write_text(text, encoding="utf-8")
        print(f"wrote {len(papers)} papers to {args.out}")
    else:
        print(text)
    if not args.no_state:
        for paper in papers:
            seen.update({paper["key"], paper["_title"]})
        state_path.write_text(json.dumps(sorted(seen), indent=0), encoding="utf-8")
    for source, message in errors.items():
        print(f"warning: {source} failed: {message}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
