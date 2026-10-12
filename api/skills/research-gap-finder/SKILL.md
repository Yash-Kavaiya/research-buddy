---
name: research-gap-finder
description: "Lists open problems and under-explored areas in a research topic, each backed by retrieved papers. Use when choosing a thesis or paper topic. Not for testing one idea; use novelty-checker."
version: 1.0.0
metadata:
  author: "Yash Kavaiya <yash.kavaiya3@gmail.com>"
  tags: [research-gaps, literature, topic-selection]
---

# Research Gap Finder

Produce a ranked list of research gaps, each backed by evidence from named papers. A gap is a specific question the literature has not answered, and the list must show why you believe that.

## Purpose

Give a researcher a short, ranked list of unanswered questions in a topic, with the papers that show each one is open. It replaces vague statements such as "more research is needed" with gaps that can be defended in a proposal.

## When to use

- The user has a topic and wants to know what is still open.
- The user has a pile of papers and wants the gaps across them.

Hand off instead when:

- The user already has an idea and wants to know if it is new: use `novelty-checker`.
- The user wants publication counts and hot subfields: use `topic-trend-analyzer`.

## Prerequisites

- The `paper-search` skill, or another way to retrieve real paper records.
- Network access to the scholarly APIs, and full text of the key papers where available.
- A topic narrow enough to search: a task, population, or method within a field.

## Inputs

- Topic, as narrow as the user can state it. If it is as broad as "machine learning in healthcare", ask for one narrowing choice (task, population, modality, or method family) before searching.
- Time window. Default: the last 3 years, plus the most recent survey of any age.
- Field and target output (thesis, conference paper, grant), because they change which gaps are feasible.
- Any papers the user already has.

## Instructions

1. **Collect a corpus.** Use `paper-search` to gather 25 to 40 papers: recent surveys first, then the most-cited recent work, then the newest preprints. Record the queries used. If a source fails or returns an error, say which one was not searched.
2. **Read where gaps are stated.** For each paper read the abstract, the limitations and future-work sections, and the conclusion. For surveys read the "open challenges" section in full. Use full text when it is available; say so when only abstracts were read.
3. **Extract candidate gaps** into a working table: paper, claim or limitation, type. Use these types:
   - *Stated*: authors name it as future work or a limitation.
   - *Contradiction*: two papers report conflicting findings on the same question.
   - *Coverage*: a population, language, domain, scale, or setting no paper evaluates.
   - *Method*: a missing baseline, an assumption nobody tests, an evaluation everyone shares that has a known flaw.
   - *Transfer*: a technique established in a neighbouring area and not yet tried here.
4. **Cluster** candidates that describe the same gap, and keep every supporting paper.
5. **Check each cluster is still open.** Run one targeted search per gap for work from the last 18 months that closes it. Drop closed gaps or restate what remains.
6. **Rank** by evidence strength (how many independent papers point to it), importance (what changes if it is answered), and feasibility for this user.
7. **Report** using the format below, and offer `research-question-formulator` for the gap the user picks.

## Output format

```markdown
## Research gaps: <topic>
Corpus: <N> papers, <years>, sources searched, queries used. Full text read for <M>.

### 1. <Gap stated as an unanswered question>
- Type: stated | contradiction | coverage | method | transfer
- Evidence: <Paper A (year)> reports ...; <Paper B (year)> lists ... as future work.
- Why it matters: <one or two sentences>
- What a study would need: <data, method, resources>
- Confidence it is still open: high | medium | low, because <the check you ran>

### 2. ...

## Gaps considered and dropped
- <gap>: closed by <paper>.

## Coverage limits
- <what was not searched or not read in full>
```

Give 5 to 8 gaps. Fewer, well-supported gaps are better than a long list.

## Reference files

Open these only when the step calls for them; they are not needed for every request.

- `references/gap-types-and-evidence.md`: Read at step 3, when classifying candidate gaps and deciding how much evidence each one needs.
- `assets/gap-report-template.md`: Copy and fill for the final gap report.

## Examples

Requests that should trigger this skill:

- "What are the research gaps in federated learning for medical imaging?"
- "Find me a PhD topic in low-resource speech recognition."
- "What is still unsolved in graph anomaly detection?"
- "Here are 20 papers on microplastics in soil. What has nobody studied yet?"
- "Where can I contribute in explainable AI for credit scoring?"

Requests that belong to another skill:

- "Has anyone already done contrastive pretraining on ECG signals?" → use `novelty-checker`
- "Is prompt engineering a growing research area?" → use `topic-trend-analyzer`
- "Summarise this paper for me." → use `paper-summarizer`

### Worked example

**Request:** "Find research gaps in federated learning for medical imaging. I need a master's thesis topic I can finish in one year with public data."

**What the agent does:**

1. Searches for recent surveys, the most-cited work since 2022, and new preprints (about 30 papers), and records the queries.
2. Reads limitations, future-work sections, and the surveys' open-challenges sections; builds a table of candidate gaps by type.
3. Runs one targeted search per gap to check it is still open, and drops two that recent papers closed.
4. Ranks the remaining gaps by evidence, importance, and feasibility for a one-year project with public data.

**Result (excerpt):**

```markdown
### 1. Does federated training keep its accuracy when hospitals label the same finding differently?
- Type: coverage
- Evidence: Survey A (2023) lists label heterogeneity as open; Papers B and C evaluate only on identically labelled sites.
- What a study would need: two public chest X-ray datasets with different labelling schemes
- Confidence it is still open: medium (search "federated label shift radiology", 2024 onward, returned 3 papers, none multi-site)
```

## Quality bar and pitfalls

- Every gap cites at least one real paper you retrieved, with title and year. Never cite from memory without retrieving the record.
- "Little research exists on X" needs a search that shows it. State the query and the count.
- Do not present the absence of a paper in your sample as proof nobody has done it. Report it as "not found in this search".
- A contradiction needs both sides named, with the conditions under which each result was obtained. Many apparent contradictions are differences in dataset or metric.
- Avoid gaps that are just "apply method M to dataset D" unless there is a reason the result would be informative.
- If only abstracts were read, say so in the corpus line. Limitations rarely appear in abstracts.

## Limitations

- The gaps reflect the papers that were retrieved. A gap can be closed by work the search did not find, in another language, or still under review.
- When only abstracts are available, limitations and future-work statements are mostly missed, so stated gaps are under-counted.
- Feasibility is judged from what the user reports about their resources; it is not verified.

## Troubleshooting

| Problem | Likely cause | Solution |
|---|---|---|
| The search returns few or no relevant papers | The topic wording is not the field's own term, or the topic is too narrow | Try the field's standard terms and synonyms, remove one qualifier, and search for a survey first |
| Every gap found is generic ("more data needed") | Only abstracts were read | Obtain full text for the surveys and the five most relevant papers and reread their limitations sections |
| A reported gap turns out to be already addressed | The still-open check used too narrow a query | Rerun the check with the method name alone and with a recent year filter, then drop or restate the gap |

## Related skills

- `paper-search` and `citation-graph-explorer` to build the corpus.
- `topic-trend-analyzer` to see whether a gap sits in a growing or fading area.
- `novelty-checker` to test a specific idea that comes out of a gap.
- `research-question-formulator` to turn a chosen gap into questions and hypotheses.
