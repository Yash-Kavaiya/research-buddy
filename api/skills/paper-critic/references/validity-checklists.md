# Validity checklists by study type

Use the block for the paper's type. For each item answer yes, no, or not reported, and note the location.

## 1. Any empirical paper

| # | Check | Why it matters |
|---|---|---|
| 1 | Is each claim in the abstract supported by a specific result? | Abstracts overstate |
| 2 | Is the comparison condition fair (same data, effort, resources)? | Unequal effort explains many gains |
| 3 | Is variability reported (SD, CI, runs)? | Without it, a difference may be noise |
| 4 | Are effect sizes given, not only p-values? | Significance is not magnitude |
| 5 | Were the outcomes and analyses fixed before seeing data? | Flexible analysis inflates findings |
| 6 | Are exclusions and missing data reported? | Selective exclusion biases results |
| 7 | Does the scope of the conclusion match the scope of the sample or data? | Over-generalisation |
| 8 | Are data and code available? | Checkability |

## 2. Machine learning and other computational experiments

| Area | Checks |
|---|---|
| Baselines | Strongest current method included? Baselines tuned with the same budget, or copied from older papers? A simple baseline present? |
| Data | Standard splits? Any overlap between training and test data, or between test data and pretraining corpora? Preprocessing identical across methods? |
| Tuning | Hyperparameter search described for all methods? Model selection on validation, not test? |
| Variance | Number of seeds; mean and spread; significance tests where gaps are small |
| Ablations | Does the gain come from the claimed component? Any change in parameters, data, or compute bundled with it? |
| Metrics | Standard metric and implementation? Does the metric measure the claimed property? |
| Generality | More than one dataset or task? Results where the method does worse reported? |
| Cost | Compute, parameters, latency reported when efficiency is claimed? |
| Reproducibility | Code, configs, seeds, hardware |

## 3. Randomised experiments and trials

| Area | Checks |
|---|---|
| Randomisation | Method described; allocation concealed |
| Blinding | Participants, staff, outcome assessors |
| Attrition | Dropout by arm; intention-to-treat analysis |
| Outcomes | Primary outcome prespecified and matching the registration; no switched outcomes |
| Power | Sample-size calculation given and met |
| Analysis | Baseline balance; adjustment prespecified; multiplicity handled |
| Harms | Adverse events reported |

## 4. Observational studies

| Area | Checks |
|---|---|
| Confounding | Plausible confounders measured and adjusted; residual confounding discussed |
| Selection | How participants entered the study; who is missing |
| Measurement | Exposure and outcome measured the same way in all groups; recall bias |
| Temporality | Exposure measured before outcome |
| Reverse causation | Considered and addressed |
| Causal language | Conclusions phrased as associations unless a causal design is used |

## 5. Surveys and questionnaire studies

| Area | Checks |
|---|---|
| Sampling | Frame, method, response rate, non-response bias |
| Instrument | Validated scale or new items; reliability reported; pilot |
| Common-method bias | Predictor and outcome from the same self-report at one time |
| Analysis | Ordinal data handled appropriately; multiple testing |

## 6. Qualitative studies

| Area | Checks |
|---|---|
| Sampling | Rationale; who was not reached |
| Data | How collected, by whom, recorded and transcribed |
| Analysis | Approach named and followed; how themes were developed; more than one analyst or an audit trail |
| Reflexivity | The researcher's position and its influence |
| Evidence | Quotes from several participants per theme; negative cases |
| Claims | Transferability argued, not statistical generalisation claimed |

## 7. Theory papers

| Area | Checks |
|---|---|
| Assumptions | All stated; realistic; which results need which |
| Proofs | Complete, or sketched with full versions in the appendix; steps that do not obviously follow |
| Tightness | Is the bound tight or vacuous in practical regimes? |
| Relation to practice | Do experiments use settings where the assumptions hold? |

## 8. Common statistical problems

| Problem | Sign |
|---|---|
| Multiple comparisons | Many tests, no correction, a few significant |
| Pseudo-replication | Repeated measures treated as independent observations |
| Wrong test for the design | Independent test on paired data, or the reverse |
| Significance filter | Only significant outcomes reported |
| Difference of significance | "A is significant, B is not" presented as A differing from B |
| Small sample, large effect | Likely overestimate |
| Regression to the mean | Extreme groups improving without a control |

## 9. Severity

| Rating | Meaning | Example |
|---|---|---|
| Critical | A main claim does not follow | Test-set tuning; no control for an obvious confound |
| Major | A claim is weakened or its scope narrows | Single dataset for a general claim; untuned baselines |
| Minor | Completeness or clarity | Missing hyperparameter; unclear figure |

## 10. Fairness rules for the critic

- Check the appendix before saying something is missing.
- Judge the paper against what it claims, and against the standard of its venue and year.
- Name the missing baseline, and confirm it existed before submission.
- "Not shown" is different from "false". Most weaknesses are insufficient evidence.
