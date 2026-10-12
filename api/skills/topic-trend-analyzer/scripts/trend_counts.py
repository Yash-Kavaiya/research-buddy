#!/usr/bin/env python3
"""Publication trend for a topic, from OpenAlex.

Reports papers per year, the topic's share of all indexed papers (so growth of
the whole literature is not mistaken for growth of the topic), and the
subtopics and keywords that grew most between two time windows.

Examples:
    python trend_counts.py "diffusion models" --from 2015
    python trend_counts.py "federated learning" --from 2018 --window 2 --format json
"""

from __future__ import annotations

import argparse
import datetime
import json
import sys

sys.dont_write_bytecode = True  # keep the skill folder free of __pycache__

import _scholarly_api as api  # noqa: E402

GROUP_LIMIT = 200  # OpenAlex returns at most this many groups per group_by call


def group_counts(data: dict) -> dict[str, int]:
    """OpenAlex group_by response to {display name: count}."""
    return {str(g.get("key_display_name") or g.get("key")): int(g.get("count") or 0)
            for g in data.get("group_by") or []}


def yearly_series(topic_counts: dict[str, int], total_counts: dict[str, int],
                  year_from: int, year_to: int) -> list[dict]:
    series = []
    for year in range(year_from, year_to + 1):
        count = topic_counts.get(str(year), 0)
        total = total_counts.get(str(year), 0)
        series.append({"year": year, "count": count,
                       "share_per_10k": round(10000 * count / total, 2) if total else None})
    return series


def cagr(first: float, last: float, years: int) -> float | None:
    """Compound annual growth rate as a fraction; None when it is undefined."""
    if first <= 0 or years <= 0:
        return None
    return (last / first) ** (1 / years) - 1


def growth_table(recent: dict[str, int], earlier: dict[str, int], min_recent: int = 5, top: int = 15) -> list[dict]:
    """Rank groups by growth from the earlier window to the recent one.

    OpenAlex returns only the 200 largest groups. When the earlier window is
    truncated like that, a group missing from it is not necessarily new: its
    earlier count is only known to be below the smallest listed count, which
    is reported as `earlier_below`. Groups with no earlier count are listed
    first, since a ratio cannot be computed for them.
    """
    truncated = len(earlier) >= GROUP_LIMIT
    floor = min(earlier.values()) if truncated else 0
    rows = []
    for name, now in recent.items():
        if now < min_recent:
            continue
        before = earlier.get(name)
        rows.append({"name": name, "recent": now, "earlier": before if before is not None else 0,
                     "earlier_below": floor if before is None and truncated else None,
                     "ratio": round(now / before, 2) if before else None})
    rows.sort(key=lambda r: (r["ratio"] is None, r["ratio"] or 0, r["recent"]), reverse=True)
    return rows[:top]


def topic_params(query: str, fulltext: bool, year_filter: str) -> dict:
    """Match the phrase in titles and abstracts by default; --fulltext casts a wider, noisier net."""
    if fulltext:
        return {"search": query, "filter": year_filter}
    phrase = query if '"' in query else f'"{query}"'
    return {"filter": f"title_and_abstract.search:{phrase},{year_filter}"}


def analyze(query: str, year_from: int, year_to: int, window: int, top: int, fulltext: bool = False) -> dict:
    years = f"publication_year:{year_from}-{year_to}"
    topic = group_counts(api.openalex_get("works", {**topic_params(query, fulltext, years),
                                                    "group_by": "publication_year"}))
    total = group_counts(api.openalex_get("works", {"filter": years, "group_by": "publication_year"}))
    series = yearly_series(topic, total, year_from, year_to)

    recent_range = f"publication_year:{year_to - window + 1}-{year_to}"
    earlier_range = f"publication_year:{year_to - 2 * window + 1}-{year_to - window}"
    rising = {}
    for label, field in (("subtopics", "primary_topic.id"), ("keywords", "keywords.id")):
        recent = group_counts(api.openalex_get("works", {**topic_params(query, fulltext, recent_range),
                                                         "group_by": field}))
        earlier = group_counts(api.openalex_get("works", {**topic_params(query, fulltext, earlier_range),
                                                          "group_by": field}))
        rising[label] = growth_table(recent, earlier, top=top)

    growth = cagr(series[0]["count"], series[-1]["count"], len(series) - 1)
    return {"query": query, "year_from": year_from, "year_to": year_to, "series": series,
            "cagr": round(growth, 4) if growth is not None else None,
            "windows": {"recent": recent_range.split(":")[1], "earlier": earlier_range.split(":")[1]},
            "rising": rising}


def to_markdown(result: dict) -> str:
    lines = [f"## Publication trend: {result['query']} ({result['year_from']} to {result['year_to']})", "",
             "| Year | Papers | Share per 10,000 indexed papers |", "|---|---|---|"]
    lines += [f"| {r['year']} | {r['count']} | {r['share_per_10k']} |" for r in result["series"]]
    growth = result["cagr"]
    lines += ["", "Compound annual growth in paper count: "
              + (f"{growth:.1%}" if growth is not None else "undefined (no papers in the first year)")]
    for label, rows in result["rising"].items():
        lines += ["", f"### Rising {label} ({result['windows']['earlier']} vs {result['windows']['recent']})", "",
                  "| Name | Earlier | Recent | Ratio |", "|---|---|---|---|"]
        for r in rows:
            earlier = f"under {r['earlier_below']}" if r["earlier_below"] is not None else r["earlier"]
            lines.append(f"| {r['name']} | {earlier} | {r['recent']} | {r['ratio'] if r['ratio'] else 'new or emerging'} |")
    return "\n".join(lines)


def main() -> int:
    last_full_year = datetime.date.today().year - 1
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("query")
    parser.add_argument("--from", dest="year_from", type=int, default=last_full_year - 9)
    parser.add_argument("--to", dest="year_to", type=int, default=last_full_year,
                        help="last year to include (default: last complete calendar year)")
    parser.add_argument("--window", type=int, default=3, help="years in each comparison window")
    parser.add_argument("--top", type=int, default=15)
    parser.add_argument("--fulltext", action="store_true",
                        help="search full text for the words instead of the exact phrase in title or abstract")
    parser.add_argument("--format", choices=("json", "md"), default="md")
    args = parser.parse_args()
    api.utf8_stdout()
    try:
        result = analyze(args.query, args.year_from, args.year_to, args.window, args.top, args.fulltext)
    except api.ApiError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    print(to_markdown(result) if args.format == "md" else json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
