---
name: paper-to-slides
description: "Turns a research paper into a talk: slide-by-slide outline with one message per slide, visuals, timed speaker notes, and backup slides. Use for conference or defence talks. Not for posters."
version: 1.0.0
metadata:
  author: "Yash Kavaiya <yash.kavaiya3@gmail.com>"
  tags: [presentation, slides, conference-talk, beamer]
---

# Paper to Slides

Design the talk first and the slides second. A talk carries one main idea and enough evidence to make the audience want to read the paper.

## Purpose

Design a talk that carries one main idea and enough evidence to make the audience want to read the paper, then produce the slides and timed notes. The talk is planned first; the paper's section order is followed only where it serves the story.

## When to use

- A conference, workshop, seminar, lab-meeting, or defence talk about the user's paper.
- A journal-club presentation of someone else's paper.
- Shortening or restructuring an existing deck.

Hand off instead for a poster (`paper-to-poster`), a video script (`paper-to-explainer-video`), or defence question practice (`viva-defense-prep`).

## Prerequisites

- The paper and its figures as separate image or vector files.
- The slot length, question time, and audience.
- A slide tool for the build: LaTeX Beamer, PowerPoint, or a Markdown slide framework, plus any required template.

## Inputs

- The paper, with its figures and tables as files.
- The slot: total minutes, and how many are reserved for questions.
- The audience: specialists in the subfield, the broader field, or mixed.
- Output format and any required template (the conference's, the university's). If the session offers a dedicated slide or deck tool, use it for the build.
- For a journal club: the user's own assessment of the paper.

## Instructions

1. **Set the budget.** Roughly one content slide per minute of speaking time, fewer for dense slides. A 12-minute talk plus 3 for questions is 10 to 12 slides. Lightning talks (3 to 5 minutes) get 3 to 5 slides and one result.
2. **Write the takeaway**: the single sentence the audience should remember. Then choose the two or three results that support it. Everything else in the paper stays in the paper.
3. **Plan the arc** and allocate time:

   | Part | Share of time | Content |
   |---|---|---|
   | Hook and problem | 15% | Why this matters, with a concrete example |
   | Gap | 10% | What existing approaches cannot do |
   | Key idea | 20% | The approach, as a picture, at the level of intuition |
   | Evidence | 35% | Two or three results, one per slide |
   | Limits and implications | 10% | What it does not show; what it enables |
   | Close | 10% | Takeaway, link to paper and code, contact |

4. **Outline slide by slide.** For each slide write: an assertion title (a full sentence stating the slide's point, such as "Pretraining on synthetic data halves the labelling needed"), the visual that supports it, and the notes. Topic titles like "Results" waste the most-read line on the slide.
5. **Rebuild figures for projection.** Paper figures are too dense and too small. Show one comparison per slide, enlarge fonts to at least 18 to 20 pt on the slide, highlight the series under discussion, and reveal complex figures in steps. Regenerate from data where possible (`publication-figure-maker`); replace tables with a chart or a three-row extract.
6. **Keep text minimal**: at most about 6 lines or 30 words per slide, no full paragraphs, and equations only when they are the point, with every symbol explained aloud.
7. **Write speaker notes** for each slide: what to say, in spoken sentences, with the transition to the next slide. Total the notes at about 130 words per minute and check them against the slot.
8. **Prepare backup slides** after the final slide: extra experiments, ablations, proofs, dataset details, limitations, and answers to the likely questions (from `self-peer-reviewer` or the actual reviews).
9. **Build the deck** in the requested format, using the supplied template. Number the slides. Check contrast, colour-blind-safe colours, and readability from the back of a room.
10. **Rehearsal plan**: time a run-through, mark the slide where the midpoint should fall, and identify what to drop if time runs short.

## Output format

```markdown
# Talk: <title> (<N> min + <Q> min questions, <audience>)
Takeaway: <one sentence>

| # | Time | Slide title (assertion) | Visual | Notes summary |
|---|---|---|---|---|
| 1 | 0:00 | <Title, authors, venue> | | |
| 2 | 0:30 | <Problem stated as a claim> | photo or example | ... |

## Speaker notes
### Slide 2
<spoken text, ~100 words>

## Backup slides
B1. ...

## Cut list if short on time
```

Then the deck itself: Beamer `.tex`, `.pptx`, or Markdown for Marp, reveal.js, or Quarto.

## Examples

Requests that should trigger this skill:

- "Make slides from my paper for a 12-minute conference talk."
- "Prepare a 20-minute seminar on my thesis chapter."
- "Turn this paper into a journal club presentation."
- "Write speaker notes for my slides."
- "My deck has 40 slides for a 15-minute talk. Cut it down."

Requests that belong to another skill:

- "Design a poster for my paper." → use `paper-to-poster`
- "Write a video script explaining my paper." → use `paper-to-explainer-video`
- "Practise questions for my defence." → use `viva-defense-prep`

### Worked example

**Request:** "12-minute talk plus 3 minutes of questions at an NLP workshop on my paper about tokenizer-free models for code-mixed text. Beamer."

**What the agent does:**

1. Budgets 11 slides and writes the takeaway sentence.
2. Chooses two results and plans the arc with time per part.
3. Outlines each slide with an assertion title, one visual, and notes; rebuilds the main table as a bar chart.
4. Writes speaker notes, totals them at about 130 words per minute, and adds four backup slides.

**Result (excerpt):**

```markdown
| # | Time | Slide title (assertion) | Visual |
|---|---|---|---|
| 2 | 0:30 | Half of informal Hindi text online mixes in English | two example messages |
| 4 | 2:30 | Subword tokenizers split the same romanised word five different ways | token split diagram |
| 7 | 6:30 | Dropping the tokenizer improves F1 by 3.1 points on two benchmarks | bar chart from Table 2 |

### Slide 7 notes (about 90 words)
"Here is the main result. On both benchmarks the character-level model is ahead of mBERT, by 3.1 points on average..."
```

## Quality bar and pitfalls

- Use only results and figures from the paper. Do not add numbers, simplify a result into something the paper does not show, or drop the caveat that changes its meaning.
- The talk is not the paper read aloud. Cutting material is the main work; follow the paper's section order only when it serves the story.
- One message per slide. A slide with three charts has no message.
- Do not put on a slide what the speaker will not explain.
- Related work is a sentence or one slide in a short talk, unless positioning is the point.
- Respect the time. Running over costs the question period, which is where interest is expressed.
- Credit images and data from others on the slide where they appear.
- For a journal club, separate the authors' claims from the presenter's critique, and say which is which.
- Compile or open the deck and look at every slide before delivering it. Report if it could not be rendered.

## Limitations

- The deck contains only what the paper supports; it does not add results or demonstrations.
- Timing is estimated from word counts and must be confirmed by rehearsal.
- Rendering can be checked only where the slide tool is available; otherwise the source is delivered unrendered and labelled so.
- Design polish (animations, branding) beyond a clean template is outside the scope.

## Troubleshooting

| Problem | Likely cause | Solution |
|---|---|---|
| The talk runs over time | Too many slides or dense notes | Cut a result, not the pace; apply the cut list and keep one message per slide |
| Figures are unreadable when projected | Paper figures were pasted in | Rebuild them with larger fonts and one comparison each using `publication-figure-maker` |
| Beamer fails to compile | A fragile frame, missing package, or invalid figure path causes an error | Add `[fragile]` to frames with verbatim content and check paths; compile after each fix |
| The audience is outside the subfield | The deck assumes specialist background | Add one slide of background and define each term when first used |

## Related skills

- `paper-summarizer` to extract the core of the paper, especially for a journal club.
- `paper-critic` for the critique section of a journal-club talk.
- `publication-figure-maker` and `architecture-diagram-maker` to rebuild visuals for projection.
- `paper-to-poster` and `paper-to-explainer-video` for other formats of the same story.
- `viva-defense-prep` for the question session after a defence talk.
- `self-peer-reviewer` to predict questions for the backup slides.
