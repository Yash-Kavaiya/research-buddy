# Search syntax and strategy by source

## 1. What each source is good for

| Source | Coverage | Strengths | Weaknesses |
|---|---|---|---|
| arXiv | Preprints in physics, maths, CS, statistics, quantitative biology and finance, EESS, economics | Newest work; full text free; field syntax | Not peer reviewed; no citation counts; every word must match |
| Semantic Scholar | Broad, strong in CS and biomedicine | Citation counts, abstracts, relevance ranking | Rate-limits without a key |
| OpenAlex | Very broad, all fields | Filters, citation counts, open-access links, no key | Some duplicate and mis-dated records |
| PubMed | Biomedicine and life sciences | MeSH indexing, precise field tags | Abstracts need a second call; biomedical only |
| Crossref | Any work with a DOI, all publishers | Best for exact titles and pasted references | Weak relevance ranking; many records lack abstracts |

## 2. Query syntax

### arXiv

| Need | Syntax | Example |
|---|---|---|
| Title words | `ti:` | `ti:"graph neural"` |
| Abstract words | `abs:` | `abs:hallucination` |
| Author | `au:` | `au:bengio` |
| Category | `cat:` | `cat:cs.CL` |
| Combine | `AND`, `OR`, `ANDNOT` | `cat:cs.CL AND abs:retrieval ANDNOT ti:survey` |
| Phrase | double quotes | `all:"few-shot learning"` |

A plain query is searched as all words required. Keep it to two to four words.

### PubMed

| Need | Syntax | Example |
|---|---|---|
| Title or abstract | `[tiab]` | `"machine learning"[tiab]` |
| MeSH heading | `[Mesh]` | `"Diabetes Mellitus, Type 2"[Mesh]` |
| Publication type | `[pt]` | `randomized controlled trial[pt]` |
| Date | `[dp]` | `2021:2025[dp]` |
| Truncation | `*` | `diagnos*[tiab]` |
| Combine | `AND`, `OR`, `NOT` with parentheses | `(A[tiab] OR B[Mesh]) AND C[tiab]` |

### OpenAlex and Semantic Scholar

Free-text queries. The script adds year filters and sorting. For OpenAlex, phrases in double quotes match exactly.

### Crossref

Paste the title, or the whole reference string. It matches bibliographic fields, so author surname plus title words works well.

## 3. Building queries

1. Split the topic into two or three concepts (for example: *retrieval augmentation*, *question answering*, *medicine*).
2. List synonyms and acronyms for each concept.
3. Write one query per plausible phrasing instead of one long query. Long queries fail on arXiv and blur ranking elsewhere.
4. Run the most specific query first. If it returns under 10 relevant papers, drop the least important concept.

| Result problem | Adjustment |
|---|---|
| Too many, off-topic | Add the third concept; restrict years; switch to title search (`ti:`, `[ti]`) |
| Too few | Remove a concept; use the broader term; add synonyms with OR; drop the year filter |
| Right topic, wrong kind of paper | Add "survey" or "review", "benchmark", "dataset", or a method name |
| Known paper missing | Search its exact title; it may be indexed under a different term |

## 4. Finding specific things

| Looking for | Do this |
|---|---|
| A survey to start from | Query plus "survey" or "review"; sort by citations; prefer the last three years |
| The seminal paper | Sort by citations with no year filter, then confirm with citation-graph-explorer |
| The newest work | Year filter on the last one or two years; sort by year; include arXiv |
| A paper from a partial title | Crossref with the title fragment and an author surname |
| A DOI's metadata | Crossref lookup by DOI (bibtex-manager can fetch BibTeX) |
| An open-access copy | The OpenAlex landing page, arXiv, PubMed Central, or the author's institutional repository |

## 5. Screening results

Read the title and abstract of each hit and assign one of three labels.

| Label | Rule |
|---|---|
| Keep | Addresses the topic directly |
| Maybe | Related; decide after reading the introduction |
| Drop | Shares words but not the subject |

Record how many were returned, kept, and dropped, and the reason for the commonest drop. That count is the honest answer to "how much is there on this".

## 6. Judging a record

| Signal | Use | Caution |
|---|---|---|
| Citation count | Finds landmarks | Favours old papers; differs by source and field |
| Venue | Indicates peer review and audience | Good work appears in modest venues, and the reverse |
| Preprint only | May be the newest result | Not reviewed; check for a published version |
| Retraction or correction notice | Disqualifies or qualifies the paper | Check the publisher page for key papers |
| Found by several sources | More likely a real, well-indexed record | Not a quality signal |

## 7. Recording the search

Keep, for every search you report: date, sources (including any that failed), the exact queries, filters, and counts returned and kept. Without this the search cannot be repeated or defended.
