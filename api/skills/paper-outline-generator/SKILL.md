---
name: paper-outline-generator
description: "Produces a section-by-section paper outline for a target venue with each section's claim, display items, and length budget. Use when starting or restructuring a draft. Not for thesis chapters."
version: 1.0.0
metadata:
  author: "Yash Kavaiya <yash.kavaiya3@gmail.com>"
  tags: [paper-outline, imrad, academic-writing, planning]
---

# Paper Outline Generator

Plan the paper as an argument before any prose is written: what it claims, what evidence supports each claim, and where each piece goes within the venue's limits.

## Purpose

Plan a paper as an argument before prose is written: one message, the claims that support it, the evidence for each claim, and where each piece goes within the venue's limits. The outline also lists what is missing before drafting can start.

## When to use

- Results exist (or are planned) and a draft is about to start.
- A draft has structural problems and needs re-planning.
- Converting a thesis chapter or report into a paper.

Hand off instead for a thesis chapter (`thesis-chapter-writer`) or for writing individual sections (`abstract-writer`, `introduction-writer`).

## Prerequisites

- The contribution in one or two sentences and the main results, existing or planned.
- The target venue's current author guidelines: length limit, required sections, and template.
- A list of available figures, tables, and experiments.

## Inputs

- The contribution in one or two sentences, and the main results.
- Target venue and paper type (full research paper, short paper, journal article, review, systems or dataset paper).
- The venue's current call for papers or author guidelines: page or word limit, required sections, template.
- Available figures, tables, and experiments, and what is still missing.

## Instructions

1. **Get the venue's rules** from its current author guidelines. Limits and required sections change yearly; do not rely on memory. Record: length limit and what counts toward it (references and appendices often do not), required statements (ethics, limitations, data availability, reproducibility checklist), anonymisation, template.
2. **Write the one-sentence message** of the paper: "We show that X, which matters because Y." If this cannot be written, the paper is not ready to outline; say so.
3. **List the claims** (usually 2 to 4) and attach the evidence for each: an experiment, a table, a proof, a study. A claim with no evidence is either cut or becomes a to-do item.
4. **Choose the structure** for the paper type and field:

   | Type | Typical structure |
   |---|---|
   | Empirical (sciences, medicine, social science) | IMRaD: Introduction, Methods, Results, Discussion; structured abstract |
   | ML or CS conference | Introduction, Related Work, Method, Experiments, (Analysis), Limitations, Conclusion |
   | Systems | Introduction, Background and Motivation, Design, Implementation, Evaluation, Related Work, Conclusion |
   | Theory | Introduction, Preliminaries, Main Results, Proof Sketches, Discussion; full proofs in appendix |
   | Dataset or benchmark | Introduction, Related Datasets, Construction, Statistics and Analysis, Baselines, Limitations and Ethics |
   | Review | Introduction, Method of the review, Thematic sections, Open Problems, Conclusion |

5. **Outline each section** with: its purpose in one sentence, the points in order (one line per paragraph), the figures and tables it contains, and its length budget.
6. **Plan the display items first.** Most readers look at figures and tables before the text. Decide Figure 1 (the overview or key result), the main results table, and which results go to the appendix.
7. **Budget the length.** Set a page or word budget for each section so the total fits the limit. For an 8 to 9 page conference paper a common split is: introduction 1 to 1.25, related work 0.75 to 1, method 2 to 2.5, experiments 2.5 to 3, discussion and conclusion 0.5. Adjust to the paper.
8. **Check the flow**: reading only the section headings and the first sentence of each paragraph should convey the whole argument.
9. **List the gaps**: missing experiments, figures, citations, or decisions, each with an owner and priority.

## Output format

```markdown
# Outline: <working title>
Venue: <name, year>. Limit: <pages/words, what counts>. Template: <name>. Required: <statements>.
Message: <one sentence>

## Claims and evidence
| # | Claim | Evidence | Where |

## Sections
### 1. Introduction (≈1 page)
Purpose: ...
- P1: context ...
- P2: problem and gap ...
- P3: approach ...
- P4: contributions (bulleted)
Display: Fig. 1 (overview)

### 2. ...

## Display items
| Item | Shows | Supports claim | Status |

## Appendix plan
## Missing before drafting
| Item | Needed for | Priority |
```

## Examples

Requests that should trigger this skill:

- "Outline my paper on a new method for anomaly detection for ICML."
- "What sections should my empirical psychology paper have?"
- "Plan the paper before I start writing; here are my results."
- "Turn this thesis chapter into a journal paper outline."
- "My draft is disorganised. Re-plan the structure."

Requests that belong to another skill:

- "Structure my thesis chapter." → use `thesis-chapter-writer`
- "Write the introduction." → use `introduction-writer`
- "Which venue should I target?" → use `venue-recommender`

### Worked example

**Request:** "Outline an 8-page conference paper. Contribution: a pruning method that keeps 98% of accuracy at half the parameters. I have results on two datasets and one ablation."

**What the agent does:**

1. Asks for the venue's guideline page and records the limit and required sections, marking unconfirmed items.
2. Writes the one-sentence message and three claims with their evidence.
3. Chooses the ML conference structure and outlines each section to paragraph level with a page budget.
4. Plans Figure 1 and the main table first and lists gaps.

**Result (excerpt):**

```markdown
Message: A one-shot pruning rule halves parameters while keeping 98% of accuracy, without retraining.

| # | Claim | Evidence | Where |
|---|---|---|---|
| 1 | Halves parameters at 98% accuracy | Table 1, two datasets | Section 4.1 |
| 2 | Needs no retraining | Table 2 timing | Section 4.2 |
| 3 | The saliency term is responsible | ablation, Table 3 | Section 4.3 |

### 1. Introduction (about 1 page)
- P1: cost of large models in deployment
- P2: existing pruning needs retraining (gap)

Missing before drafting: variance over seeds for Table 1 (P0).
```

## Quality bar and pitfalls

- Do not state a venue's page limit or required sections from memory as fact. Take them from the current guidelines, or mark them "typical, confirm".
- The outline must not include results that do not exist. Mark planned experiments as planned.
- Every section earns its place by supporting a claim. Cut sections that only record effort.
- One main message. Papers that try to carry three unrelated contributions get rejected for lack of focus.
- Put the main result early. Do not make the reader wait for it until page 7.
- Keep the outline at the level of paragraphs. Section headings alone are not an outline.

## Limitations

- Venue rules change yearly and must be read from the current call; anything not confirmed is marked as typical.
- An outline cannot supply missing evidence. Claims without results are flagged, not planned around.
- Page budgets are estimates and shift once figures and tables are placed.

## Troubleshooting

| Problem | Likely cause | Solution |
|---|---|---|
| The one-sentence message cannot be written | The paper has no single main result yet | Stop outlining and settle the claims with `results-interpreter` first |
| The budget exceeds the page limit | Too many claims or display items | Move secondary results to the appendix and cut the weakest claim |
| The venue's required sections are unknown | The guidelines were not provided | Fetch the current call for papers; until then mark the items as unconfirmed, since invalid assumptions cause desk rejection |

## Related skills

- `results-interpreter` supplies the claims the outline is built on.
- `venue-recommender` if the venue is not yet chosen.
- `introduction-writer`, `abstract-writer`, `related-work-writer`, and `limitations-and-future-work-writer` draft the sections.
- `publication-figure-maker`, `architecture-diagram-maker`, and `latex-table-generator` produce the display items.
- `latex-paper-formatter` sets up the venue template.
- `idea-to-paper-pipeline` runs this as one stage of the full sequence.
