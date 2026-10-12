---
name: survey-questionnaire-designer
description: "Designs questionnaires and interview guides: constructs mapped to items, response scales, wording checks, and a pilot plan. Use when building a research instrument. Not for analysing responses."
version: 1.0.0
metadata:
  author: "Yash Kavaiya <yash.kavaiya3@gmail.com>"
  tags: [survey, questionnaire, likert, interview-guide]
---

# Survey and Questionnaire Designer

## Purpose

Build an instrument in which every item measures something the research question needs, and plan how its validity and reliability will be shown. Validated scales are preferred over new items, and new or adapted scales are labelled as such.

## When to use

- A new questionnaire, an adaptation of an existing scale, or a semi-structured interview guide.
- Reviewing a draft survey for wording and structure problems.

Hand off instead for the choice of design (`methodology-designer`), the sample size (`sample-size-power-calculator`), or analysing responses (`statistical-test-selector`, `qualitative-coding-assistant`).

## Prerequisites

- The research questions and the constructs to measure.
- A description of the respondents, the mode of delivery, and a length limit.
- Access to `paper-search` to look for validated scales and their reported reliability.

## Inputs

- Research questions and the constructs to measure.
- Respondents: who they are, language, literacy, how they will be reached.
- Mode: online, paper, phone, face to face.
- Length limit (aim for under 10 to 12 minutes online) and any existing instruments the user knows of.

## Instructions

1. **List the constructs** from the research questions and define each one. For every construct record its dimensions and the source of the definition.
2. **Search for validated scales first.** Check with `paper-search` whether an established instrument exists (for example SUS for usability, TAM items for technology acceptance, PHQ-9 for depression, NASA-TLX for workload). Using or adapting a validated scale is stronger than writing a new one. Record the scale's source, its reported reliability, and its licence or permission terms; some scales require permission or a fee.
3. **Build the blueprint**: a table of construct, dimension, item, source (adopted, adapted, new), and scale. Aim for 3 to 5 items per dimension for multi-item scales. Any item that maps to no construct is cut.
4. **Write or adapt the items.** Rules:
   - One idea per item. Split "The system is fast and easy to use".
   - Plain words, no jargon, under about 20 words.
   - No leading wording ("How helpful was our excellent support?"), no loaded terms.
   - No double negatives. Use reverse-worded items sparingly and mark them for reverse scoring.
   - A specific time frame where behaviour is asked about ("in the past 7 days").
   - Response options that are exhaustive and mutually exclusive, with "Not applicable" or "Prefer not to say" where needed.
5. **Choose response scales.** Likert agreement with 5 or 7 points, all points labelled, same direction throughout. Use frequency or quality anchors when the item is not an agreement statement. Keep one scale format per block.
6. **Order the questionnaire**: information and consent, screening questions, easy and engaging items first, grouped by topic, sensitive items late, demographics last. Add an attention check for long online surveys and disclose it in the methods.
7. **Plan validity and reliability:**
   - Content validity: review by 3 to 5 experts; compute a content validity index if the field expects it.
   - Face validity and comprehension: cognitive interviews with 5 to 8 people from the target group.
   - Pilot: 20 to 30 respondents or more; check completion time, missing data, floor and ceiling effects, item variance.
   - Reliability: Cronbach's alpha or McDonald's omega per scale (0.70 or above is the usual threshold), item-total correlations.
   - Construct validity: exploratory factor analysis for new scales (plan about 5 to 10 respondents per item), confirmatory analysis in a second sample when possible.
8. **For translated instruments**, plan forward and back translation and a comprehension check.
9. **For interview guides**: 6 to 10 open main questions, each with probes; no yes/no or leading questions; an opening warm-up and a closing "anything else".
10. **Deliver** the instrument, the blueprint, the scoring key, and the validation plan.

## Output format

```markdown
## Blueprint
| Construct | Dimension | Item ID | Item | Source | Scale | Reverse |

## Questionnaire
### Information and consent
### Section A: <topic>
A1. <item>   ( ) Strongly disagree ( ) Disagree ( ) Neutral ( ) Agree ( ) Strongly agree

### Demographics

## Scoring key
- <Scale>: mean of A1 to A5; A3 reverse-scored.

## Validation and pilot plan
| Step | Who | n | Criterion |

## Notes for the methods section
```

## Examples

Requests that should trigger this skill:

- "Design a questionnaire to measure job satisfaction among remote workers."
- "Write Likert-scale items for technology acceptance of a learning app."
- "Review my survey for leading or double-barrelled questions."
- "Create a semi-structured interview guide on patients' experience of telehealth."
- "How do I validate my questionnaire?"

Requests that belong to another skill:

- "Which test do I use on my survey results?" → use `statistical-test-selector`
- "Code my open-ended responses." → use `qualitative-coding-assistant`
- "Draft the consent form for my survey." → use `ethics-irb-drafter`

### Worked example

**Request:** "I need a short questionnaire on students' acceptance of an AI tutoring app: perceived usefulness, ease of use, and intention to use. Online, under 8 minutes."

**What the agent does:**

1. Defines the three constructs and searches for validated technology-acceptance scales.
2. Builds a blueprint mapping each construct to adapted items with their source.
3. Rewrites items to one idea each, sets a 5-point fully labelled agreement scale, and orders the sections.
4. Plans expert review, cognitive interviews, a pilot, and reliability analysis.

**Result (excerpt):**

```markdown
| Construct | Item ID | Item | Source | Scale |
|---|---|---|---|---|
| Perceived usefulness | PU1 | Using the tutor helps me understand course material faster. | adapted from TAM (source to be cited after retrieval) | 1 Strongly disagree to 5 Strongly agree |
| Ease of use | EU1 | I find the tutor easy to use. | adapted | same |

Validation: 4 experts review content; 6 students do cognitive interviews; pilot n = 30; Cronbach's alpha per scale, target 0.70 or above. The adapted scale is not yet validated in this population.
```

## Quality bar and pitfalls

- Do not present a newly written scale as validated. It is validated only after the evidence is collected.
- Do not reproduce a copyrighted scale's items without confirming the terms. Give the citation and tell the user to obtain permission where required.
- Never invent reliability figures for an existing scale. Quote them from the retrieved source or say they need to be looked up.
- Changing item wording or the number of scale points alters a validated scale; report it as adapted and re-check reliability.
- Likert items are ordinal. Summed multi-item scales are commonly treated as interval; single items should not be.
- Collect only the demographics the analysis needs. Each extra personal item raises ethics and privacy cost.
- Every survey with human respondents needs ethics review and informed consent (`ethics-irb-drafter`).

## Limitations

- A new or adapted instrument is not validated until the planned evidence is collected. The skill cannot supply that evidence.
- Copyrighted scales cannot be reproduced without permission; only the citation and permission route are given.
- Reliability figures for existing scales are quoted only from retrieved sources and may not transfer to a new population or language.

## Troubleshooting

| Problem | Likely cause | Solution |
|---|---|---|
| An item measures two things | Double-barrelled wording | Split it into two items, one idea each |
| The questionnaire is too long | Items do not all map to a construct | Cut every item with no row in the blueprint, then the weakest items per scale |
| No validated scale exists for a construct | The construct is new or niche | Write new items, label them as new, and plan content validation and factor analysis |
| Pilot reliability fails (alpha below 0.70) | Items do not hang together or are misread | Inspect item-total correlations, revise or drop weak items, and re-pilot |

## Related skills

- `research-question-formulator` and `methodology-designer` for the constructs and design.
- `paper-search` to find validated scales.
- `sample-size-power-calculator` for the number of respondents.
- `ethics-irb-drafter` for consent and the ethics application.
- `statistical-test-selector` and `qualitative-coding-assistant` to analyse the responses.
