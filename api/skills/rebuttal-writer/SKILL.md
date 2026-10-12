---
name: rebuttal-writer
description: "Writes point-by-point responses to peer reviewers for conference rebuttals and journal revisions within the venue's limit. Use when reviews have arrived. Not for pre-submission review."
version: 1.0.0
metadata:
  author: "Yash Kavaiya <yash.kavaiya3@gmail.com>"
  tags: [rebuttal, peer-review, revision, response-letter]
---

# Rebuttal Writer

## Purpose

Answer every reviewer comment completely, courteously, and with evidence, so the editor or area chair can see that each concern was resolved. Each response states the answer, the evidence, and the change made to the manuscript.

## When to use

- Reviews have arrived for a conference with an author-response phase.
- A journal has returned a decision of minor or major revision.
- A rejected paper is being revised for resubmission and the response to prior reviews is needed.

Hand off instead for anticipating reviews before submission (`self-peer-reviewer`).

## Prerequisites

- All reviews, the meta-review, and the editor's letter in full.
- The manuscript, and what the authors can change or run in the time available.
- The venue's response rules: length limit, whether new results or a revised PDF are allowed, and the deadline.

## Inputs

- All reviews, the meta-review, and the editor's letter, in full.
- The manuscript, and what the authors can change or run in the time available.
- The venue's rules: length limit (characters, words, or one page), whether new experiments, figures, links, or a revised PDF are allowed, anonymity, and the deadline.
- The authors' own view of which criticisms are right.

## Instructions

1. **Read everything, then wait before writing.** Summarise each review neutrally: what the reviewer understood, their main concerns, and their score. Identify the reviewer who can be moved and the concern that drives the decision.
2. **Split the reviews into individual comments** and number them (R1.1, R1.2, R2.1). Miss nothing, including remarks inside paragraphs and questions.
3. **Classify each comment and choose the response:**

   | Comment type | Response |
   |---|---|
   | Valid criticism | Agree, fix it, and say exactly what changed |
   | Misunderstanding | Clarify without blaming the reader, and revise the text so the next reader does not misread it |
   | Request for an experiment or analysis | Do it and report the result; or explain concretely why it is infeasible or out of scope, and offer what can be done |
   | Missing reference | Add and discuss it; state the difference from your work |
   | Disagreement on substance | Disagree politely with evidence: data, a citation, or a proof |
   | Minor or editorial | Fix; group these and answer briefly |

4. **Build the response matrix** with the authors: comment, type, response strategy, action, owner, and status. Decide the new experiments first; they take the longest.
5. **Find the shared concerns.** Issues raised by more than one reviewer go first, in a general response, since they weigh most.
6. **Draft each response** in this shape:
   - Open with the answer or the action in the first sentence. No preamble.
   - Give the evidence: the new result with numbers, the clarified reasoning, or the citation.
   - State the change: where in the manuscript (section, page, line), and quote the new text for important changes.
7. **Set the tone**: appreciative once at the top, then direct. Never defensive, sarcastic, or dismissive, including toward an unfair review; the editor reads it too. Avoid "the reviewer failed to notice"; write "we have clarified this in Section 3".
8. **Fit the format.**
   - *Conference rebuttal* (tight limit): lead with the 3 or 4 decisive points, answer shared concerns once, compress minor points into a line, and reference comments by tag. Every sentence carries information.
   - *Journal response letter* (no tight limit): a cover note to the editor summarising the main changes, then every comment quoted in full, each followed by the response and the manuscript change. Mark changes in the manuscript (colour or `latexdiff`).
9. **Verify the response against the revision.** Every "we have added" must be true of the revised manuscript, with correct section and line references.
10. **Check completeness and length**, then give the authors the list of promises made.

## Output format

Conference rebuttal:

```markdown
We thank the reviewers for their careful reading. We address the main concerns first.

**[R1, R3] Comparison with X.** We ran X under our protocol: it obtains 71.2 ± 0.3 vs. our 74.8 ± 0.2 (new Table 2 row). ...
**[R2] Clarity of the loss derivation.** ...
**Minor points.** R1.4: fixed. R3.2: we now define ...
```

Journal response letter:

```markdown
Dear Dr. <Editor>,
<summary of the revision in 3 to 5 sentences>

## Reviewer 1
**Comment 1.1.** "<reviewer's text quoted in full>"
**Response.** ...
**Change.** Section 4.2, lines 310–318: "<new text>"
```

Also deliver the response matrix and a checklist of every promised change.

## Examples

Requests that should trigger this skill:

- "Write my rebuttal; here are three reviews."
- "Draft a response letter for my major revision."
- "How do I reply to Reviewer 2's comment about missing baselines?"
- "Help me plan the response to these reviews; I have 7 days and 5,000 characters."
- "Write the response to reviewers for my journal resubmission."

Requests that belong to another skill:

- "Review my paper before submission." → use `self-peer-reviewer`
- "Write the cover letter for a new submission." → use `cover-letter-writer`
- "Plan the new experiments reviewers asked for." → use `experiment-planner`

### Worked example

**Request:** "Rebuttal, 4,000 characters. R1 and R3 ask for a comparison with method X; R2 says the loss derivation is unclear. We ran X: 71.2 ± 0.3 vs our 74.8 ± 0.2."

**What the agent does:**

1. Summarises each review and splits them into numbered comments.
2. Classifies each: requested experiment (done), misunderstanding (clarify and revise), minor.
3. Leads with the shared concern and the new result, then the clarification with the change made.
4. Checks the character count and lists promised changes.

**Result (excerpt):**

```markdown
We thank the reviewers for their careful reading.

**[R1, R3] Comparison with X.** We ran X under our protocol (same data, tuning budget, 5 seeds): X obtains 71.2 ± 0.3 against our 74.8 ± 0.2. This is added as a row in Table 2.

**[R2] Loss derivation.** We agree the step from Eq. 3 to Eq. 4 was too terse. We now show the intermediate step and state the independence assumption (Section 3.2).

(1,160 of 4,000 characters)

Promised changes: Table 2 row; Section 3.2 derivation.
```

## Quality bar and pitfalls

- Never claim an experiment was run, a result obtained, or a change made unless it was. Report only real numbers supplied by the authors; where a result is pending, write a clearly marked placeholder for them to fill, or state what will be done.
- Do not promise what cannot be delivered by the camera-ready or revision deadline.
- Answer every comment. A skipped comment reads as evasion.
- Concede what is right. Conceding valid points buys credibility for the points you contest.
- Do not argue with the score, the reviewer's competence, or their motives.
- Do not introduce a substantially different paper in the rebuttal; many venues disallow it. Follow the venue's rules on new results and links, and keep anonymity.
- Respect the limit exactly; overlong rebuttals are truncated or ignored.
- If a criticism reveals a real flaw in the main claim, tell the authors, and advise narrowing the claim over defending it.

## Limitations

- Responses can only report results the authors have actually obtained. Pending experiments appear as marked placeholders.
- A rebuttal cannot rescue a flaw in the main claim; narrowing the claim may be the only honest option.
- Venue rules on new results, links, and revised PDFs differ and must be read from the instructions.
- The decision rests with reviewers and the editor; a good response improves the odds without guaranteeing an outcome.

## Troubleshooting

| Problem | Likely cause | Solution |
|---|---|---|
| The draft exceeds the limit | Minor points are answered at length | Lead with decisive points, merge shared concerns, and compress minor ones to a line each |
| A requested experiment cannot be finished in time or fails | It is too costly or infeasible | Say so concretely, offer what can be done, and do not promise what cannot be delivered |
| A reviewer misread the paper | The text was unclear | Clarify without blaming the reader and revise the passage so the next reader does not misread it |
| The response and the revised manuscript disagree | A promised change was not made | Verify every "we have added" against the revision before sending |

## Related skills

- `self-peer-reviewer` to anticipate criticisms and stress-test the draft response.
- `experiment-planner` and `ablation-study-designer` for the requested experiments.
- `statistical-test-selector` and `results-interpreter` for requested analyses.
- `paper-search` and `related-work-writer` for references reviewers say are missing.
- `limitations-and-future-work-writer` for concerns best handled by an explicit limitation.
- `academic-tone-editor` to tighten the response to the limit.
- `cover-letter-writer` for the letter that accompanies a revised submission.
- `camera-ready-checker` after acceptance.
