#!/usr/bin/env python3
"""Convert a CSV of results into a LaTeX booktabs table, with the best value in each column in bold.

The first column is the row label. Numeric columns are detected automatically;
cells such as "85.3 ± 0.4" or "85.3 (0.4)" are compared by their leading number.

Examples:
    python csv_to_booktabs.py results.csv --caption "Main results." --label tab:main
    python csv_to_booktabs.py results.csv --lower-is-better "Error,Latency (ms)" --second --arrows
    python csv_to_booktabs.py results.csv --decimals 1 --midrule-before "Ours" --out table.tex

The output needs \\usepackage{booktabs} in the preamble.
"""

from __future__ import annotations

import argparse
import csv
import re
import sys

NUMBER_RE = re.compile(r"^\s*([-+]?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?)\s*(%?)\s*(?:(±|\+/-|\\pm)\s*(\d+(?:\.\d+)?)|\((\d+(?:\.\d+)?)\))?\s*$")
ESCAPES = {"&": r"\&", "%": r"\%", "_": r"\_", "#": r"\#"}


def parse_cell(cell: str) -> dict | None:
    """Split a numeric cell into value, percent sign, and spread; None for text cells."""
    match = NUMBER_RE.match(cell)
    if not match:
        return None
    return {"value": float(match.group(1)), "raw": match.group(1), "percent": bool(match.group(2)),
            "spread": match.group(4) or match.group(5), "paren": match.group(5) is not None}


def escape(text: str) -> str:
    """Escape LaTeX special characters in plain text; cells containing maths or commands pass through."""
    if "$" in text or "\\" in text:
        return text
    return "".join(ESCAPES.get(ch, ch) for ch in text)


def render_number(parsed: dict, decimals: int | None) -> str:
    def fix(raw: str) -> str:
        return f"{float(raw):.{decimals}f}" if decimals is not None else raw

    text = fix(parsed["raw"]) + (r"\%" if parsed["percent"] else "")
    if parsed["spread"]:
        text += f" ({fix(parsed['spread'])})" if parsed["paren"] else rf" $\pm$ {fix(parsed['spread'])}"
    return text


def rank_column(values: list[float | None], lower_is_better: bool) -> tuple[set[int], set[int]]:
    """Row indices holding the best and the second-best value (ties share a rank)."""
    present = sorted({v for v in values if v is not None}, reverse=not lower_is_better)
    if not present:
        return set(), set()
    best = {i for i, v in enumerate(values) if v == present[0]}
    second = {i for i, v in enumerate(values) if len(present) > 1 and v == present[1]}
    return best, second


def build_table(rows: list[list[str]], caption: str = "", label: str = "", lower_is_better: set[str] | None = None,
                no_bold: set[str] | None = None, second: bool = False, decimals: int | None = None,
                arrows: bool = False, midrule_before: str | None = None, position: str = "t",
                star: bool = False) -> str:
    header, body = rows[0], rows[1:]
    lower_is_better, no_bold = lower_is_better or set(), no_bold or set()
    unknown = (lower_is_better | no_bold) - set(header)
    if unknown:
        raise ValueError(f"columns not in the CSV header: {sorted(unknown)}")
    width = len(header)
    body = [row + [""] * (width - len(row)) for row in body]
    parsed = [[parse_cell(cell) for cell in row] for row in body]
    numeric = [col > 0 and any(p[col] for p in parsed) and all(p[col] or not row[col].strip() or row[col].strip() in "-–"
                                                              for p, row in zip(parsed, body))
               for col in range(width)]

    marks: dict[tuple[int, int], str] = {}
    for col in range(width):
        if not numeric[col] or header[col] in no_bold:
            continue
        # compare at the displayed precision so values that print the same are tied
        values = [round(p[col]["value"], decimals) if p[col] and decimals is not None else (p[col]["value"] if p[col] else None)
                  for p in parsed]
        best, runner_up = rank_column(values, header[col] in lower_is_better)
        for row in best:
            marks[(row, col)] = "bold"
        if second:
            for row in runner_up:
                marks[(row, col)] = "underline"

    head_cells = []
    for col, name in enumerate(header):
        text = escape(name)
        if arrows and numeric[col] and name not in no_bold:
            text += r" $\downarrow$" if name in lower_is_better else r" $\uparrow$"
        head_cells.append(text)

    lines = [rf"\begin{{table{'*' if star else ''}}}[{position}]", r"  \centering"]
    if caption:
        lines.append(rf"  \caption{{{caption}}}")
    if label:
        lines.append(rf"  \label{{{label}}}")
    lines += [rf"  \begin{{tabular}}{{{''.join('c' if numeric[c] else 'l' for c in range(width))}}}", r"    \toprule",
              "    " + " & ".join(head_cells) + r" \\", r"    \midrule"]
    for r, row in enumerate(body):
        if midrule_before and r > 0 and row[0].strip().startswith(midrule_before):
            lines.append(r"    \midrule")
        cells = []
        for col, cell in enumerate(row):
            p = parsed[r][col]
            text = render_number(p, decimals) if numeric[col] and p else escape(cell.strip())
            mark = marks.get((r, col))
            if mark == "bold":
                text = rf"\textbf{{{text}}}"
            elif mark == "underline":
                text = rf"\underline{{{text}}}"
            cells.append(text)
        lines.append("    " + " & ".join(cells) + r" \\")
    lines += [r"    \bottomrule", r"  \end{tabular}", rf"\end{{table{'*' if star else ''}}}"]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("csv")
    parser.add_argument("--caption", default="")
    parser.add_argument("--label", default="")
    parser.add_argument("--lower-is-better", default="", help="comma-separated column names where smaller is better")
    parser.add_argument("--no-bold", default="", help="comma-separated numeric columns to leave unmarked (e.g. Params)")
    parser.add_argument("--second", action="store_true", help="underline the second-best value")
    parser.add_argument("--decimals", type=int, help="round all numbers to this many decimals")
    parser.add_argument("--arrows", action="store_true", help="add up/down arrows to numeric column headers")
    parser.add_argument("--midrule-before", help="add a rule before rows whose label starts with this text")
    parser.add_argument("--position", default="t")
    parser.add_argument("--star", action="store_true", help="use table* (spans both columns)")
    parser.add_argument("--out")
    args = parser.parse_args()

    with open(args.csv, newline="", encoding="utf-8-sig") as handle:
        rows = [row for row in csv.reader(handle) if any(cell.strip() for cell in row)]
    if len(rows) < 2:
        print("error: the CSV needs a header row and at least one data row", file=sys.stderr)
        return 1
    split = lambda text: {name.strip() for name in text.split(",") if name.strip()}  # noqa: E731
    try:
        table = build_table(rows, args.caption, args.label, split(args.lower_is_better), split(args.no_bold),
                            args.second, args.decimals, args.arrows, args.midrule_before, args.position, args.star)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    if args.out:
        with open(args.out, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(table + "\n")
        print(f"wrote {args.out}")
    else:
        sys.stdout.reconfigure(encoding="utf-8")
        print(table)
    return 0


if __name__ == "__main__":
    sys.exit(main())
