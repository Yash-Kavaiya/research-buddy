#!/usr/bin/env python3
"""Measure how close a draft is to its source texts.

For each sentence of the draft it reports the longest run of words copied from
a source and the share of the sentence's word trigrams that appear in a source,
and flags sentences that are verbatim or too closely paraphrased.

This compares the draft only with the source files you give it. It is not a
check against the web or a publisher database.

Examples:
    python similarity.py draft.txt source1.txt source2.txt
    python similarity.py draft.md paper.txt --min-run 6 --threshold 0.4 --format json
"""

from __future__ import annotations

import argparse
import difflib
import json
import re
import sys
from pathlib import Path

WORD_RE = re.compile(r"[A-Za-z0-9]+(?:['’][A-Za-z]+)?")
ABBREVIATION_RE = re.compile(r"(?:\b(?:et al|e\.g|i\.e|cf|vs|Fig|Figs|Eq|Eqs|Sec|Tab|No|Dr|Prof|Mr|Ms|Mrs|approx|resp)\.)$")


def words(text: str) -> list[str]:
    return [w.lower().replace("’", "'") for w in WORD_RE.findall(text)]


def sentences(text: str) -> list[str]:
    text = re.sub(r"\s+", " ", text).strip()
    parts = re.split(r"(?<=[.!?])[\"')\]]*\s+(?=[\"'(\[]?[A-Z])", text)
    merged: list[str] = []
    for part in (p.strip() for p in parts if p.strip()):
        # "et al. Smith" and "Fig. A" are not sentence boundaries
        if merged and ABBREVIATION_RE.search(merged[-1]):
            merged[-1] += " " + part
        else:
            merged.append(part)
    return merged


def ngrams(tokens: list[str], n: int) -> set[tuple[str, ...]]:
    return {tuple(tokens[i:i + n]) for i in range(len(tokens) - n + 1)}


def longest_shared_run(a: list[str], b: list[str]) -> tuple[int, int]:
    """Length and start (in a) of the longest run of consecutive words shared by a and b."""
    matcher = difflib.SequenceMatcher(None, a, b, autojunk=False)
    block = matcher.find_longest_match(0, len(a), 0, len(b))
    return block.size, block.a


def is_quoted(sentence: str, run_text: list[str]) -> bool:
    """True when the copied run sits inside quotation marks in the draft sentence."""
    for quoted in re.findall(r"[\"“]([^\"”]+)[\"”]", sentence):
        joined = " ".join(words(quoted))
        if " ".join(run_text) in joined:
            return True
    return False


def analyze(draft: str, sources: dict[str, str], min_run: int = 8, threshold: float = 0.5, n: int = 3) -> dict:
    source_tokens = {name: words(text) for name, text in sources.items()}
    source_grams = {name: ngrams(tokens, n) for name, tokens in source_tokens.items()}
    flagged, total_grams, shared_grams = [], 0, 0
    draft_sentences = sentences(draft)
    for index, sentence in enumerate(draft_sentences, 1):
        tokens = words(sentence)
        grams = ngrams(tokens, n)
        if not grams:
            continue
        best = {"source": None, "overlap": 0.0, "run": 0, "run_text": []}
        any_shared: set = set()
        for name in sources:
            common = grams & source_grams[name]
            any_shared |= common
            overlap = len(common) / len(grams)
            run, start = longest_shared_run(tokens, source_tokens[name])
            if (run, overlap) > (best["run"], best["overlap"]):
                best = {"source": name, "overlap": overlap, "run": run, "run_text": tokens[start:start + run]}
        total_grams += len(grams)
        shared_grams += len(any_shared)
        if best["run"] >= min_run:
            kind = "quoted" if is_quoted(sentence, best["run_text"]) else "verbatim"
        elif best["overlap"] >= threshold:
            kind = "close_paraphrase"
        else:
            continue
        flagged.append({"sentence_number": index, "kind": kind, "source": best["source"],
                        "trigram_overlap": round(best["overlap"], 2), "longest_copied_run": best["run"],
                        "copied_text": " ".join(best["run_text"]) if best["run"] >= min_run else "",
                        "sentence": sentence})
    return {
        "sentences": len(draft_sentences),
        "flagged": len([f for f in flagged if f["kind"] != "quoted"]),
        "overall_trigram_overlap": round(shared_grams / total_grams, 3) if total_grams else 0.0,
        "settings": {"min_run": min_run, "threshold": threshold, "ngram": n},
        "items": flagged,
    }


def to_markdown(result: dict) -> str:
    lines = [f"Draft sentences: {result['sentences']}. Flagged: {result['flagged']}. "
             f"Overall trigram overlap with the sources: {result['overall_trigram_overlap']:.1%}.", ""]
    labels = {"verbatim": "Copied run without quotation marks", "close_paraphrase": "Too close to the source wording",
              "quoted": "Quoted (check it has a citation and page number)"}
    for item in result["items"]:
        lines += [f"### Sentence {item['sentence_number']}: {labels[item['kind']]}",
                  f"Source: {item['source']}. Trigram overlap {item['trigram_overlap']:.0%}, "
                  f"longest copied run {item['longest_copied_run']} words.",
                  f"> {item['sentence']}"]
        if item["copied_text"]:
            lines.append(f"Copied words: \"{item['copied_text']}\"")
        lines.append("")
    return "\n".join(lines).rstrip()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("draft")
    parser.add_argument("sources", nargs="+", help="plain-text files of the sources the draft drew on")
    parser.add_argument("--min-run", type=int, default=8, help="consecutive shared words that count as copying")
    parser.add_argument("--threshold", type=float, default=0.5, help="trigram overlap that counts as too close")
    parser.add_argument("--format", choices=("md", "json"), default="md")
    args = parser.parse_args()
    for stream in (sys.stdout, sys.stderr):
        stream.reconfigure(encoding="utf-8", errors="replace")

    read = lambda path: Path(path).read_text(encoding="utf-8-sig", errors="replace")  # noqa: E731
    result = analyze(read(args.draft), {Path(s).name: read(s) for s in args.sources}, args.min_run, args.threshold)
    print(to_markdown(result) if args.format == "md" else json.dumps(result, indent=2, ensure_ascii=False))
    return 1 if result["flagged"] else 0


if __name__ == "__main__":
    sys.exit(main())
