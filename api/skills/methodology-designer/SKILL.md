---
name: methodology-designer
description: "Selects and justifies a quantitative, qualitative, or mixed research design with sampling, analysis, and validity plan. Use when planning a study or methodology chapter. Not for sample-size numbers."
version: 1.0.0
metadata:
  author: "Yash Kavaiya <yash.kavaiya3@gmail.com>"
  tags: [methodology, research-design, mixed-methods, validity]
---

# Methodology Designer

## Purpose

Choose a research design that can answer the question within the researcher's constraints, and justify each choice against the alternatives. The output is a design specification and, on request, the methodology section.

## When to use

- A study is being planned and the design is open.
- A methodology chapter or section must be written or defended.

Hand off instead for computational experiment details (`experiment-planner`), sample-size numbers (`sample-size-power-calculator`), or the instrument itself (`survey-questionnaire-designer`).

## Prerequisites

- The research questions and hypotheses. If they are vague, run `research-question-formulator` first.
- The field, and the user's constraints: time, budget, access to participants or data, and skills.
- No scripts or API keys are required.

## Inputs

- Research question(s) and hypotheses. If they are vague, run `research-question-formulator` first.
- Field and its norms.
- Constraints: time, budget, access to participants or data, equipment, skills, ethics limits.
- What already exists: datasets, instruments, pilot results.

## Instructions

1. **Classify the question.** The type of question drives the design:

   | Question asks | Family | Typical designs |
   |---|---|---|
   | Does X cause Y? | Quantitative, experimental | RCT, quasi-experiment, A/B test, controlled lab or computational experiment |
   | How much, how often, how related? | Quantitative, descriptive or correlational | Cross-sectional survey, cohort, case-control, secondary data analysis |
   | How or why do people experience X? | Qualitative | Phenomenology, grounded theory, case study, ethnography, narrative |
   | Both the pattern and the explanation | Mixed methods | Convergent, explanatory sequential (quant then qual), exploratory sequential (qual then quant) |
   | Does this artefact work? | Design science, engineering | Build and evaluate, benchmark study, simulation |

2. **State the stance briefly** when the field expects it: positivist or post-positivist, interpretivist, pragmatist. One paragraph, tied to the question.
3. **Compare two or three candidate designs** in a table: what each could answer, what it costs, its main threat to validity, and feasibility for this user. Recommend one.
4. **Specify the chosen design:**
   - *Population and sampling*: target population, sampling frame, method (random, stratified, purposive, snowball), and sample size with its basis (power analysis, or saturation for qualitative work).
   - *Variables or phenomena*: independent, dependent, control, and confounding variables with operational definitions; or the phenomenon and sensitising concepts.
   - *Data collection*: instruments, procedures, setting, timeline, pilot.
   - *Analysis*: the method for each research question, with software.
   - *Quality*: for quantitative work, internal, external, construct, and statistical-conclusion validity, and reliability. For qualitative work, credibility, transferability, dependability, and confirmability, with the technique used for each (triangulation, member checking, audit trail).
   - *Ethics*: consent, confidentiality, risk, data handling.
   - *Limitations and delimitations.*
5. **Build the alignment matrix**: each research question mapped to data source, instrument, and analysis. A row with a missing cell means the design cannot answer that question.
6. **Draft the methodology section.** Use the venue's or university's structure, with future tense for proposals and past tense for completed studies.

## Output format

```markdown
## Recommended design: <name>
Why this design: ...

## Alternatives considered
| Design | Answers the RQ? | Cost and time | Main validity threat | Verdict |

## Alignment matrix
| Research question | Data source | Instrument | Analysis |

## Design specification
### Population and sampling
### Variables and operational definitions
### Data collection procedure
### Analysis plan
### Validity and reliability (or trustworthiness)
### Ethical considerations
### Limitations and delimitations

## Open decisions and risks
```

Follow with the prose methodology section when asked.

## Examples

Requests that should trigger this skill:

- "Which methodology should I use to study why nurses leave the profession?"
- "Qualitative or quantitative for my research question?"
- "Design my study on the effect of flipped classrooms on maths scores."
- "Write the methodology chapter for my thesis."
- "Justify my choice of a mixed-methods design."

Requests that belong to another skill:

- "How many participants do I need?" → use `sample-size-power-calculator`
- "Design the questionnaire items." → use `survey-questionnaire-designer`
- "Plan my deep learning experiments." → use `experiment-planner`

### Worked example

**Request:** "I want to know why first-year engineering students drop out at my university. I have six months and access to student records and current students. Which design?"

**What the agent does:**

1. Classifies the question as explanatory (why) with an available quantitative pattern.
2. Compares a survey-only design, interviews only, and an explanatory sequential mixed design in a table.
3. Recommends the sequential design and specifies sampling, instruments, analysis, and validity for each strand.
4. Builds the alignment matrix and lists risks.

**Result (excerpt):**

```markdown
## Recommended design: explanatory sequential mixed methods
Phase 1 analyses records for all first-year students (2019 to 2024) to find which factors are associated with dropout. Phase 2 interviews 12 to 15 students, sampled purposively from the high-risk profiles found in phase 1, to explain the pattern.

| Research question | Data source | Instrument | Analysis |
|---|---|---|---|
| Which factors are associated with dropout? | student records | n/a | logistic regression |
| How do students explain leaving? | interviews | semi-structured guide | reflexive thematic analysis |

Integration point: phase 1 results select the interview sample and shape the guide.
```

## Quality bar and pitfalls

- Justify by fit to the question, not by preference or familiarity. Say why the rejected designs were rejected.
- Do not claim causation from a design that cannot support it. Correlational designs get correlational wording throughout.
- Mixed methods needs a reason and an integration point (where and how the strands are combined). Two unconnected studies are not mixed methods.
- Qualitative sample sizes are justified by saturation and depth, not power analysis.
- Convenience sampling is acceptable when stated as such with its consequence for generalisation.
- Cite methodological sources for the design (for example Creswell, Yin, Braun and Clarke) only after confirming the reference details.
- A design the user cannot execute in their time and access is the wrong design. Say so and scale it.

## Limitations

- The design is built on what the user reports about access and resources. Whether ethics approval or data access is granted is outside the skill's control.
- Field-specific conventions differ; a supervisor or methodologist should confirm the choice.
- Methodological references are suggested for citation only after their details are retrieved and verified.

## Troubleshooting

| Problem | Likely cause | Solution |
|---|---|---|
| No design answers every research question | The questions need different kinds of evidence | Use a mixed design with a stated integration point, or narrow the questions |
| The chosen design exceeds the time available | The scope is too large | Reduce sites, waves, or sample, or replace primary collection with secondary data, and state the consequence |
| The alignment matrix has an empty cell | A question has no data source or analysis | Add the missing element or drop the question; a design that fails to cover a question is invalid |

## Related skills

- `research-question-formulator` supplies the questions and hypotheses.
- `sample-size-power-calculator` for the quantitative sample size.
- `survey-questionnaire-designer` for instruments.
- `experiment-planner` for computational and lab experiments.
- `statistical-test-selector` and `qualitative-coding-assistant` for the analysis plan.
- `ethics-irb-drafter` for the ethics application.
- `thesis-chapter-writer` and `phd-research-proposal-writer` use the methodology section.
