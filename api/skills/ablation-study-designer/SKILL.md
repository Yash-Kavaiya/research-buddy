---
name: ablation-study-designer
description: "Designs ablation studies that show which components drive a method's performance: what to remove, fair controls, runs, and table layout. Use when attributing gains. Not for the full evaluation plan."
version: 1.0.0
metadata:
  author: "Yash Kavaiya <yash.kavaiya3@gmail.com>"
  tags: [ablation, experiment-design, machine-learning]
---

# Ablation Study Designer

Plan the smallest set of controlled comparisons that shows where a method's gain comes from, and report them so a reader can trust the attribution.

## Purpose

Plan the smallest set of controlled comparisons that shows where a method's gain comes from, and lay out the table and text that report them. Each component's ablation is tied to the claim it supports.

## When to use

- A method has several components or design choices and the paper claims they matter.
- Reviewers asked for ablations or sensitivity analysis.
- The user wants to know which parts of a system can be removed.

Hand off instead for the overall evaluation plan (`experiment-planner`).

## Prerequisites

- A description of the full method, its components, and which ones are the paper's contribution.
- The baseline, the main metric and datasets, and the cost of one run.
- A compute budget for the ablations.

## Inputs

- The full method, broken into its components and design choices.
- Which components are the paper's contribution, and which are inherited.
- The baseline the method starts from.
- The main metric, datasets, and cost of one run.
- The compute budget for ablations.

## Instructions

1. **List the components** and for each write the claim it supports ("the contrastive term improves robustness"). A component with no claim may not need an ablation; a claim with no ablation is unsupported.
2. **Choose the ablation type per component:**
   - *Remove*: delete the component (drop a loss term, skip a module).
   - *Replace*: swap it for the standard or simplest alternative (learned positional encoding with sinusoidal; your sampler with uniform sampling). Prefer this when removal breaks the model or changes capacity.
   - *Vary*: sweep a continuous choice (loss weight, number of layers, temperature) to show sensitivity.
   - *Add*: build up from the baseline, adding one component at a time.
3. **Choose the structure:**
   - *Leave-one-out* from the full model: n + 1 runs. Shows that each part is needed in the presence of the others. The default.
   - *Additive* from the baseline: n + 1 runs. Shows how the gain accumulates; the order matters, so justify it.
   - *Factorial* (all on/off combinations): 2^n runs. Shows interactions. Use for 2 or 3 key components only.
   - Use leave-one-out plus the baseline row at minimum; add a 2×2 factorial for the two main contributions when their interaction is part of the claim.
4. **Control confounds** so the only difference is the ablated component:
   - Same data, splits, training budget, and tuning effort.
   - Match capacity when a removal shrinks the model (widen another layer, or report parameter counts and discuss).
   - Retune hyperparameters that depend on the removed part (a learning rate tuned for the full model can handicap an ablated variant), or state that they were not retuned.
5. **Decide runs and datasets.** Use the same number of seeds as the main results (3 or more) and report mean and standard deviation. To save compute, run ablations on one or two representative datasets or a smaller scale, and say so.
6. **Add the analyses reviewers commonly expect**: sensitivity to the one or two most important hyperparameters; behaviour with less training data; compute or latency cost of each component.
7. **Predict before running.** Write the expected direction for each row. Surprises then become findings instead of being explained away.
8. **Lay out the table** and the text that reads it.

## Output format

```markdown
## Components and claims
| Component | Claim it supports | Ablation type | Variant |

## Runs
| ID | Variant | Changed vs full | Seeds | Dataset(s) | Cost | Expected |
Total cost: ... Budget: ...

## Ablation table (template)
| Variant | Comp. A | Comp. B | Comp. C | Metric ↑ (mean ± sd) | Δ vs full | Params |
|---|---|---|---|---|---|---|
| Full | ✓ | ✓ | ✓ | | 0 | |
| w/o A | – | ✓ | ✓ | | | |
| w/o B | ✓ | – | ✓ | | | |
| w/o C | ✓ | ✓ | – | | | |
| Baseline | – | – | – | | | |

## Controls
- Held fixed: ... Retuned: ... Capacity matched by: ...

## How to report
One paragraph per component: what was changed, the difference with its variation, and what it shows.
```

## Examples

Requests that should trigger this skill:

- "What ablations should I run for my model with three new modules?"
- "Reviewers asked for an ablation study. Design it."
- "How do I show that each component of my method matters?"
- "Which component contributes most to my accuracy gain?"
- "Lay out an ablation table for my paper."

Requests that belong to another skill:

- "Plan all experiments for my paper." → use `experiment-planner`
- "Typeset the finished ablation table." → use `latex-table-generator`
- "Interpret the ablation results." → use `results-interpreter`

### Worked example

**Request:** "My segmentation model adds a boundary loss, a multi-scale decoder, and test-time augmentation over a U-Net baseline. One run takes 6 GPU hours and I have 150 hours."

**What the agent does:**

1. Lists the three components with the claim each supports.
2. Chooses leave-one-out from the full model plus the baseline row, with replace-type ablation for the decoder to keep capacity matched.
3. Sets 3 seeds on one dataset and computes the cost.
4. Writes expected directions and the empty table template.

**Result (excerpt):**

```markdown
| ID | Variant | Changed vs full | Seeds | Cost | Expected |
|---|---|---|---|---|---|
| A0 | Full | none | 3 | 18 h | best |
| A1 | w/o boundary loss | Dice loss only | 3 | 18 h | lower boundary F1 |
| A2 | single-scale decoder | decoder widened to match parameters | 3 | 18 h | lower on small objects |
| A3 | w/o test-time augmentation | evaluation only | 3 | 1 h | small drop |
| A4 | U-Net baseline | all removed | 3 | 18 h | lowest |

Total: 73 h of 150 h. Result cells stay empty until the runs finish.
```

## Quality bar and pitfalls

- Leave the result cells empty until the runs are done. Never fill an ablation table with expected or estimated values.
- A difference inside the seed-to-seed standard deviation does not show a component matters. Report it as no measurable effect.
- If removing a component does not hurt, say so and reconsider the claim. Ablations that find a part unnecessary are useful results.
- Do not ablate only the components that make the method look good.
- Removing a component can change parameter count, training time, or data seen. Unreported, these are alternative explanations.
- Additive tables depend on the order. Do not present the order that maximises your component's apparent gain without saying it is one of several.
- Run ablations on the same evaluation protocol as the main table, and never select variants on the test set.
- State the scale honestly when ablations use a smaller model or subset.

## Limitations

- Leave-one-out ablations do not reveal interactions between components; a factorial design is needed for that and costs far more.
- Removing a component can change capacity or training dynamics in ways that are hard to control fully.
- Ablations run at reduced scale may not transfer to the full setting, and this must be stated.

## Troubleshooting

| Problem | Likely cause | Solution |
|---|---|---|
| Removing a component breaks the model | The component is structurally required | Use a replace-type ablation with the standard or simplest alternative |
| Differences are within seed-to-seed noise | The component has little effect, or too few seeds were run | Add seeds; if still within noise, report no measurable effect and reconsider the claim |
| The ablation budget is exceeded or runs fail | Too many variants or seeds | Ablate on one representative dataset or a smaller model and state the scale |

## Related skills

- `experiment-planner` for the main evaluation the ablations sit inside.
- `experiment-logger` to track ablation runs.
- `statistical-test-selector` to test differences between variants.
- `results-interpreter` to read the completed table.
- `latex-table-generator` to typeset the table with the best result bolded.
- `rebuttal-writer` when the ablations answer a reviewer's request.
