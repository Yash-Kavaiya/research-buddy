---
name: reproducibility-checklist
description: "Completes reproducibility and reporting checklists (NeurIPS, CONSORT, STROBE) from evidence in the manuscript and lists gaps. Use when a venue requires one. Not for reimplementing papers."
version: 1.0.0
metadata:
  author: "Yash Kavaiya <yash.kavaiya3@gmail.com>"
  tags: [reproducibility, checklist, reporting-guidelines, neurips]
---

# Reproducibility Checklist

## Purpose

Answer each checklist item from what the paper and its artifacts actually contain, cite where, and turn every gap into a concrete fix. A truthful "No" with a justification is preferred to an unsupported "Yes".

## When to use

- A venue requires a reproducibility or paper checklist with the submission.
- Preparing code, data, and models for release.
- Auditing a draft for missing experimental details before reviewers do.

Hand off instead for reimplementing someone else's paper (`paper-to-code-reproducer`).

## Prerequisites

- The manuscript with its appendix, and the venue and year.
- The venue's current checklist text, from the call for papers or the template.
- The code repository, configs, experiment log, and dataset documentation where they exist.

## Inputs

- The manuscript with appendix, and the venue and year.
- The venue's current checklist text. Obtain it from the call for papers or the template; items and answer formats change between years.
- The code repository, configs, experiment log, and dataset documentation.

## Instructions

1. **Get the right checklist** for the venue and year:

   | Context | Checklist or guideline |
   |---|---|
   | NeurIPS | Paper checklist in the LaTeX template (claims, limitations, theory, experimental reproducibility, open access to data and code, experimental details, statistical significance, compute resources, ethics, broader impacts, safeguards, licences, assets, human subjects, LLM usage) |
   | ICML, ICLR, AAAI, ACL venues | Venue-specific reproducibility or responsible-research checklist |
   | General ML | ML Reproducibility Checklist (Pineau et al.); ML Code Completeness Checklist |
   | Datasets | Datasheets for Datasets; Data Statements |
   | Models | Model Cards |
   | Clinical trials | CONSORT; SPIRIT for protocols |
   | Observational studies | STROBE |
   | Systematic reviews | PRISMA 2020 |
   | Diagnostic accuracy | STARD |
   | Prediction models, clinical AI | TRIPOD+AI, CONSORT-AI |
   | Animal research | ARRIVE |
   | Qualitative research | COREQ, SRQR |

   The EQUATOR Network lists reporting guidelines for health research.
2. **Answer each item from evidence.** Search the manuscript, appendix, and repository for the information. Record the answer in the venue's format (Yes, No, N/A, or as specified), a one- or two-sentence justification, and the location (section, table, appendix, file).
3. **Apply the evidence rule**: "Yes" requires a location. If the information exists only in the author's head or the code, the answer is "No, to be added", and it becomes an action.
4. **Audit the experimental details** that reviewers most often find missing:
   - *Data*: sources, versions, licences, splits and how they were made, preprocessing, exclusions, statistics.
   - *Model and training*: architecture details, parameter counts, every hyperparameter with its final value, the search space and method and budget, selection criterion.
   - *Evaluation*: metric definitions, number of runs or seeds, what error bars represent, statistical tests.
   - *Compute*: hardware type, memory, runtime per run, total compute including failed and preliminary runs.
   - *Code*: dependencies with versions, training and evaluation commands, pretrained weights, random seeds, expected results.
   - *Theory*: full assumptions and complete proofs.
5. **Check the artifacts.** For a code release, against the ML Code Completeness items: dependency specification, training code, evaluation code, pretrained models, and a README with results and the commands that produce them. Verify the README commands run from a clean environment if possible.
6. **Handle anonymity.** For double-blind review, release code through an anonymised repository or supplementary zip, with no names, usernames, paths, or institution identifiers in code, commit history, or notebooks.
7. **Do not treat "No" as failure.** Venues state that an honest "No" with a justification is acceptable (for example proprietary data that cannot be released). A false "Yes" is a problem.
8. **Produce the action list**, ordered by reviewer impact, and draft the text to add for each gap.
9. **Write the reproducibility statement** where the venue asks for one: a short paragraph pointing to where data, code, hyperparameters, and proofs are found.

## Output format

```markdown
## <Checklist name>, <venue and year>

| # | Item | Answer | Justification | Where |
|---|---|---|---|---|
| 3 | Statistical significance: error bars reported and defined? | Yes | Mean ± s.d. over 5 seeds; defined in captions | Tables 2–3, §5.1 |
| 5 | Compute resources reported? | No (to add) | GPU type given; runtime and total compute missing | n/a |

## Actions before submission
| Priority | Gap | Text or artifact to add | Where |

## Reproducibility statement (draft)
> ...

## Items answered N/A, with the reason
```

For NeurIPS, also deliver the answers in the template's `\answerYes{}`, `\answerNo{}`, `\answerNA{}` form with justifications.

## Examples

Requests that should trigger this skill:

- "Fill in the NeurIPS paper checklist for my submission."
- "Complete the ML reproducibility checklist for this paper."
- "Is my paper reproducible? What is missing?"
- "Write a reproducibility statement for ICLR."
- "Check my trial report against CONSORT."

Requests that belong to another skill:

- "Reimplement this paper from the PDF." → use `paper-to-code-reproducer`
- "Check page limits and anonymisation." → use `camera-ready-checker`
- "Log my experiment runs." → use `experiment-logger`

### Worked example

**Request:** "Complete the NeurIPS checklist for the attached paper and tell me what to add before the deadline."

**What the agent does:**

1. Obtains this year's checklist from the template and reads the paper and appendix.
2. Answers each item with Yes, No, or N/A, a justification, and the location; applies the rule that Yes needs a location.
3. Audits experimental details: finds seeds and error bars reported, compute and hyperparameter search missing.
4. Writes the action list with draft text for each gap.

**Result (excerpt):**

```markdown
| # | Item | Answer | Justification | Where |
|---|---|---|---|---|
| 7 | Statistical significance | Yes | Mean and s.d. over 5 seeds; defined in captions | Tables 2 and 3 |
| 8 | Compute resources | No (to add) | GPU type is given; runtime and total compute are not | n/a |

## Actions before submission
| Priority | Gap | Text to add | Where |
| 1 | Compute | "Each run took [hours] on one [GPU]; all experiments, including preliminary runs, used about [total] GPU hours." | Appendix B |

Placeholders are for the authors to fill from their logs.
```

## Quality bar and pitfalls

- Answer truthfully. Never mark "Yes" for something not in the submission; reviewers check, and some venues desk-reject for inaccurate checklists.
- Do not invent details to close a gap (seeds, runtimes, hardware, hyperparameters). Ask the author or leave it as an action.
- Use the checklist wording for the current year. Do not reproduce an older version from memory as if it were current.
- "Code will be released upon acceptance" is a "No" for the submission as reviewed. Say so in the justification.
- Report total compute, including runs that did not make it into the paper, where the checklist asks.
- Releasing data has conditions: licences, consent, and personal information. Check before promising release.
- Reproducibility information in the appendix must be referenced from the main text, or readers will not find it.

## Limitations

- Answers are based on the manuscript and files provided. Information that exists only in the authors' heads cannot be confirmed and is recorded as a gap.
- Checklist wording changes yearly; an outdated version leads to wrong items.
- The skill does not run the code, so it cannot confirm that released code reproduces the results.
- Completing a checklist documents reproducibility; it does not create it.

## Troubleshooting

| Problem | Likely cause | Solution |
|---|---|---|
| An item cannot be answered from the paper | The information is missing | Answer "No (to add)", ask the authors, and draft the text with placeholders |
| The checklist version is uncertain | The venue's current template was not provided | Fetch the current template; do not rely on a remembered version, which may be invalid |
| Authors want to answer Yes for unreleased code | Release is planned after acceptance | Answer No for the submission as reviewed and state the release plan in the justification |

## Related skills

- `experiment-logger` holds the configs, seeds, commits, and run times the checklist asks for.
- `experiment-planner` plans for these items before experiments start.
- `limitations-and-future-work-writer` for the limitations item.
- `ethics-irb-drafter` for human-subjects and data-consent items.
- `dataset-finder` for dataset licences and documentation.
- `self-peer-reviewer` uses the completed checklist as part of the pre-submission review.
- `camera-ready-checker` confirms the checklist is included in the final PDF.
