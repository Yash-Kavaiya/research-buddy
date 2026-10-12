---
name: paper-critic
description: "Critiques a research paper for weak assumptions, missing baselines, and validity threats, rated by severity. Use when deciding how far to trust a paper. Not for summaries; use paper-summarizer."
version: 1.0.0
metadata:
  author: "Yash Kavaiya <yash.kavaiya3@gmail.com>"
  tags: [critical-appraisal, peer-review, validity]
---

# Paper Critic

Assess whether a paper's evidence supports its claims. Every criticism must point at something specific in the paper and explain what it changes about the conclusions.

## Purpose

Assess whether a paper's evidence supports its claims, and say which claims stand, which stand with a narrower scope, and which are unsupported. Every criticism points at a specific place in the paper and explains what it changes.

## When to use

- Deciding how much to rely on a paper.
- Journal club, reading group, or a critical appraisal assignment.
- Writing a formal review of someone else's submission.

Hand off instead for a neutral summary (`paper-summarizer`) or for stress-testing the user's own draft before submission (`self-peer-reviewer`).

## Prerequisites

- The full text of the paper, including appendix and supplementary material where available.
- Knowledge of the field's standard baselines and evaluation, or the ability to look them up with `paper-search`.
- No scripts or API keys are required.

## Inputs

- Full text of the paper, including appendix and supplementary material when available.
- The user's purpose: build on it, cite it, review it, or teach it.
- Field, which decides the checklist in step 3.

## Instructions

1. **List the claims.** Write down each claim made in the abstract, introduction, and conclusion. Number them. The critique is organised around these.
2. **Map evidence to claims.** For each claim, find the experiment, analysis, proof, or citation offered for it. A claim with no evidence, or evidence weaker than the claim's wording, is your first finding.
3. **Run the validity checks** for the paper type:

   | Area | Questions |
   |---|---|
   | Internal validity | Confounds? Was the comparison fair (same data, tuning budget, compute)? Randomisation and blinding? Leakage between train and test? |
   | Baselines | Are the strongest current baselines included? Were they tuned or copied from old papers? Is there a simple baseline? |
   | Statistics | Sample size, number of seeds or runs, variance reported, tests appropriate, multiple comparisons corrected, effect sizes given? |
   | Measurement | Do the metrics capture the claimed property? Any validated instrument? Ceiling effects? |
   | External validity | How many datasets, populations, or settings? Are they representative of the claimed scope? |
   | Ablations | Is the gain attributed to the right component? Is anything bundled together? |
   | Assumptions (theory) | Which are needed, are they realistic, and where do the proofs use them? |
   | Reproducibility | Code, data, hyperparameters, preregistration? |
   | Reporting | Selective reporting, cherry-picked examples, claims in the abstract absent from the results? |

4. **Rate each issue**: *critical* (a main claim does not follow), *major* (a claim is weakened or its scope narrows), *minor* (clarity or completeness).
5. **Say what would fix it**: the experiment, analysis, or rewording that would resolve the issue.
6. **Record strengths** with the same specificity. A critique that lists only faults misjudges the paper.
7. **Give the bottom line**: which claims stand, which stand with a narrower scope, and which are unsupported.

## Output format

```markdown
# Critical reading: <Title> (<authors>, <year>)

## Claims and support
| # | Claim | Evidence offered | Supported? |
|---|---|---|---|
| 1 | ... | Table 2, §5.1 | yes / partly / no |

## Strengths
- ... (where in the paper)

## Issues
### Critical
- **<issue>** (§/Table/Fig). Why it matters: ... What would resolve it: ...
### Major
### Minor

## Bottom line
What can be relied on, and under which conditions.

## Questions for the authors
1. ...
```

## Reference files

Open these only when the step calls for them; they are not needed for every request.

- `references/validity-checklists.md`: Read at step 3, when running the validity checks for the paper's study type.
- `assets/critical-appraisal-template.md`: Copy and fill for the critical appraisal.

## Examples

Requests that should trigger this skill:

- "Critique this paper for our journal club."
- "What are the weaknesses of this study?"
- "Can I trust the results in this preprint?"
- "Is the methodology of this RCT sound?"
- "I have to review this submission. What should I look for?"

Requests that belong to another skill:

- "Just summarise the paper." → use `paper-summarizer`
- "Review my own draft before I submit." → use `self-peer-reviewer`
- "Which test should they have used?" → use `statistical-test-selector`

### Worked example

**Request:** "Critically appraise the attached paper. It claims a new optimizer trains ResNets faster than Adam."

**What the agent does:**

1. Lists the claims from the abstract and conclusion and numbers them.
2. Maps each claim to its evidence and checks the comparison for fairness.
3. Runs the validity checks: baselines, tuning budget, seeds, datasets, ablations.
4. Rates each issue and states what would resolve it.

**Result (excerpt):**

```markdown
### Major
- **Baselines were not tuned** (Section 4.1, Table 1). Adam uses its default learning rate while the new optimizer's rate was searched over 12 values. Why it matters: the speed-up may come from tuning. What would resolve it: the same search budget for both.
- **Single seed** (Table 2). No variance is reported, so the 0.4-point gap cannot be separated from noise.

## Bottom line
The claim of faster convergence is not yet supported; the claim that the method trains stably is.
```

## Quality bar and pitfalls

- Locate every criticism: section, table, figure, or equation. Unlocated criticism cannot be checked.
- Verify before asserting absence. "No variance reported" requires having looked in the appendix.
- Criticise what the paper claims, not what you wish it had studied. Missing scope is a limitation only if the paper claims that scope.
- Distinguish "not shown" from "false". Most weaknesses are insufficient evidence.
- Do not demand experiments that are impossible for the setting (a new clinical trial, industrial-scale compute) without saying so.
- Name the baseline you think is missing, and check it existed before the paper's submission date.
- Keep tone professional. The target is the work.

## Limitations

- The critique is limited to what the paper and its supplement report. Raw data and code are usually not inspected.
- Judging whether a baseline is missing depends on the reviewer's knowledge of the field and should be checked by retrieval.
- A critique identifies insufficient evidence. It rarely proves a result false.

## Troubleshooting

| Problem | Likely cause | Solution |
|---|---|---|
| The critique lists only generic issues | Claims were not mapped to evidence first | Go back to the numbered claims table and tie each issue to a claim and a location |
| An issue is raised that the appendix already answers | The supplementary material was not read | Read the appendix and supplement before asserting that something is missing |
| The field's standards are unfamiliar | The paper is outside the reviewer's area | Retrieve two recent papers from the same venue and compare their evaluation setup |

## Related skills

- `paper-summarizer` to establish what the paper says before judging it.
- `math-and-equation-explainer` to check a derivation step by step.
- `statistical-test-selector` to confirm whether the paper's test was appropriate.
- `self-peer-reviewer` applies the same scrutiny to the user's own draft.
- `paper-comparison-matrix` to see how the paper's setup compares with its neighbours.
