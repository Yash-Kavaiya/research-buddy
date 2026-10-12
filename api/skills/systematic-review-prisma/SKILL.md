---
name: systematic-review-prisma
description: "Runs a PRISMA 2020 systematic review: protocol, search strings, de-duplication, screening, extraction, and a checked flow diagram. Use for systematic or scoping reviews. Not for narrative reviews."
version: 1.0.0
compatibility: "Requires Python 3.10 or later. Runs locally with no network access."
allowed-tools: "Bash(python:*) Read Write"
metadata:
  author: "Yash Kavaiya <yash.kavaiya3@gmail.com>"
  tags: [systematic-review, prisma, screening, evidence-synthesis]
---

# Systematic Review (PRISMA 2020)

Carry out a review that someone else could repeat: a written protocol, documented searches, explicit criteria, recorded decisions, and a flow diagram whose numbers add up.

## Purpose

Carry out a literature review that another team could repeat: a written protocol, documented searches, explicit eligibility criteria, recorded screening decisions, and a flow diagram whose numbers add up. The script handles record merging, counting, and the diagram so those numbers come from the screening sheet.

## When to use

- A systematic review, scoping review (PRISMA-ScR), or systematic mapping study.
- Any single stage of one: search strings, screening, extraction, or the flow diagram.

Hand off instead for a narrative or thematic review without a protocol (`literature-review-writer`).

## Prerequisites

- Python 3.10 or later; the script uses only the standard library.
- Database exports in CSV or RIS format. The user exports these from Scopus, Web of Science, PubMed, or similar; the agent usually cannot query subscription databases.
- A review question and, ideally, a second reviewer for screening.
- For the TikZ diagram: a LaTeX installation with the `tikz` package.

## Inputs

- Review question, and the review type (systematic, scoping, mapping, rapid).
- Databases the user can access (Scopus, Web of Science, PubMed, IEEE Xplore, ACM DL, PsycINFO, ERIC). Access decides the search plan.
- Date range, languages, publication types.
- Number of reviewers. One-reviewer screening is a limitation that must be reported.

## Instructions

1. **Protocol.** Write it before searching: question in PICO, PECO, or SPIDER form (`research-question-formulator`), eligibility criteria, databases, search strategy, screening process, extraction fields, appraisal tool, synthesis method. Recommend registering it (PROSPERO for health, OSF otherwise).
2. **Eligibility criteria.** A table of inclusion and exclusion criteria, each testable from a title, abstract, or full text. Number them; exclusion reasons at full text cite these numbers.
3. **Search strings.** Build concept blocks: synonyms joined with OR inside a block, blocks joined with AND. Then write the string in each database's syntax:
   - Scopus: `TITLE-ABS-KEY(("machine learning" OR "deep learning") AND (diagnos* OR detect*))`
   - Web of Science: `TS=(("machine learning" OR "deep learning") AND (diagnos* OR detect*))`
   - PubMed: `("machine learning"[tiab] OR "Machine Learning"[Mesh]) AND (diagnos*[tiab] OR detect*[tiab])`
   - IEEE Xplore: `("All Metadata":"machine learning" OR "All Metadata":"deep learning") AND ...`

   Test each string against 3 to 5 known relevant papers; if any is missed, revise. Record the final string, database, date, and hit count.
4. **Export and de-duplicate.** The user exports results as CSV or RIS (the agent usually cannot query subscription databases). Then:

   ```bash
   python scripts/prisma_flow.py dedupe pubmed.ris scopus.csv wos.csv --out screening.csv --counts counts.json
   ```

   This merges the exports, removes duplicates by DOI and normalized title, writes *screening.csv* with empty decision columns, and records identification counts.
5. **Title and abstract screening.** Fill `title_abstract_decision` with `include` or `exclude` for every row, applying the criteria. When in doubt, include; doubt is resolved at full text. With two reviewers, screen independently and report agreement (Cohen's kappa).
6. **Full-text screening.** For each included row, fill `fulltext_decision` with `include`, `exclude`, or `not_retrieved`. Every exclusion needs an `exclusion_reason` using a fixed short list tied to the criteria ("Wrong population", "No empirical data").
7. **Snowball.** Run `citation-graph-explorer` on the included studies and screen the additions the same way. PRISMA 2020 reports these under "other methods"; report their counts separately in the text.
8. **Tally and draw the flow diagram.**

   ```bash
   python scripts/prisma_flow.py tally screening.csv --counts counts.json
   python scripts/prisma_flow.py diagram counts.json --format mermaid   # or --format tikz
   ```

   `tally` refuses incomplete sheets (missing decisions or reasons). `diagram` refuses counts that do not add up and names the inconsistent box.
9. **Extract data** from included studies into a table with predefined fields (`paper-comparison-matrix`).
10. **Appraise quality or risk of bias** with a tool suited to the designs: RoB 2 (randomised trials), ROBINS-I (non-randomised), CASP (qualitative), JBI checklists, QUADAS-2 (diagnostic), MMAT (mixed). Report per-study judgements.
11. **Synthesize.** Narrative or thematic synthesis by default; meta-analysis only when studies are similar enough in design, outcome, and measure. Report heterogeneity.
12. **Write up** against the PRISMA 2020 checklist (27 items) and state which items are not applicable.

## Available Scripts

| Script | Purpose | Arguments |
|---|---|---|
| `scripts/prisma_flow.py dedupe` | Merges CSV or RIS exports, removes duplicates by DOI and normalized title, writes the screening sheet | `FILES...` (required), `--out screening.csv`, `--counts counts.json` |
| `scripts/prisma_flow.py tally` | Counts screening decisions and exclusion reasons; refuses incomplete sheets | `SHEET` (required), `--counts counts.json` |
| `scripts/prisma_flow.py diagram` | Validates that the counts add up and prints the PRISMA 2020 flow diagram | `COUNTS` (required), `--format mermaid|tikz` |

Run a script with the agent's script tool, for example `run_script("scripts/prisma_flow.py dedupe", args=[...])`, or from a shell in the skill folder with `python scripts/prisma_flow.py dedupe ...`. Each script prints usage with `--help`, validates its arguments, and exits with a non-zero code and an `error:` message on failure.

## Output format

Deliver these files, plus the manuscript sections on request:

- *protocol.md*: question, criteria table, databases, search strings, process.
- *search-log.md*: table of database, date, exact string, hits.
- *screening.csv*: every record with decisions and reasons.
- *counts.json* and the flow diagram (Mermaid or TikZ).
- *extraction.csv* and the quality-appraisal table.
- A PRISMA checklist table: item, where reported.

## Examples

Requests that should trigger this skill:

- "Help me do a systematic literature review on machine learning for sepsis prediction."
- "Write Scopus and PubMed search strings for my SLR."
- "I exported 800 records from three databases. Remove duplicates and make a screening sheet."
- "Make a PRISMA flow diagram from my screening results."
- "Set up a scoping review protocol following PRISMA-ScR."

Requests that belong to another skill:

- "Write a literature review chapter from these 20 papers." → use `literature-review-writer`
- "Find some papers on sepsis prediction." → use `paper-search`
- "Compare these papers in a table." → use `paper-comparison-matrix`

### Worked example

**Request:** "I have pubmed.ris and scopus.csv for my review on ML sepsis prediction. De-duplicate them, and after I screen, give me the PRISMA diagram."

**What the agent does:**

1. Confirms the protocol and numbered eligibility criteria exist, and drafts them if not.
2. Runs `run_script("scripts/prisma_flow.py", args="dedupe pubmed.ris scopus.csv --out screening.csv --counts counts.json")`.
3. After the user fills the decision columns, runs `tally` and then `diagram --format mermaid`.
4. Reports the counts and any inconsistency the script found.

**Result (excerpt):**

```markdown
{"identified": {"pubmed": 412, "scopus": 388}, "duplicates_removed": 171, "records_to_screen": 629}

flowchart TD
    A["Records identified (n = 800): pubmed (n = 412); scopus (n = 388)"] --> B["Records screened (n = 629)"]
    A --> A2["Records removed before screening: duplicates (n = 171)"]
    D["Reports assessed for eligibility (n = 58)"] --> E["Studies included in review (n = 21)"]
```

## Quality bar and pitfalls

- Never invent hit counts, screening decisions, or flow-diagram numbers. Every number comes from the exported files and the screening sheet.
- The free APIs in `paper-search` do not replace Scopus or Web of Science. If the user has no database access, use them and state that the search covered OpenAlex, PubMed, and so on, by name.
- A string that was never tested against known relevant papers is a draft.
- Screening decisions made by an AI assistant must be reported as such in the methods, and a human should check a sample at least. Say this to the user.
- Excluding at full text without a recorded reason breaks the flow diagram and the review.
- Do not pool results from incompatible designs or outcomes to obtain a single number.
- Scoping reviews do not need quality appraisal; systematic reviews do. Do not mix the labels.

## Limitations

- The free APIs do not replace Scopus, Web of Science, or Embase. A review that used only open indexes must say so.
- Duplicate removal matches on DOI and normalized title. Records with different titles for the same study (for example a translated title) are kept and need manual checking.
- The script does not screen. Decisions are made by the reviewers; screening done by an AI assistant must be reported and sample-checked by a human.
- Meta-analysis, risk-of-bias scoring, and forest plots are outside the script and are done with dedicated tools.

## Troubleshooting

| Problem | Likely cause | Solution |
|---|---|---|
| `error: N records have no title/abstract decision` | The screening sheet is incomplete | Fill `title_abstract_decision` with include or exclude for every row, then rerun `tally` |
| `error: included is X but assessed minus full-text exclusions gives Y` | The counts file was edited by hand or decisions changed after tallying | Rerun `tally` from the current sheet so every count is recomputed, then `diagram` |
| Records lose their titles after `dedupe` | The export uses column names the script does not recognise | Rename the columns to title, authors, year, doi, abstract, or export as RIS |
| Too few duplicates removed | One database exports DOIs with a URL prefix or titles with trailing notes | DOI prefixes are normalized automatically; clean title suffixes in the export and rerun |

## Related skills

- `research-question-formulator` for the PICO or SPIDER question.
- `paper-search` for open-database searching and `citation-graph-explorer` for snowballing.
- `paper-comparison-matrix` for the extraction table.
- `paper-critic` for per-study appraisal reasoning.
- `literature-review-writer` to write the synthesis.
- `bibtex-manager` to clean the included-studies bibliography.
- `publication-figure-maker` for forest plots and summary charts.
