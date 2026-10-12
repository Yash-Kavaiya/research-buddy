---
name: paper-comparison-matrix
description: "Builds a table comparing papers on method, dataset, metrics, and results, marking unreported cells. Use when comparing three or more papers. Not for prose synthesis; use literature-review-writer."
version: 1.0.0
metadata:
  author: "Yash Kavaiya <yash.kavaiya3@gmail.com>"
  tags: [literature-matrix, comparison-table, synthesis]
---

# Paper Comparison Matrix

Line up N papers on the same dimensions so differences and patterns are visible. The table is a reading aid first and a manuscript table second.

## Purpose

Line up a set of papers on the same dimensions so that patterns, conflicts, and unreported items become visible. The table serves as a reading aid, a synthesis matrix for a review, and a draft of a state-of-the-art table.

## When to use

- Three or more papers on the same problem need comparing.
- A literature review or related-work section needs a summary table.
- Choosing a baseline or method to build on.

Hand off instead for one paper (`paper-summarizer`) or for prose synthesis (`literature-review-writer`).

## Prerequisites

- The papers, as PDFs, links, or a result list from `paper-search`. Full text is needed for results and setup.
- The purpose of the comparison, which decides the columns.
- No scripts or API keys are required.

## Inputs

- The papers: PDFs, links, or a list from `paper-search`. Full text is needed for results and setup.
- The purpose of the comparison, which decides the columns.
- Output format: Markdown (default), CSV, or LaTeX.

## Instructions

1. **Choose columns from the purpose.** Start from the set for the study type and trim to what matters. Six to nine columns is readable.

   | Study type | Columns |
   |---|---|
   | ML or computational | Paper, Year, Task, Method (core idea), Dataset(s), Metric(s), Main result, Baselines compared, Code available, Limitation |
   | Clinical or experimental | Study, Year, Design, Population (N), Intervention, Comparator, Outcome, Effect (with CI), Follow-up, Risk of bias |
   | Qualitative or social science | Study, Year, Context, Sample, Design, Data collection, Analysis approach, Key themes, Limitation |
   | Systems or engineering | Paper, Year, Problem, Architecture, Workload, Metric, Result, Scale, Open source |

2. **Define each column** in one line before filling, so every row is filled the same way ("Main result = the headline number on the most common benchmark").
3. **Fill row by row from the paper**, noting the source location of each number. Use `NR` for "not reported" and `n/a` for "not applicable". Never leave a cell blank or guess.
4. **Make results comparable or say they are not.** Before putting numbers in one column, confirm the same dataset, split, metric definition, and evaluation protocol. Otherwise add a column for the difference or a footnote.
5. **Order the rows** meaningfully: chronologically, by method family, or by result. Add a group header row per family when there are more than 8 papers.
6. **Write the reading** under the table: 3 to 6 observations that the table makes visible, such as common datasets, a metric nobody reports, results that conflict, and conditions nobody tests.
7. **Export.** For LaTeX, save as CSV and pass to `latex-table-generator`.

## Output format

```markdown
## Comparison: <topic> (<N> papers)
Column definitions: Method = ...; Main result = ...; NR = not reported.

| Paper | Year | Method | Dataset | Metric | Main result | Code | Limitation |
|---|---|---|---|---|---|---|---|
| Author et al. [1] | 2023 | ... | ... | F1 | 87.2 (Tab. 3) | yes | ... |

Notes
- a: evaluated on a different split; not directly comparable.

## What the table shows
1. ...

## Gaps visible in the table
- ...
```

## Reference files

Open these only when the step calls for them; they are not needed for every request.

- `references/column-sets-and-comparability.md`: Read at steps 1 to 4, when choosing columns for the study type and deciding whether results can share a column.
- `assets/comparison-matrix-template.md`: Copy and fill for the comparison table and its reading.

## Examples

Requests that should trigger this skill:

- "Compare these eight papers on dataset, metric, and result."
- "Make a literature matrix for my review chapter."
- "Build a synthesis matrix from these PDFs."
- "Which of these methods should I use as a baseline? Put them in a table."
- "Create a state-of-the-art table for image segmentation on this benchmark."

Requests that belong to another skill:

- "Summarise this one paper." → use `paper-summarizer`
- "Write the literature review from these papers." → use `literature-review-writer`
- "Turn my results CSV into a LaTeX table." → use `latex-table-generator`

### Worked example

**Request:** "Compare these five papers on few-shot text classification: method, datasets, metric, main result, and whether code is available."

**What the agent does:**

1. Chooses the ML column set and writes a one-line definition for each column.
2. Fills each row from the paper, noting the table or section for every number and writing NR where nothing is reported.
3. Checks that results share dataset, split, and metric before placing them in one column, and footnotes one that does not.
4. Writes the observations the table makes visible.

**Result (excerpt):**

```markdown
| Paper | Year | Method | Dataset | Metric | Main result | Code |
|---|---|---|---|---|---|---|
| Author A et al. | 2021 | prompt-based fine-tuning | SST-2, 16 shots | accuracy | 92.7 (Tab. 3) | yes |
| Author B et al. | 2022 | contrastive pretraining | SST-2, 16 shots (a) | accuracy | 91.0 (Tab. 2) | NR |

a: different sampling of the 16 shots; not directly comparable.

## What the table shows
1. All five papers evaluate on English sentiment data; none reports a non-English dataset.
```

## Quality bar and pitfalls

- Every cell comes from the paper. `NR` is correct and useful; an invented value is a fabrication.
- Do not rank papers by numbers measured under different protocols. This is the most common error in such tables.
- Keep cells short (a phrase or a number). Long explanations go in notes under the table.
- Use the same unit, decimal places, and metric direction throughout a column.
- Report each paper's own numbers for its own method. Numbers a paper reports for its competitors are often lower than the competitors' own.
- State the selection: how these N papers were chosen and what was left out.
- If only abstracts were available for some rows, mark those rows.

## Limitations

- Cells can only hold what the papers report. Different protocols often make numbers non-comparable, and the table says so instead of ranking them.
- Rows built from abstracts alone are incomplete and are marked.
- The table reflects the papers selected; it is not evidence about papers left out.

## Troubleshooting

| Problem | Likely cause | Solution |
|---|---|---|
| Many cells are NR | The columns do not match what this literature reports | Replace the column with one the papers do report, or keep it and treat the empty cells as a finding |
| Results in one column are not comparable | Papers use different splits, metrics, or protocols | Add a protocol column or footnotes, and do not sort by that column |
| The table is too wide to read | Too many columns | Keep six to nine columns and move the rest to a second table or notes |

## Related skills

- `paper-search` and `citation-graph-explorer` to choose the papers.
- `paper-summarizer` for per-paper notes that feed the rows.
- `latex-table-generator` to typeset the matrix.
- `literature-review-writer` and `related-work-writer` to write the synthesis around it.
- `research-gap-finder` uses the empty and `NR` cells as gap candidates.
- `systematic-review-prisma` uses the matrix as its data-extraction table.
