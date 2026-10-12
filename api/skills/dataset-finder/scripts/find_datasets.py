#!/usr/bin/env python3
"""Search Hugging Face Hub and OpenML for datasets.

Examples:
    python find_datasets.py "sentiment analysis" --limit 10
    python find_datasets.py "chest x-ray" --sources huggingface --format json
    python find_datasets.py "credit" --sources openml

Kaggle, UCI, and Papers with Code need a login or have no stable public search
API; SKILL.md explains how to search them.
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.parse

sys.dont_write_bytecode = True  # keep the skill folder free of __pycache__

import _scholarly_api as api  # noqa: E402


def tag_values(tags: list[str], prefix: str) -> list[str]:
    return [tag.split(":", 1)[1] for tag in tags or [] if tag.startswith(prefix + ":")]


def parse_huggingface(items: list[dict]) -> list[dict]:
    datasets = []
    for item in items:
        tags = item.get("tags") or []
        name = item.get("id") or ""
        datasets.append({
            "name": name,
            "source": "huggingface",
            "url": f"https://huggingface.co/datasets/{name}",
            "downloads": item.get("downloads"),
            "likes": item.get("likes"),
            "license": ", ".join(tag_values(tags, "license")) or "not stated",
            "tasks": tag_values(tags, "task_categories"),
            "modalities": tag_values(tags, "modality"),
            "languages": tag_values(tags, "language")[:5],
            "size": ", ".join(tag_values(tags, "size_categories")),
            "updated": (item.get("lastModified") or "")[:10],
            "gated": bool(item.get("gated")),
        })
    return datasets


def search_huggingface(query: str, limit: int) -> list[dict]:
    data = json.loads(api.http_get("https://huggingface.co/api/datasets", {
        "search": query, "limit": limit, "sort": "downloads", "direction": -1, "full": "true",
    }).decode("utf-8"))
    return parse_huggingface(data)


def parse_openml(data: dict) -> list[dict]:
    datasets = []
    for item in (data.get("data") or {}).get("dataset") or []:
        qualities = {q.get("name"): q.get("value") for q in item.get("quality") or []}
        rows, features = qualities.get("NumberOfInstances"), qualities.get("NumberOfFeatures")
        datasets.append({
            "name": item.get("name") or "",
            "source": "openml",
            "url": f"https://www.openml.org/d/{item.get('did')}",
            "downloads": None,
            "likes": None,
            "license": "see dataset page",
            "tasks": [],
            "modalities": ["tabular"],
            "languages": [],
            "size": f"{int(float(rows))} rows x {int(float(features))} features" if rows and features else "",
            "updated": "",
            "gated": False,
            "version": item.get("version"),
            "status": item.get("status"),
        })
    return datasets


def search_openml(query: str, limit: int) -> list[dict]:
    # OpenML matches on dataset name only, so use the first keyword.
    keyword = urllib.parse.quote(query.split()[0])
    try:
        data = api.get_json(f"https://www.openml.org/api/v1/json/data/list/data_name/{keyword}/limit/{limit}")
    except api.ApiError as exc:
        if "412" in str(exc):  # OpenML answers 412 when nothing matches
            return []
        raise
    return parse_openml(data)


def to_markdown(datasets: list[dict]) -> str:
    lines = ["| Dataset | Source | Size | License | Tasks | Downloads | Updated |", "|---|---|---|---|---|---|---|"]
    for d in datasets:
        gated = " (gated)" if d["gated"] else ""
        lines.append(f"| [{d['name']}]({d['url']}){gated} | {d['source']} | {d['size'] or 'n/s'} | {d['license']} | "
                     f"{', '.join(d['tasks']) or 'n/s'} | {d['downloads'] if d['downloads'] is not None else 'n/s'} | "
                     f"{d['updated'] or 'n/s'} |")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("query")
    parser.add_argument("--sources", default="huggingface,openml")
    parser.add_argument("--limit", type=int, default=10, help="results per source")
    parser.add_argument("--format", choices=("json", "md"), default="md")
    args = parser.parse_args()
    api.utf8_stdout()

    searchers = {"huggingface": search_huggingface, "openml": search_openml}
    datasets, errors = [], {}
    for source in [s.strip() for s in args.sources.split(",") if s.strip()]:
        if source not in searchers:
            errors[source] = "unknown source"
            continue
        try:
            datasets.extend(searchers[source](args.query, args.limit))
        except api.ApiError as exc:
            errors[source] = str(exc)
    if args.format == "md":
        print(to_markdown(datasets) if datasets else "No datasets found.")
    else:
        print(json.dumps({"query": args.query, "errors": errors, "datasets": datasets}, indent=2, ensure_ascii=False))
    for source, message in errors.items():
        print(f"warning: {source} failed: {message}", file=sys.stderr)
    return 0 if datasets or not errors else 1


if __name__ == "__main__":
    sys.exit(main())
