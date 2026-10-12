---
name: thesis-chapter-writer
description: "Drafts and revises thesis chapters with a shared terminology sheet, cross-references, and chapter introductions and summaries. Use for dissertation chapters. Not for standalone papers."
version: 1.0.0
metadata:
  author: "Yash Kavaiya <yash.kavaiya3@gmail.com>"
  tags: [thesis, dissertation, academic-writing, long-form]
---

# Thesis Chapter Writer

## Purpose

Write chapters that read as parts of one document: the same terms, the same notation, and an argument that runs from the first chapter to the last. A terminology sheet is maintained across chapters and each chapter is written against a map of the thesis argument.

## When to use

- Drafting any thesis chapter from notes, results, or papers.
- Converting published papers into chapters.
- Fixing inconsistency across chapters written at different times.

Hand off instead for a standalone paper (`paper-outline-generator`) or a proposal written before the research (`phd-research-proposal-writer`).

## Prerequisites

- The university's thesis regulations: format, required sections, length limits, and rules on including published work.
- The thesis statement or research questions, and the chapter's source material (results, notes, papers, `.bib` file).
- Existing chapters and any terminology already fixed.

## Inputs

- The university's thesis regulations: format (monograph or by publication), required sections, length limits, citation style, rules on including published work.
- The thesis statement or central research questions.
- The chapter's source material: results, notes, drafts, published papers, the `.bib` file.
- Existing chapters and any terminology or notation already fixed.
- The supervisor's preferences, if known.

## Instructions

1. **Set up the thesis map** (once): the central argument, the research questions, and one sentence per chapter saying what it contributes to answering them. Each chapter is written against this map.
2. **Create or update the terminology sheet** (*thesis-terms.md*) before drafting, and consult it on every chapter:

   | Term | Definition | First defined | Do not use |
   |---|---|---|---|
   | participant | a person who completed the study | §3.2 | subject, respondent |

   Include abbreviations, mathematical notation with symbols, names of methods and datasets, spelling variant, and capitalisation choices.
3. **Choose the chapter's structure** by its role:

   | Chapter | Sections |
   |---|---|
   | Introduction | Background, problem statement, aims and research questions, scope, significance, contributions, thesis outline |
   | Literature review | see `literature-review-writer` |
   | Methodology | see `methodology-designer` |
   | Results or study chapters | Chapter introduction, method specifics, results by research question, chapter discussion, summary |
   | Discussion | Summary of findings, interpretation against the literature, implications, limitations |
   | Conclusion | Answers to the research questions, contributions, limitations, future work |

4. **Outline to paragraph level** and agree it with the user before drafting long chapters.
5. **Draft section by section.** Each chapter opens with a short introduction (what this chapter does and how it follows from the last) and closes with a summary (what was established and what the next chapter does with it).
6. **Write at thesis depth.** A thesis explains what a paper only states: the reasoning behind choices, the alternatives rejected, the full method, negative and secondary results, and definitions for a reader outside the subfield.
7. **When adapting a published paper:** remove the paper's standalone introduction and related work (they move to the thesis's early chapters), restore cut detail, unify terms and notation with the sheet, add linking text, and follow the university's rules for declaring co-authored and previously published material.
8. **Cross-reference** with labels (`\ref`, or "Section 3.2"), never "above" or "in the previous chapter" alone. Refer back when a concept returns instead of redefining it.
9. **Run the consistency check** at the end of each chapter: terms and abbreviations against the sheet, notation, tense, numbering and caption style, and that every claim about another chapter matches that chapter.
10. **List what the user must supply**: missing results, references, and decisions.

## Output format

```markdown
# Chapter <N>: <Title>

## <N>.1 Introduction
## <N>.2 ...
## <N>.x Summary

---
## Chapter notes
- Contribution to the thesis argument: ...
- New terms added to the terminology sheet: ...
- Cross-references to check: ...
- [citation needed] / [result needed] items: ...
- Word count: <n> of <target>
```

Deliver the updated *thesis-terms.md* with every chapter.

## Examples

Requests that should trigger this skill:

- "Write chapter 4 of my thesis from these results and notes."
- "Turn my published paper into a thesis chapter."
- "Help me structure my dissertation into chapters."
- "My chapters use different terms for the same thing. Fix the consistency."
- "Draft the introduction chapter of my PhD thesis."

Requests that belong to another skill:

- "Outline a conference paper." → use `paper-outline-generator`
- "Write a PhD admission proposal." → use `phd-research-proposal-writer`
- "Prepare me for the viva." → use `viva-defense-prep`

### Worked example

**Request:** "Convert my published conference paper on route optimisation into chapter 5 of my thesis. Chapters 1 to 4 exist; here is thesis-terms.md."

**What the agent does:**

1. Reads the thesis map and terminology sheet and notes that the paper says "vehicle" where the thesis says "agent".
2. Removes the paper's standalone introduction and related work, restores cut method detail and the negative results.
3. Adds a chapter introduction linking to chapter 4 and a summary leading to chapter 6.
4. Unifies terms and notation, replaces "above" with labelled cross-references, and flags the co-authorship declaration.

**Result (excerpt):**

```markdown
## 5.1 Introduction
Chapter 4 showed that the exact formulation does not scale beyond 50 agents. This chapter develops a heuristic for larger instances and evaluates it on the benchmark introduced in Section 3.4.

---
## Chapter notes
- New terms added to the terminology sheet: "instance" (do not use "scenario")
- To confirm: the university's declaration form for co-authored published work
- [result needed]: runtime on the 500-agent instances, which the paper omitted
```

## Quality bar and pitfalls

- The thesis is the candidate's work. Write from their material: their results, their notes, their reading. Do not invent findings, data, or sources, and mark every gap for the user to fill.
- Cite only supplied or retrieved sources; mark unsupported statements `[citation needed]`.
- Tell the user to check their university's policy on AI assistance in theses and to declare it as required.
- Reusing published text has rules: publisher permissions, co-author statements, and self-plagiarism policies. Flag them when papers are adapted.
- One term for one concept, everywhere. A thesis that calls the same thing by three names reads as three documents.
- Do not pad to reach a length. Examiners read every page.
- Results chapters report; the discussion interprets. Keep the division the university's format expects.
- The introduction and conclusion must match: every research question asked is answered.

## Limitations

- The chapter is built from the candidate's material. Missing results, sources, or reasoning are marked for the candidate to supply.
- University rules on format, published-work inclusion, and AI assistance vary and must be checked by the candidate.
- Consistency across very long theses depends on the terminology sheet being kept up to date.

## Troubleshooting

| Problem | Likely cause | Solution |
|---|---|---|
| Terms differ between chapters | Chapters were written at different times | Update *thesis-terms.md*, then search each chapter for the banned variants and replace them |
| The chapter repeats the literature review | A paper's related work was pasted in | Move it to chapter 2 and refer back by section number |
| A cross-reference is wrong or validation of numbering fails | Sections were reordered | Use labels instead of typed numbers and recompile |
| The chapter is far over length | Paper-level and thesis-level detail are both present | Move derivations and extra tables to an appendix and keep the argument in the chapter |

## Related skills

- `literature-review-writer` and `methodology-designer` for those chapters.
- `results-interpreter` for results chapters, and `qualitative-coding-assistant` for qualitative findings.
- `limitations-and-future-work-writer` for the closing chapter.
- `academic-tone-editor` for language, and `citation-verifier` and `bibtex-manager` for references.
- `latex-paper-formatter` for the university's LaTeX template.
- `research-progress-tracker` to plan chapter milestones.
- `viva-defense-prep` once the thesis is drafted.
