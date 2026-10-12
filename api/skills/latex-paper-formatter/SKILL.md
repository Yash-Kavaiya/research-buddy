---
name: latex-paper-formatter
description: "Converts a draft into a venue's official LaTeX template (IEEE, ACM, Springer, NeurIPS, ACL) and fixes compile errors. Use when formatting for submission. Not for final compliance checks."
version: 1.0.0
metadata:
  author: "Yash Kavaiya <yash.kavaiya3@gmail.com>"
  tags: [latex, templates, formatting, ieee, acm]
---

# LaTeX Paper Formatter

## Purpose

Move a draft into the venue's official template without altering its content, and deliver a project that compiles cleanly. The template itself is never modified, and anything that had to change in the text is reported.

## When to use

- A draft must be put into a specific venue's LaTeX template.
- A paper is being resubmitted to a venue with a different template.
- A LaTeX project has compile errors or layout warnings.

Hand off instead for final pre-submission checks (`camera-ready-checker`), tables (`latex-table-generator`), or figures (`publication-figure-maker`).

## Prerequisites

- A LaTeX distribution (TeX Live or MiKTeX) with `latexmk`, and pandoc when converting from Word or Markdown.
- The venue's official template for the current year and submission type.
- The draft with its figures, tables, and `.bib` file.

## Inputs

- The draft and its assets: text, figures, tables, and the `.bib` file.
- Target venue, year, and submission type (review or camera-ready; anonymous or not).
- The official template, or permission to obtain it.

## Instructions

1. **Get the official template for the current year** from the venue or publisher. Never reconstruct a template from memory or modify its style file.

   | Venue family | Class or style | Source |
   |---|---|---|
   | IEEE conferences and journals | `IEEEtran` | CTAN, IEEE Template Selector |
   | ACM | `acmart` (options such as `sigconf`, `manuscript`, `review`, `anonymous`) | CTAN, ACM primary article template page |
   | Springer LNCS | `llncs` | Springer's LNCS author page |
   | Springer journals | `sn-jnl` | Springer Nature LaTeX template page |
   | NeurIPS, ICML, ICLR | venue style file for that year | the conference website |
   | ACL, EMNLP, NAACL | `acl` style | the `acl-org/acl-style-files` repository |
   | Elsevier | `elsarticle` | CTAN, Elsevier author pages |
   | CVPR, ICCV, ECCV | author kit for that year | the conference website |

2. **Start from the template's sample file.** Copy it, confirm it compiles unchanged, then move content in. This isolates template problems from content problems.
3. **Convert the content:**
   - From Word or Markdown: `pandoc draft.docx -o body.tex --wrap=none` (or *draft.md*), then clean the result: headings to `\section`, lists, citations to `\cite{}`, cross-references to `\label` and `\ref`. Pandoc's output for tables and equations usually needs rewriting.
   - From another LaTeX class: keep the body, replace the preamble with the new template's, and port only the packages the paper needs.
4. **Map the front matter** to the template's commands: title, authors, affiliations, emails, abstract, keywords, CCS concepts (ACM), and the anonymous option for review. These differ in every class; use the sample file's pattern.
5. **Fix package conflicts.** Templates load their own packages; remove duplicates (`geometry`, `times`, `caption`, `natbib`, `hyperref` are frequent offenders) and anything that changes margins, fonts, or spacing.
6. **Set up the bibliography** the way the template does: its `.bst` with BibTeX, or `biblatex` only if the venue allows. Use the citation commands the style expects (`\citep` and `\citet` for author-year, `\cite` for numeric).
7. **Fit figures and tables** to the new column width: `\includegraphics[width=\columnwidth]`, `figure*` and `table*` for full width in two-column layouts, and regenerate figures at the new size if text in them becomes unreadable.
8. **Compile** with `latexmk -pdf main.tex` and resolve, in order: errors, undefined references and citations, overfull hboxes above a few points, and float placement.
9. **Check the length** against the limit. If over, report by how much and suggest content cuts or moving material to the appendix.
10. **Deliver** the project, the compiled PDF, and a list of anything that needs the author's decision.

## Output format

```
paper/
  main.tex            # template preamble, \input of sections
  sections/*.tex
  figures/
  references.bib
  <template files, unmodified>
  main.pdf
```

Plus a report:

```markdown
- Template: <name, version or year, source URL>
- Compile: <N> errors, <M> warnings remaining (listed)
- Length: <pages> of <limit>
- Changes made to content: none | <list>
- Needs your decision: <items>
```

## Examples

Requests that should trigger this skill:

- "Format my paper for the IEEE conference template."
- "Convert this Word draft to the NeurIPS LaTeX style."
- "Move my paper from ACM sigconf to Springer LNCS."
- "Fix the LaTeX errors in my project; it won't compile."
- "After switching templates I'm over the page limit. What can I do?"

Requests that belong to another skill:

- "Check anonymisation and fonts before upload." → use `camera-ready-checker`
- "Make a booktabs table from my CSV." → use `latex-table-generator`
- "Clean my .bib file." → use `bibtex-manager`

### Worked example

**Request:** "My paper is in the ACM sigconf class. Reformat it for Springer LNCS; the files are main.tex, refs.bib, and figures/."

**What the agent does:**

1. Obtains the current `llncs` template from Springer and compiles its sample unchanged.
2. Keeps the body, replaces the preamble, and maps title, authors, and institutes to the LNCS commands.
3. Removes conflicting packages, switches to *splncs04.bst*, and resizes full-width figures to the single-column text width.
4. Compiles with `latexmk -pdf`, clears undefined references and overfull boxes, and reports the page count.

**Result (excerpt):**

```markdown
- Template: llncs (Springer LNCS author kit, retrieved today from the Springer author page)
- Compile: 0 errors, 2 warnings remaining (overfull hbox 3.1pt in Section 4; one float moved to next page)
- Length: 16 pages of 15 allowed (including references)
- Changes made to content: none
- Needs your decision: cut about one page, or move Table 4 to an appendix if the venue allows it
```

## Quality bar and pitfalls

- Do not change the template's margins, fonts, font sizes, or spacing to gain space (`\vspace` hacks, `\small` body text, altered `\baselinestretch`). Venues reject or desk-return papers for this.
- Do not alter the paper's content during formatting. Report any sentence, number, or reference that had to change.
- Use the template for the correct year and submission type; review and camera-ready versions differ.
- Do not claim the paper compiles unless it was compiled. If no TeX installation is available, say the output is untested.
- Keep anonymity for double-blind review: no author names, acknowledgements, or identifying metadata, and third-person self-citation.
- A missing or unresolved citation prints as `[?]`. Clear all of them before delivery.
- Type 3 fonts in figures cause rejections at IEEE and ACM venues; embed TrueType fonts (see `publication-figure-maker`).

## Limitations

- The agent can only confirm compilation where a TeX installation is available; otherwise the project is delivered untested and labelled so.
- Pandoc conversion of complex Word documents loses equations, tables, and cross-references, which need manual repair.
- Template rules beyond what LaTeX enforces (for example exact margins after edits) are checked by eye, not guaranteed.
- The skill does not shorten content; meeting a page limit may require the author's cuts.

## Troubleshooting

| Problem | Likely cause | Solution |
|---|---|---|
| `! LaTeX Error: File ... not found` for a `.sty` file | A package is missing from the TeX installation | Install it with the distribution's package manager (`tlmgr install x` or the MiKTeX console) |
| `! LaTeX Error: Option clash for package hyperref` | The template already loads the package with different options | Remove the duplicate `\usepackage` or pass options with `\PassOptionsToPackage` before the class |
| Citations print as `[?]` | BibTeX was not run, or keys are missing | Run `latexmk -pdf` (it runs BibTeX), then fix undefined keys reported in the log |
| The PDF fails the publisher's font validation | A figure contains Type 3 fonts | Regenerate the figure with embedded TrueType fonts using `publication-figure-maker` |

## Related skills

- `paper-outline-generator` for structure and length budget.
- `latex-table-generator` and `publication-figure-maker` for items resized to the new template.
- `bibtex-manager` and `citation-style-converter` for the bibliography.
- `camera-ready-checker` for the final compliance check.
- `math-and-equation-explainer` when equations need retyping from a Word draft.
- `academic-tone-editor` if cuts are needed to meet the page limit.
