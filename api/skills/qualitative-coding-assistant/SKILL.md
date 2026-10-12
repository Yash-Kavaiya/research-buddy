---
name: qualitative-coding-assistant
description: "Supports thematic analysis of interviews and open-ended responses: coding with verbatim excerpts, a codebook, themes, and write-up. Use when analysing qualitative text. Not for statistics."
version: 1.0.0
metadata:
  author: "Yash Kavaiya <yash.kavaiya3@gmail.com>"
  tags: [qualitative-research, thematic-analysis, coding, interviews]
---

# Qualitative Coding Assistant

Help the researcher code qualitative data systematically. Every code is anchored to exact words in the data, and the researcher makes the interpretive decisions.

## Purpose

Help a researcher code qualitative material systematically, with every code anchored to exact words from a named participant and location. The assistant produces a first pass and an audit trail; the researcher makes the interpretive decisions.

## When to use

- Interview or focus-group transcripts, field notes, documents, or free-text survey answers need analysing.
- A codebook must be built or applied.
- Themes need developing, reviewing, or writing up.

Hand off instead for the choice of qualitative design (`methodology-designer`) or the interview guide (`survey-questionnaire-designer`).

## Prerequisites

- Transcripts or responses with participant identifiers and line or turn numbers.
- Confirmation that the material is anonymised and that the ethics approval and consent allow processing with an AI tool.
- The research question and the chosen approach (reflexive thematic analysis, codebook, framework, grounded theory, or content analysis).

## Inputs

- The data, with participant identifiers (P01, P02) and line or turn numbers. Add them if absent.
- The research question.
- The approach: reflexive thematic analysis (Braun and Clarke), codebook or template analysis, framework analysis, grounded theory coding (open, axial, selective), or content analysis. If undecided, explain the choice and recommend one.
- Inductive (codes from the data), deductive (codes from a theory or framework the user supplies), or both.
- Confidentiality terms from the ethics approval.

**Check confidentiality first.** Ask whether the transcripts are anonymised and whether the ethics approval and consent allow processing with an AI tool. If names, places, or employers remain, replace them with placeholders before analysis.

## Instructions

1. **Familiarise.** Read each transcript fully. Write a short memo per transcript: what stands out, and first impressions marked as impressions.
2. **Code a first subset** (2 or 3 transcripts) line by line. For each meaningful segment record: participant, location, the verbatim excerpt, a short code, and a note. Codes describe what is in the segment (semantic) or what underlies it (latent); say which.
3. **Draft the codebook** from the first pass: code name, definition, when to apply, when not to apply, and an example excerpt. Merge duplicates and split codes that cover different ideas.
4. **Review the codebook with the researcher** before coding the rest. Their knowledge of the context and the participants shapes the codes.
5. **Code the remaining data** with the codebook. Add new codes when the data requires it, record when each was added, and recheck earlier transcripts for it.
6. **Check consistency.** When two coders are involved (the researcher and the assistant, or two researchers), compare on a sample, discuss disagreements, and refine definitions. Compute Cohen's kappa only when the approach calls for it (codebook and content analysis); reflexive thematic analysis treats coder subjectivity as a resource and does not use inter-rater reliability.
7. **Develop themes.** Group codes into candidate themes. A theme is a pattern of shared meaning organised around a central idea, not a topic heading or an interview question. Write a one-sentence central idea per theme.
8. **Review themes** against the coded excerpts and against the whole dataset: does each theme hold together, is it distinct from the others, and does it answer the research question? Look for negative cases that contradict it, and keep them.
9. **Define and name themes**, with sub-themes where useful, and build a thematic map.
10. **Write up**: each theme with its analytic claim, two or three quotes from different participants, and interpretation linked to the question and the literature. Report how many participants contributed to each theme without turning it into statistics.
11. **Keep an audit trail**: codebook versions, memos, and decisions.

## Output format

```markdown
## Coded excerpts
| ID | Participant | Location | Excerpt (verbatim) | Code(s) | Note |
|---|---|---|---|---|---|
| 14 | P03 | lines 88–91 | "I stopped asking because nobody ever answered" | Unanswered requests | withdrawal from help-seeking |

## Codebook (v2)
| Code | Definition | Apply when | Do not apply when | Example | Count (participants) |

## Themes
### Theme 1: <name>
Central idea: ...
Codes: ...
Evidence: P03 (88–91), P07 (12–15), P11 (140–144)
Negative cases: P05 (60–63)

## Thematic map
## Memos and decisions
## Draft findings section
```

Deliver the coded-excerpt table as CSV as well, so it can be imported into NVivo, ATLAS.ti, MAXQDA, or a spreadsheet.

## Examples

Requests that should trigger this skill:

- "Code these interview transcripts and find the themes."
- "Do a thematic analysis of 12 interviews about remote teaching."
- "Build a codebook from these two transcripts."
- "Analyse 300 open-ended survey answers about campus safety."
- "Review my themes using Braun and Clarke's approach."

Requests that belong to another skill:

- "Run a t test on my survey scores." → use `statistical-test-selector`
- "Write the interview guide." → use `survey-questionnaire-designer`
- "Which qualitative design should I use?" → use `methodology-designer`

### Worked example

**Request:** "Here are three anonymised interview transcripts (P01 to P03) with nurses about night shifts. Start coding inductively for my question: how do nurses cope with fatigue?"

**What the agent does:**

1. Confirms anonymisation and consent terms, then reads each transcript fully and writes a memo.
2. Codes line by line, recording participant, location, verbatim excerpt, code, and note.
3. Drafts a codebook with definitions and examples and asks the researcher to review it.
4. Proposes candidate themes with their central ideas and negative cases.

**Result (excerpt):**

```markdown
| ID | Participant | Location | Excerpt (verbatim) | Code(s) | Note |
|---|---|---|---|---|---|
| 7 | P02 | lines 41–43 | "We cover for each other, twenty minutes each, nobody writes it down" | Informal rest swaps | collective, unofficial |
| 12 | P03 | lines 88–90 | "I just drink coffee till four and hope nothing happens" | Stimulant reliance | individual coping |

Candidate theme: Coping is organised by the team, not the employer. Central idea: rest is arranged informally among colleagues. Negative case: P01 (lines 20–24) reports no such arrangement.
```

## Quality bar and pitfalls

- Quotes are verbatim and traceable to a participant and location. Never compose, merge, or "tidy" a quote, and never attribute one to the wrong participant. Mark any trimming with [...].
- Do not report themes that the data does not contain. If there is not enough data for a theme, say so.
- The assistant's coding is a first pass. The researcher must review it; say this, and recommend that AI assistance be reported in the methods.
- Themes do not "emerge". They are developed by the analyst; write it that way.
- A theme summarising answers to one interview question is a topic summary. Look for the meaning across questions.
- Do not quantify beyond what the design supports ("most participants" needs counting; percentages from 12 interviews mislead).
- Keep contradicting cases. They strengthen the analysis.
- Do not paste identifiable data into tools or outputs beyond what the ethics approval covers.

## Limitations

- The assistant's coding is a first pass that reflects the text alone. It lacks the researcher's knowledge of context, tone, and setting.
- Themes drawn from a few transcripts are provisional until the rest are coded.
- The analysis cannot be more trustworthy than the transcripts; errors in transcription carry through.
- Use of an AI tool in analysis should be reported in the methods and must be permitted by the ethics approval.

## Troubleshooting

| Problem | Likely cause | Solution |
|---|---|---|
| Transcripts contain names or identifying details | Anonymisation is incomplete | Stop, replace identifiers with placeholders, and confirm the ethics terms before continuing |
| Themes mirror the interview questions | Topic summaries were produced instead of patterns of meaning | Regroup codes across questions and write a central idea for each theme |
| A quote cannot be found in the transcript | It was paraphrased or merged | Treat it as an error: replace it with the exact words and location, or remove it |
| Two coders disagree often | Code definitions are ambiguous | Refine the definitions with apply and do-not-apply rules and recode a sample |

## Related skills

- `methodology-designer` for the qualitative approach and trustworthiness strategy.
- `survey-questionnaire-designer` for the interview guide that produced the data.
- `ethics-irb-drafter` for the confidentiality terms that govern this work.
- `results-interpreter` and `thesis-chapter-writer` to write the findings chapter.
- `experiment-logger` can hold the audit trail of coding decisions.
