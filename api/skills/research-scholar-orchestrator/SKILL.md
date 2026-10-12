---
name: research-scholar-orchestrator
description: "Routes a research request to the right research-scholar skills in sequence, from topic selection to submission. Use when a request spans stages or the right skill is unclear. Not for single tasks."
version: 1.0.0
metadata:
  author: "Yash Kavaiya <yash.kavaiya3@gmail.com>"
  tags: [orchestration, routing, research-workflow]
---

# Research Scholar Orchestrator

Work out where the user is in the research lifecycle, pick the smallest set of skills that gets them to their stated goal, and run them in an order where each one's output feeds the next.

## Purpose

Work out where a researcher is in the research lifecycle, pick the smallest set of skills that reaches their stated goal, and run them in an order where each output feeds the next. It also applies the collection's integrity rules at every step.

## When to use

- The request needs more than one skill, or the right skill is not obvious.
- The user describes a goal, not a task.
- A long project needs a plan across stages.

Go straight to a single skill when the request names one task that one skill covers. Use `idea-to-paper-pipeline` when the user wants the whole path from topic to reviewed draft.

## Prerequisites

- The other research-scholar skills installed alongside this one.
- The user's goal, field, deadline, and what already exists (topic, papers, results, draft).
- Whatever the routed skills need: several require Python and network access.

## Inputs

- The goal, in the user's words, and the deadline if there is one.
- The field and the type of output (paper, thesis, proposal, review, talk).
- What already exists: topic, papers collected, data, results, draft, reviews.
- Constraints: venue, word limits, institutional rules, tools available.

Ask at most two or three questions, only for what cannot be inferred. State the assumption and proceed for everything else.

## Instructions

1. **Locate the stage.** Identify the furthest point the user has reached: no topic; topic but no question; question but no design; data but no analysis; results but no draft; draft but not submission-ready; under review; accepted; or applying for a position or funding.
2. **Match the request to skills** with the routing table.

   | The user wants to | Skills, in order |
   |---|---|
   | Find a topic or problem | `topic-trend-analyzer` → `research-gap-finder` → `novelty-checker` → `research-question-formulator` |
   | Check an idea is new | `novelty-checker` (uses `paper-search`, `citation-graph-explorer`) |
   | Find and read papers | `paper-search` → `citation-graph-explorer` → `paper-summarizer` |
   | Understand or judge one paper | `paper-summarizer` → `math-and-equation-explainer` → `paper-critic` |
   | Compare several papers | `paper-comparison-matrix` |
   | Write a literature review | `paper-search` → `paper-comparison-matrix` → `literature-review-writer` → `citation-verifier` |
   | Do a systematic review | `research-question-formulator` → `systematic-review-prisma` → `literature-review-writer` |
   | Write related work | `novelty-checker` → `related-work-writer` |
   | Build a reading list with notes | `paper-search` → `annotated-bibliography-builder` |
   | Design a study | `research-question-formulator` → `methodology-designer` → `sample-size-power-calculator` → `survey-questionnaire-designer` → `ethics-irb-drafter` |
   | Plan computational experiments | `dataset-finder` → `experiment-planner` → `ablation-study-designer` → `experiment-logger` |
   | Reproduce a paper | `paper-summarizer` → `paper-to-code-reproducer` → `experiment-logger` |
   | Analyse quantitative data | `statistical-test-selector` → `results-interpreter` |
   | Analyse interviews or text | `qualitative-coding-assistant` → `results-interpreter` |
   | Write a paper from results | `results-interpreter` → `paper-outline-generator` → `publication-figure-maker` / `architecture-diagram-maker` / `latex-table-generator` → `introduction-writer` → `related-work-writer` → `limitations-and-future-work-writer` → `abstract-writer` → `academic-tone-editor` |
   | Write a thesis | `thesis-chapter-writer`, with `literature-review-writer` and `methodology-designer` for those chapters |
   | Fix references | `bibtex-manager` → `citation-verifier` → `citation-style-converter` |
   | Check originality of wording | `plagiarism-and-paraphrase-checker` |
   | Get a paper submission-ready | `self-peer-reviewer` → `citation-verifier` → `reproducibility-checklist` → `latex-paper-formatter` → `camera-ready-checker` |
   | Choose where to submit | `venue-recommender` → `cover-letter-writer` |
   | Respond to reviews | `rebuttal-writer`, then `camera-ready-checker` after acceptance |
   | Apply for funding | `grant-proposal-writer` |
   | Apply for a PhD or position | `supervisor-finder` → `phd-research-proposal-writer` → `sop-and-research-statement-writer` |
   | Present or publicise work | `paper-to-slides`, `paper-to-poster`, `paper-to-blog`, `paper-to-explainer-video` |
   | Prepare for a defence | `viva-defense-prep` |
   | Keep up with the field | `weekly-paper-digest` |
   | Track a long project | `research-progress-tracker` |
   | Go from idea to draft in one run | `idea-to-paper-pipeline` |

3. **Trim the sequence** to what the goal needs. Skip any step whose output the user already has, after checking that it is adequate.
4. **Present the plan** in a few lines: the steps, what each produces, and where the user's decision is needed. Then start; do not wait for approval of an obvious plan.
5. **Run each skill fully**, following its own instructions, and pass its output to the next. Keep working files in one project folder so later steps can read them.
6. **Stop at decision points** that belong to the user: choice of topic, research question, design, venue, and anything that would be submitted in their name.
7. **Apply the integrity rules at every step** (below), and run `citation-verifier` before any document with references is treated as finished.
8. **Close with status**: what was produced, what remains, and the next step, recorded with `research-progress-tracker` for multi-session projects.

## Output format

```markdown
## Plan for: <goal>
Stage: <where you are now>. Deadline: <date or none>.

| Step | Skill | Produces | Needs from you |
|---|---|---|---|
| 1 | paper-search | corpus of ~30 papers | topic confirmation |
| 2 | ... | ... | ... |

(work proceeds, one section per step)

## Status
- Done: ...
- Open decisions: ...
- Next: ...
```

## Examples

Requests that should trigger this skill:

- "Help me with my research; I'm starting a master's thesis on smart grids."
- "I have results and a deadline in three weeks. What do I do next?"
- "Get this paper ready to submit to a journal."
- "Take me from this dataset to a conference paper."
- "I don't know where to start with my literature review and methodology."

Requests that belong to another skill:

- "Find papers on smart grids." → use `paper-search`
- "Check my references are real." → use `citation-verifier`
- "Run the whole pipeline from idea to draft." → use `idea-to-paper-pipeline`

### Worked example

**Request:** "I have a finished draft and results for a paper on anomaly detection in smart meters. Deadline in 10 days for a journal I haven't chosen. What should I do?"

**What the agent does:**

1. Locates the stage: draft exists, not submission-ready, venue open.
2. Matches the request to the submission-readiness and venue routes and trims steps already done.
3. Presents a five-step plan with what each produces and the decisions needed, then starts with the mock review.
4. Runs each skill, stops at the venue decision, and closes with status.

**Result (excerpt):**

```markdown
| Step | Skill | Produces | Needs from you |
|---|---|---|---|
| 1 | self-peer-reviewer | mock review and fix list | the journal type you aim for |
| 2 | citation-verifier | verified bibliography | refs.bib and the .tex file |
| 3 | venue-recommender | ranked shortlist | indexing and fee constraints |
| 4 | latex-paper-formatter | draft in the journal template | choice of journal |
| 5 | camera-ready-checker, cover-letter-writer | checked PDF and letter | declarations |
```

## Quality bar and pitfalls

These rules hold across every skill in the collection:

- **No fabrication.** Never invent references, quotations, data, results, statistics, reviewer comments, approvals, or facts about venues, people, or funders. Retrieve them or mark them as unknown.
- **Verify citations.** Any reference that did not come from a retrieved record is unverified until `citation-verifier` has checked it.
- **The work is the researcher's.** The skills help plan, analyse, draft, and check. Research decisions, the data, and responsibility for what is submitted remain with the user, who should read and understand everything that goes out under their name.
- **Disclose AI assistance** as the venue, institution, or funder requires. When the user is unsure of the policy, tell them to check it.
- **Report honestly.** State limitations, negative results, failed checks, and anything that could not be verified.
- **Protect confidential material**: unpublished manuscripts, participant data, and papers under review.

Routing pitfalls:

- Do not run a long chain when one skill answers the question.
- Do not skip the design and analysis skills to reach the writing skills; a paper written on weak results needs the results fixed, not better prose.
- Do not continue past a failed step (no gap found, idea already published, underpowered design, unverifiable references). Report it and replan.
- Current facts (deadlines, page limits, scheme rules, templates) come from the source at the time of use.

## Limitations

- The orchestrator plans and sequences; the quality of each step depends on the routed skill and its inputs.
- It cannot do the research itself: collecting observations, running experiments, and obtaining approvals remain with the user.
- Long projects span sessions; continuity depends on files kept in the project folder.
- Routing reflects the skills in this collection and does not cover tasks outside them.

## Troubleshooting

| Problem | Likely cause | Solution |
|---|---|---|
| It is unclear which stage the user is at | The request names a goal without the current state | Ask what exists (topic, papers, results, draft) in at most three questions |
| A step fails or returns a blocking finding | For example no gap found, idea already published, or references that cannot be verified | Stop, report it, and replan from the earlier stage instead of continuing |
| The plan is too long for the deadline | Too many skills were chained | Keep the steps that affect acceptance and integrity and drop the optional ones |
| A routed skill is not installed | Only part of the collection was copied | Install the missing skill or follow its steps manually and say so |

## Related skills

- `idea-to-paper-pipeline` for the full sequence from topic to self-reviewed draft.
- `research-progress-tracker` to hold the plan, milestones, and next actions across sessions.
- `weekly-paper-digest` to keep the literature current while the project runs.
- `paper-search` and `citation-verifier`, which most routes depend on.
- `research-gap-finder`, `methodology-designer`, `results-interpreter`, `paper-outline-generator`, and `self-peer-reviewer` are the usual entry points for the five main stages.
