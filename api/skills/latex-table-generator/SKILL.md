---
name: latex-table-generator
description: "Converts CSV results into LaTeX booktabs tables with best values bolded, optional second-best underline, arrows, and consistent decimals. Use when typesetting results tables. Not for plots."
version: 1.0.0
compatibility: "Requires Python 3.10 or later. Runs locally with no network access."
allowed-tools: "Bash(python:*) Read Write"
metadata:
  author: "Yash Kavaiya <yash.kavaiya3@gmail.com>"
  tags: [latex, tables, booktabs, results]
---

# LaTeX Table Generator

Typeset results tables that are correct, readable, and consistent, with the marking of best results done by code instead of by eye.

## Purpose

Typeset results tables that are correct and consistent, with the marking of best results decided by code instead of by eye. The table can be regenerated from the CSV whenever numbers change.

## When to use

- Results in a CSV, spreadsheet, or pasted text need to become a LaTeX table.
- An existing table needs booktabs styling, best-result marking, or to fit the column width.

Hand off instead for trends better shown as a plot (`publication-figure-maker`) or for building the comparison content itself (`paper-comparison-matrix`).

## Prerequisites

- Python 3.10 or later; the script uses only the standard library.
- A CSV whose first row is the header and whose first column is the row label.
- `\usepackage{booktabs}` in the paper's preamble.

## Inputs

- The data as CSV: first row is the header, first column is the row label (method, model, variant).
- For each numeric column, whether higher or lower is better.
- Columns that should not be marked (parameter counts, years).
- Caption, label, and whether the table spans one column or both.

## Instructions

1. **Prepare the CSV.** One row per method, one column per metric. Spread goes in the same cell as `85.3 ± 0.4` or `85.3 (0.4)`. Put the user's own method last. Keep the numbers exactly as they came from the experiment log.
2. **Generate the table:**

   ```bash
   python scripts/csv_to_booktabs.py results.csv --caption "Main results on ImageNet-1k." --label tab:main \
     --lower-is-better "Error,Latency (ms)" --no-bold "Params (M)" --second --arrows \
     --midrule-before "Ours" --decimals 1 --out main-table.tex
   ```

   - `--lower-is-better`: comma-separated columns where smaller wins; all others are higher-is-better.
   - `--no-bold`: numeric columns to leave unmarked.
   - `--second`: underline the second-best value.
   - `--arrows`: add ↑ or ↓ to metric headers.
   - `--decimals N`: round every number to N places. Ties at the displayed precision are all bolded.
   - `--midrule-before TEXT`: add a rule before rows whose label starts with TEXT, to separate your method or a group.
   - `--star`: use `table*` for a full-width table in two-column layouts. `--position` sets the float placement.

   Text cells are escaped (`&`, `%`, `_`, `#`); cells containing `$` or a backslash pass through unchanged so LaTeX in cells is kept.
3. **Add to the paper** with `\usepackage{booktabs}` in the preamble and `\input{main-table}`.
4. **Refine by hand where needed:**
   - Column groups: `\multicolumn{2}{c}{Dataset A}` with `\cmidrule(lr){2-3}` under it.
   - Row groups: `\multirow` (package `multirow`) or a `\midrule` with an italic group label.
   - Decimal alignment: the `siunitx` `S` column type.
   - Notes under the table: `threeparttable`.
5. **Fit the width.** In order of preference: shorten headers and abbreviate with a caption key; reduce decimals; drop a low-value column or move it to the appendix; `\setlength{\tabcolsep}{4pt}`; `table*`; and only then `\resizebox{\columnwidth}{!}{...}`, which shrinks the font.
6. **Write the caption** above the table (the convention for tables): what is reported, the metric and its direction, what bold and underline mean, what the spread is and over how many runs.
7. **Compile and check** the table against the CSV, cell by cell for the marked values.

## Available Scripts

| Script | Purpose | Arguments |
|---|---|---|
| `scripts/csv_to_booktabs.py` | Builds a booktabs table, bolding the best value per numeric column and escaping LaTeX special characters | `CSV` (required), `--caption`, `--label`, `--lower-is-better COLS`, `--no-bold COLS`, `--second`, `--decimals N`, `--arrows`, `--midrule-before TEXT`, `--position`, `--star`, `--out FILE` |

Run a script with the agent's script tool, for example `run_script("scripts/csv_to_booktabs.py", args=[...])`, or from a shell in the skill folder with `python scripts/csv_to_booktabs.py ...`. Each script prints usage with `--help`, validates its arguments, and exits with a non-zero code and an `error:` message on failure.

## Output format

```latex
\begin{table}[t]
  \centering
  \caption{Main results on ImageNet-1k. Best in \textbf{bold}, second best \underline{underlined}. Mean $\pm$ s.d. over 5 seeds.}
  \label{tab:main}
  \begin{tabular}{lccc}
    \toprule
    Method & Accuracy $\uparrow$ & Error $\downarrow$ & Params (M) \\
    \midrule
    ResNet-50 & 76.13 $\pm$ 0.12 & 23.87 & 25.6 \\
    ViT-B/16 & \underline{81.07 $\pm$ 0.21} & \underline{18.93} & 86.6 \\
    \midrule
    Ours & \textbf{82.40 $\pm$ 0.15} & \textbf{17.60} & 22.1 \\
    \bottomrule
  \end{tabular}
\end{table}
```

Deliver the `.tex` file, the CSV it was generated from, and the command used, so the table can be regenerated when numbers change.

## Examples

Requests that should trigger this skill:

- "Turn results.csv into a LaTeX table with the best results in bold."
- "Make a booktabs table from this spreadsheet."
- "Bold the best and underline the second best in each column."
- "Format my ablation results as a LaTeX table; lower error is better."
- "My table is too wide for one column. Fix it."

Requests that belong to another skill:

- "Plot these results instead." → use `publication-figure-maker`
- "Build a comparison table of papers from the literature." → use `paper-comparison-matrix`
- "Decide which ablations to run." → use `ablation-study-designer`

### Worked example

**Request:** "results.csv has Method, Accuracy, Error, Params (M). Higher accuracy and lower error are better; don't bold parameters. Put a rule before our method (row "Ours")."

**What the agent does:**

1. Checks the CSV: header row, row labels first, spread written as `82.40 ± 0.15`.
2. Runs `run_script("scripts/csv_to_booktabs.py", args="results.csv --lower-is-better Error --no-bold 'Params (M)' --second --arrows --midrule-before Ours --caption 'Main results.' --label tab:main")`.
3. Compiles the table and compares the marked cells with the CSV.
4. Writes the caption explaining bold, underline, and the spread.

**Result (excerpt):**

```markdown
    Method & Accuracy $\uparrow$ & Error $\downarrow$ & Params (M) \\
    \midrule
    ResNet-50 & 76.13 $\pm$ 0.12 & 23.87 & 25.6 \\
    ViT-B/16 & \underline{81.07 $\pm$ 0.21} & \underline{18.93} & 86.6 \\
    \midrule
    Ours & \textbf{82.40 $\pm$ 0.15} & \textbf{17.60} & 22.1 \\
    \bottomrule
```

## Quality bar and pitfalls

- The numbers in the table are the numbers in the CSV. Never retype, adjust, or fill in a value; missing results stay as `--` with a note.
- Let the script decide what is bold. Hand-bolding is where tables go wrong, especially for lower-is-better columns.
- Bold marks the best value in the column, including when it belongs to a baseline. Do not bold your own method when it is not best.
- When differences are within the reported spread, say so in the caption or text. Bold alone implies a meaningful win.
- Booktabs style: no vertical rules, and only `\toprule`, `\midrule`, `\bottomrule`, and `\cmidrule`.
- Use the same number of decimals within a column, and no more precision than the measurement supports.
- State the metric direction (arrows or caption) for every metric column.
- Numbers copied from other papers must be marked as such and be from a comparable protocol.

## Limitations

- The script produces simple tables. Multi-row headers, merged cells, and decimal alignment are added by hand afterward.
- Best values are chosen by numeric comparison only; it does not test whether differences are statistically meaningful.
- Cells that mix text and numbers in unexpected formats are treated as text and left unmarked.
- Width is not checked; fitting the column is done with the steps in the instructions.

## Troubleshooting

| Problem | Likely cause | Solution |
|---|---|---|
| `error: columns not in the CSV header: ['Eror']` | A column name passed to `--lower-is-better` or `--no-bold` is misspelled | Use the header text exactly, including spaces and units |
| A numeric column is not bolded | Some cells contain text such as `n/a`, so the column is treated as text | Leave missing cells empty or as `-` |
| `error: the CSV needs a header row and at least one data row` | The file is empty or was saved with a different delimiter | Export as comma-separated values with a header row |
| LaTeX error: `Undefined control sequence \toprule` | The booktabs package is not loaded | Add `\usepackage{booktabs}` to the preamble |

## Related skills

- `experiment-logger` is the source of the numbers.
- `results-interpreter` decides what the table needs to show.
- `ablation-study-designer` supplies the ablation table layout.
- `paper-comparison-matrix` for literature comparison tables.
- `statistical-test-selector` for significance markers.
- `latex-paper-formatter` to fit tables into the venue template.
- `publication-figure-maker` when a plot communicates the result better.
