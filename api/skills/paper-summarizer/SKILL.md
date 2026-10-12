---
name: paper-summarizer
description: "Summarizes a research paper: problem, method, setup, results with numbers, and limitations. Use when a paper must be understood quickly. Not for judging soundness; use paper-critic."
version: 1.0.0
metadata:
  author: "Yash Kavaiya <yash.kavaiya3@gmail.com>"
  tags: [paper-summary, reading-notes, literature]
---

# Paper Summarizer

Summarize what the paper actually says, in a fixed structure that makes papers comparable and makes each claim checkable against the source.

## Purpose

Report what a paper says in a fixed structure, so that papers can be compared and every statement in the summary can be checked against the source. It separates the authors' claims from the reader's own observations.

## When to use

- One paper needs to be understood quickly.
- Several papers need notes in the same format for a review.

Hand off instead for evaluation of the paper's soundness (`paper-critic`), side-by-side comparison (`paper-comparison-matrix`), or a derivation walk-through (`math-and-equation-explainer`).

## Prerequisites

- The full text of the paper as a PDF, link, or pasted text. With only an abstract, the summary is labelled abstract-level.
- The reader's background and purpose, which set the depth.
- No scripts or API keys are required.

## Inputs

- The paper: PDF, link, or pasted text. Get the full text. If only the abstract is available, say so and produce an abstract-level summary labelled as such.
- Reader's background and purpose (deciding whether to read it, citing it, reproducing it, reviewing it). This sets the depth.
- Length wanted: one paragraph, one page (default), or detailed notes.

## Instructions

1. **Read in passes.** Title, abstract, introduction's contribution list, and conclusion first. Then figures and tables with captions. Then method and experiments. Then limitations, appendix, and footnotes where caveats live.
2. **Identify the paper type** (empirical, method, theory, survey, position, dataset, systems) and adapt the sections: a survey has a taxonomy instead of a method; a theory paper has assumptions and theorems instead of data.
3. **Extract, do not infer.** For each section below, pull the paper's own statements and note where they appear (section, table, figure, or page).
4. **Record results with their conditions**: metric, dataset, baseline, and the size of the difference. "Improves accuracy" is not a result; "84.1% vs 81.3% top-1 on ImageNet-1k against ResNet-50 (Table 2)" is.
5. **Separate the authors' claims from your reading.** Limitations the authors state go under Limitations. Anything you noticed that they did not say goes under Reader notes and is marked as yours.
6. **Write the one-sentence takeaway last**, after the details are fixed.
7. **Check every number** in the summary against the paper once more before sending. If a value fails this check, correct it from the table or figure, or mark it "not reported".

## Output format

```markdown
# <Title> (<First author> et al., <year>, <venue>)
Link/DOI: ...   Type: <empirical | method | theory | survey | dataset | position>
Read: <full text | abstract only | sections X to Y>

**One-sentence takeaway:** ...

## Problem
What is being solved, and why existing approaches fall short (as the authors frame it).

## Approach
The core idea in plain language, then the key technical steps. Name the components.

## Data and setup
Datasets, sample sizes, participants, baselines, metrics, compute.

## Results
- <Result with numbers, metric, dataset, baseline> (Table/Fig/§)
- ...

## Limitations stated by the authors
- ...

## Reader notes (mine, not the authors')
- Unstated assumptions, missing comparisons, questions to check.

## Useful for
How this paper could be used or cited in the reader's work.

## Terms
| Term | Meaning in this paper |
```

For a one-paragraph summary keep the order: problem, approach, main result with numbers, main limitation.

## Reference files

Open these only when the step calls for them; they are not needed for every request.

- `references/reading-by-paper-type.md`: Read at steps 1 to 4, when deciding how to read a paper of a given type and what to extract from each section.
- `assets/paper-summary-template.md`: Copy and fill for a one-page structured summary.

## Examples

Requests that should trigger this skill:

- "Summarize this paper: https://arxiv.org/abs/1706.03762"
- "Give me the key findings of the attached PDF."
- "TL;DR this paper for my lab meeting."
- "Explain what this paper does and how they evaluated it."
- "Make reading notes for these five papers in the same format."

Requests that belong to another skill:

- "Is this paper's methodology sound?" → use `paper-critic`
- "Compare these six papers in a table." → use `paper-comparison-matrix`
- "How did they get from equation 3 to equation 4?" → use `math-and-equation-explainer`

### Worked example

**Request:** "Summarize the attached paper (Attention Is All You Need) in one page. I know RNNs but not attention."

**What the agent does:**

1. Reads the abstract, contributions, and conclusion, then figures and tables, then method and experiments, then the appendix.
2. Identifies it as a method paper and pulls each section's statements with their locations.
3. Records results with metric, dataset, and comparison.
4. Writes the one-sentence takeaway last and rechecks every number.

**Result (excerpt):**

```markdown
**One-sentence takeaway:** A sequence model built only from attention layers, with no recurrence, reaches better translation quality than earlier models at lower training cost.

## Results
- 28.4 BLEU on WMT 2014 English-to-German, above the best previously reported results including ensembles (Table 2)
- 41.8 BLEU on English-to-French after 3.5 days on eight GPUs (Table 2)

## Reader notes (mine, not the authors')
- Evaluation is on translation and constituency parsing only.
```

## Quality bar and pitfalls

- Never state a number, dataset, or claim that is not in the paper. If the paper is unclear, write "not reported".
- Do not summarize from the abstract and present it as a full reading. Abstracts overstate.
- Keep the authors' hedges. "Suggests" must not become "shows".
- Report the comparison, not just the headline number. Gains over weak or untuned baselines read very differently.
- Use the paper's own terminology first, then explain it. Renaming things makes the summary hard to match to the source.
- For long papers, say which appendices were not read.

## Limitations

- Accuracy depends on the text supplied. Scanned PDFs, missing appendices, and figures that cannot be read reduce coverage, and this is stated in the summary.
- A summary reports what the paper claims. It does not establish that the claims are correct.
- Very long papers and supplements may be read in part; the sections not read are listed.

## Troubleshooting

| Problem | Likely cause | Solution |
|---|---|---|
| Only the abstract is accessible | The paper is paywalled or the link did not load | Ask the user for the PDF, look for an open-access version, or deliver a summary labelled "abstract only" |
| Numbers in the summary do not match the paper | A value was taken from the abstract or from a different table row | Recheck each number against its table or figure and cite the location next to it |
| The paper has no method section | It is a survey, position, or theory paper | Switch the structure: taxonomy for surveys, assumptions and theorems for theory |

## Related skills

- `paper-search` to obtain the paper and its metadata.
- `paper-critic` for a critical assessment after the summary.
- `paper-comparison-matrix` to line up several summaries.
- `math-and-equation-explainer` when the method section needs unpacking.
- `annotated-bibliography-builder` and `literature-review-writer` consume these summaries.
- `paper-to-code-reproducer` when the next step is implementing the method.
