---
name: literature-review-writer
description: "Writes a literature review organized by themes, debates, and gaps, with claims tied to supplied or retrieved sources. Use for review chapters and articles. Not for a short related-work section."
version: 1.0.0
metadata:
  author: "Yash Kavaiya <yash.kavaiya3@gmail.com>"
  tags: [literature-review, synthesis, academic-writing]
---

# Literature Review Writer

Write a review that argues something about the state of knowledge. Each paragraph makes a point about the literature and uses several sources to support it.

## Purpose

Produce a review that argues something about the state of knowledge: what is established, what is contested, and what is unknown. Each paragraph makes a point about the literature and supports it with several sources, ending at the gap the user's study addresses.

## When to use

- A thesis literature-review chapter, a review article, or an extended background section.
- Restructuring a paper-by-paper draft into a synthesis.

Hand off instead for a short related-work section positioned against a specific contribution (`related-work-writer`), a protocol-driven review (`systematic-review-prisma`), or annotated entries (`annotated-bibliography-builder`).

## Prerequisites

- The sources: PDFs, notes, summaries, a `.bib` file, or a comparison matrix. Without sources, build the corpus first with `paper-search`.
- The research question the review leads to, plus length and citation style.
- No scripts or API keys are required.

## Inputs

- The sources: PDFs, notes, summaries, a `.bib` file, or a comparison matrix. If there are none, build the corpus first with `paper-search`.
- The review's purpose and the research question it leads to.
- Length, citation style, and audience (examiner, journal reader, general).
- The user's own position, if they have one. The review should build toward their study.

## Instructions

1. **Inventory the sources.** List each with a one-line note on what it contributes. Mark which were read in full, which only as abstracts, and which the user summarised.
2. **Build a synthesis matrix.** Rows are sources; columns are the themes, variables, or questions that recur. Fill cells with each source's finding or position. `paper-comparison-matrix` produces this.
3. **Find the structure in the matrix.** Choose one organising principle:
   - *Thematic*: by concept or sub-question (the default).
   - *Methodological*: by approach, when the methods are the debate.
   - *Chronological*: by period, only when the development of ideas is itself the point.
   - *Theoretical*: by framework or school.
4. **Outline with claims, not topics.** Each section heading gets a one-sentence claim about the literature ("Evidence for X is consistent in adults and absent in adolescents"). Show the outline to the user before drafting long reviews.
5. **Draft each paragraph** in this shape:
   - Topic sentence stating the point about the literature.
   - Evidence from two or more sources, compared: who agrees, who differs, and why (sample, method, measure, context).
   - Your evaluation: strength of evidence, limitations shared across the studies.
   - A link to the next point or to the gap.
6. **Write the transitions between sections** so the review moves from broad context to the specific gap.
7. **Close with the gap.** Summarise what is established, what is contested, and what is unknown, then state the gap the user's study addresses and how.
8. **Check every citation** against the source: does the cited paper say this? Then run `citation-verifier` on the finished text.

## Output format

```markdown
# Literature Review: <topic>

## 1. Introduction
Scope, how sources were found and selected, and how the review is organised.

## 2. <Theme stated as a claim>
Synthesised paragraphs with citations (Author, Year) or [n].

## 3. <Theme>
### 3.1 <Sub-theme>

## N. Summary and research gap
Established / contested / unknown, then the gap and the study that follows.

## References
```

Also deliver the synthesis matrix, and a list of claims you could not support from the supplied sources.

## Examples

Requests that should trigger this skill:

- "Write a literature review on remote work and employee wellbeing from these 25 papers."
- "Help me write chapter 2 of my thesis."
- "My review reads like a list of summaries. Restructure it by theme."
- "Synthesize these notes into a review section."
- "Turn this comparison matrix into a thematic literature review."

Requests that belong to another skill:

- "Write the related work section for my conference paper." → use `related-work-writer`
- "Run a PRISMA systematic review." → use `systematic-review-prisma`
- "Write annotations for each source." → use `annotated-bibliography-builder`

### Worked example

**Request:** "Here are 18 papers on gamification in university courses. Write a 1,200-word literature review for my thesis on gamified statistics teaching."

**What the agent does:**

1. Inventories the sources and notes which were read in full.
2. Builds a synthesis matrix with themes: engagement, learning outcomes, design elements, duration of effects.
3. Outlines sections as claims and confirms the outline with the user.
4. Drafts each paragraph as point, compared evidence, evaluation, and link to the gap; lists two statements that still need a source.

**Result (excerpt):**

```markdown
## 2.2 Engagement gains are consistent, learning gains are not
Across the reviewed studies, gamified courses report higher participation than conventional ones (Author A, 2019; Author B, 2021; Author C, 2022). Evidence for improved grades is mixed: two controlled studies found gains (Author B, 2021; Author D, 2020), while three found none (Author E, 2018; ...). The studies reporting gains ran for a full semester, whereas the null results came from interventions of four weeks or less, which suggests duration moderates the effect.

[citation needed]: claim that novelty effects fade after six weeks
```

## Quality bar and pitfalls

- Cite only sources that were supplied or retrieved, and only for what they say. Never invent a reference or attach a real one to a claim it does not make. Mark unsupported statements `[citation needed]` for the user to resolve.
- Paragraphs that begin "Smith (2020) found ... Jones (2021) found ..." are summaries. Start with the idea and bring authors in as evidence.
- Compare and evaluate. A review that only reports is incomplete.
- Explain disagreements between studies by their differences in design or context where the sources allow it.
- Do not present a source you read only as an abstract as if you knew its methods.
- Keep direct quotation rare, and keep paraphrases far enough from the source wording (`plagiarism-and-paraphrase-checker`).
- Balance recency and foundations: include the seminal work and the last two years.
- Use one tense convention: past for specific findings, present for established knowledge.

## Limitations

- The review can only be as complete as the sources supplied or retrieved. It does not certify that the literature has been covered exhaustively.
- Claims drawn from sources read only as abstracts are less reliable and are marked.
- The synthesis is a draft for the researcher to check against the sources and revise in their own voice.

## Troubleshooting

| Problem | Likely cause | Solution |
|---|---|---|
| The draft still reads paper by paper | It was written from summaries instead of from the matrix | Rebuild from the synthesis matrix and start each paragraph with a claim about the literature |
| A statement has no supporting source | The corpus lacks a paper for it | Mark it `[citation needed]`, search with `paper-search`, or remove the statement |
| Citation checks fail afterward | A reference was attached to a claim it does not make | Run `citation-verifier`, reread the source, and correct or drop the claim |

## Related skills

- `paper-search` and `citation-graph-explorer` to build the corpus.
- `paper-summarizer` and `paper-comparison-matrix` to prepare the synthesis matrix.
- `research-gap-finder` to sharpen the closing gap statement.
- `related-work-writer` for the short, contribution-focused version.
- `citation-verifier` and `plagiarism-and-paraphrase-checker` before submission.
- `thesis-chapter-writer` when the review is a thesis chapter.
- `academic-tone-editor` for a final language pass.
