---
name: research-progress-tracker
description: "Maintains a research plan in Markdown: milestones, supervisor meeting agendas and minutes, decisions, and action items. Use to plan and track a thesis or paper. Not for logging experiment runs."
version: 1.0.0
metadata:
  author: "Yash Kavaiya <yash.kavaiya3@gmail.com>"
  tags: [project-tracking, phd-planning, milestones, supervisor-meetings]
---

# Research Progress Tracker

Keep one small set of files that answers three questions at any time: where is the project against its deadlines, what was agreed with the supervisor, and what is the next action.

## Purpose

Keep one small set of files that says, at any time, where a research effort stands against its deadlines, what was agreed with the supervisor, and what the next action is. It prepares meeting agendas, writes minutes, and runs a weekly review.

## When to use

- Setting up a plan for a thesis, paper, or funded project.
- Before a supervisor or committee meeting (agenda) and after it (minutes and actions).
- A weekly or monthly review, or a formal progress report.
- The user feels stuck or behind and needs the next concrete step.

Hand off instead for logging experiment runs (`experiment-logger`) or planning the experiments themselves (`experiment-planner`).

## Prerequisites

- The goal and hard deadlines of the thesis, paper, or funded work.
- The current state, meeting notes, and realistic weekly time available.
- Write access to a `research-tracker/` folder; existing tracker files are read first.

## Inputs

- The project goal and hard deadlines: submission dates, funding end, committee reviews, conference deadlines.
- The current state: what is done, in progress, and not started.
- Meeting notes, however rough.
- Time actually available per week, and known absences.
- Existing tracker files, if any. Read them first.

## Instructions

1. **Set up the tracker** in a `research-tracker/` folder in the project (or use the existing one):

   ```
   research-tracker/
     PLAN.md         # goal, milestones, timeline
     ACTIONS.md      # open and done action items
     DECISIONS.md    # dated decisions with reasons
     meetings/       # one file per meeting, named by date and type
     reviews/        # one file per weekly review, named by ISO week
   ```

2. **Build the plan backwards from the deadline.** List the deliverables (chapters, papers, studies), then the milestones each needs, then place them on the calendar from the deadline back to today. Include the slow items people forget: ethics approval, data access, co-author and supervisor review rounds (two to four weeks each), formatting, and administrative submission steps. Add a buffer of about 20 to 30%.
3. **Make milestones checkable.** "Literature review" is a topic; "Chapter 2 draft sent to supervisor" is a milestone. Each has a date, an owner, a status, and a dependency if any.
4. **Before a meeting, prepare the agenda:**
   - Progress since last meeting, against the actions that were set.
   - Results or drafts to show, sent in advance.
   - Decisions needed from the supervisor, each phrased as a question with options and the user's recommendation.
   - Blockers and what would unblock them.
   - Plan until the next meeting.
5. **After a meeting, write the minutes** from the user's notes, the same day: date and attendees, points discussed, decisions (copied to *DECISIONS.md* with the reason), and action items with owner and due date (copied to *ACTIONS.md*). Draft a short follow-up email summarising decisions and actions, for the user to send so both sides share one record.
6. **Run the weekly review:** what was completed, what slipped and why, which milestone is at risk, and the three most important actions for the coming week. Update statuses in *PLAN.md*. If a milestone slips, move the dependent dates and say what the new end date is; do not leave an impossible plan in place.
7. **Pick the next action** when the user is stuck: the smallest concrete step on the critical path that can be done in one sitting ("write the 150-word summary of paper X", not "work on chapter 2").
8. **Write progress reports** for committees or funders from the tracker: progress against planned milestones, outputs (papers, talks, datasets), deviations with reasons, plan for the next period, and risks. Use the institution's or funder's form.
9. **Render a timeline** when asked, as a Mermaid Gantt chart generated from *PLAN.md*.

## Output format

*PLAN.md*:

```markdown
# <Project> plan
Goal: ...  Hard deadline: 2027-06-30 (thesis submission). Updated: 2026-03-09.

| # | Milestone | Due | Status | Depends on | Notes |
|---|---|---|---|---|---|
| M1 | Ethics approval received | 2026-04-15 | in progress | | submitted 2026-03-01 |
| M2 | Data collection complete | 2026-08-31 | not started | M1 | |

Status values: not started, in progress, done, at risk, blocked.
```

*ACTIONS.md*:

```markdown
| ID | Action | Owner | Due | Status | From |
|---|---|---|---|---|---|
| A14 | Send Chapter 2 draft to supervisor | me | 2026-03-20 | open | meeting 2026-03-09 |
```

Meeting file:

```markdown
# Supervisor meeting, 2026-03-09
Attendees: ...
## Agenda
## Discussion
## Decisions
- D7: Use dataset B instead of A, because ...
## Actions
- A14 (me, 2026-03-20): ...
## Next meeting
```

Gantt (Mermaid):

```mermaid
gantt
  dateFormat YYYY-MM-DD
  section Study 1
  Ethics approval      :active, m1, 2026-03-01, 45d
  Data collection      :m2, after m1, 120d
```

## Examples

Requests that should trigger this skill:

- "Plan my thesis timeline; I must submit in 18 months."
- "Prepare the agenda for my supervisor meeting tomorrow."
- "Turn these rough notes into meeting minutes with action items."
- "What should I work on next? I'm stuck."
- "Write my six-month progress report for the committee."

Requests that belong to another skill:

- "Log this training run and its metrics." → use `experiment-logger`
- "Plan which experiments to run." → use `experiment-planner`
- "Write my thesis chapter." → use `thesis-chapter-writer`

### Worked example

**Request:** "Here are my notes from today's supervisor meeting: agreed to switch to dataset B because A has label noise; I send chapter 2 draft in two weeks; she will introduce me to Dr. K; next meeting in three weeks."

**What the agent does:**

1. Reads the existing tracker files.
2. Writes the meeting file with discussion, decisions, and actions.
3. Copies the decision with its reason to *DECISIONS.md* and the actions with owner and due date to *ACTIONS.md*.
4. Updates the milestone dates affected and drafts a follow-up email.

**Result (excerpt):**

```markdown
## Decisions
- D7: Use dataset B instead of A, because of label noise in A.

## Actions
- A14 (me, due in 2 weeks): send Chapter 2 draft to supervisor
- A15 (supervisor, date to confirm with supervisor): introduction to Dr. K

PLAN.md updated: M3 "Experiments on dataset A" renamed and moved two weeks later because of the dataset change; thesis submission date unchanged, buffer reduced from 8 to 6 weeks.
```

## Quality bar and pitfalls

- Record what was actually said and decided. Do not add decisions, feedback, or commitments that are not in the user's notes; mark unclear points "to confirm with supervisor".
- Do not mark anything done that the user has not confirmed is done.
- Be honest about slippage. A plan that shows everything on track when it is not serves nobody; show the new date and the consequence.
- Every action has an owner and a date. Actions without them do not get done.
- Do not plan at 100% capacity. Teaching, illness, reviews, and revisions take time.
- Notes may contain personal or sensitive remarks about people. Keep the tracker private to the project, and keep minutes factual.
- Keep the system small. A tracker that takes longer to maintain than it saves will be abandoned; four files are enough.
- Update existing files; do not create a new plan each session.

## Limitations

- The tracker records what the user reports. It cannot verify that work was done or that a supervisor agreed to something.
- Plans are estimates; research timelines slip, and the tracker shows slippage without preventing it.
- It keeps plain Markdown files and does not sync with calendars or task apps.
- Continuity across sessions depends on the files being kept in the project.

## Troubleshooting

| Problem | Likely cause | Solution |
|---|---|---|
| A milestone has slipped | Work took longer or a dependency was late | Move the dependent dates, show the new end date and remaining buffer, and record the reason |
| Meeting notes are ambiguous | Decisions and owners were not captured | Write the unclear points as "to confirm with supervisor" and include them in the follow-up email |
| The plan no longer fits the deadline | Scope exceeds the time left, so the plan fails | Show which deliverable must shrink or move and ask the user and supervisor to decide |
| Tracker files conflict with each other | A new plan was created instead of updating the old one | Merge into the existing files and keep one PLAN.md |

## Related skills

- `research-scholar-orchestrator` and `idea-to-paper-pipeline` to decide what the next stage of work is.
- `experiment-logger` for run-level records that the weekly review summarises.
- `experiment-planner` and `methodology-designer` for the content of the milestones.
- `thesis-chapter-writer` for chapter milestones.
- `grant-proposal-writer` for the work plan of a funded project, and reports against it.
- `weekly-paper-digest` to feed a reading list into the actions.
- `viva-defense-prep` when the final milestone approaches.
- `supervisor-finder` uses the tracker to log contacts and replies.
