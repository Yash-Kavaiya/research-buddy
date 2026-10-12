---
name: bibtex-manager
description: "Cleans a BibTeX file: normalizes fields, protects title capitalization, merges duplicates, reports missing fields, and can fill DOIs. Use for messy bibliographies. Not for verifying references."
version: 1.0.0
compatibility: "Requires Python 3.10 or later. Makes read-only HTTPS requests to Crossref (only with --fill-doi); sends only the search terms or identifiers given to it."
allowed-tools: "Bash(python:*) Read Write"
permissions: [network, env, file_write]
metadata:
  author: "Yash Kavaiya <yash.kavaiya3@gmail.com>"
  tags: [bibtex, bibliography, latex, reference-management]
---

# BibTeX Manager

## Purpose

Turn a messy `.bib` file into a consistent one, with every change reported and the original left untouched. Duplicates are merged with a key mapping so citations in the manuscript can be updated.

## When to use

- A `.bib` file has duplicates, inconsistent formatting, missing fields, or capitalisation problems.
- BibTeX or biber prints warnings.
- Entries need creating from DOIs, titles, or a pasted reference list.

Hand off instead to confirm references are real (`citation-verifier`) or to output a formatted reference list in a named style (`citation-style-converter`).

## Prerequisites

- Python 3.10 or later; the script uses only the standard library.
- The `.bib` file, and the `.tex` files that cite it if keys may change.
- Network access to Crossref only when `--fill-doi` is used.

## Inputs

- The `.bib` file.
- The `.tex` files that cite it, when keys may change.
- The venue's bibliography style, which decides how much detail is needed.
- Preferences: keep or regenerate keys, keep or drop abstracts and notes.

## Instructions

1. **Clean the file into a new file:**

   ```bash
   python scripts/clean_bibtex.py refs.bib --out refs.clean.bib --report bib-report.json
   python scripts/clean_bibtex.py refs.bib --out refs.clean.bib --fill-doi --sort
   python scripts/clean_bibtex.py refs.bib --out refs.clean.bib --rekey
   ```

   The script:
   - lowercases entry types and field names, collapses whitespace, and expands `@string` macros;
   - normalises DOIs to the bare form and drops a `url` that only repeats the DOI;
   - converts page ranges to `123--130`;
   - protects words with inner capitals in titles (`{BERT}`, `{ImageNet}`, `{mRNA}`) so bibliography styles do not lowercase them;
   - drops empty fields and, by default, `abstract`, `file`, and `keywords` (change with `--strip`; `--strip ""` keeps everything);
   - merges duplicates (same DOI, or same title and year), keeping the fuller entry and reporting `removed key → kept key`;
   - reports missing required fields per entry type, preprints that may have a published version, `et al` in author lists, and odd years.

   Options: `--fill-doi` looks up missing DOIs in Crossref and accepts only a near-exact title match with a matching year. `--rekey` regenerates keys as `authorYEARfirstword` (for example `vaswani2017attention`). `--sort` orders entries by key.
2. **Read the report** and act on each part:
   - *duplicates_merged*: replace the removed keys in the `.tex` files with the kept keys.
   - *keys_changed* (with `--rekey`): update every `\cite` accordingly. Only rekey when the user wants it; it touches the whole manuscript.
   - *problems*: fill missing fields from the publisher page or Crossref; replace preprints with the published version where one exists.
3. **Fix what the script cannot judge:**
   - Proper nouns with only an initial capital in titles (`{Bayesian}`, `{Markov}`, `{Europe}`): brace them by hand.
   - Venue names: use one form for each venue throughout (full name or the standard abbreviation, as the style requires).
   - Author names: `Last, First` form; `and` between authors; corporate authors in double braces `{{World Health Organization}}`; accents as Unicode with biber or as LaTeX commands with classic BibTeX.
   - Entry types: `@inproceedings` for conference papers, `@article` for journals, `@misc` with `eprint` and `archivePrefix` for arXiv preprints.
4. **Create entries for new references** from authoritative metadata:
   - By DOI: `curl -LH "Accept: application/x-bibtex" https://doi.org/<DOI>`.
   - By title: find the record with `paper-search`, then fetch by its DOI.
   - Publisher and DBLP exports are good; Google Scholar's BibTeX is often incomplete (missing pages, abbreviated venues) and needs checking.
5. **Compile** the document and clear the remaining BibTeX or biber warnings and any `[?]` citations.
6. **Replace the original only after the user agrees**, keeping a backup.

## Available Scripts

| Script | Purpose | Arguments |
|---|---|---|
| `scripts/clean_bibtex.py` | Normalizes entries, protects capitals in titles, merges duplicates, reports problems, optionally fills DOIs and regenerates keys | `BIBFILE` (required), `--out FILE` (required), `--strip FIELDS`, `--fill-doi`, `--rekey`, `--sort`, `--report FILE` |

Run a script with the agent's script tool, for example `run_script("scripts/clean_bibtex.py", args=[...])`, or from a shell in the skill folder with `python scripts/clean_bibtex.py ...`. Each script prints usage with `--help`, validates its arguments, and exits with a non-zero code and an `error:` message on failure.

## Output format

- *refs.clean.bib*, formatted one field per line with a consistent field order.
- A report:

```markdown
## BibTeX cleanup
Entries: 142 in, 135 out.

### Duplicates merged (update these \cite keys)
| Removed key | Kept key |

### DOIs added
### Problems to resolve
| Key | Problem | Suggested fix |

### Manual changes made
```

## Examples

Requests that should trigger this skill:

- "Clean my refs.bib exported from Zotero."
- "Remove duplicate entries from my bibliography."
- "My reference titles lose their capital letters in the PDF. Fix the BibTeX."
- "Add missing DOIs to my .bib file."
- "Generate a BibTeX entry for DOI 10.1038/nature14539."

Requests that belong to another skill:

- "Check these references actually exist." → use `citation-verifier`
- "Format my reference list in APA." → use `citation-style-converter`
- "Find papers on this topic." → use `paper-search`

### Worked example

**Request:** "Clean refs.bib (142 entries from Mendeley and Google Scholar), fill missing DOIs, and tell me which keys changed."

**What the agent does:**

1. Runs `run_script("scripts/clean_bibtex.py", args="refs.bib --out refs.clean.bib --fill-doi --report bib-report.json")`.
2. Reads the report: merged duplicates, DOIs added, and problems.
3. Replaces the removed duplicate keys in the `.tex` files.
4. Fixes proper nouns the script cannot detect and compiles to confirm no undefined citations.

**Result (excerpt):**

```markdown
{
  "entries_in": 142, "entries_out": 135,
  "duplicates_merged": {"vaswani2017b": "vaswani2017attention"},
  "dois_filled": {"devlin2019": "10.18653/v1/n19-1423"},
  "problems": {"vaswani2017": ["preprint: check whether a published version exists and cite that instead"], "smith2020": ["missing journal"]}
}
```

## Quality bar and pitfalls

- **Tell the user what leaves their machine.** The script sends reference titles and first-author surnames, and only when `--fill-doi` is used to the public APIs named under Prerequisites, and nothing else. If the topic is unpublished, confidential, or under embargo, say this before running and ask the user to confirm or to supply more general search terms.
- Never invent a missing field. Volume, pages, year, and DOI come from the publisher, Crossref, or DBLP, or stay empty and reported.
- The script writes to a new file and refuses to overwrite its input. Keep the original until the document compiles with the new file.
- Changing keys breaks citations. Report every changed key and update the `.tex` files in the same step.
- Duplicate detection by title and year can merge two distinct works with the same title (an arXiv version and a journal version are the same work; a paper and its erratum are not). Review the merge list.
- An entry being well formed does not make it real. Run `citation-verifier` on references of uncertain origin.
- Do not brace an entire title (`{{Whole Title}}`) to preserve case. It defeats the bibliography style; brace only the words that need it.
- A DOI filled by title search should be opened once to confirm it is the right paper.

## Limitations

- A well-formed entry is not necessarily a real one; existence is checked by `citation-verifier`.
- Capital protection catches words with inner capitals (BERT, ImageNet). Proper nouns with only an initial capital (Bayesian, Europe) must be braced by hand.
- Duplicate detection by title and year can merge distinct works that share a title, so the merge list needs review.
- The parser handles standard BibTeX. Unusual biblatex constructs may be passed through unchanged.

## Troubleshooting

| Problem | Likely cause | Solution |
|---|---|---|
| `error: --out must differ from the input so the original is kept` | The output path equals the input path | Choose a new file name such as *refs.clean.bib* |
| Citations become undefined after cleaning | Duplicate keys were merged or `--rekey` changed keys | Apply the `duplicates_merged` and `keys_changed` mappings to every `\cite` in the manuscript |
| `warning: Crossref lookup failed for <key>` | A network error or rate limit during `--fill-doi` | Rerun later; entries without a filled DOI are otherwise unchanged |
| An entry disappeared | It was merged as a duplicate of another | Check `duplicates_merged`; if the two are different works, give them distinct titles or DOIs and rerun |
| Two different works were merged (for example a paper and its erratum, or two editions of a book) | They share a title and year and neither has a DOI | Restore both from the original file, add each work's DOI or a distinguishing `year` or `edition`, and rerun; entries with different DOIs are never merged |
| A filled DOI points to the wrong paper | Another paper has a near-identical title | Open `https://doi.org/<doi>` and compare authors and venue; if it is wrong, delete the `doi` field and look the reference up by hand |
| Entries are missing from the output, or the count is lower than expected with no merges reported | Malformed BibTeX: an unbalanced brace or a missing comma ends parsing of that entry early | Compare `entries_in` with the number of `@` entries in the file, fix the brace or comma near the first missing key, and rerun |
| Accented names appear as `?` or garbled characters | The file is not UTF-8 (often Latin-1 from older reference managers) | Re-save the file as UTF-8, or keep LaTeX accent commands such as `{\"o}`, and rerun |

## Related skills

- `citation-verifier` to confirm entries exist and match their sources.
- `citation-style-converter` to render the list in APA, IEEE, Vancouver, or Harvard.
- `paper-search` to find records for new entries.
- `latex-paper-formatter` for the venue's bibliography setup.
- `annotated-bibliography-builder` uses the cleaned file.
- `camera-ready-checker` checks the final reference list.
