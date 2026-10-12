---
name: viva-defense-prep
description: "Prepares a candidate for a thesis viva or defence: likely examiner questions, answer outlines, mock sessions, and a final-week plan. Use before a viva or proposal defence. Not for making slides."
version: 1.0.0
metadata:
  author: "Yash Kavaiya <yash.kavaiya3@gmail.com>"
  tags: [viva, thesis-defense, oral-exam, phd]
---

# Viva and Defence Prep

Get the candidate ready to explain, justify, and defend their own work aloud. The preparation is built from their thesis, and the answers must be ones they understand and can give themselves.

## Purpose

Get a candidate ready to explain, justify, and defend their own work aloud. Questions are generated from the candidate's thesis and the examiners' interests, answers are outlined for the candidate to phrase themselves, and mock sessions give feedback.

## When to use

- A thesis viva or defence, at master's or doctoral level.
- A proposal defence, confirmation or upgrade review, qualifying exam, or pre-submission seminar.
- A job talk or conference question session about the candidate's research.

Hand off instead for the defence slides (`paper-to-slides`) or for a critique of the thesis as a document (`self-peer-reviewer`).

## Prerequisites

- The thesis or proposal, ideally in full.
- The examination format and regulations of the university, and the examiners' names and fields if known.
- The candidate's own list of worries and the time until the examination.

## Inputs

- The thesis or proposal, in full if possible; at least the abstract, contributions, methodology, and conclusions.
- The exam format: country and institution conventions (closed viva with two examiners, public defence with a committee, presentation length), duration, and possible outcomes.
- The examiners' names and fields, if known.
- The candidate's own list of what worries them.
- Time until the exam.

## Instructions

1. **Establish the format** from the university's regulations and the supervisor: who examines, how long, whether there is a presentation, and what outcomes are possible.
2. **Read the thesis as an examiner would.** Note the claimed contributions, every methodological choice, the weakest evidence, anything unusual, and any inconsistency between chapters.
3. **Generate questions in the standard categories**, specific to this thesis and referring to its chapters and figures:

   | Category | Examples |
   |---|---|
   | Opening | Summarise your thesis in three minutes. What is your main contribution? Why this topic? |
   | Contribution and originality | What do we know now that we did not before? How does it differ from <closest work>? |
   | Literature | Which works most influenced you? What has appeared since you submitted? Why did you not engage with <school or author>? |
   | Methodology | Why this design and not <alternative>? How did you choose the sample, dataset, or parameters? What threatens validity? |
   | Results | Walk me through Figure X. Is this difference meaningful? What surprised you? How do you explain <anomalous result>? |
   | Limitations | What is the weakest part? What would you do differently? How far do the findings generalise? |
   | Implications | Who should care? What follows for practice or theory? |
   | Future work | What is the next study? What would you do with three more years? |
   | Ownership | Which parts were your own work in the co-authored chapters? Explain how you implemented <component>. |
   | Fundamentals | Define <core concept>. Derive or explain <basic result your method relies on>. |

4. **Predict examiner-specific questions.** Look up each examiner's recent work (`paper-search`) and note where their methods, theories, or findings touch the thesis. Examiners ask from their own expertise, and it is reasonable to expect their relevant papers to be cited.
5. **Mark the hard questions**: the ones aimed at real weaknesses. Prepare these most.
6. **Outline answers with the candidate.** For each question give bullet points drawn from the thesis with chapter and page pointers, and have the candidate say the answer in their own words. A useful structure: answer directly in one sentence, give the reasoning or evidence, acknowledge the limit, and stop.
7. **Teach the handling techniques:**
   - Pause before answering; ask for clarification of an unclear question.
   - For a real weakness: agree it is a limitation, explain the reason for the choice, say what effect it has on the conclusions, and what would address it. Defend the reasoning; do not deny the weakness.
   - When you do not know: say so, then reason aloud about how you would find out.
   - When the examiner is right: concede and note it as a correction.
   - Keep answers to one or two minutes unless asked to expand.
8. **Run mock sessions.** Ask one question at a time, wait for the candidate's answer, then give feedback on content, structure, and length, with follow-up questions as an examiner would press. Increase difficulty across rounds. Record recurring problems.
9. **Prepare the opening presentation** if required: contributions-first, timed to the slot (`paper-to-slides`), and the three-minute spoken summary regardless.
10. **Plan the final week**: reread the thesis and mark it with tabs; list typos and errors found, to bring as a corrections sheet; reread key references and check for new publications in the area; rehearse the summary aloud; settle logistics.

## Output format

```markdown
# Defence preparation: <thesis title>
Format: <examiners, duration, presentation>. Date: ...

## Three-minute summary (outline for you to say in your own words)
## Question bank
### Likely (prepare all)
| # | Question | Category | Answer points (thesis location) |
### Hard (prepare most carefully)
### Examiner-specific
| Examiner | Their relevant work | Likely questions |

## Weak points and how to discuss them
| Weakness | Why the choice was made | Effect on conclusions | What would fix it |

## Mock session log
| Round | Question | Feedback | To improve |

## Final-week checklist
```

## Examples

Requests that should trigger this skill:

- "Prepare me for my PhD viva next month."
- "What questions will examiners ask about my thesis?"
- "Run a mock defence with me."
- "How do I answer questions about the limitations of my study?"
- "Help me prepare for my proposal defence."

Requests that belong to another skill:

- "Make the slides for my defence talk." → use `paper-to-slides`
- "Review my thesis as a document." → use `self-peer-reviewer`
- "Write my thesis corrections." → use `thesis-chapter-writer`

### Worked example

**Request:** "My viva is in three weeks: thesis on machine learning for crop disease detection from phone photos, two examiners, one from agronomy and one from computer vision. Start with likely questions."

**What the agent does:**

1. Establishes the format and reads the thesis as an examiner would.
2. Generates questions by category, tied to chapters and figures.
3. Looks up each examiner's recent work and predicts examiner-specific questions.
4. Outlines answer points with page pointers and starts a mock session, one question at a time.

**Result (excerpt):**

```markdown
| # | Question | Category | Answer points (thesis location) |
|---|---|---|---|
| 3 | Why did you collect photos in one season only? | Methodology | funding window (Section 3.2); effect: no seasonal variation (limitation, Section 7.1); what would fix it |
| 9 | Walk me through Figure 5.4. | Results | axes; what the gap at low light shows; link to Section 5.3 |

Mock feedback, question 3: the answer defended the choice but did not state the consequence. Add one sentence on what the single season means for generalisation, then stop.
```

## Quality bar and pitfalls

- Answers come from the candidate's thesis and understanding. Do not write polished answers to memorise; examiners detect recitation and follow-up questions break it. Give points and have the candidate phrase them.
- Do not invent content the thesis does not contain, or supply justifications for choices the candidate did not make. Ask them why they made each choice.
- Predicted questions are probabilities. Tell the candidate that unexpected questions will come and that the skill being practised is reasoning aloud about their own work.
- Do not advise evasion or bluffing. Admitting a limit and reasoning about it is the answer examiners respect.
- Check examiner facts from retrieved sources; do not attribute papers or views to an examiner from memory.
- Be honest in feedback. If an answer is weak or the candidate cannot explain a part of their thesis, say so now, while there is time to fix it.
- Formats and outcomes differ by country and institution. Take them from the regulations, not from general knowledge.
- Preparation covers the whole thesis, including the early chapters written years ago.

## Limitations

- Predicted questions are probabilities; unexpected ones will come.
- Answer outlines come from the thesis. The candidate must phrase and own the answers; memorised text fails under follow-up.
- Examination formats and outcomes differ by institution and are taken from its regulations.
- Text-based mock sessions do not reproduce the pressure of speaking aloud to examiners.

## Troubleshooting

| Problem | Likely cause | Solution |
|---|---|---|
| The candidate cannot explain a part of the thesis | It was written long ago or by a co-author | Reread that chapter, re-derive the key step, and rehearse explaining it aloud |
| Answers run too long | No structure | Answer in one sentence, give the reasoning, acknowledge the limit, and stop |
| A question exposes a real weakness or an error | The thesis has a limitation or mistake | Agree, explain the choice, state its effect, and say what would address it; note errors on a corrections sheet |
| Examiner information is missing | Examiners are not yet announced | Prepare the standard categories and add examiner-specific questions once names are known |

## Related skills

- `self-peer-reviewer` and `paper-critic` to find the weaknesses examiners will find.
- `limitations-and-future-work-writer` for articulating limitations clearly.
- `paper-to-slides` for the opening presentation.
- `paper-search` and `citation-graph-explorer` to check examiners' work and recent publications.
- `math-and-equation-explainer` to rehearse explaining derivations aloud.
- `thesis-chapter-writer` for corrections after the defence.
- `research-progress-tracker` to schedule the preparation.
