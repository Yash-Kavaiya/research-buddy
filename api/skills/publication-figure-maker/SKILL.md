---
name: publication-figure-maker
description: "Creates publication-quality matplotlib or TikZ plots at a venue's column width with embedded fonts and colour-blind-safe colours. Use when plotting results for a paper. Not for architecture diagrams."
version: 1.0.0
compatibility: "Requires Python 3.10 or later with matplotlib and NumPy. Runs locally with no network access."
allowed-tools: "Bash(python:*) Read Write"
metadata:
  author: "Yash Kavaiya <yash.kavaiya3@gmail.com>"
  tags: [figures, matplotlib, plots, visualization]
---

# Publication Figure Maker

Produce figures that are legible at printed size, honest about the data, and accepted by the publisher's production checks.

## Purpose

Produce plots that are legible at printed size, honest about the measurements, and accepted by publishers' production checks. The style module sets figure size from the venue's column width, embeds TrueType fonts, and supplies a colour-blind-safe palette.

## When to use

- Results need plotting for a paper, thesis, poster, or slides.
- An existing figure has small text, wrong size, poor colours, or font-embedding problems.

Hand off instead for model and pipeline schematics (`architecture-diagram-maker`) or tables (`latex-table-generator`).

## Prerequisites

- Python 3.10 or later with matplotlib and NumPy (`pip install matplotlib numpy`).
- The values to plot, with variance across runs if it exists.
- The target venue and whether the figure spans one column or the full width.

## Inputs

- The data (CSV, JSON, arrays, or the experiment log), with variance across runs if it exists.
- The message of the figure: the one comparison or trend the reader should see.
- Venue and whether the figure spans one column or the full width.
- Output needs: PDF for LaTeX, PNG for slides, greyscale-safe if the venue prints in black and white.

## Instructions

1. **State the figure's point in one sentence.** It decides the chart type and what is emphasised.
2. **Choose the chart type:**

   | To show | Use | Avoid |
   |---|---|---|
   | Trend over an ordered variable | Line plot with markers | Bars for many x values |
   | Comparison across categories | Bar chart or dot plot, sorted | Pie charts, 3D bars |
   | Distribution | Box, violin, or histogram; strip plot for small n | Bar of means alone |
   | Relationship between two variables | Scatter, with fit only if justified | Connecting unordered points |
   | Matrix (confusion, correlation, attention) | Heatmap with a perceptually uniform colormap (`viridis`, `cividis`) | `jet` and rainbow maps |
   | Many conditions | Small multiples with shared axes | One crowded panel |

3. **Set the style and size with the script:**

   ```python
   import matplotlib.pyplot as plt
   import pubstyle                      # copy scripts/pubstyle.py next to the plotting script

   pubstyle.apply("ieee")               # 8 pt fonts, thin axes, embedded TrueType fonts
   fig, ax = plt.subplots(figsize=pubstyle.figsize("ieee", columns=1))
   for i, (name, y, sd) in enumerate(series):
       ax.plot(x, y, color=pubstyle.PALETTE[i], marker=pubstyle.MARKERS[i],
               linestyle=pubstyle.LINESTYLES[i], label=name)
       ax.fill_between(x, y - sd, y + sd, color=pubstyle.PALETTE[i], alpha=0.15, linewidth=0)
   ax.set_xlabel("Training epochs"); ax.set_ylabel("Accuracy (%)"); ax.legend()
   pubstyle.save(fig, "figures/accuracy")   # accuracy.pdf (vector) and accuracy.png (300 dpi)
   ```

   ```bash
   python scripts/pubstyle.py widths                      # column and text widths per venue
   python scripts/pubstyle.py demo --venue neurips --out demo
   ```

   Venues: `ieee`, `acm`, `neurips`, `icml`, `iclr`, `acl`, `cvpr`, `springer-lncs`, `nature`, `elsevier`, `thesis-a4`. `figsize(venue, columns=2)` gives the full text width; `aspect` or `height` sets the height. Confirm the width against the current template.
4. **Create the figure at final size** and include it in LaTeX without scaling (`\includegraphics{figures/accuracy}`), so 8 pt text in the figure is 8 pt on the page.
5. **Encode redundantly.** Distinguish series by colour and by marker or line style, so the figure works in greyscale and for colour-blind readers. `PALETTE` is the Okabe-Ito set.
6. **Show uncertainty**: error bars or bands, with the caption saying what they are (standard deviation, standard error, or 95% CI) and over how many runs.
7. **Label everything**: axis labels with units, a legend or direct labels, and tick labels that are readable. No title inside the figure; the caption carries it.
8. **Write the caption**: what is plotted, the conditions, what the error bars are, and the takeaway in one sentence.
9. **Check the output.** Open the PDF at 100% zoom. Verify fonts are embedded (`pdffonts figure.pdf`: no Type 3) and the size matches the column.
10. **For TikZ/pgfplots** (when the venue or user wants native LaTeX figures), export the data to CSV and write a `pgfplots` axis with the same width, `\pgfplotsset{compat=1.18}`, and the same colours. Compile it before delivering.

## Available Scripts

| Script | Purpose | Arguments |
|---|---|---|
| `scripts/pubstyle.py (import)` | Style module: `apply(venue)`, `figsize(venue, columns, aspect, height)`, `save(fig, path)`, `PALETTE`, `MARKERS`, `LINESTYLES` | import as a module after copying it next to the plotting script |
| `scripts/pubstyle.py widths` | Lists column and text widths for each supported venue | none |
| `scripts/pubstyle.py demo` | Draws a sample figure to check fonts and size | `--venue NAME`, `--columns 1|2`, `--out PATH` |

Run a script with the agent's script tool, for example `run_script("scripts/pubstyle.py (import)", args=[...])`, or from a shell in the skill folder with `python scripts/pubstyle.py (import) ...`. Each script prints usage with `--help`, validates its arguments, and exits with a non-zero code and an `error:` message on failure.

## Output format

- `figures/<name>.pdf` and `figures/<name>.png`
- The plotting script, reading the data file, so the figure can be regenerated
- The caption text and the LaTeX include snippet:

```latex
\begin{figure}[t]
  \centering
  \includegraphics{figures/accuracy}
  \caption{Validation accuracy over training. Shaded bands show $\pm 1$ standard deviation over 5 seeds.}
  \label{fig:accuracy}
\end{figure}
```

## Examples

Requests that should trigger this skill:

- "Make a line plot of these accuracy curves for my IEEE paper."
- "Plot these results as a bar chart with error bars."
- "My figure text is too small in the PDF. Fix it."
- "PDF eXpress complains about Type 3 fonts in my figures."
- "Convert this matplotlib plot to pgfplots."

Requests that belong to another skill:

- "Draw my model architecture." → use `architecture-diagram-maker`
- "Make a LaTeX table from this CSV." → use `latex-table-generator`
- "Make the PRISMA flow diagram." → use `systematic-review-prisma`

### Worked example

**Request:** "Plot validation accuracy over 10 epochs for three methods from curves.csv (mean and sd over 5 seeds) as a single-column figure for an IEEE conference paper."

**What the agent does:**

1. States the figure's point: method A converges fastest.
2. Copies `pubstyle.py` next to the script, calls `pubstyle.apply("ieee")` and `figsize("ieee", columns=1)`.
3. Plots each series with its own colour, marker, and line style, and shaded bands for the standard deviation.
4. Saves PDF and PNG, opens the PDF to check size and fonts, and writes the caption.

**Result (excerpt):**

```markdown
wrote accuracy.pdf in figures/ (3.5 x 2.38 in, fonts embedded as TrueType)
wrote accuracy.png in figures/

\begin{figure}[t]
  \centering
  \includegraphics{figures/accuracy}
  \caption{Validation accuracy over training. Shaded bands show $\pm 1$ standard deviation over 5 seeds.}
  \label{fig:accuracy}
\end{figure}
```

## Quality bar and pitfalls

- Plot only the data provided. Never fabricate, smooth away, or omit points to improve the picture, and say so if outliers were removed.
- Bar charts start at zero. If the axis is truncated on a line plot, make it obvious.
- Do not use two y-axes to imply a relationship, or different axis ranges across panels meant for comparison.
- A mean without spread hides the result. If there is one run, say so in the caption.
- Text in the figure should be no smaller than about 6 to 7 pt at printed size.
- Rasterised plots (PNG, JPG) of line art blur in print. Use PDF or EPS; rasterise only dense scatter layers or images.
- Remove chart junk: gridlines darker than the data, boxes, shadows, redundant legends.
- Keep colours and names consistent for the same method across all figures in the paper.
- Run the script and look at the result before delivering it.

## Limitations

- Venue widths in the module are taken from the standard templates and can change; the current author kit is the authority.
- The module styles matplotlib only. TikZ or pgfplots figures are written by hand following the same sizes and colours.
- Fonts fall back to the nearest installed family when Times or Arial is absent, which changes the look slightly.
- The script cannot judge whether a chart type suits the message; that choice is the author's and the agent's.

## Troubleshooting

| Problem | Likely cause | Solution |
|---|---|---|
| `ValueError: unknown venue 'x'` | The venue name is not in the width table | Run `pubstyle.py widths` to list names, or pass `height` and set the width from the venue's template |
| Text is clipped at the figure edge | Long labels with constrained layout at a small size | Shorten labels, rotate tick labels, or increase `height` |
| The saved figure is wider or narrower than the column | `bbox_inches="tight"` was passed when saving | Save with *pubstyle.save* and no tight bounding box so the width is preserved |
| `ModuleNotFoundError: No module named 'pubstyle'` | The module is not on the import path | Copy `scripts/pubstyle.py` next to the plotting script or add its folder to *sys.path* |

## Related skills

- `results-interpreter` decides what the figure should show.
- `statistical-test-selector` supplies intervals and significance marks.
- `experiment-logger` is the source of run data.
- `architecture-diagram-maker` for schematic figures.
- `latex-table-generator` when exact values matter more than the trend.
- `latex-paper-formatter` to place figures in the template.
- `paper-to-slides` and `paper-to-poster` reuse the figures at larger font sizes.
