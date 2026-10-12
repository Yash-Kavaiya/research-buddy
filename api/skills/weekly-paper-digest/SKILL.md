---
name: weekly-paper-digest
description: "Produces a recurring digest of new arXiv and OpenAlex papers for saved queries, skipping papers already reported. Use for literature alerts. Not for full literature searches; use paper-search."
version: 1.0.0
compatibility: "Requires Python 3.10 or later. Makes read-only HTTPS requests to arXiv and OpenAlex; sends only the search terms or identifiers given to it."
allowed-tools: "Bash(python:*) Read Write"
permissions: [network, env, file_write]
metadata:
  author: "Yash Kavaiya <yash.kavaiya3@gmail.com>"
  tags: [literature-alerts, arxiv, digest, current-awareness]
---

# Weekly Paper Digest

Keep the user current with a short, filtered list of new papers, generated the same way each time so nothing is repeated and little is missed.

## Purpose

Keep a researcher current with a short, filtered list of new papers, generated the same way each time so nothing is repeated. The script fetches and ranks; the agent selects what matters for this user and says why.

## When to use

- The user wants regular updates on one or more topics.
- A one-off "what appeared recently on X".
- Watching for competing or concurrent work during a project.

Hand off instead for a full literature search (`paper-search`) or long-term trend analysis (`topic-trend-analyzer`).

## Prerequisites

- Python 3.10 or later; the script uses only the standard library.
- Network access to arXiv and OpenAlex (no key needed; `OPENALEX_MAILTO` recommended).
- Two to six search queries, and a writable folder for the state file and saved digests. Scheduling needs cron, Task Scheduler, or the agent's scheduling command.

## Inputs

- Topics, as 2 to 6 search queries. Ask for the terms the user's community uses, and for arXiv categories if relevant (*cs.CL*, *stat.ML*, *q-bio.GN*).
- Period (default 7 days) and how many papers they want to see (default: top 10 to 15).
- Terms that raise priority: methods, datasets, or author groups the user follows.
- Where the digest should go: a file in the project, or a message.
- Whether it should run on a schedule.

## Instructions

1. **Write the queries.** Keep each to a phrase of 2 to 4 words. For arXiv, field syntax narrows results: `cat:cs.CL AND all:hallucination`, `ti:"graph neural"`, `au:lastname`. Plain phrases are searched as all words required on arXiv and as an exact phrase in title or abstract on OpenAlex.
2. **Save a config file** so every run uses the same settings:

   ```json
   {
     "queries": ["retrieval augmented generation", "cat:cs.CL AND all:hallucination"],
     "days": 7,
     "sources": ["arxiv", "openalex"],
     "max_per_query": 15,
     "boost": ["benchmark", "survey", "low-resource"]
   }
   ```

3. **Run the digest:**

   ```bash
   python scripts/digest.py --config digest.json --out digest-2026-03-09.md
   python scripts/digest.py --query "diffusion models" --query "cat:cs.CV AND all:video generation" --days 7
   ```

   The script fetches the newest arXiv submissions and recent OpenAlex articles and preprints per query, keeps those dated within the period (future-dated records are discarded), merges duplicates across queries and sources, drops anything recorded in the state file from earlier runs, and ranks by number of matching queries, then boost terms, then date. The state file is updated after each run; `--no-state` leaves it untouched for a trial run.
4. **Check the output.** If a source failed, the digest says so at the top; that source is not covered for this period, so rerun or note it. If results are off-topic, tighten the query; if empty, loosen it or lengthen the period.
5. **Curate.** Read the titles and abstracts returned. Select the papers that matter for this user and write one or two lines for each: what it does and why it is relevant to their work. Base this on the abstract, and say so; open the paper for anything that looks important or competing.
6. **Flag what needs action**: a paper that overlaps the user's current project (suggest `novelty-checker`), a new dataset or baseline, a survey worth reading in full.
7. **Deliver** the digest in the format below and save it next to earlier digests.
8. **Schedule it** if asked:
   - In Claude Code, use the `/schedule` command (or `/loop` within a session) with a prompt such as "Run the weekly-paper-digest skill with digest.json and save to digests/".
   - With cron: `0 8 * * 1 cd /path/to/project && python /path/to/scripts/digest.py --config digest.json --out digests/$(date +\%F).md`
   - On Windows, a Task Scheduler job running the same command weekly.

   A scheduled script run produces the raw list; the curation in step 5 needs an agent run.
9. **Review the queries every month or two**: add terms from papers the user found useful, and drop queries that only return noise.

## Available Scripts

| Script | Purpose | Arguments |
|---|---|---|
| `scripts/digest.py` | Fetches recent papers per query, drops those already reported, ranks them, and writes a Markdown digest | `--config FILE`, `--query TEXT` (repeatable), `--days N`, `--sources arxiv,openalex`, `--max-per-query N`, `--boost TERMS`, `--state FILE`, `--no-state`, `--out FILE` |

Run a script with the agent's script tool, for example `run_script("scripts/digest.py", args=[...])`, or from a shell in the skill folder with `python scripts/digest.py ...`. Each script prints usage with `--help`, validates its arguments, and exits with a non-zero code and an `error:` message on failure.

## Output format

```markdown
# Paper digest: 2026-03-02 to 2026-03-09
Queries: `...`; `...`. Sources: arXiv, OpenAlex. <N> new papers; <k> selected.

## Read first
1. **Title** (authors, date, venue or arXiv id) <link>
   What: ...  Why it matters to you: ...
   Based on: abstract | full text

## Also relevant
- **Title** <link>: one line

## Needs action
- <paper> overlaps with your current project on X: run a novelty check.

## Not covered this period
- <source that failed, or none>
```

## Examples

Requests that should trigger this skill:

- "Send me new papers on retrieval augmented generation every week."
- "Set up a weekly arXiv digest for cs.CL hallucination papers."
- "What's new in graph neural networks this week?"
- "Track new papers on perovskite solar cells."
- "Keep me updated on work that competes with my project."

Requests that belong to another skill:

- "Find the key papers on this topic from the last five years." → use `paper-search`
- "How has this topic trended over a decade?" → use `topic-trend-analyzer`
- "Summarise this paper." → use `paper-summarizer`

### Worked example

**Request:** "Weekly digest for "retrieval augmented generation" and arXiv cs.CL papers on hallucination; boost benchmark and survey papers."

**What the agent does:**

1. Saves *digest.json* with the two queries, 7 days, both sources, and the boost terms.
2. Runs `run_script("scripts/digest.py", args="--config digest.json --out digest-latest.md")`.
3. Reads the returned titles and abstracts, selects the relevant ones, and writes why each matters.
4. Flags one paper that overlaps the user's project and explains how to schedule the run.

**Result (excerpt):**

```markdown
# Paper digest: last 7 days
Queries: `retrieval augmented generation`; `cat:cs.CL AND all:hallucination`. 10 new papers; 4 selected.

## Read first
1. **Classical Query Routing for Adaptive Retrieval-Augmented Generation** (preprint) <link>
   What: compares simple routers for deciding when to retrieve. Why it matters to you: a cheap baseline for your routing module.
   Based on: abstract

## Needs action
- Paper 3 evaluates on the benchmark you planned to introduce: run a novelty check.
```

## Quality bar and pitfalls

- **Tell the user what leaves their machine.** The script sends the saved search queries to the public APIs named under Prerequisites, and nothing else. If the topic is unpublished, confidential, or under embargo, say this before running and ask the user to confirm or to supply more general search terms.
- List only papers the script returned. Do not add papers from memory, and do not describe a paper beyond what its abstract or text says.
- A digest is not a complete search. arXiv and OpenAlex miss work in other venues and index with a delay; recent journal articles may appear weeks late.
- Preprints are not peer reviewed. Mark them, and be careful with strong claims in abstracts.
- Keep the state file with the project. Deleting it repeats old papers; sharing one state file across unrelated topics hides papers.
- arXiv asks clients to pause between requests; the script waits three seconds per call. Do not remove the delay or run it in tight loops.
- Fewer, better-chosen papers are more useful than a long list the user will not read. Ten is plenty.
- Say when a period returned nothing; silence can also mean the query is broken.

## Limitations

- A digest is not a complete search. It covers arXiv and OpenAlex only, and journal articles can appear weeks late.
- Ranking uses query matches and boost terms, not an understanding of relevance; the agent's curation is based on abstracts unless a paper is opened.
- Preprints are not peer reviewed.
- A scheduled script run yields the raw list; the curated notes need an agent run.

## Troubleshooting

| Problem | Likely cause | Solution |
|---|---|---|
| `0 new papers` every run | The query is too narrow, or every result is already in the state file | Test with `--no-state` and a longer `--days`; loosen the query if still empty |
| The same papers appear again | The state file was deleted or a different path was used | Keep one state file per digest and pass the same `--state` path |
| The digest lists a failed source | arXiv or OpenAlex was unreachable or rate-limited | Rerun later; that source is not covered for the period until it succeeds |
| `error: give at least one --query or a config with queries` | No query was supplied or the config path is invalid | Pass `--query` or check the path and JSON of the config file |

## Related skills

- `paper-search` for a deeper search when a digest item opens a new thread.
- `paper-summarizer` for papers selected to read in full.
- `novelty-checker` when a new paper overlaps the user's idea.
- `topic-trend-analyzer` for the longer view of the same topics.
- `research-progress-tracker` to log papers to read and follow-ups.
- `bibtex-manager` to add selected papers to the project's bibliography.
