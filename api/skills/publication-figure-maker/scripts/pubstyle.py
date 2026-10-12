#!/usr/bin/env python3
"""Matplotlib settings for publication figures: correct physical size, readable fonts, safe colours.

Copy this file next to your plotting script (or add its folder to sys.path), then:

    import matplotlib.pyplot as plt
    import pubstyle

    pubstyle.apply("ieee")                               # fonts, line widths, embedded fonts
    fig, ax = plt.subplots(figsize=pubstyle.figsize("ieee", columns=1))
    ax.plot(x, y, color=pubstyle.PALETTE[0], marker=pubstyle.MARKERS[0], label="Ours")
    pubstyle.save(fig, "figures/accuracy")               # writes accuracy.pdf and accuracy.png

Command line:
    python pubstyle.py widths                            # list venue widths
    python pubstyle.py demo --venue neurips --out demo   # draw a sample figure

Widths are the column and text widths of each venue's standard template. Check
them against the current author kit before submission; templates change.
"""

from __future__ import annotations

import argparse
import sys

MM = 1 / 25.4  # inches per millimetre

# (single-column width, full text width) in inches
WIDTHS = {
    "ieee": (3.5, 7.16),
    "acm": (3.33, 7.0),
    "neurips": (5.5, 5.5),
    "icml": (3.25, 6.75),
    "iclr": (5.5, 5.5),
    "acl": (3.03, 6.3),
    "cvpr": (3.25, 6.875),
    "springer-lncs": (4.8, 4.8),
    "nature": (89 * MM, 183 * MM),
    "elsevier": (90 * MM, 190 * MM),
    "thesis-a4": (6.0, 6.0),
}

# Okabe-Ito palette: distinguishable under the common forms of colour-vision deficiency.
PALETTE = ["#0072B2", "#D55E00", "#009E73", "#CC79A7", "#E69F00", "#56B4E9", "#F0E442", "#000000"]
MARKERS = ["o", "s", "^", "D", "v", "P", "X", "*"]
LINESTYLES = ["-", "--", "-.", ":", (0, (5, 1)), (0, (3, 1, 1, 1))]


def figsize(venue: str = "ieee", columns: int = 1, aspect: float = 0.68, height: float | None = None) -> tuple[float, float]:
    """Figure size in inches. columns=1 is one column; columns=2 is the full text width."""
    if venue not in WIDTHS:
        raise ValueError(f"unknown venue {venue!r}; known: {', '.join(WIDTHS)}")
    if columns not in (1, 2):
        raise ValueError("columns must be 1 or 2")
    width = WIDTHS[venue][columns - 1]
    return (round(width, 3), round(height if height is not None else width * aspect, 3))


def rc(venue: str = "ieee", font_size: float = 8, serif: bool | None = None, usetex: bool = False) -> dict:
    """The rcParams this style sets, as a dict."""
    if serif is None:
        serif = venue not in ("nature", "acm")
    return {
        "font.size": font_size,
        "axes.labelsize": font_size,
        "axes.titlesize": font_size,
        "xtick.labelsize": font_size - 1,
        "ytick.labelsize": font_size - 1,
        "legend.fontsize": font_size - 1,
        "font.family": "serif" if serif else "sans-serif",
        "font.serif": ["Times New Roman", "Times", "Nimbus Roman", "DejaVu Serif"],
        "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
        "mathtext.fontset": "stix" if serif else "dejavusans",
        "text.usetex": usetex,
        "axes.linewidth": 0.6,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.prop_cycle": _cycler(),
        "lines.linewidth": 1.2,
        "lines.markersize": 3.5,
        "xtick.major.width": 0.6,
        "ytick.major.width": 0.6,
        "xtick.direction": "out",
        "ytick.direction": "out",
        "grid.linewidth": 0.4,
        "grid.alpha": 0.4,
        "legend.frameon": False,
        "legend.handlelength": 1.6,
        "figure.dpi": 150,
        "savefig.dpi": 300,
        "savefig.bbox": "standard",  # "tight" would crop the figure and change its width
        "pdf.fonttype": 42,   # embed TrueType fonts; Type 3 fonts are rejected by IEEE and ACM
        "ps.fonttype": 42,
        "figure.constrained_layout.use": True,
    }


def _cycler():
    from cycler import cycler
    return cycler(color=PALETTE)


def apply(venue: str = "ieee", font_size: float = 8, serif: bool | None = None, usetex: bool = False) -> None:
    """Set matplotlib rcParams for the venue. Call once before creating figures."""
    import matplotlib as mpl
    mpl.rcParams.update(rc(venue, font_size, serif, usetex))


def save(fig, path: str, formats: tuple[str, ...] = ("pdf", "png")) -> list[str]:
    """Save `path`.pdf (vector, for the paper) and `path`.png (300 dpi, for slides and previews)."""
    import os
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    written = []
    for extension in formats:
        name = f"{path}.{extension}"
        fig.savefig(name)
        written.append(name)
    return written


def demo(venue: str, columns: int, out: str) -> list[str]:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np

    apply(venue)
    x = np.arange(1, 11)
    fig, ax = plt.subplots(figsize=figsize(venue, columns))
    for i, name in enumerate(["Method A", "Method B", "Method C"]):
        y = 60 + 30 * (1 - np.exp(-x / (2.0 + i)))
        ax.plot(x, y, color=PALETTE[i], marker=MARKERS[i], linestyle=LINESTYLES[i], label=name)
        ax.fill_between(x, y - 1.5, y + 1.5, color=PALETTE[i], alpha=0.15, linewidth=0)
    ax.set_xlabel("Training epochs")
    ax.set_ylabel("Accuracy (%)")
    ax.legend(loc="lower right")
    written = save(fig, out)
    plt.close(fig)
    return written


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("widths", help="list venue widths in inches")
    p = sub.add_parser("demo", help="draw a sample figure with synthetic data")
    p.add_argument("--venue", default="ieee", choices=sorted(WIDTHS))
    p.add_argument("--columns", type=int, default=1, choices=(1, 2))
    p.add_argument("--out", default="pubstyle-demo", help="output path without extension")
    args = parser.parse_args()
    if args.command == "widths":
        print(f"{'venue':<15}{'one column':>12}{'full width':>12}   (inches)")
        for venue, (single, double) in WIDTHS.items():
            print(f"{venue:<15}{single:>12.2f}{double:>12.2f}")
    else:
        for name in demo(args.venue, args.columns, args.out):
            print(f"wrote {name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
