---
name: limitations-and-future-work-writer
description: "Writes limitations and future-work sections: real validity threats, their effect on conclusions, and specific follow-up studies. Use when a paper needs these sections. Not for a full critique."
version: 1.0.0
metadata:
  author: "Yash Kavaiya <yash.kavaiya3@gmail.com>"
  tags: [limitations, future-work, threats-to-validity, academic-writing]
---

# Limitations and Future Work Writer

State plainly where the study's conclusions stop, and what would extend them. A good limitations section raises a reader's trust; a vague one lowers it.

## Purpose

State plainly where a study's conclusions stop and what would extend them. Each limitation names its consequence for a specific claim and any mitigation, and each future-work item follows from a finding or limitation.

## When to use

- A paper, thesis, or report needs a limitations, threats-to-validity, or future-work section.
- A venue requires a limitations statement (several ML and NLP venues do).
- Reviewers criticised the limitations as generic.

Hand off instead for a full critique of the draft (`self-peer-reviewer`).

## Prerequisites

- The paper's claims and the methods and results behind them.
- Caveats noted during analysis, and the weaknesses the author already knows.
- The venue's requirement: a separate section or part of the discussion, and any length rule.

## Inputs

- The paper's claims and the methods and results behind them. Read the methods and results sections, not just the abstract.
- The caveats already noted during analysis (`results-interpreter` output, lab notebook).
- Venue requirements: separate section or part of the discussion, any length rule, any required broader-impact content.
- What the user already knows is weak. They usually know; ask.

## Instructions

1. **List the claims** the paper makes. Limitations are limits on these claims.
2. **Audit the study** against each category and write down what applies:

   | Category | Questions |
   |---|---|
   | Sample and data | Size, how selected, single site or source, time period, missing data, label quality |
   | Internal validity | Confounds, no control or randomisation, baseline tuning, leakage, researcher degrees of freedom |
   | Measurement | Proxy metrics, self-report, instrument validity, annotator agreement, ceiling effects |
   | External validity | Other populations, languages, domains, scales, settings, time |
   | Statistical | Power, number of seeds or runs, multiple comparisons, assumptions |
   | Scope | What was deliberately not studied (delimitations) |
   | Method assumptions | Conditions under which the method works; known failure cases |
   | Resources | Compute, cost, or data requirements that restrict who can use or reproduce it |
   | Ethics and impact | Bias, privacy, misuse potential, environmental cost |

3. **Select the limitations that matter**: those that could change a conclusion or its scope. Usually 3 to 6. Drop ones that apply to all research ("more data would help").
4. **Write each limitation in three parts:**
   - *What*: the specific limitation.
   - *Consequence*: which claim it affects and in which direction (might overstate the effect, may not hold for X).
   - *Mitigation or bound*: what was done to reduce it, or why the main conclusion still stands, or an honest statement that it is unresolved.

   Example: "All participants were undergraduate students at one university, so the usability results may not transfer to older or less technically experienced users; the error-rate findings, which depend on the interface and not on prior experience, are less likely to be affected."
5. **Order** by importance to the conclusions, most serious first.
6. **Derive future work from the limitations and findings.** Each item names the question, the approach, and why it follows:
   - Weak: "Future work could explore other datasets."
   - Strong: "Because all three evaluation corpora are English news text, the next step is to test whether the gain holds on low-resource languages, starting with the X benchmark, where tokenisation differences may reduce it."
7. **Separate near and far.** Two or three concrete next studies, then at most one or two longer-term directions.
8. **Check the tone**: factual, without apology and without defensiveness.

## Output format

```markdown
## Limitations
<3 to 6 paragraphs or a compact list, each: limitation, consequence, mitigation or bound>

## Future Work
<2 to 4 specific directions, each tied to a finding or limitation>

---
## Notes for the author
| Limitation | Affects claim | Severity | Addressed in text? |
- Limitations considered and left out, with the reason
- Any limitation serious enough that a claim in the abstract or introduction should be reworded
```

## Examples

Requests that should trigger this skill:

- "Write the limitations section for my survey study."
- "What are the limitations of my experiment?"
- "Write future work for my paper on sentiment analysis."
- "Reviewers say my limitations are superficial. Rewrite them."
- "Write a threats-to-validity section for my software engineering study."

Requests that belong to another skill:

- "Review my whole paper critically." → use `self-peer-reviewer`
- "Interpret my results." → use `results-interpreter`
- "Fill in the NeurIPS checklist." → use `reproducibility-checklist`

### Worked example

**Request:** "Write limitations and future work. Study: a usability test of a medication-reminder app with 24 university students over one week; main claim is that reminders reduced missed doses."

**What the agent does:**

1. Lists the claims and audits the study by category: sample, validity, measurement, scope.
2. Selects the limitations that could change a conclusion and writes each as what, consequence, and bound.
3. Orders them by importance and derives future work from them.
4. Notes that the abstract's wording should be narrowed.

**Result (excerpt):**

```markdown
## Limitations
Participants were 24 university students, who are younger and more familiar with smartphones than the older adults who most often manage several medications; the reduction in missed doses may not transfer to that group. The one-week duration cannot show whether adherence persists once the novelty fades. Missed doses were self-reported, which may understate them in both conditions.

## Future Work
The next step is a four-week study with adults over 60 on multiple prescriptions, using pill-bottle sensors in place of self-report.

Note for the author: the abstract says "improves adherence"; consider "reduced self-reported missed doses over one week among students".
```

## Quality bar and pitfalls

- Limitations must be true of this study. Do not invent weaknesses to fill the section, and do not omit a real one because it is uncomfortable.
- Do not describe mitigations that were not carried out.
- A limitation with no stated consequence is filler. Say what it does to the conclusions.
- Do not follow every limitation with "however, this does not affect our results". Say so only when you can explain why.
- If a limitation undermines a headline claim, the claim needs rewording in the abstract and introduction. Tell the user; do not bury it here.
- Future work is not a list of everything left undone, and not a reservation of territory. Reviewers discount vague lists.
- Do not promise future work as if it were a result ("we will show").
- Distinguish limitations (weaknesses) from delimitations (chosen scope).

## Limitations

- Limitations are identified from the manuscript and the author's account. Problems visible only in raw records or lab practice are not seen.
- The skill states weaknesses; it cannot remove them. Serious ones may require new analysis or narrower claims.
- Future-work suggestions are informed proposals, not a search of what others are already doing.

## Troubleshooting

| Problem | Likely cause | Solution |
|---|---|---|
| The section reads as generic | Limitations are not tied to this study's claims | Rewrite each with the specific claim affected and the direction of the effect |
| A limitation undermines the main claim | The claim is stated too broadly | Tell the author and reword the claim in the abstract and introduction instead of burying it |
| Future work is a list of topics | Items do not follow from the findings | For each item give the question, the approach, and the finding or limitation it follows from |
| A stated mitigation was not actually done | Text was written from intention, creating an invalid statement | Remove it; describe only mitigations that were carried out |

## Related skills

- `results-interpreter` records the caveats this section draws on.
- `paper-critic` and `self-peer-reviewer` find the weaknesses a reviewer would raise.
- `research-gap-finder` reads other papers' versions of this section to find gaps.
- `abstract-writer` and `introduction-writer` when claims must be reworded to match.
- `reproducibility-checklist` covers resource and reporting limits in checklist form.
- `thesis-chapter-writer` for the thesis conclusion chapter.
