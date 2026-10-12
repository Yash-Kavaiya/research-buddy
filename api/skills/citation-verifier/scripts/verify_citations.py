#!/usr/bin/env python3
"""Check that every entry in a BibTeX file corresponds to a real publication.

Each entry is looked up in Crossref and OpenAlex (and arXiv for arXiv ids) and
given a status:

    verified        a record was found and title, year, and first author agree
    mismatch        a record was found but some fields disagree (listed)
    possible_match  only a loosely similar record was found; check by hand
    lookup_failed   the databases could not be reached; run again
    not_found       no record found. This is a strong warning sign for a
                    fabricated reference, but books, theses, reports, and
                    older or non-English work are often not indexed.

With --tex, the sentences that cite each key are extracted so the claim can be
checked against the source, and keys cited but missing from the .bib are listed.

Examples:
    python verify_citations.py refs.bib
    python verify_citations.py refs.bib --tex paper.tex --format json --out report.json
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time

sys.dont_write_bytecode = True  # keep the skill folder free of __pycache__

import _scholarly_api as api  # noqa: E402

TITLE_MATCH = 0.9      # token Jaccard at or above this counts as the same title
TITLE_POSSIBLE = 0.6
CITE_RE = re.compile(r"\\[A-Za-z]*cite[A-Za-z]*\*?(?:\[[^\]]*\])*\{([^}]*)\}")


def compare(entry: dict, record: dict) -> list[str]:
    """Differences between a BibTeX entry and a database record (empty list when they agree)."""
    fields, problems = entry["fields"], []
    similarity = api.title_similarity(fields.get("title"), record.get("title"))
    if fields.get("title") and similarity < TITLE_MATCH:
        problems.append(f"title differs (similarity {similarity:.2f}): database has \"{record.get('title')}\"")
    year = re.search(r"\d{4}", fields.get("year", ""))
    if year and record.get("year") and abs(int(year.group(0)) - record["year"]) > 1:
        problems.append(f"year differs: entry {year.group(0)}, database {record['year']}")
    people = api.bib_authors(fields.get("author", ""))
    if people and record.get("authors"):
        first = api.surname(people[0])
        found = [api.normalize_title(a).replace(" ", "") for a in record["authors"]]
        if first and not any(first in name or name.endswith(first) for name in found):
            problems.append(f"first author '{people[0]}' is not among the database authors "
                            f"({api.short_authors(record['authors'])})")
    return problems


def classify(entry: dict, by_id: dict | None, candidates: list[dict]) -> dict:
    """Decide the status from an identifier lookup (`by_id`) and title-search candidates."""
    result = {"key": entry["key"], "title": entry["fields"].get("title", "")}
    if by_id is not None:
        problems = compare(entry, by_id)
        return {**result, "status": "mismatch" if problems else "verified", "problems": problems,
                "matched": _brief(by_id)}
    best, best_score = None, 0.0
    for candidate in candidates:
        score = api.title_similarity(entry["fields"].get("title"), candidate.get("title"))
        if score > best_score:
            best, best_score = candidate, score
    if best is not None and best_score >= TITLE_MATCH:
        problems = compare(entry, best)
        return {**result, "status": "mismatch" if problems else "verified", "problems": problems,
                "matched": _brief(best)}
    if best is not None and best_score >= TITLE_POSSIBLE:
        return {**result, "status": "possible_match", "matched": _brief(best),
                "problems": [f"closest title has similarity {best_score:.2f}; confirm it is the same work"]}
    return {**result, "status": "not_found", "problems": ["no matching record in Crossref or OpenAlex"],
            "matched": None}


def _brief(record: dict) -> dict:
    return {k: record.get(k) for k in ("title", "authors", "year", "venue", "doi", "url", "source")}


def arxiv_id(fields: dict) -> str | None:
    for value in (fields.get("eprint", ""), fields.get("journal", ""), fields.get("url", ""), fields.get("doi", ""),
                  fields.get("note", ""), fields.get("howpublished", "")):
        match = re.search(r"(?<![\d.])(\d{4}\.\d{4,5})(?:v\d+)?(?![\d])", value)
        if match and ("arxiv" in value.lower() or value == fields.get("eprint")):
            return match.group(1)
    return None


def lookup(entry: dict) -> tuple[dict | None, list[dict], list[str]]:
    """Return (record found by identifier, title-search candidates, notes about failed lookups)."""
    fields, notes = entry["fields"], []
    doi = api.normalize_doi(fields.get("doi"))
    if doi:
        try:
            record = api.crossref_doi(doi)
            if record is None:  # DataCite DOIs (arXiv, Zenodo) are not in Crossref
                try:
                    record = api.openalex_work(doi)
                except api.ApiError:
                    record = None
            if record is not None:
                return record, [], notes
            notes.append(f"DOI {doi} was not found in Crossref or OpenAlex")
        except api.ApiError as exc:
            notes.append(f"DOI lookup failed: {exc}")
    identifier = arxiv_id(fields)
    if identifier:
        try:
            found = api.parse_arxiv(api.http_get("https://export.arxiv.org/api/query", {"id_list": identifier}))
            if found and found[0]["title"] and found[0]["title"].lower() != "error":
                return found[0], [], notes
            notes.append(f"arXiv id {identifier} was not found")
        except api.ApiError as exc:
            notes.append(f"arXiv lookup failed: {exc}")
    candidates: list[dict] = []
    title = fields.get("title")
    if title:
        people = api.bib_authors(fields.get("author", ""))
        query = api.normalize_title(title) + (" " + api.surname(people[0]) if people else "")
        for name, search in (("Crossref", lambda: api.search_crossref(query, limit=5)),
                             ("OpenAlex", lambda: api.search_openalex(api.normalize_title(title), limit=5))):
            try:
                candidates.extend(search())
            except api.ApiError as exc:
                notes.append(f"{name} search failed: {exc}")
            time.sleep(0.2)
    else:
        notes.append("entry has no title")
    return None, candidates, notes


def verify(entries: list[dict]) -> list[dict]:
    results = []
    for entry in entries:
        by_id, candidates, notes = lookup(entry)
        result = classify(entry, by_id, candidates)
        if notes:
            result["problems"] = result["problems"] + notes
            # A lookup that errored is not evidence of absence.
            if result["status"] == "not_found" and any("failed" in note for note in notes):
                result["status"] = "lookup_failed"
            # The work exists, but the identifier given for it does not resolve.
            if result["status"] == "verified" and any("was not found" in note for note in notes):
                result["status"] = "mismatch"
        results.append(result)
    return results


def cite_contexts(tex: str) -> dict[str, list[str]]:
    """Map each cited key to the sentences that cite it (LaTeX comments removed)."""
    tex = re.sub(r"(?<!\\)%.*", "", tex)
    contexts: dict[str, list[str]] = {}
    sentences = re.split(r"(?<=[.!?])\s+(?=[A-Z\\])|\n\s*\n", tex)
    for sentence in sentences:
        sentence = " ".join(sentence.split())
        for group in CITE_RE.findall(sentence):
            for key in (k.strip() for k in group.split(",")):
                if key and sentence not in contexts.setdefault(key, []):
                    contexts[key].append(sentence)
    return contexts


def to_markdown(results: list[dict], contexts: dict[str, list[str]] | None, bib_keys: set[str]) -> str:
    counts: dict[str, int] = {}
    for r in results:
        counts[r["status"]] = counts.get(r["status"], 0) + 1
    lines = ["## Citation check", ", ".join(f"{n} {status}" for status, n in sorted(counts.items())), "",
             "| Key | Status | Details |", "|---|---|---|"]
    for r in sorted(results, key=lambda r: r["status"] == "verified"):
        lines.append(f"| {r['key']} | {r['status']} | {'; '.join(r['problems']) or 'ok'} |")
    if contexts is not None:
        missing = sorted(set(contexts) - bib_keys)
        unused = sorted(bib_keys - set(contexts))
        lines += ["", "## Cited in the text but missing from the .bib", ", ".join(missing) or "none",
                  "", "## In the .bib but never cited", ", ".join(unused) or "none",
                  "", "## Claims to check against each source"]
        for key in sorted(contexts):
            lines.append(f"- **{key}**")
            lines += [f"  - {sentence}" for sentence in contexts[key]]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("bibfile")
    parser.add_argument("--tex", action="append", help="LaTeX file to extract citing sentences from; repeatable")
    parser.add_argument("--format", choices=("md", "json"), default="md")
    parser.add_argument("--out", help="write the report here instead of stdout")
    args = parser.parse_args()
    api.utf8_stdout()

    with open(args.bibfile, encoding="utf-8-sig") as handle:
        entries = api.parse_bibtex(handle.read())
    contexts = None
    if args.tex:
        contexts = {}
        for name in args.tex:
            with open(name, encoding="utf-8-sig") as handle:
                for key, sentences in cite_contexts(handle.read()).items():
                    contexts.setdefault(key, []).extend(sentences)
    results = verify(entries)
    keys = {e["key"] for e in entries}
    if args.format == "json":
        text = json.dumps({"results": results, "contexts": contexts,
                           "cited_but_missing": sorted(set(contexts) - keys) if contexts is not None else None},
                          indent=2, ensure_ascii=False)
    else:
        text = to_markdown(results, contexts, keys)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as handle:
            handle.write(text + "\n")
        print(f"wrote {args.out}")
    else:
        print(text)
    return 0 if all(r["status"] == "verified" for r in results) else 1


if __name__ == "__main__":
    sys.exit(main())
