---
name: citation-verifier
description: "Verifies that each reference exists in Crossref, OpenAlex, or arXiv with matching metadata and supports the sentence citing it. Use before submitting referenced work. Not for formatting."
version: 1.0.0
compatibility: "Requires Python 3.10 or later. Makes read-only HTTPS requests to Crossref, OpenAlex, and arXiv; sends only the search terms or identifiers given to it."
allowed-tools: "Bash(python:*) Read Write"
permissions: [network, env, file_write]
metadata:
  author: "Yash Kavaiya <yash.kavaiya3@gmail.com>"
  tags: [citations, verification, research-integrity, hallucination-detection]
---

# Citation Verifier

Two checks for every reference: does it exist as cited, and does it say what the text claims it says. The first is done by script; the second requires reading the source.

## Purpose

Catch fabricated, mismatched, and misused citations before a document goes out. A script checks that every reference exists with the stated title, authors, and year; the agent then reads the sources to check that each supports the sentence that cites it.

## When to use

- Before submitting any paper, thesis, proposal, or report.
- Whenever references were produced by an AI assistant, copied from another paper's reference list, or typed from memory.
- When a reviewer or supervisor questions a citation.

Hand off instead for formatting and de-duplicating a `.bib` file (`bibtex-manager`) or switching citation style (`citation-style-converter`).

## Prerequisites

- Python 3.10 or later; the script uses only the standard library.
- Network access to Crossref, OpenAlex, and arXiv (no key needed; `OPENALEX_MAILTO` is recommended).
- The references as a `.bib` file, and the manuscript as `.tex` for the claim check.

## Inputs

- The references as a `.bib` file. If they are in a Word or plain-text list, convert them first (paste each into `paper-search`, or use the Crossref lookup in `bibtex-manager`).
- The manuscript (`.tex` or text), for the claim check.
- Access to the cited papers' full text where possible.

## Instructions

1. **Run the existence check:**

   ```bash
   python scripts/verify_citations.py references.bib
   python scripts/verify_citations.py references.bib --tex paper.tex --format json --out citation-report.json
   ```

   Each entry is looked up by DOI (Crossref, then OpenAlex), by arXiv id, and otherwise by title search, and receives a status:

   | Status | Meaning | Action |
   |---|---|---|
   | `verified` | A record was found; title, year, and first author agree | Proceed to the claim check |
   | `mismatch` | A record exists but fields differ (wrong year, wrong author, DOI points to another paper, DOI does not resolve) | Correct the entry from the database record |
   | `possible_match` | Only a loosely similar title was found | Open the candidate and confirm by hand |
   | `not_found` | No record in Crossref or OpenAlex | Treat as suspect; see step 2 |
   | `lookup_failed` | A database could not be reached | Rerun later; this says nothing about the reference |

   The exit code is non-zero unless every entry is verified.
2. **Investigate `not_found` entries.** Search the exact title in quotes on the web, on Google Scholar, and on the publisher's or journal's site; check the first author's publication list. Books, theses, technical reports, standards, and older or non-English work are often not indexed, and are real. If nothing turns up anywhere, the reference is very likely fabricated: remove it and find a real source for the claim with `paper-search`, or remove the claim.
3. **Fix `mismatch` entries** from the matched record. A common pattern in fabricated references is a real title with invented authors or venue, or a real DOI attached to a different paper. Do not "fix" by keeping the invented parts.
4. **Check claims against sources.** With `--tex`, the report lists the sentences that cite each key. For each one:
   - Open the source (abstract at minimum; the relevant section for specific claims, numbers, and quotations).
   - Judge: *supports* (the source states this), *partially supports* (weaker, narrower, or conditional), *does not support* (says something else, or the opposite), *cannot verify* (no access to full text).
   - Check quoted text word for word, and numbers digit for digit, with a page or section.
5. **Check the text and the list against each other.** The report lists keys cited but missing from the `.bib`, and entries never cited.
6. **Watch for citation problems beyond existence:** a retracted paper (check the publisher page or Retraction Watch); a preprint cited when a published version exists; a secondary source cited for a primary finding; a review cited for an original result.
7. **Report** every reference's status and every claim judgement, with the corrections made.

## Available Scripts

| Script | Purpose | Arguments |
|---|---|---|
| `scripts/verify_citations.py` | Looks up every BibTeX entry by DOI, arXiv id, or title and reports verified, mismatch, possible_match, not_found, or lookup_failed; with `--tex`, lists the sentences citing each key | `BIBFILE` (required), `--tex FILE` (repeatable), `--format md|json`, `--out FILE` |

Run a script with the agent's script tool, for example `run_script("scripts/verify_citations.py", args=[...])`, or from a shell in the skill folder with `python scripts/verify_citations.py ...`. Each script prints usage with `--help`, validates its arguments, and exits with a non-zero code and an `error:` message on failure.

## Output format

```markdown
## Citation verification report
Checked <N> references on <date> against Crossref, OpenAlex, arXiv.
<a> verified, <b> mismatch, <c> possible match, <d> not found, <e> lookup failed.

### Existence
| Key | Status | Problem | Correction |
|---|---|---|---|

### Claim support
| Key | Sentence | Verdict | Evidence (source location) | Fix |
|---|---|---|---|---|
| smith2021 | "X improves Y by 30% \cite{smith2021}." | partially supports | reports 30% on one of three datasets (Table 2) | add the condition |

### Cited but not in the bibliography
### In the bibliography but never cited
### Could not verify (no full-text access)
```

## Examples

Requests that should trigger this skill:

- "Check whether the references in my bibliography are real."
- "Verify these citations; ChatGPT gave me some of them."
- "Are there hallucinated references in refs.bib?"
- "Does this paper actually say what I cite it for?"
- "Run a citation check on my thesis chapter before I submit."

Requests that belong to another skill:

- "Clean up and de-duplicate my .bib file." → use `bibtex-manager`
- "Convert my references to APA." → use `citation-style-converter`
- "Find papers to support this claim." → use `paper-search`

### Worked example

**Request:** "Verify refs.bib against paper.tex before I submit tomorrow."

**What the agent does:**

1. Runs `run_script("scripts/verify_citations.py", args="refs.bib --tex paper.tex")`.
2. Corrects the mismatched entry from the database record.
3. Searches the web and the first author's publication list for the not-found entry and finds nothing.
4. Reads the abstracts and relevant sections for each citing sentence and records a verdict.

**Result (excerpt):**

```markdown
5 references checked: 3 verified, 1 mismatch, 1 not found.

| Key | Status | Problem | Correction |
|---|---|---|---|
| wrongyear | mismatch | year 2009 vs database 2016; first author not among database authors (Kaiming He et al.) | replaced with the Crossref record |
| fake2021 | not_found | no record in Crossref or OpenAlex; no trace on the web or in the authors' lists | removed; claim needs a real source |

| Key | Sentence | Verdict |
|---|---|---|
| lecun2015 | "Deep networks need no feature engineering \cite{lecun2015}." | partially supports: the paper says less hand-engineering, not none |
```

## Quality bar and pitfalls

- **Tell the user what leaves their machine.** The script sends the titles, authors, and DOIs of the references to the public APIs named under Prerequisites, and nothing else. If the topic is unpublished, confidential, or under embargo, say this before running and ask the user to confirm or to supply more general search terms.
- Never mark a reference verified from memory. Verified means a database record was retrieved in this run.
- `not_found` is a warning, not a verdict. State what else was checked before calling a reference fabricated.
- Never repair a suspect reference by inventing plausible details. Replace it with a retrieved record or remove it.
- A real paper cited for something it does not say is still a citation error. The existence check alone is half the job.
- Say which claims were checked against full text and which only against an abstract. Abstract-level checks cannot confirm specific numbers.
- A title-search match can be a different paper with a similar title. Compare authors, year, and venue.
- Be honest about coverage: list everything that could not be verified so the author can check it.

## Limitations

- `not_found` is a strong warning, not proof of fabrication. Books, theses, reports, standards, and older or non-English work are often not indexed.
- Title matching can accept a different paper with a near-identical title; authors, year, and venue must be compared.
- The claim check depends on access to the source. Verdicts made from an abstract cannot confirm specific numbers or quotations.
- The script reads BibTeX only. Reference lists in Word or plain text must be converted first.

## Troubleshooting

| Problem | Likely cause | Solution |
|---|---|---|
| Status `lookup_failed` for many entries | A database was unreachable or rate-limited | Wait and rerun; this status says nothing about whether the reference exists |
| A real book or thesis is reported `not_found` | The work is not indexed by Crossref or OpenAlex | Confirm it through the publisher, library catalogue, or repository and record how it was verified |
| A real paper is reported `mismatch` | The entry has a wrong year, author order, or DOI | Correct the entry from the matched record shown in the report |
| `possible_match` with a similar title | A preprint and published version differ in title, or it is a different paper | Open the candidate and confirm authors and venue by hand |

## Related skills

- `bibtex-manager` to clean and complete entries after verification.
- `paper-search` to find a real source for a claim whose reference was removed.
- `citation-style-converter` once the list is correct.
- `paper-summarizer` to read a source closely for the claim check.
- `self-peer-reviewer` and `camera-ready-checker` run this before submission.
- `literature-review-writer`, `related-work-writer`, and `introduction-writer` should all end with this check.
