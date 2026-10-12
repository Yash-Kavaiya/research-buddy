---
name: paper-search
description: "Searches arXiv, Semantic Scholar, OpenAlex, PubMed, and Crossref for papers and returns de-duplicated records. Use when references on a topic are needed. Not for citation chasing."
version: 1.0.0
compatibility: "Requires Python 3.10 or later. Makes read-only HTTPS requests to arXiv, Semantic Scholar, OpenAlex, PubMed, and Crossref; sends only the search terms or identifiers given to it."
allowed-tools: "Bash(python:*) Read Write"
permissions: [network, env, file_write]
metadata:
  author: "Yash Kavaiya <yash.kavaiya3@gmail.com>"
  tags: [literature-search, arxiv, openalex, pubmed, crossref]
---

# Paper Search

Retrieve real paper records from free scholarly APIs. No API key is needed. This is the base skill other research skills call whenever they need papers.

## Purpose

Retrieve real paper records, with authors, year, venue, DOI, link, abstract, and citation count, from five free scholarly indexes. It is the base skill the other research skills call whenever a claim about the literature needs a retrieved record behind it.

## When to use

- Any request for papers, references, or reading lists.
- Finding a specific paper from a partial title, author, or DOI.
- Whenever a claim about the literature needs a retrieved record behind it.

Hand off instead for citation chasing from known papers (`citation-graph-explorer`) or a protocol-driven search for a systematic review (`systematic-review-prisma`).

## Prerequisites

- Python 3.10 or later; the script uses only the standard library.
- Network access. No API key is needed. Optional: `OPENALEX_MAILTO`, `S2_API_KEY`, `NCBI_API_KEY` for higher rate limits.
- A topic expressed as short keyword queries.

## Inputs

- Topic or question. Convert questions into keyword queries.
- Field, which decides the sources.
- Year range, and whether the user wants seminal work, recent work, or both.
- How many papers they want back.

## Instructions

1. **Pick sources by field.**

   | Field | Sources |
   |---|---|
   | CS, ML, physics, maths, statistics | `arxiv,semantic_scholar,openalex` |
   | Biomedicine, health, life sciences | `pubmed,openalex,crossref` |
   | Social sciences, humanities, engineering, other | `openalex,crossref,semantic_scholar` |
   | Unknown or interdisciplinary | all five (the default) |

2. **Write 2 to 4 queries**, not one: the user's terms, the field's standard terms, and a synonym or acronym variant. Short keyword queries work better than sentences.
3. **Run the search:**

   ```bash
   python scripts/search_papers.py "retrieval augmented generation" --limit 10 --format md --abstracts 300
   python scripts/search_papers.py "CRISPR off-target effects" --sources pubmed,openalex --year-from 2021 --sort citations
   python scripts/search_papers.py "graph neural networks survey" --format json --out results.json
   ```

   Options: `--sources`, `--limit` (per source), `--year-from`, `--year-to`, `--sort relevance|citations|year`, `--format json|md`, `--abstracts N`, `--out FILE`.
4. **Check the warnings.** A source that fails (Semantic Scholar often rate-limits without a key) is reported on stderr and in the `errors` field. Retry it once after a pause, or state that it was not searched.
5. **Screen the results.** Lexical search returns papers that share words, not meaning, so check each hit against the user's question. Keep a paper when its title or abstract addresses the same problem, method, or population; drop it when the shared words carry a different sense (for example "transformer" in electrical engineering), when it falls outside the requested years or field, or when it is a duplicate record. If more than about half the hits are dropped, the query is too loose: add a domain term and run it again.
6. **Fill gaps.** Check the kept set for these gaps and run one targeted search for each that applies:
   - No survey or review: search the topic with "survey" or "review".
   - Nothing from the last two years: rerun with `--year-from` and `--sort year`.
   - A paper the user named or that several results cite is missing: search its exact title.
   - Only one research group or venue appears: search a synonym or the method's alternative name.

   For the two or three key papers, follow up with `citation-graph-explorer`. State any gap that remains.
7. **Present** the kept papers grouped by sub-theme or by role (survey, seminal, recent), with one line each on why it is relevant.

Optional environment variables for higher rate limits: `OPENALEX_MAILTO` (contact email), `S2_API_KEY`, `NCBI_API_KEY`. Never print their values.

## Available Scripts

| Script | Purpose | Arguments |
|---|---|---|
| `scripts/search_papers.py` | Queries the selected sources, merges duplicate records by DOI or title, filters by year, and sorts | `QUERY` (required), `--sources`, `--limit`, `--year-from`, `--year-to`, `--sort relevance|citations|year`, `--format json|md`, `--abstracts N`, `--out FILE` |

Run a script with the agent's script tool, for example `run_script("scripts/search_papers.py", args=[...])`, or from a shell in the skill folder with `python scripts/search_papers.py ...`. Each script prints usage with `--help`, validates its arguments, and exits with a non-zero code and an `error:` message on failure.

## Output format

```markdown
## Papers on <topic>
Searched: <sources> on <date>. Queries: "...", "...". Not searched: <failed sources>.

### <Group, e.g. Surveys>
1. **Title** (year). First Author et al. *Venue*. <link> (N citations)
   Why relevant: <one line>

### <Group, e.g. Recent methods>
...

## Notes
- <gaps, missing full text, suggested follow-up searches>
```

When another skill is the consumer, pass the JSON file path instead.

## Reference files

Open these only when the step calls for them; they are not needed for every request.

- `references/search-syntax-and-strategy.md`: Read at steps 1 to 3 and 6, when choosing sources, writing queries in each database's syntax, and widening or narrowing a search.
- `assets/search-log-template.md`: Copy and fill to report a search and its results.

## Examples

Requests that should trigger this skill:

- "Find papers on retrieval augmented generation for question answering."
- "Search the literature on CRISPR off-target effects since 2021."
- "Get me the most cited surveys on graph neural networks."
- "Find the paper titled Attention Is All You Need and give me its DOI."
- "I need 15 recent references on microplastics in drinking water."

Requests that belong to another skill:

- "Who cited this paper?" → use `citation-graph-explorer`
- "Run a PRISMA systematic review search." → use `systematic-review-prisma`
- "Are these references real?" → use `citation-verifier`

### Worked example

**Request:** "Find recent papers on retrieval augmented generation in medicine."

**What the agent does:**

1. Chooses PubMed, OpenAlex, and Crossref because the topic is biomedical, and writes three short queries.
2. Runs `run_script("scripts/search_papers.py", args="'retrieval augmented generation medicine' --sources pubmed,openalex,crossref --year-from 2023 --format md --abstracts 300")`.
3. Reads titles and abstracts, drops off-topic hits, and groups the rest.
4. Notes that Semantic Scholar was not searched.

**Result (excerpt):**

```markdown
### Reviews
1. **Retrieval augmented generation for large language models in healthcare: A systematic review** (2025). Amugongo LM et al. *PLOS Digital Health*. https://pubmed.ncbi.nlm.nih.gov/...
   Why relevant: maps the field and lists evaluation gaps

### Benchmarks
2. **Benchmarking Retrieval-Augmented Generation for Medicine** (2024). Guangzhi Xiong et al. https://doi.org/10.18653/v1/2024.findings-acl.372 (276 citations)
```

## Quality bar and pitfalls

- **Tell the user what leaves their machine.** The script sends the search query to the public APIs named under Prerequisites, and nothing else. If the topic is unpublished, confidential, or under embargo, say this before running and ask the user to confirm or to supply more general search terms.
- Only report papers the script returned. Never add a paper from memory without retrieving its record; if you believe one exists, search for it by title.
- Report every field as retrieved. If the venue or DOI is empty, leave it empty.
- Citation counts differ between sources and favour older papers. Use them to find landmarks, not to rank recent work.
- arXiv requires every query word to appear, so long queries return little. Use 2 to 4 words there.
- PubMed accepts its own syntax (`"term"[tiab]`, MeSH, AND/OR). Use it for biomedical precision.
- Crossref covers the most publishers and has the weakest relevance ranking. It is best for exact titles and pasted reference strings.
- Preprints and their published versions may appear as two records when their DOIs and titles differ. Merge them by hand and cite the published version.
- Do not help bypass paywalls. Point to open-access versions (arXiv, PubMed Central, the OpenAlex landing page) when they exist.

## Limitations

- Coverage is limited to the five indexes. Subscription databases such as Scopus and Web of Science, and most books, are not searched.
- Search is lexical. Papers that use different terms for the same idea are missed unless a query uses those terms.
- Citation counts differ between sources and favour older papers.
- Abstracts are missing for some records, especially from Crossref and PubMed summaries.

## Troubleshooting

| Problem | Likely cause | Solution |
|---|---|---|
| `warning: semantic_scholar failed: ... HTTP 429` | Semantic Scholar rate-limits unauthenticated requests | Retry after a minute, set `S2_API_KEY`, or drop that source and report it as not searched |
| arXiv returns nothing for a long query | arXiv requires every query word to appear | Shorten the query to 2 to 4 words or use field syntax such as `ti:` and `cat:` |
| The same paper appears twice | A preprint and its published version have different DOIs and titles | Merge them by hand and cite the published version |
| Exit code 1 with no papers | Every selected source failed, usually a network problem | Check connectivity and rerun; the stderr warnings name each failed source |

## Related skills

- `citation-graph-explorer` to expand from the best hits.
- `paper-summarizer` and `paper-comparison-matrix` to digest what was found.
- `annotated-bibliography-builder` and `literature-review-writer` to write from the results.
- `bibtex-manager` to turn chosen papers into clean BibTeX.
- `citation-verifier` to check references that came from elsewhere.
