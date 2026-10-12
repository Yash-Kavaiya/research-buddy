---
name: topic-trend-analyzer
description: "Measures a research topic's trend from yearly publication counts and rising keywords in OpenAlex. Use when judging if a field is growing. Not for open problems; use research-gap-finder."
version: 1.0.0
compatibility: "Requires Python 3.10 or later. Makes read-only HTTPS requests to OpenAlex; sends only the search terms or identifiers given to it."
allowed-tools: "Bash(python:*) Read Write"
permissions: [network, env]
metadata:
  author: "Yash Kavaiya <yash.kavaiya3@gmail.com>"
  tags: [bibliometrics, trends, openalex]
---

# Topic Trend Analyzer

Answer "how is this topic moving?" with counts from OpenAlex, and separate real growth from the growth of the literature as a whole.

## Purpose

Answer "is this topic growing, flat, or fading" with numbers, and separate real growth from the growth of the literature as a whole. The output supports topic choice and the motivation paragraph of a proposal.

## When to use

- Choosing between topics, or deciding whether an area is rising, mature, or fading.
- Supporting a motivation paragraph with numbers.

Hand off instead when the user wants specific open problems (`research-gap-finder`) or the key papers (`citation-graph-explorer`).

## Prerequisites

- Python 3.10 or later; the script uses only the standard library.
- Network access to the OpenAlex API. No key is needed; set `OPENALEX_MAILTO` to a contact email for the polite pool.
- The topic as a phrase that appears in titles or abstracts, plus any alternative names.

## Inputs

- The topic as a phrase that would appear in a title or abstract. Ask for alternative names (for example "LLM" and "large language model").
- Year range. Default: the last 10 complete years.
- Optional comparison topics.

## Instructions

1. **Run the trend script** for the topic and for each synonym or comparison topic:

   ```bash
   python scripts/trend_counts.py "diffusion models" --from 2016
   python scripts/trend_counts.py "federated learning" --from 2018 --window 2 --format json
   ```

   - The query is matched as an exact phrase in titles and abstracts. Add `--fulltext` to match the words anywhere, which is wider and noisier.
   - The current year is excluded by default because it is incomplete.
   - `--window N` sets the length of the two periods compared for rising subtopics and keywords.
2. **Check the query is measuring the topic.** Look at the rising subtopics. If unrelated fields appear (a search for "transformer" returning electrical engineering), tighten the phrase and rerun.
3. **Read the three signals together:**
   - *Count per year*: raw volume.
   - *Share per 10,000 indexed papers*: volume relative to everything published. A rising count with a flat share means the topic is only keeping pace.
   - *Compound annual growth*: one number for the whole range. It hides shape, so look at the series too.
4. **Classify the stage**: emerging (small counts, fast growth), rapid growth, plateau (share flat for 2 or more years), or decline.
5. **Interpret the rising lists.** "under N" in the Earlier column means the group was outside the 200 largest in the earlier window, so its true count is unknown and below N. Treat such rows as "new or emerging", not as growth from zero.
6. **Add context** the counts cannot give: a landmark paper, dataset, or tool release that explains an inflection. Verify it with `paper-search` before stating it.
7. **Report** with the table, a plot if the user wants one (`publication-figure-maker`), and the caveats.

## Available Scripts

| Script | Purpose | Arguments |
|---|---|---|
| `scripts/trend_counts.py` | Counts papers per year, computes share per 10,000 indexed papers and compound growth, and ranks rising subtopics and keywords | `QUERY` (required), `--from YEAR`, `--to YEAR`, `--window N`, `--top N`, `--fulltext`, `--format md|json` |

Run a script with the agent's script tool, for example `run_script("scripts/trend_counts.py", args=[...])`, or from a shell in the skill folder with `python scripts/trend_counts.py ...`. Each script prints usage with `--help`, validates its arguments, and exits with a non-zero code and an `error:` message on failure.

## Output format

```markdown
## Trend: <topic>, <from> to <to>
Query: "<phrase>" in title and abstract (OpenAlex, retrieved <date>).

| Year | Papers | Share per 10,000 |
|---|---|---|

- Stage: <emerging | rapid growth | plateau | decline>
- Compound annual growth: <x>%
- Inflection: <year>, plausibly due to <verified event>, or "no clear cause identified"

## Rising subtopics
| Subtopic | Earlier window | Recent window | Change |

## Rising keywords
| Keyword | Earlier window | Recent window | Change |

## What this means for you
<two to four sentences tied to the user's decision>

## Caveats
```

## Reference files

Open these only when the step calls for them; they are not needed for every request.

- `references/reading-trend-data.md`: Read at steps 2 to 6, when checking the query, classifying the stage, and interpreting rising subtopics and keywords.
- `assets/trend-report-template.md`: Copy and fill for the trend report.

## Examples

Requests that should trigger this skill:

- "Is federated learning still a hot topic?"
- "Show publication trends for diffusion models since 2018."
- "Which subfields of quantum machine learning are emerging?"
- "Is research on blockchain in healthcare growing or saturated?"
- "I need numbers for my proposal showing interest in this area is rising."

Requests that belong to another skill:

- "What are the unsolved problems in this field?" → use `research-gap-finder`
- "Find the key papers on diffusion models." → use `paper-search`
- "Send me new papers every week." → use `weekly-paper-digest`

### Worked example

**Request:** "Is "diffusion models" still growing as a research topic? Give me numbers from 2019."

**What the agent does:**

1. Runs `run_script("scripts/trend_counts.py", args="'diffusion models' --from 2019")`.
2. Checks the rising subtopics to confirm the query is not also matching physical diffusion papers.
3. Reads count, share, and growth together, and classifies the stage.
4. Reports the table with caveats about indexing lag.

**Result (excerpt):**

```markdown
| Year | Papers | Share per 10,000 |
|---|---|---|
| 2022 | 2897 | 2.8 |
| 2023 | 6561 | 5.94 |
| 2024 | 12394 | 11.14 |

- Stage: rapid growth; share quadrupled from 2022 to 2024
- Compound annual growth in count, 2019 to 2025: 38%
- Caveat: the phrase also matches reaction-diffusion modelling before 2022, so early counts are inflated
```

## Quality bar and pitfalls

- **Tell the user what leaves their machine.** The script sends the topic phrase to the public APIs named under Prerequisites, and nothing else. If the topic is unpublished, confidential, or under embargo, say this before running and ask the user to confirm or to supply more general search terms.
- Report the exact query. Trend numbers are meaningless without it, and synonyms change counts by large factors.
- Always give the share alongside the count. Global publication volume grows every year.
- Recent years are undercounted because indexing lags. Flag the last complete year as provisional.
- Publication volume is not quality or opportunity. A crowded topic can still have gaps, and a quiet one can be quiet for good reason.
- OpenAlex topic and keyword labels are assigned automatically and can be wrong. Treat them as hints.
- Do not attribute an inflection to an event you have not verified.

## Limitations

- Counts depend entirely on the query phrase. Synonyms and acronyms are not merged automatically.
- OpenAlex returns only the 200 largest groups, so a rising keyword's earlier count may be known only as "under N".
- The most recent year is undercounted because of indexing lag, and OpenAlex topic labels are assigned automatically and can be wrong.
- Publication volume says nothing about research quality or about how many open problems remain.

## Troubleshooting

| Problem | Likely cause | Solution |
|---|---|---|
| Counts are far larger than expected | `--fulltext` was used, or the phrase is ambiguous across fields | Remove `--fulltext` and use a more specific phrase, for example "denoising diffusion" |
| Every rising keyword shows "under N" in the Earlier column | The earlier window is truncated to the top 200 groups | Treat those rows as new or emerging, or widen `--window` so the earlier period has more papers |
| `error: request failed after 3 attempts` | OpenAlex is unreachable or rate-limiting | Wait and rerun, and set `OPENALEX_MAILTO` to use the polite pool |

## Related skills

- `paper-search` to find the papers behind an inflection.
- `research-gap-finder` to look for open problems inside a rising subtopic.
- `publication-figure-maker` to plot the series.
- `venue-recommender` to see where the topic is being published.
- `weekly-paper-digest` to keep following the topic.
