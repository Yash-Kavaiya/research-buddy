---
name: sop-and-research-statement-writer
description: "Helps write statements of purpose and research statements from the applicant's real experience, tailored to each prompt. Use for graduate, postdoc, or faculty applications. Not for full proposals."
version: 1.0.0
metadata:
  author: "Yash Kavaiya <yash.kavaiya3@gmail.com>"
  tags: [statement-of-purpose, research-statement, admissions, applications]
---

# SOP and Research Statement Writer

## Purpose

Help an applicant tell a true, specific account of what they have done, what they want to do, and why a given programme or position is the place to do it. The statement is built from an interview with the applicant and stays in their voice.

## When to use

- Statement of purpose or personal statement for master's or PhD admission.
- Research statement for a fellowship, postdoctoral, or faculty application.
- Revising, tailoring, or shortening an existing statement.

Hand off instead for a full research proposal (`phd-research-proposal-writer`) or the email to a professor (`supervisor-finder`).

## Prerequisites

- The exact prompt and length limit for each application.
- The applicant's CV and the details behind each experience: their role, the methods, and the outcome.
- The target programme's faculty and resources, verified on the department's site.

## Inputs

- The exact prompt and limits (words, characters, or pages) for each application. Prompts differ; some ask for separate research and personal statements.
- The applicant's CV and the stories behind it: for each project, what they did, what was hard, what they found, and what it changed in their thinking.
- Research interests, as specifically as they can state them.
- The target programme: faculty they want to work with and why, labs, courses, resources.
- Anything to address: a low grade, a gap, a change of field.

Interview the applicant before drafting. Without their specifics, a statement is generic, and generic statements are the ones that fail.

## Instructions

1. **Read the prompt** and list what it asks. Answer every part, in the order that serves the reader.
2. **Collect the raw material.** For each significant experience ask: What was the problem? What exactly did you do, as distinct from the team? What tools or methods? What was the result (numbers, a paper, a deployed system)? What did you learn that shapes what you want to do next?
3. **Find the thread**: the question or theme that connects the experiences to the proposed study. The statement argues that the applicant's past leads to this next step.
4. **Choose the structure:**

   *Statement of purpose (admission)*
   1. Opening: the research interest stated directly, with the experience or question that produced it. No childhood anecdotes or quotations.
   2. Preparation: two or three experiences in depth, with contribution and outcome, in preference to a list of everything.
   3. Research interests and goals: the problems the applicant wants to work on and why they matter, at a level that shows they have read the area.
   4. Fit: specific faculty (two or three), with what in their recent work connects to the applicant's interests; relevant resources.
   5. Career goals and close.

   *Research statement (postdoc or faculty)*
   1. Research vision in one paragraph.
   2. Past and current work: the problems, the applicant's contributions, the results and their impact, with citations to their papers.
   3. Future agenda: two or three directions for the next 3 to 5 years, with first projects, methods, likely funding sources, and how students would be involved.
   4. Fit with the department: collaborations and facilities.

5. **Draft in the applicant's voice**: first person, active verbs, concrete nouns. Show with detail and outcome; do not assert qualities ("I am passionate and hardworking").
6. **Address weaknesses briefly and factually**, where needed: what happened, and what has changed since, in two or three sentences without excuses.
7. **Tailor each version.** Only the fit section and some emphasis should change between programmes, but those must change for real. Verify every faculty name, lab, and paper mentioned against the department's site (`supervisor-finder`, `paper-search`).
8. **Cut to the limit** by removing generalities first. Keep the specifics.
9. **Final checks**: programme and university names correct in every version; prompt fully answered; limit met; no claim the applicant cannot support in an interview.

## Output format

```markdown
## Statement of Purpose: <Programme, University> (<n> words; limit <L>)
<the statement>

---
## Notes
- Thread: ...
- Tailored elements: faculty named and why; resources
- Facts verified: <faculty and papers checked on the department site, date>
- Placeholders for you to fill or confirm: [...]
- Suggestions for other versions: what to swap for <University B>
```

For revisions, give the revised text and a short list of what changed and why.

## Examples

Requests that should trigger this skill:

- "Write my SOP for an MS in data science."
- "Draft a statement of purpose for a PhD in computational biology."
- "Write a research statement for a faculty application."
- "Tailor my SOP for a different university."
- "Cut my personal statement from 1,400 to 1,000 words."

Requests that belong to another skill:

- "Write a full PhD research proposal." → use `phd-research-proposal-writer`
- "Write an email to a professor." → use `supervisor-finder`
- "Write a cover letter for a journal." → use `cover-letter-writer`

### Worked example

**Request:** "SOP, 800 words, for a PhD in NLP. My main experience: a one-year project building a Gujarati speech corpus (40 hours) and a baseline recogniser at 23% word error rate."

**What the agent does:**

1. Reads the prompt and interviews the applicant about the project: their role, what was hard, and what they want next.
2. Finds the thread: low-resource language technology.
3. Drafts opening, preparation in depth, research interests, and fit, verifying two named faculty on the department site.
4. Lists placeholders and what to change for other universities.

**Result (excerpt):**

```markdown
I want to build speech technology for languages that have little recorded data, because I have seen what its absence costs. Over the past year I collected and transcribed a 40-hour Gujarati speech corpus and trained a baseline recogniser that reaches a 23% word error rate. Most of that error came from code-switching with English, which standard pipelines treat as noise. ...

Notes
- Facts verified: Prof. [name]'s 2025 paper on code-switched ASR (department site, today)
- To confirm: your exact role in transcription (led or contributed?)
```

## Quality bar and pitfalls

- Every experience, result, role, grade, and award in the statement must be true and the applicant's own. Never invent or inflate achievements, publications, or the applicant's share of team work. Ask when a detail is missing; do not fill it in.
- The statement must remain the applicant's. Draft from their material and keep their voice, so they can stand behind every sentence. Tell them to check each programme's policy on AI assistance in application materials; some require disclosure or prohibit it.
- Never name a professor, lab, or paper without verifying it exists and that the professor is still at the institution and taking students where that can be determined.
- Avoid the standard failures: opening with a quotation or a childhood story; listing the CV in prose; praising the university's ranking; vague interests ("AI and machine learning"); the same statement sent everywhere.
- Research statements need a future agenda that is distinct from the applicant's advisor's programme.
- Do not disclose sensitive personal information the applicant has not chosen to share.
- Respect the limit. Admissions readers stop at it.

## Limitations

- The statement can contain only what the applicant has actually done. Missing details are asked for, not invented.
- Admission outcomes depend on many factors beyond the statement.
- Faculty availability and research direction change; names are verified at the time of writing and should be rechecked.
- Programmes differ in their rules on AI assistance; the applicant is responsible for compliance.

## Troubleshooting

| Problem | Likely cause | Solution |
|---|---|---|
| The draft sounds generic | It lacks the applicant's specifics | Interview for concrete details: what exactly they did, with what result, and what it changed |
| A named professor has left or is not taking students | The department page was outdated or not checked | Reverify on the current faculty page and replace the name |
| The statement is over the limit | It lists every CV item | Keep two or three experiences in depth and cut general statements |
| A claim cannot be supported in an interview | It was inflated, making it invalid | Reword it to what the applicant actually did |

## Related skills

- `supervisor-finder` to identify faculty and verify their current work.
- `paper-search` to read a target professor's recent papers.
- `phd-research-proposal-writer` when a proposal accompanies the statement.
- `research-question-formulator` to sharpen the stated research interests.
- `academic-tone-editor` for a language pass that preserves the applicant's voice.
- `grant-proposal-writer` for fellowship applications that need a project plan.
