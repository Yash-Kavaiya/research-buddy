---
name: sample-size-power-calculator
description: "Computes required sample size, achieved power, or minimum detectable effect and writes the justification. Use when planning a quantitative study. Not for choosing the test."
version: 1.0.0
compatibility: "Requires Python 3.10 or later with SciPy. Runs locally with no network access."
allowed-tools: "Bash(python:*) Read Write"
metadata:
  author: "Yash Kavaiya <yash.kavaiya3@gmail.com>"
  tags: [power-analysis, sample-size, statistics]
---

# Sample Size and Power Calculator

Compute the number with a script, and justify every input, above all the effect size.

## Purpose

Give a defensible answer to "how many participants do I need" by computing it and by justifying every input, above all the effect size. It also reports what a fixed sample can detect, and writes the paragraph for a proposal or ethics form.

## When to use

- Planning a quantitative study (a priori sample size).
- Checking what a fixed sample can detect (sensitivity analysis).
- Writing the sample-size paragraph for a proposal, ethics form, or methods section.

Hand off instead for qualitative sample sizes, which rest on saturation (`methodology-designer`), and for choosing the test itself (`statistical-test-selector`).

## Prerequisites

- Python 3.10 or later with SciPy (`pip install scipy`).
- The primary hypothesis and the test that will analyse it.
- An expected or minimum important effect size with its source, plus alpha and target power.

## Inputs

- The primary hypothesis and the test that will analyse it.
- Expected effect size and where it comes from.
- Alpha (default 0.05), target power (default 0.80; 0.90 for confirmatory or clinical work), one- or two-sided.
- Allocation ratio, number of groups, expected attrition.

## Instructions

1. **Identify the design** from the primary analysis:

   | Analysis | Design argument | Effect size |
   |---|---|---|
   | Two independent groups, numeric outcome | `ttest-ind` | Cohen's d |
   | Before and after, or matched pairs | `ttest-paired` | Cohen's dz |
   | Three or more independent groups | `anova` | Cohen's f |
   | Two groups, binary outcome | `proportions` | Cohen's h, or `--p1` and `--p2` |
   | Association of two numeric variables | `correlation` | r |
   | Association of categorical variables, goodness of fit | `chi2` | Cohen's w, with `--df` |

2. **Establish the effect size**, in this order of preference:
   1. The smallest effect that would matter in practice (a minimal important difference), converted to a standardised effect.
   2. An estimate from a meta-analysis or several prior studies, reduced somewhat because published effects run high.
   3. A pilot study, treated as imprecise.
   4. Cohen's conventions (d = 0.2, 0.5, 0.8; f = 0.10, 0.25, 0.40; r = 0.1, 0.3, 0.5; w = 0.1, 0.3, 0.5) only as a last resort, and labelled as a convention.

   Conversions: d = (mean1 − mean2) / pooled SD. f = d / 2 for two groups. For paired designs dz = d / sqrt(2(1 − r)), where r is the correlation between the paired measures.
3. **Run the calculation:**

   ```bash
   python scripts/power_calc.py ttest-ind --effect 0.5 --power 0.8
   python scripts/power_calc.py anova --effect 0.25 --groups 3 --power 0.9 --dropout 0.15
   python scripts/power_calc.py proportions --p1 0.5 --p2 0.3 --power 0.8
   python scripts/power_calc.py ttest-paired --n 30 --effect 0.4          # achieved power
   python scripts/power_calc.py correlation --n 60 --power 0.8            # minimum detectable r
   ```

   Give two of sample size, power, and effect; the third is solved. Other options: `--alpha`, `--one-sided`, `--ratio` (n2/n1), `--dropout`. The output is JSON with the sample sizes, achieved power, and a `statement` sentence.
4. **Run a sensitivity table**: repeat for a smaller and a larger plausible effect, and show how n changes. This is what makes the choice defensible.
5. **Adjust for the design:** inflate for attrition (`--dropout`); for several primary outcomes, divide alpha (Bonferroni) and rerun with `--alpha`; for clustered data multiply by the design effect 1 + (m − 1) × ICC, where m is the cluster size.
6. **Write the justification** using the `statement` sentence as the base, adding the source of the effect size and the software.
7. **If the required n is out of reach**, give the options: a larger minimum effect of interest (with honesty about what is then undetectable), a more sensitive design (paired, covariates), a more reliable measure, or collaboration. Never adjust the effect size just to hit the available n.

## Available Scripts

| Script | Purpose | Arguments |
|---|---|---|
| `scripts/power_calc.py` | Solves for sample size, power, or detectable effect and prints JSON with a justification sentence | `DESIGN` (ttest-ind, ttest-paired, anova, proportions, correlation, chi2), `--effect`, `--p1`, `--p2`, `--n`, `--power`, `--alpha`, `--ratio`, `--groups`, `--df`, `--one-sided`, `--dropout` |

Run a script with the agent's script tool, for example `run_script("scripts/power_calc.py", args=[...])`, or from a shell in the skill folder with `python scripts/power_calc.py ...`. Each script prints usage with `--help`, validates its arguments, and exits with a non-zero code and an `error:` message on failure.

## Output format

```markdown
## Sample size
- Design and test: ...
- Effect size: d = 0.50, based on <source>
- Alpha 0.05 (two-sided), power 0.80
- Required: 64 per group, N = 128; recruit 151 allowing 15% attrition

## Sensitivity
| Effect size | n per group | Total N |
|---|---|---|

## Justification paragraph
> A priori power analysis (noncentral t distribution; SciPy) indicated that ...

## Assumptions and cautions
```

## Examples

Requests that should trigger this skill:

- "How many participants do I need to compare two teaching methods?"
- "Run a power analysis for a correlation of 0.3."
- "Is my study with 40 people underpowered?"
- "Justify my sample size for the ethics application."
- "What effect can I detect with 25 per group at 80% power?"

Requests that belong to another skill:

- "Which statistical test should I use?" → use `statistical-test-selector`
- "How many interviews do I need for a qualitative study?" → use `methodology-designer`
- "Analyse my collected data." → use `statistical-test-selector`

### Worked example

**Request:** "Two independent groups, I expect a medium effect (d = 0.5) based on a meta-analysis, alpha 0.05, 80% power, and about 15% dropout. How many do I recruit?"

**What the agent does:**

1. Identifies the design as `ttest-ind` with Cohen's d from a meta-analysis.
2. Runs `run_script("scripts/power_calc.py", args="ttest-ind --effect 0.5 --power 0.8 --dropout 0.15")`.
3. Repeats for d = 0.4 and d = 0.6 to build a sensitivity table.
4. Writes the justification paragraph with the effect-size source.

**Result (excerpt):**

```markdown
- Required: 64 per group, N = 128; recruit 151 allowing 15% attrition

| Effect size | n per group | Total N |
|---|---|---|
| 0.4 | 100 | 200 |
| 0.5 | 64 | 128 |
| 0.6 | 45 | 90 |

> For an independent-samples t test with alpha = 0.05, two-sided, 64 participants per group (N = 128) gives power of 0.80 to detect an effect of d = 0.5. Allowing for 15% attrition, 151 participants should be recruited.
```

## Quality bar and pitfalls

- Always compute with the script. Do not produce sample sizes from memory.
- The effect size is the decisive input. State its source; "medium effect" without a reason is a weak justification and reviewers know it.
- Do not run "post hoc power" from the observed effect of a finished study. It restates the p-value. Report a sensitivity analysis instead.
- The script covers simple designs. Mixed models, repeated-measures ANOVA, regression with many predictors, survival analysis, and structural equation models need simulation or dedicated software (G*Power, R `pwr`, `simr`, `WebPower`). Say so and do not force them into a simple design.
- The proportion and correlation designs use normal approximations (arcsine and Fisher z). They agree with exact methods to within a participant or two; for small samples or proportions near 0 or 1, check with an exact method.
- Power for the primary outcome does not cover secondary or subgroup analyses.
- Pilot studies estimate feasibility and variance. Their effect sizes are too noisy to plan on alone.

## Limitations

- Only simple designs are covered. Mixed models, repeated-measures ANOVA, multiple regression, survival analysis, and SEM need simulation or dedicated software.
- The proportion and correlation designs use normal approximations and can differ from exact methods by a participant or two.
- The result is only as good as the effect size supplied. A guessed effect size gives a guessed sample size.
- Clustered or multi-outcome designs need the adjustments described in the instructions; the script does not apply them.

## Troubleshooting

| Problem | Likely cause | Solution |
|---|---|---|
| `error: to solve for sample size give --effect (or --p1/--p2) and --power` | Fewer than two of sample size, power, and effect were supplied | Give any two; the third is computed |
| `error: required sample size exceeds 10,000,000` | The effect size is near zero | Check the effect-size value and units; a standardized effect is usually between 0.1 and 1 |
| `ModuleNotFoundError: No module named 'scipy'` | SciPy is not installed | Run `pip install scipy` or `pip install -r requirements.txt` |
| The result differs slightly from G*Power | Approximation for correlation or proportions | Report the method used; confirm with an exact tool when the sample is small |

## Related skills

- `research-question-formulator` for the hypothesis being powered.
- `methodology-designer` for the overall design and the qualitative case.
- `statistical-test-selector` to confirm the analysis the calculation assumes.
- `ethics-irb-drafter` and `grant-proposal-writer` use the justification paragraph.
- `results-interpreter` for interpreting non-significant results from a small sample.
