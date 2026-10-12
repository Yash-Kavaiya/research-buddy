---
name: annotated-bibliography-builder
description: "Builds an annotated bibliography: a formatted citation plus summary, evaluation, and relevance note for each source. Use for coursework or proposal bibliographies. Not for synthesis across sources."
version: 1.0.0
metadata:
  author: "Yash Kavaiya <yash.kavaiya3@gmail.com>"
  tags: [annotated-bibliography, citations, reading-notes]
---

# Annotated Bibliography Builder

## Purpose

Produce entries that let a reader judge each source without opening it: what it says, how far to trust it, and what it is for in this particular project. Citations follow the required style exactly and every source is verified.

## When to use

- A coursework, proposal, or thesis-stage annotated bibliography.
- Organised reading notes before writing a review.

Hand off instead for synthesis across sources (`literature-review-writer`) or a single in-depth summary (`paper-summarizer`).

## Prerequisites

- The sources as PDFs, links, DOIs, or a `.bib` file, or a topic to search with `paper-search`.
- The project's research question, the citation style, and any word limit per annotation.
- Optional: pandoc for formatting citations from BibTeX.

## Inputs

- The sources: PDFs, links, DOIs, or a `.bib` file. If the user has only a topic, find sources with `paper-search` and confirm the selection.
- The project's research question, so relevance notes are specific.
- Citation style (APA 7, MLA 9, Chicago, IEEE, Harvard) and any length rule per annotation (commonly 100 to 200 words).
- Annotation type required: descriptive (summary only), evaluative (summary and assessment), or reflective (adds use in the project). Default: all three parts.
- Ordering: alphabetical by author (default), chronological, or grouped by theme.

## Instructions

1. **Verify the metadata** of each source against Crossref or the publisher page (`citation-verifier`): authors, year, title, venue, volume, pages, DOI.
2. **Read each source** to the depth its role needs. Record whether it was read in full or as an abstract.
3. **Write the citation** in the required style.
4. **Write the annotation** in three parts:
   - *Summary* (2 to 4 sentences): the question, the method or approach, and the main finding or argument.
   - *Evaluation* (1 to 3 sentences): source type and authority, strength of evidence, limitations, and how it compares with other sources in the list.
   - *Relevance* (1 to 2 sentences): what this source does for the user's project: background, method to adopt, evidence for a claim, a counter-position, or a gap it exposes.
5. **Keep a consistent voice and length.** Third person, present tense for what the source argues, past tense for what a study did.
6. **Add a tag line** when the list is long: theme, method, and a relevance rating (core, supporting, peripheral).
7. **Order and format** the list. For APA, the annotation is a new paragraph indented under a hanging-indent citation.
8. **Summarise the set**: coverage by theme and year, and what is missing.

## Output format

```markdown
# Annotated Bibliography: <project title>
Research question: ...
Style: APA 7. <N> sources.

Author, A. A., & Author, B. B. (2023). Title of the article. *Journal Name, 12*(3), 45–67. https://doi.org/...

> **Summary.** ...
> **Evaluation.** ...
> **Relevance.** ...
> *Tags: theme; method; core. Read: full text.*

(next entry)

## Coverage notes
| Theme | Sources | Gap |
```

Offer a `.bib` export with the annotation in the `annote` field when the user works in LaTeX.

## Examples

Requests that should trigger this skill:

- "Create an annotated bibliography in APA 7 for these ten sources."
- "Write 150-word annotations for my references on urban heat islands."
- "I need an annotated bibliography for my proposal on teacher burnout."
- "Annotate these papers with summary, evaluation, and relevance."
- "Make a reading list with notes on each paper's usefulness for my thesis."

Requests that belong to another skill:

- "Write a literature review from these sources." → use `literature-review-writer`
- "Summarise this single paper in depth." → use `paper-summarizer`
- "Convert my reference list to IEEE style." → use `citation-style-converter`

### Worked example

**Request:** "Annotated bibliography, APA 7, about 120 words each, for my project on whether green roofs reduce urban heat. Start with this DOI: 10.1016/j.example.2021.01.001."

**What the agent does:**

1. Verifies the metadata against Crossref before formatting.
2. Reads the source and records whether it was read in full.
3. Writes the APA citation, then summary, evaluation, and relevance.
4. Tags the entry by theme and method.

**Result (excerpt):**

```markdown
Author, A. A., & Author, B. B. (2021). Cooling effect of extensive green roofs in a temperate city. *Journal Name, 45*(2), 101–115. https://doi.org/...

> **Summary.** Measures roof-surface and air temperatures on 12 paired green and conventional roofs over two summers and finds lower surface temperatures on green roofs.
> **Evaluation.** A paired field design with two seasons of measurements; limited to one city and to extensive (shallow) roofs.
> **Relevance.** Provides the measured effect size this project will compare with simulation studies.
> *Tags: field measurement; core. Read: full text.*
```

## Quality bar and pitfalls

- Every entry is a real, verified source. Never fabricate an entry to reach a required count; say how many could be found.
- Do not annotate from the abstract and present it as a reading. Mark abstract-only entries.
- An annotation is not the abstract reworded. Write it in your own words and add evaluation.
- Evaluation needs a basis: sample size, design, venue, recency, whether findings were replicated. "A useful source" says nothing.
- Relevance must name the project. "Relevant to my topic" says nothing.
- Follow the style manual for the citation exactly (capitalisation, italics, DOI format). Mixed styles are the most common fault.
- Keep within the length rule. Markers count words.

## Limitations

- Only sources that can be retrieved and verified are included. If fewer exist than the assignment requires, the shortfall is reported.
- Evaluation of a source's quality is a reasoned judgement from its design and venue, not a formal appraisal score.
- Fine points of a citation style (unusual source types) should be checked against the official manual.

## Troubleshooting

| Problem | Likely cause | Solution |
|---|---|---|
| A source's metadata cannot be verified | The DOI is wrong or the work is not indexed | Search by exact title; if it still fails, ask the user for the source and mark the entry unverified |
| Annotations exceed the word limit | The summary repeats the abstract | Cut the summary to the question, method, and main finding, and keep the evaluation and relevance |
| The citation format looks wrong | The entry type or capitalisation in the data is invalid | Fix the underlying record and re-render with `citation-style-converter` |

## Related skills

- `paper-search` to find sources, and `citation-verifier` to confirm their metadata.
- `paper-summarizer` and `paper-critic` for the summary and evaluation parts.
- `citation-style-converter` to switch the list between styles.
- `bibtex-manager` for the `.bib` export.
- `literature-review-writer` to turn the annotations into a synthesis.
