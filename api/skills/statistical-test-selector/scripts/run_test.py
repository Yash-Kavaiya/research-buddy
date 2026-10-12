#!/usr/bin/env python3
"""Check assumptions, pick a statistical test, run it, and report in APA style.

Reads a CSV in long format (one row per observation).

Subcommands:
    two-groups    compare a numeric outcome between two groups (add --paired with --subject)
    multi-groups  compare a numeric outcome across three or more independent groups
    correlation   association between two numeric variables
    categorical   association between two categorical variables

Examples:
    python run_test.py two-groups data.csv --value score --group condition
    python run_test.py two-groups data.csv --value score --group time --paired --subject id
    python run_test.py multi-groups data.csv --value accuracy --group model
    python run_test.py correlation data.csv --x hours --y grade
    python run_test.py categorical data.csv --row treatment --col outcome

The test is chosen from the assumption checks; --test overrides the choice.
"""

from __future__ import annotations

import argparse
import csv
import itertools
import json
import math
import sys

import numpy as np
from scipy import stats

NORMALITY_ALPHA = 0.05
LARGE_N = 30  # with n >= 30 per group the t and F tests tolerate non-normality


# ------------------------------------------------------------------ formatting


def fmt(value: float, digits: int = 2) -> str:
    return f"{value:.{digits}f}"


def fmt_p(p: float) -> str:
    return "p < .001" if p < 0.001 else "p = " + f"{p:.3f}".lstrip("0")


def fmt_unit(value: float, digits: int = 2) -> str:
    """APA drops the leading zero for statistics bounded by 1 (r, p, eta squared)."""
    text = f"{value:.{digits}f}"
    return text.replace("0.", ".", 1) if abs(value) < 1 else text


def describe(values: np.ndarray) -> dict:
    return {"n": int(values.size), "mean": float(np.mean(values)),
            "sd": float(np.std(values, ddof=1)) if values.size > 1 else float("nan"),
            "median": float(np.median(values))}


# ------------------------------------------------------------------ assumptions


def normality(values: np.ndarray) -> dict:
    if values.size < 3 or np.ptp(values) == 0:
        return {"test": "Shapiro-Wilk", "W": None, "p": None, "normal": values.size >= 3}
    w, p = stats.shapiro(values)
    return {"test": "Shapiro-Wilk", "W": float(w), "p": float(p), "normal": bool(p >= NORMALITY_ALPHA)}


def parametric_ok(groups: list[np.ndarray]) -> tuple[bool, str]:
    checks = [normality(g) for g in groups]
    if all(c["normal"] for c in checks):
        return True, "Shapiro-Wilk did not reject normality in any group"
    if all(g.size >= LARGE_N for g in groups):
        return True, f"normality was rejected, but every group has n >= {LARGE_N}, where the test is robust"
    return False, f"Shapiro-Wilk rejected normality and at least one group has n < {LARGE_N}"


def holm(p_values: list[float]) -> list[float]:
    """Holm step-down adjusted p-values, in the original order."""
    order = sorted(range(len(p_values)), key=lambda i: p_values[i])
    adjusted = [0.0] * len(p_values)
    running = 0.0
    for rank, index in enumerate(order):
        running = max(running, (len(p_values) - rank) * p_values[index])
        adjusted[index] = min(1.0, running)
    return adjusted


# ------------------------------------------------------------------ two groups


def hedges_g(a: np.ndarray, b: np.ndarray) -> float:
    pooled = math.sqrt(((a.size - 1) * np.var(a, ddof=1) + (b.size - 1) * np.var(b, ddof=1)) / (a.size + b.size - 2))
    d = (np.mean(a) - np.mean(b)) / pooled
    return float(d * (1 - 3 / (4 * (a.size + b.size) - 9)))


def two_groups(a: np.ndarray, b: np.ndarray, names: tuple[str, str], paired: bool = False,
               force: str | None = None) -> dict:
    result = {"design": "paired" if paired else "independent",
              "descriptives": {names[0]: describe(a), names[1]: describe(b)}}
    if paired:
        diff = a - b
        ok, reason = parametric_ok([diff])
        test = force or ("paired-t" if ok else "wilcoxon")
        result["assumptions"] = {"normality_of_differences": normality(diff)}
        if test == "paired-t":
            t, p = stats.ttest_rel(a, b)
            dz = float(np.mean(diff) / np.std(diff, ddof=1))
            result.update(test="Paired-samples t test", statistic=float(t), df=int(a.size - 1), p=float(p),
                          effect_size={"name": "Cohen's dz", "value": dz},
                          apa=f"t({a.size - 1}) = {fmt(t)}, {fmt_p(p)}, dz = {fmt(dz)}")
        else:
            res = stats.wilcoxon(a, b)
            nonzero = diff[diff != 0]
            ranks = stats.rankdata(np.abs(nonzero))
            r_rb = float((ranks[nonzero > 0].sum() - ranks[nonzero < 0].sum()) / ranks.sum())
            result.update(test="Wilcoxon signed-rank test", statistic=float(res.statistic), p=float(res.pvalue),
                          effect_size={"name": "matched-pairs rank-biserial r", "value": r_rb},
                          apa=f"W = {fmt(res.statistic, 1)}, {fmt_p(res.pvalue)}, r = {fmt_unit(r_rb)}")
        result["reason"] = reason if not force else "test forced with --test"
        return result

    ok, reason = parametric_ok([a, b])
    levene_stat, levene_p = stats.levene(a, b)
    result["assumptions"] = {"normality": {names[0]: normality(a), names[1]: normality(b)},
                             "levene": {"W": float(levene_stat), "p": float(levene_p)}}
    test = force or ("welch-t" if ok else "mann-whitney")
    if test in ("welch-t", "student-t"):
        res = stats.ttest_ind(a, b, equal_var=(test == "student-t"))
        g = hedges_g(a, b)
        ci = res.confidence_interval()
        label = "Welch's t test" if test == "welch-t" else "Student's t test"
        result.update(test=label, statistic=float(res.statistic), df=float(res.df), p=float(res.pvalue),
                      mean_difference=float(np.mean(a) - np.mean(b)), ci95=[float(ci.low), float(ci.high)],
                      effect_size={"name": "Hedges' g", "value": g},
                      apa=f"t({fmt(res.df)}) = {fmt(res.statistic)}, {fmt_p(res.pvalue)}, g = {fmt(g)}, "
                          f"95% CI of the difference [{fmt(ci.low)}, {fmt(ci.high)}]")
        if not force:
            reason += "; Welch's test is used because it does not assume equal variances"
    else:
        res = stats.mannwhitneyu(a, b, alternative="two-sided")
        r_rb = float(2 * res.statistic / (a.size * b.size) - 1)
        result.update(test="Mann-Whitney U test", statistic=float(res.statistic), p=float(res.pvalue),
                      effect_size={"name": "rank-biserial r", "value": r_rb},
                      apa=f"U = {fmt(res.statistic, 1)}, {fmt_p(res.pvalue)}, r = {fmt_unit(r_rb)}")
    result["reason"] = reason if not force else "test forced with --test"
    return result


# ---------------------------------------------------------------- multi groups


def welch_anova(groups: list[np.ndarray]) -> tuple[float, float, float, float]:
    k = len(groups)
    n = np.array([g.size for g in groups], dtype=float)
    means = np.array([g.mean() for g in groups])
    weights = n / np.array([g.var(ddof=1) for g in groups])
    grand = (weights * means).sum() / weights.sum()
    lam = (((1 - weights / weights.sum()) ** 2) / (n - 1)).sum()
    f = ((weights * (means - grand) ** 2).sum() / (k - 1)) / (1 + 2 * (k - 2) * lam / (k * k - 1))
    df2 = (k * k - 1) / (3 * lam)
    return float(f), float(k - 1), float(df2), float(stats.f.sf(f, k - 1, df2))


def multi_groups(groups: dict[str, np.ndarray], force: str | None = None) -> dict:
    names, arrays = list(groups), list(groups.values())
    ok, reason = parametric_ok(arrays)
    levene_stat, levene_p = stats.levene(*arrays)
    equal_var = levene_p >= 0.05
    result = {"descriptives": {name: describe(values) for name, values in groups.items()},
              "assumptions": {"normality": {name: normality(values) for name, values in groups.items()},
                              "levene": {"W": float(levene_stat), "p": float(levene_p)}}}
    test = force or ("kruskal" if not ok else ("anova" if equal_var else "welch-anova"))
    pairs = list(itertools.combinations(range(len(names)), 2))

    if test == "anova":
        f, p = stats.f_oneway(*arrays)
        total = np.concatenate(arrays)
        ss_between = sum(g.size * (g.mean() - total.mean()) ** 2 for g in arrays)
        eta2 = float(ss_between / ((total - total.mean()) ** 2).sum())
        df1, df2 = len(arrays) - 1, total.size - len(arrays)
        tukey = stats.tukey_hsd(*arrays)
        posthoc = [{"pair": [names[i], names[j]], "p_adjusted": float(tukey.pvalue[i, j])} for i, j in pairs]
        result.update(test="One-way ANOVA", statistic=float(f), df=[df1, df2], p=float(p),
                      effect_size={"name": "eta squared", "value": eta2},
                      apa=f"F({df1}, {df2}) = {fmt(f)}, {fmt_p(p)}, eta squared = {fmt_unit(eta2)}",
                      posthoc={"method": "Tukey HSD", "comparisons": posthoc})
        reason += "; Levene's test did not reject equal variances"
    elif test == "welch-anova":
        f, df1, df2, p = welch_anova(arrays)
        raw = [float(stats.ttest_ind(arrays[i], arrays[j], equal_var=False).pvalue) for i, j in pairs]
        posthoc = [{"pair": [names[i], names[j]], "p_adjusted": adj} for (i, j), adj in zip(pairs, holm(raw))]
        result.update(test="Welch's ANOVA", statistic=f, df=[df1, df2], p=p,
                      apa=f"Welch's F({int(df1)}, {fmt(df2)}) = {fmt(f)}, {fmt_p(p)}",
                      posthoc={"method": "pairwise Welch t tests, Holm-adjusted", "comparisons": posthoc})
        reason += "; Levene's test rejected equal variances"
    else:
        h, p = stats.kruskal(*arrays)
        n_total = sum(g.size for g in arrays)
        eps2 = float(h / (n_total - 1))
        raw = [float(stats.mannwhitneyu(arrays[i], arrays[j], alternative="two-sided").pvalue) for i, j in pairs]
        posthoc = [{"pair": [names[i], names[j]], "p_adjusted": adj} for (i, j), adj in zip(pairs, holm(raw))]
        result.update(test="Kruskal-Wallis test", statistic=float(h), df=len(arrays) - 1, p=float(p),
                      effect_size={"name": "epsilon squared", "value": eps2},
                      apa=f"H({len(arrays) - 1}) = {fmt(h)}, {fmt_p(p)}, epsilon squared = {fmt_unit(eps2)}",
                      posthoc={"method": "pairwise Mann-Whitney U tests, Holm-adjusted", "comparisons": posthoc})
    result["reason"] = reason if not force else "test forced with --test"
    return result


# ----------------------------------------------------------------- correlation


def correlation(x: np.ndarray, y: np.ndarray, force: str | None = None) -> dict:
    ok, reason = parametric_ok([x, y])
    test = force or ("pearson" if ok else "spearman")
    result = {"n": int(x.size), "assumptions": {"normality": {"x": normality(x), "y": normality(y)}}}
    if test == "pearson":
        res = stats.pearsonr(x, y)
        ci = res.confidence_interval()
        result.update(test="Pearson correlation", statistic=float(res.statistic), df=int(x.size - 2),
                      p=float(res.pvalue), ci95=[float(ci.low), float(ci.high)],
                      apa=f"r({x.size - 2}) = {fmt_unit(res.statistic)}, {fmt_p(res.pvalue)}, "
                          f"95% CI [{fmt_unit(ci.low)}, {fmt_unit(ci.high)}]")
    else:
        res = stats.spearmanr(x, y)
        result.update(test="Spearman rank correlation", statistic=float(res.statistic), df=int(x.size - 2),
                      p=float(res.pvalue),
                      apa=f"rs({x.size - 2}) = {fmt_unit(res.statistic)}, {fmt_p(res.pvalue)}")
    result["reason"] = reason if not force else "test forced with --test"
    return result


# ----------------------------------------------------------------- categorical


def categorical(table: np.ndarray, row_labels: list[str], col_labels: list[str], force: str | None = None) -> dict:
    chi2, p, df, expected = stats.chi2_contingency(table, correction=False)
    small = bool((expected < 5).any())
    is_2x2 = table.shape == (2, 2)
    test = force or ("fisher" if small and is_2x2 else "chi2")
    n = int(table.sum())
    result = {"table": {"rows": row_labels, "cols": col_labels, "counts": table.tolist()},
              "assumptions": {"min_expected_count": float(expected.min()), "any_expected_below_5": small}}
    if test == "fisher":
        odds, p_f = stats.fisher_exact(table)
        result.update(test="Fisher's exact test", statistic=float(odds), p=float(p_f),
                      effect_size={"name": "odds ratio", "value": float(odds)},
                      apa=f"Fisher's exact test, {fmt_p(p_f)}, OR = {fmt(odds)}",
                      reason="an expected count is below 5 in a 2x2 table")
    else:
        v = float(math.sqrt(chi2 / (n * (min(table.shape) - 1))))
        result.update(test="Chi-square test of independence", statistic=float(chi2), df=int(df), p=float(p),
                      effect_size={"name": "Cramer's V", "value": v},
                      apa=f"chi-square({df}, N = {n}) = {fmt(chi2)}, {fmt_p(p)}, V = {fmt_unit(v)}",
                      reason="all expected counts are at least 5" if not small else
                             "expected counts below 5 in a table larger than 2x2: interpret with caution, "
                             "or merge sparse categories")
    if force:
        result["reason"] = "test forced with --test"
    return result


# ------------------------------------------------------------------------- CLI


def read_rows(path: str) -> list[dict]:
    with open(path, newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def numeric(rows: list[dict], column: str) -> list[float | None]:
    values = []
    for row in rows:
        try:
            value = float(row[column])
            values.append(None if math.isnan(value) else value)
        except (TypeError, ValueError):
            values.append(None)
        except KeyError:
            raise SystemExit(f"error: column {column!r} not found; columns are {list(row)}")
    return values


def grouped(rows: list[dict], value: str, group: str) -> dict[str, np.ndarray]:
    groups: dict[str, list[float]] = {}
    for row, number in zip(rows, numeric(rows, value)):
        if group not in row:
            raise SystemExit(f"error: column {group!r} not found; columns are {list(row)}")
        if number is not None and (row[group] or "").strip():
            groups.setdefault(row[group].strip(), []).append(number)
    return {name: np.array(values) for name, values in groups.items()}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("two-groups")
    p.add_argument("csv"); p.add_argument("--value", required=True); p.add_argument("--group", required=True)
    p.add_argument("--paired", action="store_true"); p.add_argument("--subject", help="id column, required with --paired")
    p.add_argument("--test", choices=("welch-t", "student-t", "mann-whitney", "paired-t", "wilcoxon"))
    p = sub.add_parser("multi-groups")
    p.add_argument("csv"); p.add_argument("--value", required=True); p.add_argument("--group", required=True)
    p.add_argument("--test", choices=("anova", "welch-anova", "kruskal"))
    p = sub.add_parser("correlation")
    p.add_argument("csv"); p.add_argument("--x", required=True); p.add_argument("--y", required=True)
    p.add_argument("--test", choices=("pearson", "spearman"))
    p = sub.add_parser("categorical")
    p.add_argument("csv"); p.add_argument("--row", required=True); p.add_argument("--col", required=True)
    p.add_argument("--test", choices=("chi2", "fisher"))
    args = parser.parse_args()
    rows = read_rows(args.csv)

    if args.command == "two-groups":
        groups = grouped(rows, args.value, args.group)
        if len(groups) != 2:
            raise SystemExit(f"error: expected 2 groups in {args.group!r}, found {len(groups)}: {list(groups)}")
        (name_a, a), (name_b, b) = groups.items()
        if args.paired:
            if not args.subject:
                raise SystemExit("error: --paired needs --subject to match observations")
            by_subject: dict[str, dict[str, float]] = {}
            for row, number in zip(rows, numeric(rows, args.value)):
                if number is not None:
                    by_subject.setdefault(row[args.subject], {})[row[args.group].strip()] = number
            complete = [v for v in by_subject.values() if name_a in v and name_b in v]
            a, b = np.array([v[name_a] for v in complete]), np.array([v[name_b] for v in complete])
        result = two_groups(a, b, (name_a, name_b), paired=args.paired, force=args.test)
    elif args.command == "multi-groups":
        groups = grouped(rows, args.value, args.group)
        if len(groups) < 3:
            raise SystemExit(f"error: expected 3 or more groups, found {len(groups)}; use two-groups")
        result = multi_groups(groups, force=args.test)
    elif args.command == "correlation":
        pairs = [(x, y) for x, y in zip(numeric(rows, args.x), numeric(rows, args.y)) if x is not None and y is not None]
        result = correlation(np.array([p[0] for p in pairs]), np.array([p[1] for p in pairs]), force=args.test)
    else:
        cells = [(r[args.row].strip(), r[args.col].strip()) for r in rows
                 if (r.get(args.row) or "").strip() and (r.get(args.col) or "").strip()]
        row_labels = sorted({c[0] for c in cells}); col_labels = sorted({c[1] for c in cells})
        table = np.zeros((len(row_labels), len(col_labels)), dtype=int)
        for r, c in cells:
            table[row_labels.index(r), col_labels.index(c)] += 1
        result = categorical(table, row_labels, col_labels, force=args.test)

    print(json.dumps(result, indent=2, default=float))
    return 0


if __name__ == "__main__":
    sys.exit(main())
