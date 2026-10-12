#!/usr/bin/env python3
"""Append-only experiment log: runs, configs, metrics, and decisions.

Entries are stored as JSON lines (default: experiments/log.jsonl) and rendered
to a Markdown lab notebook. Entries are never edited; corrections are new entries.

Subcommands:
    add       record a run
    decision  record a decision or observation
    render    write the Markdown notebook
    best      show the best run for a metric
    compare   show config and metric differences between two runs

Examples:
    python log_run.py add --name baseline-resnet50 --config lr=0.1 --config epochs=90 \
        --metric top1=76.1 --metric loss=0.94 --tags baseline --note "reference run, seed 0"
    python log_run.py add --name sweep-03 --config-file configs/sweep03.json --metric top1=77.4 --status completed
    python log_run.py decision "Dropping label smoothing: no gain over 3 seeds (runs 4-6)"
    python log_run.py best --metric top1 --mode max
    python log_run.py compare 1 3
    python log_run.py render
"""

from __future__ import annotations

import argparse
import datetime
import json
import subprocess
import sys
from pathlib import Path

DEFAULT_LOG = "experiments/log.jsonl"


def parse_value(text: str):
    """Turn 'true', '3', '0.1', '[1,2]' into typed values; leave other text as a string."""
    try:
        return json.loads(text)
    except ValueError:
        return text


def parse_pairs(pairs: list[str] | None) -> dict:
    result = {}
    for pair in pairs or []:
        key, sep, value = pair.partition("=")
        if not sep or not key:
            raise ValueError(f"expected key=value, got {pair!r}")
        result[key.strip()] = parse_value(value.strip())
    return result


def flatten(data: dict, prefix: str = "") -> dict:
    """Flatten nested config dicts to dotted keys so runs can be compared key by key."""
    flat = {}
    for key, value in data.items():
        name = f"{prefix}{key}"
        if isinstance(value, dict):
            flat.update(flatten(value, name + "."))
        else:
            flat[name] = value
    return flat


def git_state(cwd: str | None = None) -> dict:
    def run(*cmd: str) -> str | None:
        try:
            out = subprocess.run(cmd, capture_output=True, text=True, cwd=cwd, timeout=10)
        except (OSError, subprocess.SubprocessError):
            return None
        return out.stdout.strip() if out.returncode == 0 else None

    commit = run("git", "rev-parse", "--short", "HEAD")
    if commit is None:
        return {}
    return {"commit": commit, "dirty": bool(run("git", "status", "--porcelain")),
            "branch": run("git", "rev-parse", "--abbrev-ref", "HEAD")}


def read_log(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def append(path: Path, entry: dict) -> dict:
    entries = read_log(path)
    entry = {"id": max((e["id"] for e in entries), default=0) + 1,
             "time": datetime.datetime.now().astimezone().isoformat(timespec="seconds"), **entry}
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a", encoding="utf-8") as handle:
        handle.write(json.dumps(entry, ensure_ascii=False) + "\n")
    return entry


def runs(entries: list[dict]) -> list[dict]:
    return [e for e in entries if e.get("type") == "run"]


def best_run(entries: list[dict], metric: str, mode: str = "max") -> dict | None:
    candidates = [e for e in runs(entries) if isinstance(e.get("metrics", {}).get(metric), (int, float))]
    if not candidates:
        return None
    pick = max if mode == "max" else min
    return pick(candidates, key=lambda e: e["metrics"][metric])


def diff_runs(a: dict, b: dict) -> dict:
    """Keys whose values differ between two runs, for config and for metrics."""
    out = {}
    for section in ("config", "metrics"):
        left, right = a.get(section, {}), b.get(section, {})
        out[section] = {key: [left.get(key), right.get(key)]
                        for key in sorted(set(left) | set(right)) if left.get(key) != right.get(key)}
    return out


def render(entries: list[dict]) -> str:
    run_entries = runs(entries)
    metrics = sorted({m for e in run_entries for m in e.get("metrics", {})})
    lines = ["# Experiment notebook", "", f"{len(run_entries)} runs, "
             f"{sum(1 for e in entries if e.get('type') == 'decision')} decisions. "
             "Generated from the JSONL log; edit the log by adding entries, not this file.", "", "## Runs", "",
             "| ID | Date | Name | Status | " + " | ".join(metrics) + " | Commit | Tags |",
             "|---|---|---|---|" + "---|" * len(metrics) + "---|---|"]
    for e in run_entries:
        git = e.get("git", {})
        commit = (git.get("commit", "") + ("*" if git.get("dirty") else "")) or "n/a"
        values = " | ".join(str(e.get("metrics", {}).get(m, "")) for m in metrics)
        lines.append(f"| {e['id']} | {e['time'][:10]} | {e.get('name', '')} | {e.get('status', '')} | {values} | "
                     f"{commit} | {', '.join(e.get('tags', []))} |")
    lines += ["", "`*` after a commit means the working tree had uncommitted changes.", "", "## Log", ""]
    for e in entries:
        stamp = e["time"][:16].replace("T", " ")
        if e.get("type") == "decision":
            lines += [f"### {stamp} · Decision (#{e['id']})", "", e.get("text", ""), ""]
        else:
            lines += [f"### {stamp} · Run #{e['id']}: {e.get('name', '')}", ""]
            if e.get("note"):
                lines += [e["note"], ""]
            if e.get("config"):
                lines += ["Config: " + ", ".join(f"`{k}={v}`" for k, v in e["config"].items()), ""]
            if e.get("metrics"):
                lines += ["Metrics: " + ", ".join(f"{k} = {v}" for k, v in e["metrics"].items()), ""]
            if e.get("artifacts"):
                lines += ["Artifacts: " + ", ".join(e["artifacts"]), ""]
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--log", default=DEFAULT_LOG, help=f"log file (default {DEFAULT_LOG})")
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("add")
    p.add_argument("--name", required=True)
    p.add_argument("--config", action="append", metavar="KEY=VALUE")
    p.add_argument("--config-file", help="JSON file merged under --config values")
    p.add_argument("--metric", action="append", metavar="KEY=VALUE")
    p.add_argument("--status", default="completed", choices=("completed", "failed", "running", "aborted"))
    p.add_argument("--tags", default="", help="comma-separated")
    p.add_argument("--note", default="")
    p.add_argument("--artifact", action="append", help="path to a checkpoint, plot, or output file")
    p = sub.add_parser("decision")
    p.add_argument("text")
    p = sub.add_parser("render")
    p.add_argument("--out", help="default: NOTEBOOK.md next to the log")
    p = sub.add_parser("best")
    p.add_argument("--metric", required=True)
    p.add_argument("--mode", choices=("max", "min"), default="max")
    p = sub.add_parser("compare")
    p.add_argument("a", type=int)
    p.add_argument("b", type=int)
    args = parser.parse_args()
    path = Path(args.log)

    try:
        if args.command == "add":
            config = {}
            if args.config_file:
                config.update(flatten(json.loads(Path(args.config_file).read_text(encoding="utf-8"))))
            config.update(parse_pairs(args.config))
            entry = append(path, {"type": "run", "name": args.name, "status": args.status, "config": config,
                                  "metrics": parse_pairs(args.metric),
                                  "tags": [t.strip() for t in args.tags.split(",") if t.strip()],
                                  "note": args.note, "artifacts": args.artifact or [], "git": git_state()})
            print(json.dumps(entry, indent=2, ensure_ascii=False))
        elif args.command == "decision":
            print(json.dumps(append(path, {"type": "decision", "text": args.text}), indent=2, ensure_ascii=False))
        elif args.command == "render":
            out = Path(args.out) if args.out else path.with_name("NOTEBOOK.md")
            out.write_text(render(read_log(path)), encoding="utf-8")
            print(f"wrote {out}")
        elif args.command == "best":
            found = best_run(read_log(path), args.metric, args.mode)
            if found is None:
                print(f"error: no run has a numeric metric named {args.metric!r}", file=sys.stderr)
                return 1
            print(json.dumps(found, indent=2, ensure_ascii=False))
        else:
            by_id = {e["id"]: e for e in read_log(path)}
            missing = [i for i in (args.a, args.b) if i not in by_id]
            if missing:
                print(f"error: no entry with id {missing}", file=sys.stderr)
                return 1
            print(json.dumps(diff_runs(by_id[args.a], by_id[args.b]), indent=2, ensure_ascii=False))
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
