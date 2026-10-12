---
name: citation-graph-explorer
description: "Follows citations backward and forward from seed papers and ranks shared references as seminal candidates. Use when expanding from known papers. Not for keyword search; use paper-search."
version: 1.0.0
compatibility: "Requires Python 3.10 or later. Makes read-only HTTPS requests to OpenAlex; sends only the search terms or identifiers given to it."
allowed-tools: "Bash(python:*) Read Write"
permissions: [network, env]
metadata:
  author: "Yash Kavaiya <yash.kavaiya3@gmail.com>"
  tags: [citations, snowballing, openalex, seminal-papers]
---

# Citation Graph Explorer

Start from papers the user trusts and walk the citation graph in both directions. This finds work that keyword search misses because it uses different vocabulary.

## Purpose

Start from papers the user trusts and find what they build on and what builds on them. Citation chasing reaches relevant work that keyword search misses because it uses different vocabulary.

## When to use

- The user has one to five good papers and wants the rest of the conversation around them.
- Finding the foundations of an area, or the latest work building on a result.
- The snowballing step of a systematic review.

Hand off instead when there are no seed papers yet (`paper-search`).

## Prerequisites

- Python 3.10 or later; the script uses only the standard library.
- Network access to the OpenAlex API (no key needed).
- One to five seed papers identified by DOI or OpenAlex work id. Titles must be resolved to DOIs first with `paper-search`.

## Inputs

- Seed papers as DOIs or OpenAlex work ids. If the user gives titles, resolve them to DOIs with `paper-search` first and confirm each match.
- Direction of interest: foundations (backward), follow-ups (forward), or both.
- How many papers to list per direction (default 10).

## Instructions

1. **Resolve seeds** to DOIs. For arXiv-only papers use the arXiv DOI form `10.48550/arXiv.<id>`.
2. **Run the explorer:**

   ```bash
   python scripts/citation_graph.py 10.18653/v1/N19-1423 --top 10
   python scripts/citation_graph.py 10.18653/v1/N19-1423 W2963403868 --top 15 --format json
   ```

   For each seed it lists the most-cited references and the most-cited citing papers. Across seeds it ranks references by how many seeds cite them, then by citation count: the seminal-paper candidates. `--max-refs` caps references fetched per seed (default 200).
3. **Use two or more seeds** when the goal is seminal papers. With one seed the "seminal" list is only that paper's most-cited references, which is dominated by general classics (datasets, optimizers).
4. **Filter by role.** Read the title and abstract of each listed paper, and how the seed cites it where the full text is available, then mark it as one of:
   - *Foundation*: the seed builds on its idea, model, or result (it appears in the seed's method or motivation).
   - *General tool*: a dataset, metric, optimizer, or software library cited across many unrelated topics.
   - *Tangential*: cited in passing for background.

   Keep foundations, drop general tools unless the user wants them, and list tangential papers only on request. Use `paper-summarizer` on any paper whose role is unclear from the abstract.
5. **Look for recent follow-ups separately.** The forward list is sorted by citations, so it favours older papers. For the newest follow-ups, search with `paper-search` using the seed's method name and a recent `--year-from`.
6. **Go one more hop** only on the two or three most relevant new papers. Unbounded snowballing grows quickly and drifts off topic.
7. **Report** the lineage: what the seeds build on, what builds on them, and which papers the user should read first.

## Available Scripts

| Script | Purpose | Arguments |
|---|---|---|
| `scripts/citation_graph.py` | Fetches each seed's references and most-cited citing papers, and ranks references by how many seeds cite them | `SEEDS...` (DOIs or OpenAlex ids, required), `--top N`, `--max-refs N`, `--format md|json` |

Run a script with the agent's script tool, for example `run_script("scripts/citation_graph.py", args=[...])`, or from a shell in the skill folder with `python scripts/citation_graph.py ...`. Each script prints usage with `--help`, validates its arguments, and exits with a non-zero code and an `error:` message on failure.

## Output format

```markdown
## Seeds
1. Title (year), DOI, N citations, R references

## Foundations (backward)
| Paper (year) | Cited by seeds | Citations | Role |
|---|---|---|---|

## Follow-up work (forward)
| Paper (year) | Citations | What it adds to the seed |
|---|---|---|

## Suggested reading order
1. ... because ...

## Coverage notes
- Seeds whose reference lists were missing or incomplete in OpenAlex
- Hops performed
```

## Reference files

Open these only when the step calls for them; they are not needed for every request.

- `references/snowballing-method.md`: Read at steps 3 to 7, when choosing seeds, deciding how far to chase citations, and classifying what comes back.
- `assets/citation-map-template.md`: Copy and fill to report the lineage around the seed papers.

## Examples

Requests that should trigger this skill:

- "What are the foundational papers behind BERT?"
- "Who has cited this paper: 10.18653/v1/N19-1423?"
- "Snowball from these three papers for my review."
- "Find follow-up work to the original Transformer paper."
- "Trace the lineage of diffusion models from these seeds."

Requests that belong to another skill:

- "Find papers on language model pretraining." → use `paper-search`
- "How is this topic trending?" → use `topic-trend-analyzer`
- "Summarise these papers." → use `paper-summarizer`

### Worked example

**Request:** "I have the BERT paper (10.18653/v1/N19-1423). What does it build on and what are the main follow-ups?"

**What the agent does:**

1. Confirms the DOI resolves to the BERT paper.
2. Runs `run_script("scripts/citation_graph.py", args="10.18653/v1/N19-1423 --top 10")`.
3. Labels each reference as a foundation of the topic or a general tool, and drops general tools such as ImageNet.
4. Runs a dated `paper-search` for the newest follow-ups, since the forward list favours older papers.

**Result (excerpt):**

```markdown
## Foundations (backward)
| Paper (year) | Citations | Role |
|---|---|---|
| Attention Is All You Need (2017) | 26920 | architecture BERT is built on |
| GloVe: Global Vectors for Word Representation (2014) | 33881 | earlier static embeddings it replaces |

## Coverage notes
- 52 references found in OpenAlex for this seed; the year shown for one record was wrong in the index and was corrected from the publisher page
```

## Quality bar and pitfalls

- **Tell the user what leaves their machine.** The script sends the DOIs or work ids of the seed papers to the public APIs named under Prerequisites, and nothing else. If the topic is unpublished, confidential, or under embargo, say this before running and ask the user to confirm or to supply more general search terms.
- Confirm each seed resolved to the intended paper. The script prints the seed's title; a wrong DOI silently explores the wrong graph.
- OpenAlex reference lists are incomplete for some papers, especially preprints and older scans. A seed showing 0 references is a data problem; try the published version's DOI.
- Records for famous preprints are sometimes duplicated with odd years or DOIs. Cross-check a surprising year against the publisher page before quoting it.
- Citation counts measure attention, not correctness. A highly cited paper may be the one everyone criticises.
- Forward citations lag. Papers from the last few months have few or none; use a dated keyword search for those.
- Describe what a citing paper adds only after reading its abstract.

## Limitations

- OpenAlex reference lists are incomplete for some papers, especially preprints, so a seed can show few or no references.
- With a single seed the seminal list is just its most-cited references, which is dominated by general classics.
- Forward lists are sorted by citation count and miss work from the last few months.
- Citation counts measure attention, not correctness.

## Troubleshooting

| Problem | Likely cause | Solution |
|---|---|---|
| `error: 404 Not Found` | The DOI is not in OpenAlex, or it has a typo | Check the DOI; for arXiv-only papers use `10.48550/arXiv.<id>`; otherwise find the OpenAlex id with `paper-search` |
| A seed shows 0 references | OpenAlex has no reference list for that record | Use the DOI of the published version instead of the preprint |
| The seminal list is all datasets and optimizers | Only one seed was given | Add two or more seeds from the same topic so shared references rise to the top |

## Related skills

- `paper-search` to resolve seeds and to find very recent follow-ups.
- `paper-summarizer` for the papers selected for reading.
- `systematic-review-prisma` uses this for backward and forward snowballing.
- `literature-review-writer` and `related-work-writer` to write up the lineage.
- `novelty-checker` uses this to check follow-ups of the closest prior work.
