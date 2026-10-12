---
name: novelty-checker
description: "Checks whether a research idea has been done by finding and comparing the closest prior work. Use before committing to an idea. Not for broad reading lists; use paper-search."
version: 1.0.0
compatibility: "Requires Python 3.10 or later. Makes read-only HTTPS requests to arXiv, OpenAlex, Semantic Scholar, and Crossref (PubMed only if selected with --sources); sends only the search terms or identifiers given to it."
allowed-tools: "Bash(python:*) Read Write"
permissions: [network, env]
metadata:
  author: "Yash Kavaiya <yash.kavaiya3@gmail.com>"
  tags: [novelty, prior-work, literature-search]
---

# Novelty Checker

Find the papers closest to an idea and report, for each, what overlaps and what does not. The output is an evidence-based judgement with stated limits, never a guarantee.

## Purpose

Tell a researcher how close existing work is to their idea, with the specific papers and the specific differences, before they invest months in it. It also produces a novelty statement that can be defended in a proposal or rebuttal.

## When to use

- Before the user commits time to an idea.
- When a proposal, introduction, or rebuttal needs a defensible novelty claim.

Hand off instead when the user has no specific idea yet (`research-gap-finder`) or wants a broad reading list (`paper-search`).

## Prerequisites

- Python 3.10 or later; the script uses only the standard library.
- Network access to arXiv, OpenAlex, Semantic Scholar, and Crossref. No API key is needed; `S2_API_KEY` and `OPENALEX_MAILTO` raise rate limits.
- The idea stated in one or two sentences.

## Inputs

- The idea in one or two sentences. If it is vague, restate it as: *task or problem* + *method or intervention* + *setting or data* + *claimed benefit*, and confirm.
- Field, and any papers the user already knows are close.

## Instructions

1. **Decompose the idea** into its components (problem, method, setting, benefit). Novelty usually lives in one component or in their combination, so name which.
2. **Write 4 to 6 query phrasings**: the user's own terms, standard field terms, synonyms and older names for the method, the problem alone, the method alone, and the method applied in a neighbouring setting.
3. **Confirm, then run the search.** Unpublished ideas are sensitive: tell the user that the query phrasings (not the full idea text) will be sent to public scholarly APIs, and proceed once they agree or after rewording the queries in general terms.

   ```bash
   python scripts/closest_work.py --idea "<idea>" \
     --query "<phrasing 1>" --query "<phrasing 2>" --query "<phrasing 3>" --top 15
   ```

   The script searches arXiv, OpenAlex, Semantic Scholar, and Crossref, merges duplicates, and ranks by term overlap and by how many phrasings found each paper. Add `--sources pubmed,openalex` for biomedical ideas. A warning about a failed source means that source was not searched; say so in the report.
4. **Read the top candidates.** Open the abstract of the top 10, and the method section of the top 3 to 5. The ranking is lexical, so a low-ranked paper with different vocabulary can still be the closest. Scan all returned titles.
5. **Chase one hop.** For the 2 closest papers, check their recent citing papers with `citation-graph-explorer`. Follow-up work is where an idea is most often already done.
6. **Compare component by component** in a table, one row per close paper.
7. **Give a verdict** from this scale, with the reason:
   - *Already done*: a paper does the same thing in the same setting.
   - *Incremental*: same approach with a minor change in data or setting.
   - *Differentiated*: a clear difference in at least one component that would change the result or its use.
   - *No close work found*: nothing within the searched sources. State this as a search result, not a fact about the world.
8. **Suggest how to sharpen** the idea so the difference is larger or easier to defend.

## Available Scripts

| Script | Purpose | Arguments |
|---|---|---|
| `scripts/closest_work.py` | Searches several query phrasings, merges duplicates, and ranks papers by term overlap with the idea | `--idea TEXT` (required), `--query TEXT` (repeat 3 to 6 times), `--sources`, `--limit`, `--top`, `--format md|json` |

Run a script with the agent's script tool, for example `run_script("scripts/closest_work.py", args=[...])`, or from a shell in the skill folder with `python scripts/closest_work.py ...`. Each script prints usage with `--help`, validates its arguments, and exits with a non-zero code and an `error:` message on failure.

## Output format

```markdown
## Idea
<restated: problem + method + setting + benefit>

## Search performed
Sources: ... (failed: ...). Queries: ... Date: <today>.

## Closest prior work
| # | Paper (year) | Same problem | Same method | Same setting | What differs |
|---|---|---|---|---|---|

## Verdict: <already done | incremental | differentiated | no close work found>
<two to four sentences of reasoning naming the papers>

## Novelty statement you can defend
> Unlike <A> and <B>, which ..., this work ...

## What this check did not cover
- <unsearched venues, non-English work, patents, papers under review, very recent preprints>

## Ways to sharpen the idea
```

## Reference files

Open these only when the step calls for them; they are not needed for every request.

- `references/query-design-and-verdicts.md`: Read at steps 2 and 6 to 8, when writing query phrasings, comparing papers component by component, and choosing the verdict.
- `assets/novelty-report-template.md`: Copy and fill for the novelty report.

## Examples

Requests that should trigger this skill:

- "Has anyone already used contrastive pretraining on ECG signals for arrhythmia detection?"
- "Is my idea novel? I want to use graph neural networks to predict bus delays."
- "Find the closest prior work to this abstract."
- "Check novelty before I start: LLM-generated unit tests ranked by mutation score."
- "A reviewer says this was done before. Can you check?"

Requests that belong to another skill:

- "Find me papers on arrhythmia detection." → use `paper-search`
- "What are the open problems in ECG analysis?" → use `research-gap-finder`
- "Write my related work section." → use `related-work-writer`

### Worked example

**Request:** "Check whether this is new: contrastive pretraining on unlabeled ECG signals to detect arrhythmia with few labels."

**What the agent does:**

1. Splits the idea into problem (arrhythmia detection), method (contrastive pretraining), setting (few labels), and benefit.
2. Writes four phrasings and runs `run_script("scripts/closest_work.py", ...)` with them.
3. Reads the abstracts of the top 10 results and the method sections of the top 3, then checks recent papers citing the two closest.
4. Fills the comparison table and gives a verdict with its limits.

**Result (excerpt):**

```markdown
| # | Paper (year) | Same problem | Same method | Same setting | What differs |
|---|---|---|---|---|---|
| 1 | Analysis of Augmentations for Contrastive ECG Representation Learning (2022) | yes | yes | partly | studies augmentations; no few-label arrhythmia benchmark |

## Verdict: incremental
Contrastive pretraining for ECG is established (papers 1 to 3). The few-label arrhythmia setting is evaluated in paper 2 on one dataset. A defensible contribution needs a difference beyond a new dataset.
```

## Quality bar and pitfalls

- **Tell the user what leaves their machine.** The script sends the search queries derived from the idea (the full idea text stays local and is used only for ranking) to the public APIs named under Prerequisites, and nothing else. If the topic is unpublished, confidential, or under embargo, say this before running and ask the user to confirm or to supply more general search terms.
- Never say "this is novel" without qualification. Say what was searched, when, and what was found.
- Every paper in the table must be a retrieved record with a working link. Do not fill the table from memory.
- Different terminology hides prior work. If all queries share the same key term, the search is too narrow.
- Check dates. A preprint from last month can overturn the verdict; sort one search by date.
- Same method on a new dataset is usually incremental. Say so, and say what would make it more than that.
- Patents, theses, and industry reports are not covered by these sources. List that under limits when it matters.

## Limitations

- The ranking is lexical. Prior work that uses different vocabulary can rank low or be missed, so all returned titles must be scanned.
- Patents, theses, industry reports, non-English work, and papers under review are not covered.
- A verdict of "no close work found" describes the search, not the world. It cannot guarantee novelty.

## Troubleshooting

| Problem | Likely cause | Solution |
|---|---|---|
| `warning: semantic_scholar failed ... 429` | Semantic Scholar rate-limits requests without a key | Wait a minute and rerun, set `S2_API_KEY`, or rerun with `--sources arxiv,openalex,crossref` and report that source as not searched |
| All top results are off-topic | The queries share one ambiguous term | Add a domain word to each query and include one query that uses the method's older or alternative name |
| The script exits with code 1 and prints nothing | No source returned results for any query | Shorten each query to 2 to 4 words; arXiv requires every word to match |

## Related skills

- `paper-search` for broader or source-specific searching.
- `citation-graph-explorer` to check follow-up work on the closest papers.
- `research-gap-finder` when the idea turns out to be done and the user needs a new direction.
- `related-work-writer` to turn the comparison table into a related-work section.
- `research-question-formulator` to rewrite the question after sharpening the idea.
