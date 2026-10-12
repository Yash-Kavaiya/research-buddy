---
name: phd-research-proposal-writer
description: "Writes a PhD research proposal or synopsis for admission or registration: background, gap, questions, methodology, timeline, and references. Use for doctoral applications. Not for grant applications."
version: 1.0.0
metadata:
  author: "Yash Kavaiya <yash.kavaiya3@gmail.com>"
  tags: [phd, research-proposal, synopsis, doctoral-admission]
---

# PhD Research Proposal Writer

Write a proposal that shows a committee three things: there is a real gap, the candidate has a workable plan to address it, and the project fits a doctoral timeline.

## Purpose

Help a candidate write a proposal that shows a committee there is a real gap, a workable plan to address it, and a scope that fits a doctoral timeline. It is built from the candidate's own interests and reading, and every reference is retrieved.

## When to use

- Applying for PhD admission where a research proposal is required.
- Preparing the synopsis for registration or a research committee (RDC, DRC, RAC).
- A confirmation or upgrade report early in the PhD.

Hand off instead for a funding application (`grant-proposal-writer`) or a personal statement (`sop-and-research-statement-writer`).

## Prerequisites

- The university's and department's required format and limits.
- The candidate's research interest, background, and any prior work.
- Access to `paper-search` for the literature, and the prospective supervisor's area if known.

## Inputs

- The university's and department's format and limits: sections, word or page count (admission proposals are often 1,500 to 3,000 words; registration synopses run longer), citation style.
- The candidate's research interest, background, and any prior work (master's thesis, publications, projects).
- The prospective supervisor's research area, if known.
- Stage: admission, registration, or confirmation. The expected depth differs.
- Resources and constraints: duration, funding, access to data, labs, or field sites.

## Instructions

1. **Get the required format** from the university. Follow its headings and limits exactly; where none is given, use the structure in the output format below.
2. **Narrow the topic** to something one person can complete in three to five years. Move from area to topic to a specific problem (`research-gap-finder`, `research-question-formulator`).
3. **Ground it in the literature.** Search and read enough to establish what is known and what is missing (`paper-search`). At admission stage 15 to 25 well-chosen sources suffice; a registration synopsis needs a fuller review. Cite only what was retrieved.
4. **State the gap and the research problem** in a short paragraph that follows from the literature.
5. **Write the research questions and objectives**: one overarching aim, and 3 to 4 objectives with measurable verbs, each of which could become a thesis chapter or paper. Add hypotheses where the design is confirmatory.
6. **Propose the methodology** per objective: design, data or materials and how they will be obtained, methods and tools, analysis, and validation. Show feasibility: name the dataset, instrument, or lab. Admission proposals may leave options open, but must show the candidate understands the choices (`methodology-designer`).
7. **Scope and limits**: what is included and excluded, and the main risk with a fallback.
8. **Plan the timeline** by semester or quarter: coursework and literature review, each objective, publications, thesis writing, submission. Be realistic about ethics approval, data collection, and writing time.
9. **State the expected contributions**: to knowledge, method, and practice. Specific and modest beats grand.
10. **Fit to the department** (admission): one or two sentences on how the project relates to the supervisor's or group's work, based on their actual publications.
11. **Write the title last**: specific, under about 15 words, naming the problem and approach.
12. **Compile the references** and verify them (`citation-verifier`).

## Output format

```markdown
# <Title>
Candidate: ...  Proposed supervisor: ...  Department: ...

## 1. Introduction and background
## 2. Review of literature and research gap
## 3. Problem statement
## 4. Research questions, aim, and objectives
## 5. Proposed methodology
| Objective | Data / materials | Method | Analysis | Outcome |
## 6. Scope and limitations
## 7. Work plan
| Activity | S1 | S2 | S3 | S4 | S5 | S6 |
## 8. Expected contributions
## 9. Ethical considerations (if applicable)
## 10. References

---
Word count: <n> of <limit>
To confirm or supply: ...
```

## Examples

Requests that should trigger this skill:

- "Write a PhD research proposal on AI for early dyslexia detection."
- "Draft my PhD synopsis for the research committee meeting."
- "I need a 2,000-word research proposal for a PhD application in the UK."
- "Improve the methodology section of my doctoral proposal."
- "Help me narrow my PhD topic and write the proposal."

Requests that belong to another skill:

- "Write a grant proposal for a funding agency." → use `grant-proposal-writer`
- "Write my statement of purpose." → use `sop-and-research-statement-writer`
- "Find potential supervisors." → use `supervisor-finder`

### Worked example

**Request:** "PhD proposal, 2,000 words, for a UK computer science department. Interest: detecting dyslexia early from children's handwriting with machine learning. I have an MSc project on handwriting recognition."

**What the agent does:**

1. Asks for the department's format and the candidate's own ideas, then narrows the topic to a specific problem.
2. Searches the literature, establishes the gap from retrieved papers, and writes the questions and objectives.
3. Proposes methodology per objective, naming a candidate public dataset to confirm.
4. Drafts the timeline and contributions and verifies the references.

**Result (excerpt):**

```markdown
## 3. Problem statement
Screening for dyslexia usually happens after reading difficulties are established. Handwriting samples are collected routinely in early schooling, but existing studies [retrieved refs] use small, single-language samples and tablets that schools rarely have.

## 4. Aim and objectives
Aim: to determine whether paper handwriting samples from children aged 5 to 7 can support early screening.
1. Assemble and annotate a handwriting dataset (months 1 to 12).

To confirm: access to schools and ethics approval for work with children.
```

## Quality bar and pitfalls

- The proposal must be the candidate's own plan, built from their interests and reading. Write it with them: ask for their ideas and background, and do not produce a generic proposal for them to submit unread. They will have to defend it in an interview.
- Tell the candidate to check the university's policy on AI assistance in application documents.
- Every reference must be real and retrieved. Committees check, and a fabricated citation ends an application.
- A proposal is a plan, not a result. Do not predict findings as facts.
- Too broad is the usual fault. "AI in healthcare" is an area; a proposal needs a problem.
- The methodology must be doable with the access the candidate actually has. Name the data source and confirm it exists.
- Do not claim "no work has been done" without a search that shows it.
- Tailoring to a supervisor means engaging with their research, not flattering them.
- Proposals are run through similarity checks. Text copied from sources, including the candidate's own master's thesis without citation, will be flagged.

## Limitations

- The proposal must be the candidate's own plan; the skill drafts from their ideas and cannot substitute for them in an interview.
- At admission stage the literature covered is a sample; a fuller review follows after enrolment.
- Feasibility depends on access (participants, facilities, datasets) that the skill cannot confirm.
- University policies on AI assistance in applications vary and must be checked by the candidate.

## Troubleshooting

| Problem | Likely cause | Solution |
|---|---|---|
| The topic is too broad for a PhD | It names an area, not a problem | Narrow by population, method, or setting until one person could complete it |
| A reference cannot be verified | It was recalled, not retrieved, and may be invalid | Remove it or replace it with a retrieved record via `paper-search` and `citation-verifier` |
| The methodology depends on unavailable access | The named dataset or site does not exist or cannot be reached | Replace it with an obtainable source and state the fallback |
| The proposal is over the word limit | The background is too long | Cut general background and keep the gap, questions, and method |

## Related skills

- `research-gap-finder`, `topic-trend-analyzer`, and `novelty-checker` to settle the topic and gap.
- `research-question-formulator` for questions and objectives.
- `paper-search` and `literature-review-writer` for the review section.
- `methodology-designer` and `sample-size-power-calculator` for the methodology.
- `ethics-irb-drafter` where human participants are involved.
- `supervisor-finder` to identify and approach potential supervisors.
- `sop-and-research-statement-writer` for the accompanying statement.
- `citation-verifier` and `plagiarism-and-paraphrase-checker` before submission.
- `viva-defense-prep` for the proposal interview or committee presentation.
