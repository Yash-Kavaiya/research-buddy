---
name: experiment-planner
description: "Plans experiments before running them: claims, baselines, datasets, metrics, seeds, ablations, and a prioritized compute budget. Use when designing an evaluation. Not for human-participant studies."
version: 1.0.0
metadata:
  author: "Yash Kavaiya <yash.kavaiya3@gmail.com>"
  tags: [experiment-design, evaluation, baselines, compute-budget]
---

# Experiment Planner

Decide what will be run, why, and at what cost before any compute or lab time is spent. Each experiment exists to support or refute a specific claim.

## Purpose

Decide what will be run, why, and at what cost before compute or lab time is spent. Every experiment is tied to a claim it could support or refute, and the list is prioritized so the essential ones fit the budget and deadline.

## When to use

- Before starting the experimental work for a paper or thesis chapter.
- When a deadline or budget forces choosing which experiments to run.
- When reviewers asked for more experiments and the response needs a plan.

Hand off instead for overall study design with human participants (`methodology-designer`) or the detailed ablation table (`ablation-study-designer`).

## Prerequisites

- The claims the paper intends to make and a description of the method.
- The resources: hardware, GPU hours or lab time, and the deadline.
- A timed pilot run, or permission to estimate cost roughly with the basis stated.

## Inputs

- The claims the paper intends to make, in order of importance.
- The method and what is new in it.
- Resources: hardware, GPU hours or lab time, people, deadline.
- Target venue, which sets the expected evaluation standard.
- Existing results, code, and datasets.

## Instructions

1. **Map claims to experiments.** Write each claim as a testable statement and list the experiment that would support it and the result that would refute it. Drop experiments that support no claim.
2. **Define variables.**
   - Independent: what you vary (method, component, hyperparameter, data size).
   - Dependent: metrics, with direction and unit.
   - Controlled: everything held equal across compared conditions (data, preprocessing, tuning budget, compute, seeds).
   - Confounds: differences that could explain the result other than your method (parameter count, pretraining data, training time).
3. **Choose baselines.** Include: the strongest published method on this benchmark; the most widely used method; a simple baseline (linear model, heuristic, previous version); and your method without its new part. Plan to tune baselines with the same budget as your method, or cite their published numbers under the same protocol.
4. **Choose datasets and splits.** At least two datasets when claiming generality. Fix train, validation, and test splits; use standard splits where they exist. Model selection uses validation only. Check for leakage (`dataset-finder` helps locate candidates).
5. **Choose metrics.** The field's standard metric first, then metrics for the property you claim (robustness, efficiency, calibration, fairness). Report cost metrics (parameters, FLOPs, latency, training time) when claiming efficiency.
6. **Plan for variance.** Fix the number of seeds (3 to 5 minimum for stochastic training) and the statistical comparison: mean with standard deviation or confidence interval, and a test when differences are small (`statistical-test-selector`).
7. **Plan ablations and analyses** (`ablation-study-designer`): component removal, sensitivity to key hyperparameters, scaling behaviour, failure cases, qualitative examples.
8. **Budget.** Estimate cost per run from a timed pilot, then multiply: configurations × datasets × seeds. Add the hyperparameter search and a 30% margin for failed and repeated runs.
9. **Prioritise.** Label each experiment P0 (the paper cannot be submitted without it), P1 (reviewers will ask), or P2 (nice to have). Schedule P0 first and set a go/no-go checkpoint after the first main result.
10. **Set up logging** before the first run (`experiment-logger`): config, seed, commit, metrics.

## Output format

```markdown
## Claims and experiments
| # | Claim | Experiment | Supports if | Refutes if | Priority |

## Setup
- Datasets and splits: ...
- Baselines: ... (source of numbers: rerun | published under same protocol)
- Metrics: ...
- Controlled factors: ...
- Seeds and statistical comparison: ...

## Experiment list
| ID | Purpose | Configs × datasets × seeds | Cost per run | Total | Priority |

## Budget
Total: <GPU hours / lab days>. Available: <...>. Margin: 30%. Cut order if over budget: ...

## Timeline and checkpoints
## Risks and fallbacks
```

## Examples

Requests that should trigger this skill:

- "Plan the experiments for my paper on a new graph pooling layer."
- "What baselines and datasets do reviewers expect for text summarization?"
- "Design the evaluation section for my method."
- "I have 400 GPU hours and three weeks. Which experiments should I run?"
- "Reviewers asked for more experiments. Help me plan them."

Requests that belong to another skill:

- "Design a survey study with students." → use `methodology-designer`
- "Which components should I ablate?" → use `ablation-study-designer`
- "Find a dataset for this task." → use `dataset-finder`

### Worked example

**Request:** "Plan experiments for a paper claiming my data augmentation improves robustness of image classifiers. I have one 24 GB GPU for a month. A CIFAR-10 run takes 2 hours."

**What the agent does:**

1. Rewrites the claims as testable statements with supporting and refuting outcomes.
2. Fixes variables, three baselines, two datasets with standard splits, clean and corrupted accuracy as metrics, and three seeds.
3. Budgets from the 2-hour pilot and adds a 30% margin.
4. Labels each experiment P0, P1, or P2 and sets a go/no-go checkpoint.

**Result (excerpt):**

```markdown
| ID | Purpose | Configs x datasets x seeds | Cost per run | Total | Priority |
|---|---|---|---|---|---|
| E1 | Main comparison vs 3 baselines | 4 x 2 x 3 | 2 h | 48 h | P0 |
| E2 | Corruption robustness | evaluation only | 0.2 h | 5 h | P0 |
| E3 | Ablation of two components | 3 x 1 x 3 | 2 h | 18 h | P1 |

Total with 30% margin: 92 GPU hours of about 700 available. Cut order if over budget: E3 to one dataset, then drop P2.
```

## Quality bar and pitfalls

- Do not invent cost estimates. Time a pilot run, or state the estimate as a guess with its basis.
- The test set is used once per reported configuration. Tuning on test data invalidates the results.
- A baseline that is not tuned, or run on a different protocol, does not support a comparison claim.
- One dataset and one seed do not support a general claim.
- Decide the analysis before seeing the results. Choosing metrics and subsets afterwards is selective reporting.
- Plan what happens if the main result is negative: which finding would still be publishable.
- If the budget does not cover P0, say so now and reduce scope (fewer datasets, smaller models) openly.

## Limitations

- Cost estimates are extrapolated from a pilot or a stated guess and can be off by a large factor.
- The plan reflects current venue expectations as the agent understands them; recent papers at the target venue should be checked.
- A plan does not guarantee the results will support the claims.

## Troubleshooting

| Problem | Likely cause | Solution |
|---|---|---|
| The budget does not cover the P0 experiments | Too many datasets, seeds, or model sizes | Reduce scope openly: fewer datasets or a smaller model, and narrow the claim to match |
| No pilot timing is available | Nothing has been run yet | Run one short timed pilot before finalising the budget; label any estimate as a guess |
| A baseline cannot be reproduced or its run fails | Code is missing or broken | Use its published numbers only if the protocol matches, and state the source |

## Related skills

- `research-question-formulator` for the claims and hypotheses.
- `dataset-finder` for datasets and benchmarks.
- `ablation-study-designer` for the component analysis.
- `experiment-logger` to record runs as they happen.
- `statistical-test-selector` for comparing results across seeds.
- `results-interpreter` once the numbers are in.
- `reproducibility-checklist` to plan for what the venue will ask.
