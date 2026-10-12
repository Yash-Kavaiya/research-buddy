---
name: research-question-formulator
description: "Turns a research interest or gap into testable questions, objectives, and hypotheses with PICO, SPIDER, and FINER. Use when framing a study. Not for study design; use methodology-designer."
version: 1.0.0
metadata:
  author: "Yash Kavaiya <yash.kavaiya3@gmail.com>"
  tags: [research-question, hypothesis, pico, finer]
---

# Research Question Formulator

Move from "I am interested in X" to one primary question, a few secondary questions, and hypotheses that a study could actually test.

## Purpose

Move a researcher from an area of interest to one primary question that data can answer, with secondary questions, measurable objectives, and hypotheses. The output is the starting point for a proposal's aims section and for the study design.

## When to use

- The user has an interest, a gap, or a draft question and needs it sharpened.
- A proposal needs an aims, objectives, or hypotheses section.

Hand off instead when the user has no gap yet (`research-gap-finder`) or wants the study design itself (`methodology-designer`).

## Prerequisites

- An interest, gap, or draft question stated by the user.
- The user's constraints: time, access to participants or datasets, and equipment or compute.
- No tools or network access are required.

## Inputs

- The interest or gap in the user's own words.
- Field and study type they expect (experiment, observational, qualitative, computational, review).
- Constraints: time, data they can access, equipment or compute, ethics limits.
- Purpose: thesis, paper, grant, coursework.

Ask only for what is missing. Two or three questions are usually enough.

## Instructions

1. **Restate the interest** in one sentence and confirm it.
2. **Pick the framing tool** by study type:

   | Study type | Framework | Elements |
   |---|---|---|
   | Intervention or comparison (clinical, education, HCI, A/B) | PICO(T) | Population, Intervention, Comparison, Outcome, (Time) |
   | Exposure or observational | PECO | Population, Exposure, Comparison, Outcome |
   | Qualitative or mixed | SPIDER | Sample, Phenomenon of Interest, Design, Evaluation, Research type |
   | Computational or engineering | Task, Method, Baseline, Metric, Setting | what is being done, how, against what, measured how, under which conditions |

3. **Fill the framework** as a table. Mark any element the user has not decided, and propose a default.
4. **Draft 3 candidate primary questions** at different scopes (narrow, medium, ambitious). Each must name its variables or phenomenon and its population or setting.
5. **Score each with FINER** in a table: Feasible, Interesting, Novel, Ethical, Relevant. Give a one-line reason per cell. Do not assert novelty without a check; say "unverified, run `novelty-checker`" until a search validates it.
6. **Recommend one** and say why.
7. **Derive from it:**
   - 2 to 4 secondary questions.
   - Objectives written with measurable verbs (estimate, compare, identify, evaluate).
   - For quantitative questions: a null and an alternative hypothesis per primary outcome, with the direction of the expected effect and the variable types.
   - For qualitative questions: no hypotheses. Give the central question and sub-questions instead.
8. **Define the terms** the question relies on, with how each would be measured.

## Output format

```markdown
## Framing (<framework>)
| Element | Value | Status |
|---|---|---|

## Candidate questions
1. Narrow: ...
2. Medium: ...
3. Ambitious: ...

## FINER assessment
| Question | Feasible | Interesting | Novel | Ethical | Relevant |
|---|---|---|---|---|---|

## Recommended primary question
> ...

## Secondary questions
## Objectives
## Hypotheses
- H0: ...
- H1: ... (direction, variables, how measured)

## Operational definitions
| Term | Definition | Measure |
|---|---|---|

## Open decisions for you
```

## Reference files

Open these only when the step calls for them; they are not needed for every request.

- `references/frameworks-and-wording.md`: Read at steps 2 to 7, when choosing a framework, wording the question, and writing objectives and hypotheses.
- `assets/research-question-worksheet.md`: Copy and fill to deliver the questions, objectives, and hypotheses.

## Examples

Requests that should trigger this skill:

- "Help me frame a research question on social media use and teenage sleep."
- "I'm interested in using LLMs for code review but don't know what to ask."
- "Write hypotheses for a study comparing two teaching methods."
- "Is this a good research question: how can we improve hospital efficiency?"
- "I need objectives and research questions for my synopsis."

Requests that belong to another skill:

- "Which research design should I use for this question?" → use `methodology-designer`
- "How many participants do I need?" → use `sample-size-power-calculator`
- "What topics are open in this field?" → use `research-gap-finder`

### Worked example

**Request:** "I want to study whether short mindfulness sessions help nursing students with exam stress. Help me write the research question and hypotheses. I have one semester and access to about 120 students."

**What the agent does:**

1. Restates the interest and chooses PICO(T) because the study compares an intervention with a control.
2. Fills the framework, marking the comparison group and outcome measure as undecided and proposing defaults.
3. Drafts narrow, medium, and ambitious questions and scores each with FINER.
4. Recommends the medium question and derives objectives, null and alternative hypotheses, and operational definitions.

**Result (excerpt):**

```markdown
## Recommended primary question
> Among second-year nursing students (P), does a four-week programme of 10-minute daily mindfulness sessions (I), compared with no programme (C), reduce exam-related stress measured by the Perceived Stress Scale (O) at the end of the semester (T)?

- H0: Mean PSS-10 scores at week 4 do not differ between groups.
- H1: Mean PSS-10 scores at week 4 are lower in the mindfulness group.
- Novel: unverified, run `novelty-checker`.
```

## Quality bar and pitfalls

- A good question can be answered by data. Reject "How can we improve X?" in favour of "Does A improve X compared with B in population P, measured by M?".
- One question, one main outcome. Split double-barrelled questions.
- Hypotheses must be falsifiable and state direction when theory supports one.
- Do not write hypotheses for exploratory or qualitative work to make it look rigorous.
- Keep the scope within the stated constraints. Say plainly when the ambitious version does not fit a master's timeline.
- Yes/no questions are fine for confirmatory studies. For exploratory work prefer "to what extent" or "how".

## Limitations

- The Novel column of FINER is an estimate until a literature search has been run.
- Feasibility is assessed from the constraints the user states; unstated obstacles such as ethics timelines are not known.
- The frameworks suit empirical studies. Purely theoretical or design-science work needs the question adapted by hand.

## Troubleshooting

| Problem | Likely cause | Solution |
|---|---|---|
| The question still cannot be answered with data | It asks "how can we improve" or contains an undefined term | Name the variables and the comparison, and define each term with how it will be measured |
| The question does not fit PICO | The study is qualitative or computational | Switch to SPIDER, or to the task, method, baseline, metric, setting form |
| Hypotheses cannot be written | The study is exploratory | Do not force them; state a central question with sub-questions and say the study is exploratory |

## Related skills

- `research-gap-finder` supplies the gap this question addresses.
- `novelty-checker` verifies the Novel column.
- `methodology-designer` and `experiment-planner` design the study that answers the question.
- `sample-size-power-calculator` uses the hypotheses and expected effect size.
- `phd-research-proposal-writer` and `grant-proposal-writer` take the questions and objectives as input.
