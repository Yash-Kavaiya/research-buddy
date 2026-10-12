---
name: plagiarism-and-paraphrase-checker
description: "Compares a draft with its sources, flags verbatim and too-close passages, and helps fix them by quoting, citing, or rewriting from understanding. Use before submission. Not for disguising copied text."
version: 1.0.0
compatibility: "Requires Python 3.10 or later. Runs locally with no network access."
allowed-tools: "Bash(python:*) Read Write"
metadata:
  author: "Yash Kavaiya <yash.kavaiya3@gmail.com>"
  tags: [plagiarism, paraphrasing, research-integrity, attribution]
---

# Plagiarism and Paraphrase Checker

Find the places where a draft is too close to its sources, and fix them properly: quote and cite, cite, or rewrite from the idea. The goal is correct attribution.

## Purpose

Find the places where a draft is too close to the sources it drew on, and fix each one properly: quote and cite, cite, or rewrite from the idea. The aim is correct attribution of the author's own work.

## When to use

- Before submitting a paper, thesis chapter, or assignment that draws on sources.
- When the author is unsure whether a paraphrase is far enough from the original.
- When reusing the author's own earlier text (self-plagiarism or text recycling).

Hand off instead to verify references exist (`citation-verifier`) or for a general language edit (`academic-tone-editor`).

**Scope.** This skill helps authors attribute their own work correctly. Do not use it to disguise copied text so that similarity software misses it, or to reword someone else's work for submission as the user's own. If that is the request, decline that part and offer the proper fix: quote, cite, or write from understanding.

## Prerequisites

- Python 3.10 or later; the script uses only the standard library.
- The draft and each source as plain text (convert PDFs with `pdftotext`, Word with pandoc).
- The set of sources the draft was written from; the check covers only these.

## Inputs

- The draft, as plain text or Markdown (convert PDF or Word to text first).
- The source texts the draft drew on, as text files. The check is only as complete as this set.
- The citation style, and the institution's or venue's rules on similarity and on reuse of the author's earlier work.

## Instructions

1. **Collect the sources.** Ask which papers each section was written from. For a literature review, that means the papers discussed in it. Convert each to text (`pdftotext paper.pdf paper.txt`, or pandoc for Word).
2. **Run the comparison:**

   ```bash
   python scripts/similarity.py draft.txt source1.txt source2.txt source3.txt
   python scripts/similarity.py draft.md paper.txt --min-run 6 --threshold 0.4 --format json
   ```

   For every draft sentence, the script finds the longest run of consecutive words shared with a source and the share of the sentence's word trigrams found in a source, then flags:

   | Flag | Criterion (defaults) | Meaning |
   |---|---|---|
   | `verbatim` | 8 or more consecutive shared words, not in quotation marks | Copied text presented as the author's own |
   | `close_paraphrase` | 50% or more of the sentence's trigrams shared | Source's sentence with words swapped |
   | `quoted` | A copied run inside quotation marks | Fine if cited with a page number; check it |

   `--min-run` and `--threshold` tighten or loosen the criteria. The exit code is non-zero when anything other than quotes is flagged.
3. **Review each flag in context.** Some matches are legitimate: technical terms, method and dataset names, standard phrases of the field ("the results are shown in Table"), and properly quoted material. Dismiss these with a note.
4. **Look beyond the script.** Lexical overlap misses:
   - *Structural paraphrase*: the same sequence of ideas and sentence structure as the source, with all words changed. Compare paragraphs with their source paragraphs.
   - *Idea plagiarism*: an idea, argument, or finding from a source stated without citation, in entirely new words.
   - *Translated text*: copied from a source in another language.
   - *Figures, tables, and data* reused without permission or credit.
5. **Check every borrowed idea has a citation** next to it, and every direct quotation has quotation marks, a citation, and a page number.
6. **Fix each flagged passage** with the author, choosing one:
   - *Quote it*: when the exact words matter. Add quotation marks, citation, and page.
   - *Cite and rewrite from understanding*: close the source, state the point in the context of the author's own argument (why it matters here, how it relates to other sources), then check against the source for accuracy. Changing words within the source's sentence is not a rewrite.
   - *Synthesize*: combine the point with what other sources say, so the sentence is the author's analysis.
   - *Remove it* if it is not needed.
7. **For the author's own earlier work**: reuse of published text needs a citation to the original and, often, the publisher's permission; methods sections have more latitude in many fields, but the venue's policy governs. Thesis reuse of the author's papers follows the university's rules.
8. **Rerun** the comparison after the fixes and report what remains.

## Available Scripts

| Script | Purpose | Arguments |
|---|---|---|
| `scripts/similarity.py` | Flags draft sentences with a long copied run or high trigram overlap with a source, and separates quoted text | `DRAFT` (required), `SOURCES...` (required), `--min-run N` (default 8), `--threshold X` (default 0.5), `--format md|json` |

Run a script with the agent's script tool, for example `run_script("scripts/similarity.py", args=[...])`, or from a shell in the skill folder with `python scripts/similarity.py ...`. Each script prints usage with `--help`, validates its arguments, and exits with a non-zero code and an `error:` message on failure.

## Output format

```markdown
## Similarity check
Draft: <file>, <N> sentences. Compared with: <list of source files>.
Flagged: <a> verbatim, <b> close paraphrase, <c> quoted. Overall trigram overlap: <x>%.

### Passages to fix
| # | Draft sentence | Source | Issue | Recommended fix |
|---|---|---|---|---|

### Dismissed matches
- Sentence 14: standard method description and dataset name.

### Attribution gaps (found by reading)
- Paragraph 3 presents <idea> from <source> without a citation.

### Not covered
- Sources not supplied: ...; no web or database comparison was run.
```

## Examples

Requests that should trigger this skill:

- "Check my literature review against these five papers for plagiarism."
- "Is this paraphrase too close to the original paragraph?"
- "Did I paraphrase this properly?"
- "I reused text from my earlier paper. Is that self-plagiarism?"
- "Check my draft for copied sentences before I submit."

Requests that belong to another skill:

- "Make this copied text pass Turnitin." → this request is declined; the skill offers quoting, citing, or rewriting from understanding
- "Verify my references exist." → use `citation-verifier`
- "Edit my writing for style." → use `academic-tone-editor`

### Worked example

**Request:** "Compare review.txt with the three papers I wrote it from (a.txt, b.txt, c.txt)."

**What the agent does:**

1. Runs `run_script("scripts/similarity.py", args="review.txt a.txt b.txt c.txt")`.
2. Reviews each flag in context and dismisses a match that is a dataset name and standard phrase.
3. Compares paragraph structure with the sources for paraphrase the script cannot see, and checks each borrowed idea has a citation.
4. Works through the flagged sentences with the author, choosing quote, rewrite, or remove.

**Result (excerpt):**

```markdown
Draft sentences: 41. Flagged: 3. Overall trigram overlap with the sources: 6.2%.

| # | Draft sentence | Source | Issue | Recommended fix |
|---|---|---|---|---|
| 12 | "Deep neural networks have achieved remarkable success in image recognition tasks in recent years." | a.txt | verbatim, 11 copied words, no quotation marks | rewrite in the context of your argument and cite |
| 19 | ... | b.txt | close paraphrase, 58% trigram overlap | restate the point from understanding; cite |

Not covered: no web or database comparison was run.
```

## Quality bar and pitfalls

- State the coverage. This compares the draft with the supplied files only. It is not a web-wide or publisher-database check, and a clean result here does not predict a similarity score from institutional software.
- Never report a percentage as "the plagiarism score". Similarity is evidence to review, and plagiarism is a judgement about attribution.
- A citation does not make copied wording acceptable. Verbatim text needs quotation marks as well.
- Do not fix a close paraphrase by substituting synonyms. That leaves the source's structure and remains too close, and it defeats the purpose of the check.
- Do not rewrite quotations, and do not change the meaning of the source when rewriting.
- Keep legitimately shared technical wording. Forcing odd synonyms for standard terms damages the text.
- Be straightforward with the author about serious cases: long unattributed passages need substantial rewriting or quotation, not polishing.

## Limitations

- The comparison covers only the source files supplied. It is not a web-wide or publisher-database check and does not predict an institutional similarity score.
- Lexical overlap misses structural paraphrase, uncited ideas in new words, and translated text; these need reading.
- Similarity is evidence to review. Whether something is plagiarism is a judgement about attribution that the script cannot make.
- PDF-to-text conversion errors (hyphenation, columns) can hide or create matches.

## Troubleshooting

| Problem | Likely cause | Solution |
|---|---|---|
| Every sentence is flagged | A source file contains the draft itself, or the threshold is too low | Check the source files and return to the default `--threshold 0.5` and `--min-run 8` |
| Nothing is flagged but the text feels close | The paraphrase changed the words and kept the structure | Compare the paragraphs side by side and rewrite from the idea |
| Standard phrases and method names are flagged | Shared technical wording | Dismiss them with a note; do not replace standard terms with odd synonyms |
| Garbled text in the report, or no matches where copying is obvious | The source is not plain UTF-8 text, so extraction failed and invalid characters were replaced | Convert with `pdftotext -enc UTF-8` or pandoc and rerun |

## Related skills

- `citation-verifier` to confirm that cited sources say what is attributed to them.
- `literature-review-writer` and `related-work-writer`, whose synthesis approach avoids close paraphrase in the first place.
- `paper-summarizer` to understand a source well enough to write about it independently.
- `academic-tone-editor` for the language pass after attribution is fixed.
- `thesis-chapter-writer` for reuse of the author's published papers in a thesis.
- `camera-ready-checker` as part of the pre-submission checks.
