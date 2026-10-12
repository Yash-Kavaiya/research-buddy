# Column sets and comparability rules

## 1. Column sets by purpose

Pick the set for the purpose, then trim to six to nine columns.

### Choosing a baseline or method

| Column | Definition |
|---|---|
| Paper, year | Citation key and year |
| Core idea | One phrase |
| Requirements | Supervision, data, compute the method needs |
| Benchmark and split | Exact name and split |
| Main result | The headline number, with table reference |
| Baselines beaten | Named |
| Code | Link or NR |
| Weakness | The main limitation |

### State-of-the-art table for a paper

| Column | Definition |
|---|---|
| Method | Name and citation |
| Venue, year | |
| Backbone or size | Parameters or model family |
| Extra data | Pretraining or external data used |
| Metric columns | One per benchmark, same protocol |
| Source of number | Own run or reported |

### Synthesis matrix for a literature review

| Column | Definition |
|---|---|
| Study | Author, year |
| Aim or question | |
| Design | |
| Sample and context | |
| Measures | |
| Key findings | One line per theme column |
| Limitations | |
| Theme columns | One per theme of the review; cell = the study's position on it |

### Systematic-review data extraction

| Column | Definition |
|---|---|
| Study ID, country | |
| Design | |
| Participants (n, characteristics) | |
| Intervention and comparator | |
| Outcomes and time points | |
| Effect estimate with CI | |
| Funding and conflicts | |
| Risk-of-bias judgement | |

### Qualitative studies

Context, participants, data collection, analytic approach, themes, quality notes.

## 2. Cell conventions

| Mark | Meaning |
|---|---|
| NR | Not reported in the paper |
| n/a | Not applicable to this paper |
| ~ | Approximate, read from a figure |
| † ‡ or a, b | Footnote: a different protocol or a caveat |
| (Tab. 3) | Where the number came from |

Never leave a cell blank, and never infer a value. NR is information: a column full of NR is a finding.

## 3. Comparability checklist

Numbers may share a column only if all of these match. Otherwise footnote the difference or split the column.

| Factor | Question |
|---|---|
| Dataset version | Same release? |
| Split | Same train, validation, and test partition? |
| Metric definition | Same formula, averaging, and tokenisation or thresholds? |
| Evaluation protocol | Same test-time settings, crops, ensembles, prompts? |
| Extra data | Same pretraining and external data? |
| Model size | Comparable capacity? If not, show it |
| Source | The paper's own number for its own method? |
| Runs | Single run, best of several, or mean? |

For human-participant studies: same outcome instrument, time point, population definition, and analysis set.

## 4. Whose number to use

1. The original paper's number for its own method.
2. A later paper's rerun, marked as such, when the original used a different protocol.
3. Your own run, marked as such.

Numbers a paper reports for its competitors are often lower than the competitors' own. Mark them when used.

## 5. Ordering and grouping

| Order | When |
|---|---|
| Chronological | To show how results developed |
| By method family, with group header rows | More than eight rows, or clear families |
| By main result | Only when the column is truly comparable |

Put the user's own method last and separate it with a rule.

## 6. Reading the finished table

Look for, and write down:

- Datasets or populations everyone uses, and ones nobody uses.
- A metric or outcome that most papers do not report.
- Conflicting results under apparently similar conditions.
- A requirement (labels, compute, data) every strong method shares.
- Trends over time: gains shrinking, costs growing.
- Rows that are not comparable with the rest, and why.

These observations are the synthesis. The table alone is not.

## 7. Selection statement

State how the papers were chosen: the search, the inclusion rule, the date, and what was left out. A comparison table of hand-picked papers without this is easy to challenge.

## 8. Output formats

| Need | Format |
|---|---|
| Working document | Markdown table |
| Sorting, filtering, more columns | CSV or spreadsheet |
| Manuscript | CSV passed to latex-table-generator |
| Wide tables | Split into two tables by column group, or rotate in the manuscript |
