---
name: paper-to-code-reproducer
description: "Implements a research paper's method from the PDF, logs every unspecified detail, and compares reproduced numbers with reported ones. Use when a paper has no usable code. Not for understanding only."
version: 1.0.0
metadata:
  author: "Yash Kavaiya <yash.kavaiya3@gmail.com>"
  tags: [reproducibility, implementation, machine-learning]
---

# Paper to Code Reproducer

Turn a paper into working code and an honest account of how close the reproduction is. Papers omit details; the work is in finding those gaps and recording how each was filled.

## Purpose

Turn a paper into working code plus an honest account of how close the reproduction is. Papers omit details, so the skill extracts a specification, records each gap and how it was filled, tests each component, and reports reproduced results next to the paper's.

## When to use

- A paper has no released code, or its code is unusable.
- A baseline must be reimplemented for a fair comparison.
- The user wants to understand a method by building it.

Hand off instead for understanding only (`paper-summarizer`, `math-and-equation-explainer`).

## Prerequisites

- The paper's full text with appendix and supplementary material.
- A Python environment with the chosen framework (for example PyTorch), and hardware adequate for at least a reduced run.
- Access to the dataset, and a chosen target: one table or figure to reproduce.

## Inputs

- The paper's full text with appendix and supplementary material.
- Which result to reproduce (a specific table or figure). Reproducing "the paper" is too broad.
- Framework, hardware, and time available.
- The dataset, or access to it.

## Instructions

1. **Look for existing code first.** Check the paper and its arXiv page for a repository link, search Papers with Code and GitHub, and check the authors' pages. If official code exists, read it; it resolves ambiguities even when you reimplement. Check its licence before reusing any of it.
2. **Fix the target**: one table or figure, the exact metric, dataset, and split.
3. **Extract the specification** into a document:
   - Data: source, preprocessing, augmentation, splits, tokenisation or normalisation.
   - Model: every layer or step with dimensions, activations, normalisation, initialisation.
   - Objective: loss terms with weights, regularisation.
   - Optimisation: optimiser, learning rate and schedule, warm-up, batch size, epochs or steps, gradient clipping, precision, weight decay, EMA.
   - Evaluation: metric definition, checkpoint selection, test-time settings, number of seeds.
   - Compute: hardware and training time reported.

   Give each item a source (section, equation, table, appendix) or mark it **unspecified**.
4. **Resolve the unspecified items** in this order: official code; the paper's cited predecessor or the standard for that benchmark; the framework default; your judgement. Record each choice and its basis in an assumptions log. Offer to draft an email to the authors for details that matter and cannot be inferred.
5. **Plan the build** in testable units: data pipeline, model, loss, training loop, evaluation. Use a config file for every hyperparameter and fix seeds.
6. **Implement with checks at each unit:**
   - Shape assertions and a forward pass on a tiny batch.
   - Parameter count against the paper's reported count.
   - Loss on random input against the expected value (for example ln(C) for C-way cross-entropy at initialisation).
   - Overfit a single small batch to near-zero loss before any full run.
   - Unit tests for equations implemented from the paper, on hand-computed cases.
   - The evaluation metric checked against a reference implementation.
7. **Run small, then scale.** A short run on a data subset first, then the full configuration. Log every run (`experiment-logger`).
8. **Compare with the paper** in a table: reported, reproduced (mean and standard deviation over seeds), and the difference. State whether the reproduction is within the paper's own variance, close, or not reproduced.
9. **Diagnose gaps** systematically: data preprocessing, evaluation protocol, schedule length, an assumption from step 4. Change one thing at a time.
10. **Write the README**: how to run, results table, assumptions log, known deviations.

## Output format

```
repo/
  README.md            # commands, results vs paper, deviations
  SPEC.md              # extracted specification with sources
  ASSUMPTIONS.md       # every unspecified detail and the choice made
  configs/<exp>.yaml
  src/{data,model,loss,train,evaluate}.py
  tests/
  requirements.txt
```

Results table in the README:

```markdown
| Setting | Paper | Ours (mean ± sd, n seeds) | Difference |
|---|---|---|---|
```

## Examples

Requests that should trigger this skill:

- "Implement this paper in PyTorch; there is no official code."
- "Reproduce Table 2 of the attached paper."
- "Turn this method section into working code."
- "I need to reimplement this baseline for a fair comparison."
- "Write code for the architecture in Figure 3 of this paper."

Requests that belong to another skill:

- "Explain the loss function in this paper." → use `math-and-equation-explainer`
- "Summarise what the paper does." → use `paper-summarizer`
- "Plan my own experiments." → use `experiment-planner`

### Worked example

**Request:** "Reproduce the CIFAR-10 result (Table 1) of this paper on a new regularizer. No code is released. I have one GPU."

**What the agent does:**

1. Searches for existing code and finds none; fixes the target as Table 1, CIFAR-10 test accuracy.
2. Writes SPEC.md with each detail's source and marks weight decay and augmentation as unspecified.
3. Fills gaps from the cited predecessor and records them in ASSUMPTIONS.md.
4. Builds and tests each unit (shapes, parameter count, single-batch overfit), runs 3 seeds, and compares.

**Result (excerpt):**

```markdown
| Setting | Paper | Ours (mean ± sd, 3 seeds) | Difference |
|---|---|---|---|
| ResNet-18 + regularizer | 95.4 | 94.9 ± 0.2 | -0.5 |
| ResNet-18 baseline | 94.8 | 94.7 ± 0.1 | -0.1 |

ASSUMPTIONS.md: weight decay 5e-4 (not stated; taken from the cited baseline paper). The gain reproduces in direction (+0.2) but is smaller than reported (+0.6).
```

## Quality bar and pitfalls

- Report the numbers you obtained. Never copy the paper's numbers into the "ours" column, and never claim a reproduction that was not run to completion. If only a reduced run was possible, label it as such.
- Do not hide deviations. A reproduction with documented differences is useful; one with silent differences misleads.
- Most failed reproductions come from data preprocessing and evaluation protocol, not the model. Check those first.
- Papers contain errors and omissions. When an equation and the text disagree, note it, pick one with a reason, and test both if cheap.
- Do not tune on the test set to match the reported number.
- Respect licences for code and data. Reimplementing from a paper is fine; copying code from a repository needs its licence to allow it and attribution.
- If compute is far below what the paper used, say what can and cannot be verified at the smaller scale.

## Limitations

- An exact match is often impossible when the paper omits details or used far more compute. The reproduction states how close it is and why.
- Reduced-scale runs verify the implementation, not the paper's headline numbers.
- Code and datasets carry licences that may restrict reuse; the skill checks but cannot grant permission.
- Results depend on hardware, library versions, and random seeds.

## Troubleshooting

| Problem | Likely cause | Solution |
|---|---|---|
| Loss is NaN or does not decrease | A bug in the loss or data pipeline, or a learning rate that is too high | Overfit one small batch first; check normalisation, label alignment, and learning rate |
| Reproduced numbers are well below the paper's | Preprocessing or evaluation protocol differs | Compare preprocessing, splits, schedule length, and checkpoint selection one at a time |
| Parameter count does not match the paper | An architectural detail was misread | Recheck layer widths, bias terms, and shared weights against the paper's table or figure |
| An equation and the text disagree | A typo or error in the paper | Note it in ASSUMPTIONS.md, pick one with a reason, and test both if cheap |

## Related skills

- `paper-summarizer` and `math-and-equation-explainer` to understand the method first.
- `dataset-finder` to obtain the data.
- `experiment-logger` to record runs and decisions.
- `experiment-planner` when the reproduction is a baseline in a larger study.
- `results-interpreter` to interpret differences from the reported numbers.
- `reproducibility-checklist` to document the reproduction.
