---
name: introduction-writer
description: "Writes a paper or thesis introduction as context, problem, gap, approach, and contributions, matched to the results. Use when drafting or fixing an introduction. Not for abstracts."
version: 1.0.0
metadata:
  author: "Yash Kavaiya <yash.kavaiya3@gmail.com>"
  tags: [introduction, academic-writing, contributions]
---

# Introduction Writer

Write an introduction that answers four questions in order: what is the problem, why does it matter, what is missing, and what does this paper add.

## Purpose

Write an introduction that answers, in order, what the problem is, why it matters, what is missing, and what this paper adds. Contributions are stated as specific, checkable items, and claims are calibrated to the results section.

## When to use

- A paper or thesis chapter needs its introduction drafted or restructured.
- Contributions need to be stated clearly.

Hand off instead for the abstract (`abstract-writer`) or the full review of prior work (`related-work-writer`, `literature-review-writer`).

## Prerequisites

- The paper's contribution and main results; the introduction is written after the results are known.
- The gap in prior work and the references that establish it, as a `.bib` file or list.
- The venue, audience, and length budget.

## Inputs

- The paper's contribution and main results (from the outline or the results section). Write the introduction after the results are known.
- The gap in prior work and the key references that establish it.
- Venue, audience, and length budget (often 1 to 1.25 pages for conference papers; longer for journals and theses).
- The user's `.bib` file or reference list.

## Instructions

1. **Fix the message**: one sentence stating what the paper shows and why it matters. The introduction exists to set up and deliver this sentence.
2. **Plan the moves** (the CARS model: establish a territory, establish a niche, occupy the niche), one paragraph each:
   1. *Context*: the area and why it matters, specific to this problem. Start close to the topic; skip the history of the field.
   2. *Problem*: the specific problem and the current state of solving it, with the key citations.
   3. *Gap*: what existing work does not do, stated precisely, with evidence. "However, ..." is the hinge of the introduction.
   4. *This paper*: what you do about the gap, in one or two sentences on the approach and why it should work.
   5. *Results and contributions*: the headline results with numbers, then the contributions.
   6. *Outline* of the paper: one or two sentences, only where the venue expects it.
3. **Write the contributions** as 2 to 4 specific, checkable items. Each names what was done and where the evidence is:
   - Weak: "We propose a novel framework for X."
   - Strong: "We introduce M, a method that does X without requiring Y (Section 3)."
   - Strong: "On benchmarks A and B, M reduces error by 12% relative to the best prior method at one third of the compute (Section 5)."
4. **Draft the paragraphs**, each starting with a sentence that states its point. A reader who reads only first sentences should follow the argument.
5. **Calibrate the claims** to the evidence: "we show" for demonstrated results, "we provide evidence that" for partial support. Match the wording used in the results section exactly.
6. **Place the citations.** Every statement about the field or prior work needs one from the supplied references. Mark statements that need a citation the user has not provided as `[citation needed]`.
7. **Point to Figure 1** if the paper has an overview figure, by the second or third paragraph.
8. **Check consistency** with the abstract, the related work, and the conclusion: same gap, same contributions, same numbers.

## Output format

```markdown
## Introduction (<N> words)
<paragraphs, with \cite{key} or (Author, Year) from the supplied references>

Our contributions are:
- ...
- ...

## Notes
- Paragraph plan: context / problem / gap / approach / results / outline
- [citation needed]: <statements still lacking a supplied source>
- Claims to verify against results: <list with section pointers>
```

## Examples

Requests that should trigger this skill:

- "Write the introduction for my paper on low-resource translation."
- "My intro is two pages and unfocused. Fix it."
- "How should I state my contributions?"
- "Write the motivation and problem statement for my thesis chapter 1."
- "Draft an introduction from this outline and results."

Requests that belong to another skill:

- "Write the abstract." → use `abstract-writer`
- "Write the related work section." → use `related-work-writer`
- "Check whether my idea is new." → use `novelty-checker`

### Worked example

**Request:** "Write a one-page introduction. Contribution: a tokenizer-free model for Hindi-English code-mixed text that beats the mBERT baseline by 3.1 F1 on two benchmarks. Refs in refs.bib."

**What the agent does:**

1. Fixes the message and plans one paragraph per move.
2. Drafts with topic sentences and places citations from refs.bib, marking one statement that needs a source.
3. Writes three contributions, each naming what was done and where the evidence is.
4. Checks the numbers and wording against the results.

**Result (excerpt):**

```markdown
Code-mixed text is the norm in informal Hindi-English writing, yet most language models assume one language per sentence \cite{key1,key2}. Subword tokenizers trained on monolingual corpora split romanised Hindi words inconsistently [citation needed], which degrades downstream accuracy. ...

Our contributions are:
- A character-level encoder for code-mixed text that requires no tokenizer (Section 3).
- On benchmarks A and B, it improves F1 by 3.1 points on average over mBERT (Section 5).
```

## Quality bar and pitfalls

- Cite only supplied or retrieved references. Never invent a citation to support a sentence; mark the need instead.
- Do not state results the paper does not contain, or round them favourably.
- The gap must be real and specific. "Little attention has been paid to X" needs to be true; check with `novelty-checker` if unsure.
- Avoid openers that could start any paper ("In recent years, deep learning has achieved great success").
- Do not criticise prior work beyond what is needed to motivate yours, and be accurate about what it does.
- Contributions are things the paper delivers, not activities ("we conduct extensive experiments" is not a contribution; what the experiments show is).
- "Novel" and "first" are claims a reviewer will test. Use "first" only with a qualifier you can defend ("to our knowledge", plus a search).
- Keep to the length budget. An introduction that fills two pages of an eight-page paper takes space from the evidence.

## Limitations

- The introduction depends on results and references supplied by the author. It cannot justify a gap that a literature search does not support.
- Statements about the field that lack a supplied source are marked, not cited from memory.
- Venue norms differ on whether to include a paper outline or a contributions list.

## Troubleshooting

| Problem | Likely cause | Solution |
|---|---|---|
| A statement needs a citation the user has not supplied | The reference list is incomplete | Leave `[citation needed]`, search with `paper-search`, and add the verified entry |
| The gap sounds generic | It is not tied to specific prior work | Name what existing approaches do and the exact thing they do not do |
| The introduction is over budget | Too much background | Start closer to the problem and move background detail to related work |
| Contributions restate activities | They list effort instead of outcomes | Rewrite each as a deliverable with a section pointer; a claim that fails to match the results must be reworded |

## Related skills

- `paper-outline-generator` supplies the message, claims, and budget.
- `results-interpreter` supplies the claim wording the results support.
- `novelty-checker` and `research-gap-finder` back the gap statement.
- `related-work-writer` covers prior work in depth so the introduction can stay brief.
- `abstract-writer` compresses the same arc.
- `citation-verifier` checks the cited claims.
- `academic-tone-editor` for the final language pass.
