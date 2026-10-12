#!/usr/bin/env python3
"""Power analysis: required sample size, achieved power, or minimum detectable effect.

Give two of {sample size, power, effect size}; the third is computed.
  - omit --n to solve for sample size (needs --effect and --power)
  - give --n and --effect to get achieved power
  - give --n and --power, omit --effect, to get the minimum detectable effect

Designs and their effect-size measure:
    ttest-ind     two independent groups           Cohen's d      (n is per group, group 1)
    ttest-paired  paired or one-sample             Cohen's dz     (n is number of pairs)
    anova         one-way, k groups                Cohen's f      (n is per group)
    proportions   two independent proportions      Cohen's h, or give --p1 and --p2
    correlation   Pearson r against zero           r
    chi2          chi-square test                  Cohen's w, with --df

Examples:
    python power_calc.py ttest-ind --effect 0.5 --power 0.8
    python power_calc.py anova --effect 0.25 --groups 3 --power 0.9 --dropout 0.15
    python power_calc.py proportions --p1 0.5 --p2 0.3 --power 0.8
    python power_calc.py ttest-paired --n 30 --effect 0.4
    python power_calc.py correlation --n 60 --power 0.8
"""

from __future__ import annotations

import argparse
import json
import math
import sys

from scipy import optimize, stats


def power_ttest_ind(n: float, d: float, alpha: float, ratio: float = 1.0, two_sided: bool = True) -> float:
    n2 = n * ratio
    df = n + n2 - 2
    ncp = d * math.sqrt(n * n2 / (n + n2))
    return _power_t(df, ncp, alpha, two_sided)


def power_ttest_paired(n: float, d: float, alpha: float, two_sided: bool = True) -> float:
    return _power_t(n - 1, d * math.sqrt(n), alpha, two_sided)


def _power_t(df: float, ncp: float, alpha: float, two_sided: bool) -> float:
    if df <= 0:
        return 0.0
    if two_sided:
        crit = stats.t.ppf(1 - alpha / 2, df)
        return float(stats.nct.sf(crit, df, ncp) + stats.nct.cdf(-crit, df, ncp))
    return float(stats.nct.sf(stats.t.ppf(1 - alpha, df), df, abs(ncp)))


def power_anova(n: float, f: float, alpha: float, groups: int) -> float:
    total = n * groups
    df1, df2 = groups - 1, total - groups
    if df2 <= 0:
        return 0.0
    crit = stats.f.ppf(1 - alpha, df1, df2)
    return float(stats.ncf.sf(crit, df1, df2, f * f * total))


def cohen_h(p1: float, p2: float) -> float:
    return 2 * math.asin(math.sqrt(p1)) - 2 * math.asin(math.sqrt(p2))


def power_proportions(n: float, h: float, alpha: float, ratio: float = 1.0, two_sided: bool = True) -> float:
    n2 = n * ratio
    return _power_normal(abs(h) * math.sqrt(n * n2 / (n + n2)), alpha, two_sided)


def power_correlation(n: float, r: float, alpha: float, two_sided: bool = True) -> float:
    if n <= 3:
        return 0.0
    return _power_normal(abs(math.atanh(r)) * math.sqrt(n - 3), alpha, two_sided)


def _power_normal(shift: float, alpha: float, two_sided: bool) -> float:
    if two_sided:
        crit = stats.norm.ppf(1 - alpha / 2)
        return float(stats.norm.sf(crit - shift) + stats.norm.cdf(-crit - shift))
    return float(stats.norm.sf(stats.norm.ppf(1 - alpha) - shift))


def power_chi2(n: float, w: float, alpha: float, df: int) -> float:
    crit = stats.chi2.ppf(1 - alpha, df)
    return float(stats.ncx2.sf(crit, df, n * w * w))


def _safe(value: float) -> float:
    """The noncentral distributions return NaN far in the tail, where power is effectively 1."""
    return 1.0 if math.isnan(value) else value


def solve_n(power_at, target: float, minimum: int = 2, maximum: int = 10_000_000) -> int:
    """Smallest integer n with power_at(n) >= target."""
    high = minimum
    while power_at(high) < target:  # grow the bracket instead of evaluating at huge n
        high *= 2
        if high > maximum:
            raise ValueError("required sample size exceeds 10,000,000; the effect is too small to detect")
    low = max(minimum, high // 2)
    while low < high:
        mid = (low + high) // 2
        if power_at(mid) >= target:
            high = mid
        else:
            low = mid + 1
    return low


def solve_effect(power_at_effect, target: float, upper: float) -> float:
    """Smallest effect size detected with the target power."""
    if power_at_effect(upper) < target:
        raise ValueError("this sample size cannot reach the target power for any plausible effect")
    return float(optimize.brentq(lambda e: power_at_effect(e) - target, 1e-6, upper))


def compute(design: str, effect: float | None, n: int | None, power: float | None, alpha: float = 0.05,
            ratio: float = 1.0, groups: int = 3, df: int = 1, two_sided: bool = True) -> dict:
    functions = {
        "ttest-ind": lambda n_, e: power_ttest_ind(n_, e, alpha, ratio, two_sided),
        "ttest-paired": lambda n_, e: power_ttest_paired(n_, e, alpha, two_sided),
        "anova": lambda n_, e: power_anova(n_, e, alpha, groups),
        "proportions": lambda n_, e: power_proportions(n_, e, alpha, ratio, two_sided),
        "correlation": lambda n_, e: power_correlation(n_, e, alpha, two_sided),
        "chi2": lambda n_, e: power_chi2(n_, e, alpha, df),
    }
    if design not in functions:
        raise ValueError(f"unknown design: {design}")
    raw = functions[design]
    fn = lambda n_, e: _safe(raw(n_, e))  # noqa: E731
    minimum_n = {"correlation": 4, "anova": 2, "chi2": 2}.get(design, 2)
    upper_effect = 0.999 if design == "correlation" else (math.pi if design == "proportions" else 10.0)

    if n is None:
        if effect is None or power is None:
            raise ValueError("to solve for sample size give --effect (or --p1/--p2) and --power")
        n = solve_n(lambda n_: fn(n_, effect), power, minimum_n)
        solved = "n"
    elif effect is None:
        if power is None:
            raise ValueError("with --n give --effect (to get power) or --power (to get the detectable effect)")
        effect = solve_effect(lambda e: fn(n, e), power, upper_effect)
        solved = "effect"
    else:
        solved = "power"
    achieved = fn(n, effect)

    result = {"design": design, "solved_for": solved, "effect_size": round(effect, 4), "alpha": alpha,
              "two_sided": two_sided if design not in ("anova", "chi2") else None,
              "target_power": power, "achieved_power": round(achieved, 4)}
    if design == "ttest-ind" or design == "proportions":
        n2 = math.ceil(n * ratio)
        result.update(n_group1=n, n_group2=n2, n_total=n + n2)
    elif design == "anova":
        result.update(groups=groups, n_per_group=n, n_total=n * groups)
    elif design == "ttest-paired":
        result.update(n_pairs=n, n_total=n)
    else:
        result.update(n_total=n)
        if design == "chi2":
            result["df"] = df
    return result


def add_dropout(result: dict, dropout: float) -> dict:
    """Inflate the total so the target n remains after the expected dropout."""
    if dropout:
        result["dropout"] = dropout
        result["n_total_to_recruit"] = math.ceil(result["n_total"] / (1 - dropout))
    return result


def sentence(result: dict) -> str:
    """A justification sentence for a methods section."""
    names = {"ttest-ind": ("an independent-samples t test", "d"), "ttest-paired": ("a paired-samples t test", "dz"),
             "anova": (f"a one-way ANOVA with {result.get('groups')} groups", "f"),
             "proportions": ("a two-proportion z test", "h"), "correlation": ("a test of a Pearson correlation", "r"),
             "chi2": (f"a chi-square test (df = {result.get('df')})", "w")}
    test, symbol = names[result["design"]]
    tail = {True: ", two-sided", False: ", one-sided", None: ""}[result["two_sided"]]
    size = (f"{result['n_per_group']} participants per group (N = {result['n_total']})" if result["design"] == "anova"
            else f"{result['n_group1']} and {result['n_group2']} participants in the two groups (N = {result['n_total']})"
            if "n_group1" in result else f"N = {result['n_total']}")
    text = (f"For {test} with alpha = {result['alpha']}{tail}, {size} gives power of "
            f"{result['achieved_power']:.2f} to detect an effect of {symbol} = {result['effect_size']}.")
    if "n_total_to_recruit" in result:
        text += (f" Allowing for {result['dropout']:.0%} attrition, {result['n_total_to_recruit']} "
                 f"participants should be recruited.")
    return text


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("design", choices=("ttest-ind", "ttest-paired", "anova", "proportions", "correlation", "chi2"))
    parser.add_argument("--effect", type=float, help="effect size in the design's measure")
    parser.add_argument("--p1", type=float, help="proportions only: expected proportion in group 1")
    parser.add_argument("--p2", type=float, help="proportions only: expected proportion in group 2")
    parser.add_argument("--n", type=int, help="sample size (per group, or pairs, or total; see design list)")
    parser.add_argument("--power", type=float, help="target power, e.g. 0.8")
    parser.add_argument("--alpha", type=float, default=0.05)
    parser.add_argument("--ratio", type=float, default=1.0, help="n2/n1 for two-group designs")
    parser.add_argument("--groups", type=int, default=3, help="anova only")
    parser.add_argument("--df", type=int, default=1, help="chi2 only")
    parser.add_argument("--one-sided", action="store_true")
    parser.add_argument("--dropout", type=float, default=0.0, help="expected attrition, e.g. 0.15")
    args = parser.parse_args()

    effect = args.effect
    if args.design == "proportions" and args.p1 is not None and args.p2 is not None:
        effect = abs(cohen_h(args.p1, args.p2))
    try:
        result = compute(args.design, effect, args.n, args.power, args.alpha, args.ratio, args.groups, args.df,
                         two_sided=not args.one_sided)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    add_dropout(result, args.dropout)
    result["statement"] = sentence(result)
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
