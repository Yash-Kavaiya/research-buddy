---
name: abstract-writer
description: "Writes or revises a research abstract within a word limit, structured or unstructured, with title and keyword options. Use when an abstract is needed or too long. Not for introductions."
version: 1.0.0
metadata:
  author: "Yash Kavaiya <yash.kavaiya3@gmail.com>"
  tags: [abstract, academic-writing, keywords]
---

# Abstract Writer

## Purpose

Write an abstract that lets a reader decide in a minute what was done, what was found, and whether to read on, using only what the paper contains. Results get the most space and every number is checked against the paper.

## When to use

- A paper, thesis, or conference submission needs an abstract.
- An existing abstract is over the limit, vague, or missing results.

Hand off instead for the introduction (`introduction-writer`) or a plain-language summary for the public (`paper-to-blog`).

## Prerequisites

- The paper or its key content: problem, method, main results with numbers, and conclusion.
- The venue's requirements: word limit, structured or unstructured form, and required headings.
- No scripts or API keys are required.

## Inputs

- The paper or its key content: problem, method, main results with numbers, conclusion. If the results are not final, say so and write placeholders the user must fill.
- Venue requirements: word limit (commonly 150 to 250), structured or unstructured, required headings, whether citations and abbreviations are allowed.
- Audience: specialist venue or broad journal.

## Instructions

1. **Check the requirements** in the venue's guidelines: limit, format, headings.
2. **Extract five things from the paper**, each as one sentence:
   - *Background*: the context the reader needs.
   - *Gap or problem*: what is unknown or unsolved.
   - *Method*: what was done, with the design, data, or approach named.
   - *Results*: the main findings with numbers and units.
   - *Conclusion*: what it means and for whom.
3. **Allocate the words.** For 250 words: background and gap 40 to 60, method 50 to 70, results 80 to 100, conclusion 30 to 40. Results get the most space.
4. **Draft** in the required form:
   - *Structured*: headings such as Background, Objective, Methods, Results, Conclusions (use the venue's exact headings).
   - *Unstructured*: one paragraph in the same order.
5. **Make the results specific.** Replace "significantly improved" with the value, the comparison, and the uncertainty: "reduced error from 12.4% to 9.1% (95% CI 8.3 to 9.9)". Include sample size or dataset.
6. **Tighten to the limit.** Cut background first, then method detail. Remove filler ("In this paper, we", "It is important to note"). Keep the numbers.
7. **Check against the paper**: every statement and number in the abstract appears in the body with the same value.
8. **Offer titles and keywords.** Three title options (descriptive, result-stating, and short), and 4 to 6 keywords that are not already in the title, using the field's indexing terms (MeSH for biomedical work).
9. **Report the word count.**

## Output format

```markdown
## Abstract (<N> words; limit <L>)
<text>

## Title options
1. ...
2. ...
3. ...

## Keywords
a; b; c; d; e

## Checks
- Numbers matched to: Table 2, §5.1
- Placeholders still to fill: [N], [effect size]
- Assumptions made: ...
```

When revising, also give a short list of what changed and why.

## Examples

Requests that should trigger this skill:

- "Write an abstract for my paper; the limit is 250 words."
- "Shorten my abstract from 320 to 200 words."
- "Make this a structured abstract with Background, Methods, Results, Conclusions."
- "Improve my abstract; it sounds vague."
- "Suggest three titles and keywords for this paper."

Requests that belong to another skill:

- "Write the introduction." → use `introduction-writer`
- "Write a plain-language summary for the public." → use `paper-to-blog`
- "Edit the tone of my whole paper." → use `academic-tone-editor`

### Worked example

**Request:** "Write a 150-word unstructured abstract. Study: 12-week RCT, 180 adults with insomnia, app-based CBT vs sleep-hygiene leaflet; ISI score fell 7.1 vs 3.2 points; difference 3.9 (95% CI 2.6 to 5.2)."

**What the agent does:**

1. Extracts background, gap, method, results, and conclusion as one sentence each.
2. Allocates words with results largest and drafts in that order.
3. Makes the result specific with the interval, and tightens to the limit.
4. Reports the word count and offers titles and keywords.

**Result (excerpt):**

```markdown
## Abstract (148 words; limit 150)
Insomnia is common, and access to cognitive behavioural therapy (CBT) is limited. We tested whether CBT delivered by a smartphone app reduces insomnia severity. In a 12-week randomised controlled trial, 180 adults with insomnia received either app-based CBT or a sleep-hygiene leaflet. Insomnia Severity Index scores fell by 7.1 points with the app and 3.2 points with the leaflet (difference 3.9, 95% CI 2.6 to 5.2). ...

## Checks
- Numbers matched to the figures supplied; follow-up beyond 12 weeks not reported.
```

## Quality bar and pitfalls

- Never invent a result, number, or sample size to make the abstract read well. Use a bracketed placeholder and flag it.
- The abstract must stand alone: no undefined abbreviations, no references to figures or sections, and citations only if the venue allows them.
- Do not claim more than the results section supports. The abstract is the most-read part and overclaiming there does the most damage.
- State the main limitation in a clause when it changes how the result should be read (single site, small sample, simulation only).
- Past tense for what was done and found; present tense for conclusions and general statements.
- Avoid opening with a sentence so general it fits any paper in the field.
- Count words the way the venue does. Stay under the limit; submission systems reject overruns.

## Limitations

- The abstract can only state what the paper contains. Missing results are left as bracketed placeholders.
- Word counts follow a plain count; some venues count hyphenated words or numbers differently.
- Titles and keywords are suggestions; indexing terms such as MeSH should be confirmed in the thesaurus.

## Troubleshooting

| Problem | Likely cause | Solution |
|---|---|---|
| The draft is over the word limit | Too much background or method detail | Cut background first, then method detail; keep the numbers |
| A result is missing or a number fails validation against the paper | Final results were not supplied or changed | Insert a bracketed placeholder and list it for the author; never estimate a value |
| The venue requires specific headings | A generic structure was used | Replace the headings with the venue's exact wording and order |

## Related skills

- `results-interpreter` provides the findings and the wording they support.
- `introduction-writer` expands the same arc into the introduction.
- `paper-outline-generator` fixes the message the abstract must carry.
- `academic-tone-editor` for a final clarity and concision pass.
- `venue-recommender` uses the abstract to match venues.
- `cover-letter-writer` reuses the abstract's main result.
