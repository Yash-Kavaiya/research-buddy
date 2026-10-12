---
name: statistical-test-selector
description: "Chooses a statistical test from the design, checks assumptions, runs it on a CSV, and reports APA-style results with effect size. Use when comparing groups. Not for sample-size planning."
version: 1.0.0
compatibility: "Requires Python 3.10 or later with NumPy and SciPy. Runs locally with no network access."
allowed-tools: "Bash(python:*) Read Write"
metadata:
  author: "Yash Kavaiya <yash.kavaiya3@gmail.com>"
  tags: [statistics, hypothesis-testing, apa, effect-size]
---

# Statistical Test Selector

Match the test to the design and the data, verify the assumptions, compute with a script, and report what the result does and does not show.

## Purpose

Match the statistical test to the study design and the observations, verify its assumptions, compute the result with code, and report it with an effect size and interval in APA style. It also says what the result does and does not show.

## When to use

- Planning the analysis for a study.
- Analysing collected data to compare groups or test an association.
- Checking whether a reported test was appropriate.

Hand off instead for sample-size planning (`sample-size-power-calculator`) and for turning results into findings (`results-interpreter`).

## Prerequisites

- Python 3.10 or later with NumPy and SciPy (`pip install numpy scipy`).
- A CSV in long format: one row per observation, with a column for the outcome and one for the group or second variable.
- Knowledge of the design: independent or paired, number of groups, and anything that breaks independence.

## Inputs

- The research question or hypothesis.
- The outcome variable and its type (continuous, ordinal, binary, count, categorical).
- The predictor or grouping: number of groups, independent or paired/repeated.
- Sample size per group, and the data file when it exists (CSV, long format: one row per observation).
- Anything that breaks independence: repeated measures, clusters, matched samples.

## Instructions

1. **Classify the question** and pick the candidate test:

   | Goal | Outcome | Design | Parametric | Non-parametric |
   |---|---|---|---|---|
   | Compare 2 groups | Continuous | Independent | Welch's t test | Mann-Whitney U |
   | Compare 2 conditions | Continuous | Paired | Paired t test | Wilcoxon signed-rank |
   | Compare 3+ groups | Continuous | Independent | One-way ANOVA or Welch's ANOVA | Kruskal-Wallis |
   | Compare 3+ conditions | Continuous | Repeated | Repeated-measures ANOVA or mixed model | Friedman |
   | Association | Two continuous | n/a | Pearson r | Spearman rho |
   | Association | Two categorical | Independent | Chi-square | Fisher's exact (2×2, small counts) |
   | Paired proportions | Binary | Paired | McNemar | n/a |
   | Predict an outcome | Continuous / binary / count | Several predictors | Linear / logistic / Poisson regression | n/a |
   | Clustered or longitudinal | Any | Nested | Mixed-effects model, GEE | n/a |

2. **Run the script** for the designs it covers. It checks assumptions, picks the test, and reports:

   ```bash
   python scripts/run_test.py two-groups data.csv --value score --group condition
   python scripts/run_test.py two-groups data.csv --value score --group time --paired --subject id
   python scripts/run_test.py multi-groups data.csv --value accuracy --group model
   python scripts/run_test.py correlation data.csv --x hours --y grade
   python scripts/run_test.py categorical data.csv --row treatment --col outcome
   ```

   The JSON output contains descriptives, assumption checks (Shapiro-Wilk, Levene, expected counts), the chosen test with the `reason`, the statistic, p-value, effect size, post hoc comparisons for 3+ groups, and an `apa` string. `--test` overrides the choice; use it when the analysis plan fixed the test in advance.
3. **How the script decides.** Independent two-group comparisons default to Welch's t test, which does not assume equal variances. Non-parametric tests are chosen when normality is rejected and a group has fewer than 30 observations. For 3+ groups, Levene's test decides between classic and Welch's ANOVA. Post hoc: Tukey HSD after ANOVA; Holm-adjusted pairwise tests otherwise.
4. **For designs the script does not cover** (repeated measures with 3+ levels, factorial ANOVA, regression, mixed models, McNemar, Friedman), write the analysis in Python (`scipy`, `statsmodels`, `pingouin`) or R, run it, and report the same elements.
5. **Inspect the data yourself.** Look at group sizes, outliers, and a plot. Assumption tests are underpowered in small samples and oversensitive in large ones; the plot and the design matter more than the Shapiro-Wilk p-value.
6. **Correct for multiple comparisons** when several tests address one question (Holm or Benjamini-Hochberg), and say which family of tests was corrected.
7. **Report** with descriptives, the test, the statistic with degrees of freedom, the exact p-value, the effect size, and a confidence interval. Start from the `apa` string and write `chi-square`, `eta squared`, and similar names as symbols (χ², η²) in the manuscript.

## Available Scripts

| Script | Purpose | Arguments |
|---|---|---|
| `scripts/run_test.py two-groups` | Compares a numeric outcome between two groups (Welch t, Mann-Whitney, paired t, Wilcoxon) | `CSV`, `--value COL`, `--group COL`, `--paired`, `--subject COL`, `--test NAME` |
| `scripts/run_test.py multi-groups` | Compares three or more independent groups (ANOVA, Welch ANOVA, Kruskal-Wallis) with post hoc tests | `CSV`, `--value COL`, `--group COL`, `--test NAME` |
| `scripts/run_test.py correlation` | Pearson or Spearman correlation with confidence interval | `CSV`, `--x COL`, `--y COL`, `--test NAME` |
| `scripts/run_test.py categorical` | Chi-square test of independence or Fisher's exact test | `CSV`, `--row COL`, `--col COL`, `--test NAME` |

Run a script with the agent's script tool, for example `run_script("scripts/run_test.py two-groups", args=[...])`, or from a shell in the skill folder with `python scripts/run_test.py two-groups ...`. Each script prints usage with `--help`, validates its arguments, and exits with a non-zero code and an `error:` message on failure.

## Output format

```markdown
## Analysis
- Question: ...
- Variables: outcome <type>, grouping <levels, independent | paired>
- Test: <name>. Why: <reason from assumption checks and design>

## Assumption checks
| Check | Result | Verdict |

## Result
Descriptives: control M = 70.2, SD = 8.1, n = 30; treatment M = 75.8, SD = 7.9, n = 30.
> Scores were higher in the treatment group than in the control group, t(57.9) = −2.71, p = .009, g = −0.69, 95% CI of the difference [−9.74, −1.46].

## Post hoc comparisons (if any)
## Interpretation and caveats
```

## Examples

Requests that should trigger this skill:

- "Which statistical test should I use to compare three teaching methods?"
- "Is the difference between these two groups significant? Here is data.csv."
- "My scores are not normally distributed. What test do I run?"
- "Run a Mann-Whitney U test and report it in APA format."
- "Is there a relationship between study hours and exam grade in this file?"

Requests that belong to another skill:

- "How many participants do I need?" → use `sample-size-power-calculator`
- "What do these results mean for my paper?" → use `results-interpreter`
- "Plot these group differences." → use `publication-figure-maker`

### Worked example

**Request:** "data.csv has columns condition (control, treatment) and score for 60 different students. Is the treatment group better?"

**What the agent does:**

1. Classifies the design: two independent groups, continuous outcome.
2. Runs `run_script("scripts/run_test.py", args="two-groups data.csv --value score --group condition")`.
3. Reads the assumption checks and the reason for the chosen test, and looks at group sizes and outliers.
4. Reports descriptives, the test, effect size, and interval.

**Result (excerpt):**

```markdown
Test: Welch's t test. Why: Shapiro-Wilk did not reject normality in any group; Welch's test is used because it does not assume equal variances.

> Scores were lower in the control group (M = 70.1, SD = 7.9, n = 30) than in the treatment group (M = 75.6, SD = 6.5, n = 30), t(58.00) = -3.01, p = .004, g = -0.77, 95% CI of the difference [-9.26, -1.86].
```

## Quality bar and pitfalls

- Run the test; never estimate a statistic or p-value. Every reported number comes from executed code.
- The design decides the test before the data does. Paired data analysed as independent, or repeated measures treated as separate observations, is the most damaging error.
- Report the effect size and interval with every test. A p-value alone says nothing about magnitude.
- p > .05 means the data are inconclusive at this sample size. It does not show there is no effect.
- Do not test several outcomes or subgroups and report only the significant ones.
- Choosing the test after seeing which one gives p < .05 is p-hacking. Record the choice and its reason first.
- Report exact p-values (p = .032), and p < .001 for very small ones. Never write p = .000.
- Likert single items are ordinal: use rank-based tests or ordinal models.

## Limitations

- The script covers two-group, multi-group, correlation, and contingency-table designs. Repeated measures with three or more levels, factorial ANOVA, regression, and mixed models must be coded separately.
- Assumption tests are underpowered in small samples and oversensitive in large ones; plots and the design matter more.
- A test cannot repair a flawed design, such as non-independent observations analysed as independent.
- Statistical significance does not establish practical importance or causation.

## Troubleshooting

| Problem | Likely cause | Solution |
|---|---|---|
| `error: column 'x' not found; columns are [...]` | The column name is misspelled or the CSV has a different header | Use one of the listed column names exactly |
| `error: expected 2 groups in 'g', found 3` | The grouping column has more than two levels | Use `multi-groups`, or filter the file to the two groups of interest |
| `error: --paired needs --subject to match observations` | A paired test was requested without an id column | Add `--subject` with the column that identifies each participant |
| Results look wrong or validation of the input fails | Non-numeric cells, missing values, or wide-format data | Rows with non-numeric outcomes are dropped; reshape wide data to long format and recheck group sizes in the output |

## Related skills

- `sample-size-power-calculator` to plan the sample for the chosen test.
- `methodology-designer` and `experiment-planner` for the analysis plan.
- `results-interpreter` to turn the output into findings.
- `publication-figure-maker` to plot the comparison.
- `latex-table-generator` for the results table.
- `paper-critic` uses the same table to check tests in published papers.
