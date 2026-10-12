---
name: dataset-finder
description: "Finds datasets and benchmarks on Hugging Face, OpenML, Kaggle, UCI, and domain archives and compares size, licence, and access. Use when choosing experiment datasets. Not for collecting new responses."
version: 1.0.0
compatibility: "Requires Python 3.10 or later. Makes read-only HTTPS requests to the Hugging Face Hub and OpenML; sends only the search terms or identifiers given to it."
allowed-tools: "Bash(python:*) Read Write"
permissions: [network, env]
metadata:
  author: "Yash Kavaiya <yash.kavaiya3@gmail.com>"
  tags: [datasets, benchmarks, huggingface, openml]
---

# Dataset Finder

Locate candidate datasets, check that each one can actually be used for the purpose (licence, access, labels, size), and recommend with reasons.

## Purpose

Locate candidate datasets for a research task, check that each can actually be used (licence, access, labels, size, known problems), and recommend a primary and secondary choice with reasons. It also identifies the benchmark most papers report on.

## When to use

- Choosing data for an experiment, thesis, or course project.
- Identifying the standard benchmark for a task so results are comparable.

Hand off instead when the user must collect new data (`survey-questionnaire-designer`, `methodology-designer`).

## Prerequisites

- Python 3.10 or later; the script uses only the standard library.
- Network access to the Hugging Face Hub and OpenML APIs (no key needed). Kaggle needs the Kaggle CLI and credentials, or the website.
- The task, modality, and whether the use is academic or commercial.

## Inputs

- Task and modality (text classification, medical image segmentation, tabular regression, time series).
- Requirements: minimum size, label type, language, domain, date range.
- Use: academic or commercial, which decides acceptable licences.
- Whether comparability with prior papers matters.

## Instructions

1. **Search the hubs with an API:**

   ```bash
   python scripts/find_datasets.py "sentiment analysis" --limit 10
   python scripts/find_datasets.py "chest x-ray" --sources huggingface --format json
   python scripts/find_datasets.py "credit" --sources openml
   ```

   Hugging Face results are sorted by downloads and include licence, task, size category, and gated status. OpenML matches on dataset name only, so give it a single keyword.
2. **Search the sources without an open API** using web search or the site itself:
   - Papers with Code: datasets by task, and which papers report results on them.
   - Kaggle: `kaggle datasets list -s "<query>"` if the Kaggle CLI is configured, otherwise the website.
   - UCI Machine Learning Repository: classic tabular datasets.
   - Zenodo, Figshare, Dataverse, OSF: datasets attached to papers.
   - Google Dataset Search for everything else.
   - Domain archives: PhysioNet (clinical signals), TCIA (cancer imaging), GEO and SRA (genomics), UK Data Service and ICPSR (social science), data.gov.in and data.gov (government), LDC and ELRA (language), OpenNeuro (neuroimaging).
3. **Find what the literature uses.** Search recent papers on the task with `paper-search` and note the datasets in their experiment sections. The benchmark most papers report on is usually the one to include.
4. **Check each candidate:**
   - *Licence*: what it permits (research only, commercial, redistribution). "Not stated" means unknown, not free.
   - *Access*: open, gated, application required, or a data use agreement. Estimate how long access takes.
   - *Content*: size, classes, label source and quality, class balance, splits provided.
   - *Provenance and ethics*: how it was collected, consent, personal data, known biases, any retraction or deprecation.
   - *Documentation*: a datasheet, data card, or paper to cite.
5. **Open the dataset card or paper** for the top candidates and confirm the details. Do not rely on the search listing.
6. **Recommend** a primary dataset and one or two secondary ones, with the reason and what each lets the user claim.

## Available Scripts

| Script | Purpose | Arguments |
|---|---|---|
| `scripts/find_datasets.py` | Searches Hugging Face Hub (sorted by downloads) and OpenML and prints a comparison table | `QUERY` (required), `--sources huggingface,openml`, `--limit N`, `--format md|json` |

Run a script with the agent's script tool, for example `run_script("scripts/find_datasets.py", args=[...])`, or from a shell in the skill folder with `python scripts/find_datasets.py ...`. Each script prints usage with `--help`, validates its arguments, and exits with a non-zero code and an `error:` message on failure.

## Output format

```markdown
## Candidates for <task>
| Dataset | Source | Size | Labels | Licence | Access | Used by | Fit |
|---|---|---|---|---|---|---|---|

## Recommendation
- Primary: <dataset>, because ...
- Secondary: <dataset>, for generalisation or comparison
- Avoid: <dataset>, because <licence, deprecation, leakage, quality>

## How to obtain
Commands or steps, including any application.

## Cite as
<the dataset paper, verified>

## Not verified
- <details taken from listings that still need checking on the dataset page>
```

## Examples

Requests that should trigger this skill:

- "Find a dataset for sentiment analysis in Hindi."
- "Is there a benchmark for chest X-ray classification?"
- "Where can I get tabular credit-risk datasets?"
- "Which datasets do papers use for abstractive summarization?"
- "I need an open dataset of ECG recordings with labels."

Requests that belong to another skill:

- "Design a survey to collect my own responses." → use `survey-questionnaire-designer`
- "Find papers about sentiment analysis." → use `paper-search`
- "Draft the ethics application for using patient records." → use `ethics-irb-drafter`

### Worked example

**Request:** "Find datasets for financial sentiment classification that I can use in a thesis."

**What the agent does:**

1. Runs `run_script("scripts/find_datasets.py", args="'financial sentiment' --limit 10")`.
2. Checks Papers with Code and recent papers for the benchmark most often reported.
3. Opens the dataset cards of the top candidates to confirm licence, size, and label source.
4. Recommends a primary and secondary dataset and lists what was not verified.

**Result (excerpt):**

```markdown
| Dataset | Source | Size | Licence | Access | Fit |
|---|---|---|---|---|---|
| zeroshot/twitter-financial-news-sentiment | huggingface | 10K<n<100K | mit | open | good: three-class labels, permissive licence |
| (second candidate) | huggingface | 1K<n<10K | not stated | open | check licence before use |

## Not verified
- Annotator agreement for the first dataset; read the dataset card before citing it.
```

## Quality bar and pitfalls

- **Tell the user what leaves their machine.** The script sends the search keywords to the public APIs named under Prerequisites, and nothing else. If the topic is unpublished, confidential, or under embargo, say this before running and ask the user to confirm or to supply more general search terms.
- Only list datasets you found. Do not describe a dataset from memory without opening its page; names, sizes, and licences are easy to get wrong.
- Popularity is not quality. Check label noise reports and known issues for widely used benchmarks.
- A missing licence does not grant permission. Flag it.
- Some well-known datasets have been withdrawn for ethical or legal reasons. Check current status before recommending.
- Medical, biometric, and personal data usually need ethics approval and a data use agreement even when "public" (`ethics-irb-drafter`).
- Watch for overlap between a candidate's test set and pretraining corpora or other training sets.
- Do not help obtain gated or restricted data by going around the access process.

## Limitations

- The script searches Hugging Face and OpenML only. Kaggle, UCI, Papers with Code, and domain archives are searched by hand or web search.
- OpenML matches on dataset name only, using the first keyword.
- Listings can be wrong or stale about licence and size; the dataset page or paper is the authority.
- Popularity does not indicate label quality, and some well-known datasets have been withdrawn.

## Troubleshooting

| Problem | Likely cause | Solution |
|---|---|---|
| `No datasets found.` | The query is too specific, or OpenML found no name match | Use one or two general keywords, or search Hugging Face alone with `--sources huggingface` |
| Licence shows `not stated` or `unknown` | The dataset card has no licence tag | Open the dataset page and paper; if no licence is given, treat the dataset as not cleared for use |
| A dataset is marked gated | Access requires accepting terms or an application | Follow the access process on the dataset page; do not attempt to obtain the files another way |
| `warning: huggingface failed` | A network error or rate limit | Wait and rerun; the error message names the failed source |

## Related skills

- `paper-search` to see which datasets recent papers use.
- `experiment-planner` to fit the datasets into the evaluation plan.
- `ethics-irb-drafter` when the data involves people.
- `paper-to-code-reproducer` when reproducing a paper needs its data.
- `reproducibility-checklist` for the dataset documentation the venue asks for.
