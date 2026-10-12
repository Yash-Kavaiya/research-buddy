---
name: self-peer-reviewer
description: "Reviews the author's own manuscript as a demanding referee: weaknesses by severity, questions, venue scores, and a fix plan. Use before submission. Not for critiquing published papers."
version: 1.0.0
metadata:
  author: "Yash Kavaiya <yash.kavaiya3@gmail.com>"
  tags: [peer-review, mock-review, pre-submission, manuscript]
---

# Self Peer Reviewer

Find the reasons a reviewer would reject the paper while there is still time to fix them. The review is strict, specific, and fair.

## Purpose

Find the reasons a reviewer would reject a paper while there is still time to fix them. The output is a full mock referee report on the venue's criteria and a fix plan sized to the time left.

## When to use

- A draft is complete, or nearly, and submission is days or weeks away.
- After a rejection, to reassess before resubmitting.
- To decide whether a paper is ready for a particular venue.

Hand off instead for critiquing someone else's published paper (`paper-critic`) or for responding to real reviews (`rebuttal-writer`).

## Prerequisites

- The full manuscript with its appendix.
- The target venue's review criteria or review form.
- The time remaining before the deadline.

## Inputs

- The full manuscript with appendix. Reviewing an abstract or outline gives a different, weaker result; say so if that is all there is.
- Target venue and its review criteria and form, from the reviewer guidelines.
- Time until the deadline, which decides what fixes are feasible.
- Anything the authors already consider weak.

## Instructions

1. **Read as a reviewer would**: title and abstract, then figures and tables, then the introduction and conclusion, then the full paper. Note first impressions after the first pass; reviewers form their opinion early.
2. **Summarise the paper** in 3 to 5 sentences in your own words: problem, approach, main claims, evidence. If this is hard to write, the paper has a clarity problem, and that is a finding.
3. **Check claims against evidence.** List every claim in the abstract and introduction and find its support. Flag claims that are unsupported, supported only partly, or stated more strongly than the results allow.
4. **Review along the standard axes:**
   - *Novelty and significance*: what is new relative to the closest work, and whether that work is cited and compared. Run `novelty-checker` if the closest work is not discussed.
   - *Technical soundness*: correctness of the method, proofs, and analysis; validity of the design; fairness of comparisons; confounds; statistics (see the table in `paper-critic`).
   - *Experimental rigour*: baselines, datasets, ablations, variance, significance, missing experiments a reviewer would ask for.
   - *Clarity*: organisation, definitions, notation, figures readable on their own, reproducible description.
   - *Related work*: coverage, accuracy, positioning.
   - *Reproducibility and ethics*: details, code and data, limitations stated, human-subjects or data issues.
5. **Take three reviewer stances** and record what each would say:
   - The expert in the subfield, who knows the closest prior work and the standard evaluation.
   - The methodologist, who checks the statistics and experimental design.
   - The outsider, who reads quickly and judges clarity and significance.
6. **Rank the weaknesses**: *fatal* (likely rejection by itself), *major* (must be addressed), *minor* (should be fixed), *nitpicks*. For each: where it is, why it matters, and what would resolve it.
7. **Score** on the venue's own scale and criteria, with a confidence level, and state the likely outcome with the reasoning. Give a range, not a certainty.
8. **Build the fix plan** for the time available: what to fix now, what to reword or scope down, what to acknowledge as a limitation, and what cannot be fixed before the deadline.
9. **Check the desk-reject risks**: scope, length, formatting, anonymity, missing required sections (`camera-ready-checker`).

## Output format

```markdown
# Mock review: <title> for <venue>

## Summary of the paper
## Strengths
1. ... (where)

## Weaknesses
### Fatal
### Major
- **W1. <issue>** (§, Table, Fig.). Why it matters: ... To resolve: ...
### Minor
### Nitpicks

## Questions for the authors
## Missing references
## Scores (venue's scale)
| Criterion | Score | Reason |
Overall: <score>, confidence <level>. Likely outcome: <range>, because ...

## What the three reviewers would say
- Expert: ...  Methodologist: ...  Outsider: ...

## Fix plan (time available: <n> days)
| Priority | Fix | Effort | Addresses |
```

## Examples

Requests that should trigger this skill:

- "Review my paper before I submit to ACL."
- "Act as Reviewer 2 on this draft."
- "What would reviewers say about my manuscript?"
- "Find the weaknesses in my paper; the deadline is in five days."
- "Will this get accepted at ICML?"

Requests that belong to another skill:

- "Critique this published paper for journal club." → use `paper-critic`
- "Write my response to the reviewers." → use `rebuttal-writer`
- "Fix the grammar in my draft." → use `academic-tone-editor`

### Worked example

**Request:** "Mock review for a top ML conference, deadline in 6 days: a paper claiming a new attention variant is faster and as accurate as the standard one."

**What the agent does:**

1. Reads in reviewer order and summarises the paper in four sentences.
2. Maps each claim to evidence and reviews novelty, soundness, experiments, and clarity.
3. Takes expert, methodologist, and outsider stances.
4. Ranks weaknesses, scores on the venue's scale, and builds a 6-day fix plan.

**Result (excerpt):**

```markdown
### Major
- **W1. Speed is measured on one sequence length** (Section 5.2, Fig. 3). The claim "faster" is made generally. To resolve: report latency at 512, 2k, and 8k tokens.
- **W2. Closest method is not compared** (Section 2). A 2023 linear-attention method addresses the same goal. To resolve: add it to Table 2 or explain why it is not comparable.

Overall: borderline, leaning reject; confidence medium. Likely outcome ranges from weak reject to weak accept depending on W1 and W2.

| Priority | Fix | Effort |
| 1 | W1 latency sweep | 1 day |
| 2 | W2 baseline | 3 days |
```

## Quality bar and pitfalls

- Be strict. A flattering review is useless here; the author asked in order to hear the problems. Do not soften a fatal flaw into a suggestion.
- Be specific and locatable. "Experiments are weak" helps nobody; "Table 2 compares against baselines from 2019 only; the 2023 method X is missing" does.
- Be fair. Do not invent flaws, demand experiments outside the paper's scope, or hold the paper to a different venue's standard.
- Verify before claiming something is missing: search the appendix. Name missing related work only after retrieving it.
- The predicted outcome is an estimate. Real reviewers vary; never promise acceptance or rejection.
- Distinguish what is wrong with the research from what is wrong with the presentation. The fixes differ.
- If the main result does not hold up, say so directly, with the evidence.
- Keep the manuscript confidential: it is unpublished work.

## Limitations

- The predicted outcome is an estimate. Real reviewers vary and may raise points not anticipated here.
- The review covers what is in the manuscript; it does not rerun experiments or verify raw results.
- Judgements about missing related work depend on retrieval and may miss very recent preprints.
- Standards differ by venue; a review against the wrong venue's bar misleads.

## Troubleshooting

| Problem | Likely cause | Solution |
|---|---|---|
| The review is too mild to be useful | Weaknesses were softened | Rank them by severity and state plainly which alone could cause rejection |
| A weakness claims something is missing that the appendix contains | The appendix was not read | Search the appendix first; if the item exists, the fix is to reference it from the main text |
| The fix plan does not fit the time left | Too many major issues | Prioritise the fatal and major ones, reword claims for the rest, and state them as limitations |
| Novelty cannot be judged | The closest prior work is unknown | Run `novelty-checker` and validate the comparison before scoring |

## Related skills

- `paper-critic` provides the validity checklist applied here.
- `novelty-checker` and `citation-verifier` for the novelty and reference checks.
- `results-interpreter` to recalibrate overclaimed results.
- `limitations-and-future-work-writer` for weaknesses best handled by stating them.
- `experiment-planner` and `ablation-study-designer` for experiments the review calls for.
- `reproducibility-checklist` and `camera-ready-checker` for compliance.
- `rebuttal-writer` uses this review to prepare for likely criticisms.
- `venue-recommender` if the review suggests a different venue.
