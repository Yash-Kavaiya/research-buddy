---
name: idea-to-paper-pipeline
description: "Runs eight checkpointed stages from research topic to self-reviewed paper draft, saving each stage's output and pausing for decisions. Use for a guided end-to-end paper. Not for one or two stages."
version: 1.0.0
metadata:
  author: "Yash Kavaiya <yash.kavaiya3@gmail.com>"
  tags: [pipeline, research-workflow, paper-writing, end-to-end]
---

# Idea to Paper Pipeline

Chain the collection's skills into one process with a checkpoint after every stage. The pipeline organises and drafts; the research itself (collecting data, running experiments) is done by the user between stages 4 and 5.

## Purpose

Chain the collection's skills into one process from topic to mock-reviewed draft, with a checkpoint after every stage where the researcher decides. The pipeline organises and drafts; the research itself is done by the user between the design and results stages.

## When to use

- Starting a paper from a topic or rough idea.
- Picking up a project part-way: enter at the stage that matches what exists.

Use `research-scholar-orchestrator` instead for a request that covers only one or two stages.

## Prerequisites

- The other research-scholar skills installed, with Python and network access for those that use scripts.
- A topic or idea, the paper type, the target venue or venue type, and the deadline.
- A project folder for stage outputs, and real results from the user before stage 5.

## Inputs

- The topic or idea, the field, and the kind of paper (empirical, method, review, short paper).
- Target venue or venue type, and the deadline.
- What exists already: papers read, data, code, results, draft text.
- Resources: data access, compute or lab time, collaborators.

## Instructions

Create a project folder and keep one file per stage. At each checkpoint, show the stage summary, state the decision needed, and wait for the user before continuing. Record progress in *pipeline-status.md*.

```
project/
  pipeline-status.md
  01-gap.md  02-novelty.md  03-literature/  04-design.md
  05-results.md  06-draft/  07-citations.md  08-review.md
```

**Stage 1. Topic and gap.**
Run `topic-trend-analyzer` on the topic, then `research-gap-finder`. Then `research-question-formulator` on the gap the user prefers.
*Output:* ranked gaps with evidence; one primary research question with objectives and hypotheses.
*Checkpoint:* the user chooses the gap and approves the question. *Stop if* no supportable gap is found: report and widen or shift the topic.

**Stage 2. Novelty.**
Run `novelty-checker` on the idea that addresses the question.
*Output:* closest prior work, differences, verdict.
*Checkpoint:* the user confirms the idea is differentiated, or revises it. *Stop if* the verdict is "already done": return to stage 1 with the next gap.

**Stage 3. Literature.**
Run `paper-search` and `citation-graph-explorer` to build the corpus; `paper-summarizer` on the key papers; `paper-comparison-matrix`; then `literature-review-writer` for a review, or `related-work-writer` for a paper's related-work section. Clean the references with `bibtex-manager`.
*Output:* corpus, matrix, review or related-work draft, `.bib` file.
*Checkpoint:* the user confirms coverage and the positioning.

**Stage 4. Design.**
For studies with participants: `methodology-designer`, `sample-size-power-calculator`, `survey-questionnaire-designer`, `ethics-irb-drafter`. For computational work: `dataset-finder`, `experiment-planner`, `ablation-study-designer`, and set up `experiment-logger`.
*Output:* methodology or experiment plan with budget, and ethics drafts where needed.
*Checkpoint:* the user (and their supervisor) approves the design. **The pipeline pauses here while the user does the research.** Ethics approval comes before data collection.

**Stage 5. Results.**
When data or results exist: `statistical-test-selector` or `qualitative-coding-assistant` for the analysis, then `results-interpreter`.
*Output:* findings with evidence, effect sizes, caveats, and the claims the paper can make.
*Checkpoint:* the user agrees the claims. *Stop if* the results do not support a paper: report what they do show and the options (more data, a narrower claim, a negative-result paper).

**Stage 6. Outline and draft.**
`paper-outline-generator` for the venue; `publication-figure-maker`, `architecture-diagram-maker`, and `latex-table-generator` for display items; then the sections: method and results text from stages 4 and 5, `introduction-writer`, the related work from stage 3, `limitations-and-future-work-writer`, and last `abstract-writer`. Finish with `academic-tone-editor` and `latex-paper-formatter`.
*Output:* a complete draft in the venue template.
*Checkpoint:* the user reads the whole draft and corrects it.

**Stage 7. Citation and integrity check.**
`citation-verifier` on the bibliography and the claims; `plagiarism-and-paraphrase-checker` against the main sources; `reproducibility-checklist` for the venue.
*Output:* verification report, with every problem fixed or listed.
*Checkpoint:* no reference remains unverified without the user knowing.

**Stage 8. Mock review and submission prep.**
`self-peer-reviewer` on the draft; fix what can be fixed; `venue-recommender` if the venue is open; `camera-ready-checker` on the PDF; `cover-letter-writer` for journals.
*Output:* mock review, fix list, compliance report.
*Checkpoint:* the user decides to submit, revise, or change venue.

After submission: `rebuttal-writer` for reviews, and `paper-to-slides`, `paper-to-poster`, or `paper-to-blog` after acceptance.

## Output format

*pipeline-status.md*, updated at every checkpoint:

```markdown
# Pipeline: <working title>
Venue: ...  Deadline: ...  Started: ...

| Stage | Status | Output file | Decision made | Date |
|---|---|---|---|---|
| 1 Topic and gap | done | 01-gap.md | Gap 2; RQ approved | 2026-03-02 |
| 2 Novelty | done | 02-novelty.md | differentiated; scope narrowed to X | 2026-03-03 |
| 3 Literature | in progress | 03-literature/ | | |

## Open items
## Assumptions made
## Next action
```

Each checkpoint message has three parts: what was produced, what was found that the user should know (including problems), and the decision needed.

## Examples

Requests that should trigger this skill:

- "Take my idea to a paper: energy-aware scheduling for edge devices."
- "Help me write a paper from scratch on this topic."
- "Run the whole research pipeline for my thesis paper."
- "Plan my paper end to end with checkpoints."
- "I have results already. Pick up the pipeline from there."

Requests that belong to another skill:

- "Just find gaps in this topic." → use `research-gap-finder`
- "Route this one request to the right skill." → use `research-scholar-orchestrator`
- "Track my milestones." → use `research-progress-tracker`

### Worked example

**Request:** "Start the pipeline: topic is detecting fake reviews with graph neural networks; target a mid-tier data mining conference in five months."

**What the agent does:**

1. Creates the project folder and *pipeline-status.md*.
2. Stage 1: runs trend and gap analysis and presents four gaps; the user picks one and approves the research question.
3. Stage 2: runs the novelty check, finds the idea incremental, and the user narrows it to cold-start reviewers.
4. Records the decision and proceeds to stage 3 after confirmation.

**Result (excerpt):**

```markdown
| Stage | Status | Output file | Decision made | Date |
|---|---|---|---|---|
| 1 Topic and gap | done | 01-gap.md | Gap 2 (cold-start reviewers); RQ approved | day 1 |
| 2 Novelty | done | 02-novelty.md | incremental as stated; narrowed to cold-start setting | day 2 |
| 3 Literature | in progress | 03-literature/ | | |

Next action: confirm corpus coverage (32 papers) before the related-work draft.
```

## Quality bar and pitfalls

- Stage 5 needs real results from the user. Never generate, simulate, or assume data or results to keep the pipeline moving, and never write a results section before results exist. A draft may be prepared with clearly marked placeholders such as `[RESULT: accuracy on dataset A]`, and stays marked as incomplete.
- Do not skip checkpoints. Each one is a decision that belongs to the researcher, and an error at stage 1 or 2 costs every later stage.
- Stop conditions are real. An idea that has been done, or results that do not support the claim, end that path; say so and return to the earlier stage.
- Every reference in the draft comes from a retrieved record, and stage 7 is mandatory before the draft is called complete.
- The user must read, understand, and take responsibility for the whole paper, and disclose AI assistance as the venue requires.
- Enter at the right stage. If results exist, start at stage 5 and backfill stage 3 for the related work; do not redo what is done.
- One pass rarely suffices. The mock review usually sends the work back to stage 5 or 6.

## Limitations

- The pipeline cannot produce results. Stage 5 waits for the user's real observations or experiments.
- Each stage inherits the limits of its skills, for example search coverage and unverifiable references.
- A full run takes weeks to months and many sessions; progress depends on the status file being kept.
- The mock review estimates reviewer reaction and does not predict the decision.

## Troubleshooting

| Problem | Likely cause | Solution |
|---|---|---|
| A stage ends in a stop condition | No supportable gap, idea already done, or results that do not support the claim | Report it, return to the earlier stage, and record the decision in the status file |
| The pipeline is resumed in a new session | Earlier context is gone | Read *pipeline-status.md* and the stage files first, then continue from the next open stage |
| Results are not ready but the user wants a draft | Stage 5 has not happened | Draft the other sections with marked placeholders; never fill results, since invented values would be invalid |
| Stage 7 reports unverified references | References came from memory or other tools | Fix or remove each one before stage 8 |

## Related skills

- `research-scholar-orchestrator` for partial routes and single tasks.
- `research-progress-tracker` to hold milestones and supervisor feedback alongside *pipeline-status.md*.
- `research-gap-finder`, `novelty-checker`, `literature-review-writer`, `methodology-designer`, `experiment-planner`, `results-interpreter`, `paper-outline-generator`, `citation-verifier`, and `self-peer-reviewer` are the main skill of each stage.
- `weekly-paper-digest` to catch new related work while the project runs.
