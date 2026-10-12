---
name: related-work-writer
description: "Writes a paper's related-work section, grouping prior work into lines of research and stating how the contribution differs from each. Use for conference or journal papers. Not for long reviews."
version: 1.0.0
metadata:
  author: "Yash Kavaiya <yash.kavaiya3@gmail.com>"
  tags: [related-work, positioning, academic-writing]
---

# Related Work Writer

Write a related-work section that does two jobs: shows the reader you know the area, and makes clear what your paper does that the others do not.

## Purpose

Write a related-work section that shows command of the area and makes the paper's difference from each line of prior work explicit. The closest papers get accurate, fair descriptions and a precise statement of what is different.

## When to use

- A conference or journal paper needs a related-work or background section.
- An existing section lists papers without positioning the contribution.

Hand off instead for a long standalone review (`literature-review-writer`) or to find out whether the idea is new at all (`novelty-checker`).

## Prerequisites

- The paper's contribution, from its abstract or introduction.
- The prior work to cover: a `.bib` file, PDFs, or the output of `novelty-checker`.
- The venue's conventions for placement, length, citation style, and anonymity.

## Inputs

- The paper's contribution: the claims from the introduction, or the abstract.
- The prior work to cover: a `.bib` file, PDFs, or the output of `novelty-checker`. If the list is thin, search first with `paper-search`.
- Venue and its conventions: placement (after the introduction or before the conclusion), length (often 0.5 to 1 page in conferences), citation style.
- Whether the submission is double-blind.

## Instructions

1. **State the contribution in one sentence.** Everything in the section is selected relative to it.
2. **Group the prior work into 3 to 5 lines of research.** Typical groups: the same problem with other methods; the same method on other problems; the components you build on; alternative formulations; benchmarks and evaluations.
3. **For each group, record** the representative papers, what they have in common, the best current result or understanding, and their limitation relevant to your work.
4. **Write one paragraph per group:**
   - A bolded run-in heading or a topic sentence naming the line of work.
   - What the line does, citing several papers together where they share an idea.
   - One or two papers discussed individually: the closest and the strongest.
   - The contrast sentence: how your work differs and why that difference matters.
5. **Treat the closest paper carefully.** Describe it accurately and fairly, then state the precise difference (assumption, setting, guarantee, scale, supervision). Reviewers often include its authors.
6. **Include concurrent work.** Mention recent preprints that overlap, labelled as concurrent, with the difference stated.
7. **Check coverage** against the venue's last two years: search the venue name with the topic so the obvious papers are not missing.
8. **Verify every citation** says what you attribute to it, then run `citation-verifier`.

## Output format

```latex
\section{Related Work}

\paragraph{<Line of research 1>.}
<What this line does> \cite{a,b,c}. <Closest work> \cite{d} ... In contrast, our approach ...

\paragraph{<Line of research 2>.}
...
```

Or the same in Markdown. Alongside the section deliver:

- A positioning table: paper, what it does, how ours differs.
- A list of cited keys that are missing from the `.bib` file.
- Any claims about prior work you could not verify from the sources.

## Examples

Requests that should trigger this skill:

- "Write the related work section for my paper on efficient attention."
- "Position my paper against these six prior works."
- "How do I differentiate my method from paper X in related work?"
- "My related work is just a list. Group it and add contrasts."
- "Draft a half-page related work for a NeurIPS submission."

Requests that belong to another skill:

- "Write a 5,000-word literature review chapter." → use `literature-review-writer`
- "Has this idea been done before?" → use `novelty-checker`
- "Write my introduction." → use `introduction-writer`

### Worked example

**Request:** "My paper proposes a sparse attention layer that needs no retraining. Write related work from refs.bib; closest papers are keys smith2022 and lee2023."

**What the agent does:**

1. States the contribution in one sentence and groups the references into four lines of research.
2. Writes one paragraph per group ending with a contrast sentence.
3. Describes the two closest papers individually and states the precise difference.
4. Lists cited keys missing from the `.bib` file and claims it could not verify.

**Result (excerpt):**

```markdown
\paragraph{Sparse attention.}
Several methods reduce attention cost by restricting each token to a subset of positions \cite{a,b,c}. \citet{smith2022} learn the sparsity pattern during training, and \citet{lee2023} prune attention heads after training followed by fine-tuning. In contrast, our layer is applied to a pretrained model without any further training.

Positioning table: lee2023 | post-hoc pruning plus fine-tuning | ours needs no fine-tuning
```

## Quality bar and pitfalls

- Never cite a paper you have not retrieved, and never describe one beyond what you have read. A wrong description of a reviewer's paper is costly.
- Every paragraph ends by relating the group to your work. A paragraph with no contrast is a list.
- State differences as facts ("requires paired data; ours does not"), not judgements ("suffers from", "fails to").
- Do not claim prior work "cannot" do something unless its authors say so or you tested it.
- Do not inflate novelty by omitting the closest paper. Reviewers will find it.
- For double-blind venues, cite your own prior work in the third person.
- Keep it proportionate. Depth belongs on the closest two or three works.
- Do not pad the reference list with papers you do not discuss.

## Limitations

- Descriptions of prior work are only as accurate as the reading behind them. Papers known only from abstracts are described briefly and flagged.
- Coverage reflects the references supplied plus a targeted search. Concurrent preprints can be missed.
- The section cannot make a contribution novel. If the closest work does the same thing, the problem is upstream.

## Troubleshooting

| Problem | Likely cause | Solution |
|---|---|---|
| A cited key is not in the `.bib` file | The reference list is incomplete | List the missing keys and add entries with `bibtex-manager` from retrieved records |
| A paragraph has no contrast with the paper | The group is not relevant to the contribution | Cut the group or state concretely how the work relates |
| The section is over the length budget | Too many papers are discussed individually | Cite groups together and keep individual discussion for the two or three closest works |
| A description of prior work may be invalid | It was written from memory | Reread the cited paper and validate the claim with `citation-verifier` |

## Related skills

- `novelty-checker` supplies the closest prior work and the differences.
- `paper-search` and `citation-graph-explorer` to check coverage.
- `paper-comparison-matrix` for the positioning table.
- `literature-review-writer` for the long-form version.
- `introduction-writer` so the gap stated in the introduction matches this section.
- `citation-verifier` and `bibtex-manager` for the references.
