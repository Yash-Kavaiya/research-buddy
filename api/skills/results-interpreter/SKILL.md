---
name: results-interpreter
description: "Turns raw results, statistical output, or metrics into findings with evidence, effect size, uncertainty, and caveats. Use when writing results and discussion. Not for running the tests."
version: 1.0.0
metadata:
  author: "Yash Kavaiya <yash.kavaiya3@gmail.com>"
  tags: [results, interpretation, discussion, scientific-writing]
---

# Results Interpreter

Say what the numbers support, how strongly, and where they stop. A finding is a claim plus its evidence plus its limits.

## Purpose

Say what a set of numbers supports, how strongly, and where the support stops. Each finding is a claim with its evidence, its size and uncertainty, the conditions under which it holds, and the wording it justifies.

## When to use

- Experiments or analyses are done and need to become findings.
- Writing the results and discussion sections.
- Deciding whether an improvement is real and whether it matters.

Hand off instead to run the statistics (`statistical-test-selector`) or to plan further experiments (`experiment-planner`, `ablation-study-designer`).

## Prerequisites

- The results: tables, CSV exports, statistical output, logs, or plots.
- The setup: datasets, baselines, metrics, sample sizes, number of runs or seeds, and what was being tested.
- Optional: Python to recompute summaries from raw numbers.

## Inputs

- The results: tables, CSV files, statistical output, training logs, confusion matrices, plots.
- What was being tested: the research questions, hypotheses, or claims.
- The setup: datasets, baselines, metrics, sample sizes, number of runs or seeds, how the baselines were obtained.
- The analysis plan, if one was fixed in advance.

Ask for the setup when it is missing. Numbers cannot be interpreted without knowing how they were produced.

## Instructions

1. **Check the numbers before reading them.** Do totals and percentages add up? Are any values impossible (accuracy above 100, negative variance, identical results across seeds)? Are the best results suspiciously good (possible leakage)? Raise problems first.
2. **Restate each question or hypothesis** and locate the numbers that bear on it.
3. **Describe before inferring.** State the direction and size of each difference in plain terms and in the metric's units: absolute difference, relative change, and effect size.
4. **Quantify uncertainty.** Use the variance across seeds or participants, confidence intervals, and tests. If there is one run and no variance, say the result is a single observation and cannot be separated from noise. Compute what can be computed from the supplied data with code, not by eye.
5. **Judge practical significance.** Compare the difference with: run-to-run noise; the gap between existing methods on this benchmark; the minimal difference that matters in use; and the extra cost of getting it.
6. **Look for the pattern across conditions.** Where does the effect hold, shrink, or reverse (datasets, subgroups, sizes, difficulty levels)? An average can hide opposite effects.
7. **Consider alternative explanations** for each finding: confounds (more parameters, more data, more tuning), selection of the best checkpoint or seed, measurement artefacts, multiple comparisons, regression to the mean.
8. **Grade each finding**: *well supported* (consistent, replicated across datasets or seeds, clear of noise), *suggestive* (right direction, limited evidence), or *inconclusive*.
9. **Report negative and null results** with the same care. State what was tried and what the data rule out.
10. **Draft the text.** Results: what was found, with numbers, in the order of the research questions, no interpretation beyond what the numbers show. Discussion: what it means, how it relates to prior work, alternative explanations, limitations.

## Output format

```markdown
## Data checks
- <anything inconsistent or suspicious, or "no issues found">

## Findings
### F1. <Claim in one sentence>
- Evidence: <numbers, table or figure reference>
- Size: <absolute, relative, effect size>; uncertainty: <CI, SD over n seeds, test>
- Holds for: ... Does not hold for: ...
- Alternative explanations: ...
- Support: well supported | suggestive | inconclusive

### F2. ...

## What you can and cannot claim
| Claim | Verdict | Wording to use |

## Suggested additional analyses
## Draft text
### Results
### Discussion
```

## Examples

Requests that should trigger this skill:

- "What do these results mean? Here is my results table."
- "Help me write the results section from this SPSS output."
- "Is a 0.6 point accuracy improvement meaningful?"
- "Explain this regression table in plain language."
- "What can I claim from these numbers and what can't I?"

Requests that belong to another skill:

- "Which test should I run on this?" → use `statistical-test-selector`
- "Design the follow-up experiments." → use `experiment-planner`
- "Write the limitations section." → use `limitations-and-future-work-writer`

### Worked example

**Request:** "My model gets 84.1 accuracy vs 83.5 for the baseline on one dataset, single run each. Can I say it outperforms?"

**What the agent does:**

1. Checks the numbers for consistency and asks how the baseline was obtained.
2. States the difference: 0.6 points absolute, on one dataset, one run each.
3. Notes that with no variance estimate the difference cannot be separated from run-to-run noise.
4. Grades the finding and gives wording that matches it, plus the analysis that would firm it up.

**Result (excerpt):**

```markdown
### F1. The model scores 0.6 points higher than the baseline on dataset A
- Evidence: 84.1 vs 83.5 accuracy, one run each
- Uncertainty: unknown; no repeated runs
- Support: inconclusive

| Claim | Verdict | Wording to use |
|---|---|---|
| "outperforms the baseline" | not supported | "obtains 0.6 points higher accuracy in a single run; repeated runs are needed to confirm" |

Suggested analysis: 5 seeds per method and a second dataset.
```

## Quality bar and pitfalls

- Use only the numbers provided or computed from them. Never fill in a missing value, standard deviation, or p-value.
- Do not turn "not significant" into "no effect", or "significant" into "important".
- Correlational results get correlational verbs: "is associated with", not "leads to" or "improves".
- "Outperforms" needs a fair comparison: same data, same tuning effort, variance reported. Otherwise write "obtains a higher score under these conditions".
- A gain smaller than the seed-to-seed standard deviation is not a finding.
- Do not explain a result with a mechanism that was not tested. Offer it as a hypothesis and say what would test it.
- Report all conditions that were run, including the ones that did not work.
- Match the strength of the wording to the grade: "shows" for well supported, "suggests" for suggestive.
- If the results contradict the user's hypothesis, say so plainly. Do not look for a framing that hides it.

## Limitations

- Interpretation is limited to the numbers and setup provided. Missing variance, seeds, or baseline details cap what can be concluded.
- Mechanisms offered to explain a result are hypotheses unless they were tested.
- The skill cannot detect errors in how the results were produced beyond visible inconsistencies.

## Troubleshooting

| Problem | Likely cause | Solution |
|---|---|---|
| Numbers do not add up or validation of a table fails | A transcription mistake, mixed units, or different denominators | Stop and ask for the raw output before interpreting |
| The setup is unknown | Only a table was pasted | Ask for datasets, baselines, seeds, and how the baselines were tuned; interpretation without them is unreliable |
| The result contradicts the hypothesis | The hypothesis may be wrong | Report it plainly, check for errors once, and describe what the result does show |

## Related skills

- `statistical-test-selector` to compute tests, effect sizes, and intervals.
- `experiment-logger` as the source of run records.
- `ablation-study-designer` and `experiment-planner` for the follow-up analyses.
- `publication-figure-maker` and `latex-table-generator` to present the findings.
- `limitations-and-future-work-writer` uses the caveats recorded here.
- `abstract-writer` and `introduction-writer` take the "wording to use" column.
- `self-peer-reviewer` checks the claims against the evidence again before submission.
