"""Figures for Part 2 of the v3 deck (DAS, deployment, outlook), in the same style as make_v3_figures.py.

  transition.png  - from a single RoF link (Part 1) to a fiber-fed DAS (Part 2)
  das_concept.png - what a DAS is: one signal source, many low-power antennas in a building
  das_types.png   - passive, active (fiber) and hybrid DAS
  das_arch.png    - multi-operator fiber DAS: base stations -> POI -> master unit -> fiber -> remote units
  stadium.png     - stadium coverage with fiber-fed remote units (documented case)
  demo.png        - research demo: 5G-NR + candidate 6G signal on one fiber
  coax_loss.png   - coax loss per 100 m at DAS frequencies vs fiber

Usage: python3 make_part2_figures.py <output_dir>
"""
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, Ellipse, FancyBboxPatch, Polygon, Rectangle

from make_v3_figures import (LYEL, YEL, arrow, canvas, handset, lattice_tower, server, span, ybox)

OUT = sys.argv[1] if len(sys.argv) > 1 else "figs_part2"
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.family": "Liberation Sans", "font.size": 12})

B = dict(fontsize=13, fontweight="bold")
L = dict(fontsize=11, style="italic", color="#444444")
FIBER = "#E67E22"      # fiber drawn orange
COAX = "#2B2B2B"       # coax drawn thick black
RU_FILL = "#D6E4F5"
MU_FILL = YEL


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=300, facecolor="white")
    plt.close(fig)


def fib(ax, xs, ys, lw=2.4, z=3):
    ax.plot(xs, ys, color=FIBER, lw=lw, solid_capstyle="round", zorder=z)


def coax(ax, xs, ys, lw=3.0, z=3):
    ax.plot(xs, ys, color=COAX, lw=lw, solid_capstyle="round", zorder=z)


def unit(ax, x, y, w, h, text, fc=RU_FILL, ec="#2B5C8A", fs=11):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.05", fc=fc, ec=ec, lw=1.3, zorder=5))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs, fontweight="bold", zorder=6, linespacing=1.1)


def bts(ax, x, y, label=None, w=0.42, h=0.7):
    """Base-station cabinet."""
    ax.add_patch(Rectangle((x, y), w, h, fc="#9E9E9E", ec="#424242", lw=1.2, zorder=5))
    for k in range(4):
        ax.add_patch(Rectangle((x + 0.06, y + 0.08 + k * 0.15), w - 0.12, 0.09, fc="#E0E0E0", ec="#616161", lw=0.6, zorder=6))
        ax.add_patch(Circle((x + w - 0.1, y + 0.125 + k * 0.15), 0.015, fc="#4CAF50", ec="none", zorder=7))
    if label:
        ax.text(x + w / 2, y - 0.08, label, ha="center", va="top", **L)


def ceiling_antenna(ax, x, y, s=1.0):
    """Indoor omni ceiling antenna, (x, y) = ceiling mount point."""
    ax.add_patch(Ellipse((x, y - 0.06 * s), 0.26 * s, 0.12 * s, fc="white", ec="#424242", lw=1.1, zorder=6))
    ax.plot([x, x], [y, y - 0.02 * s], color="#424242", lw=1, zorder=6)


def waves(ax, x, y, r=(0.12, 0.2), color="#707070"):
    for rr in r:
        ax.add_patch(matplotlib.patches.Arc((x, y), rr * 2, rr * 2, theta1=200, theta2=340, color=color, lw=1.1, zorder=6))


# =============================================================== transition
def f_transition():
    fig, ax = canvas(11, 3.4)
    # left: one RoF link (Part 1)
    ax.add_patch(FancyBboxPatch((0.15, 0.55), 4.3, 2.2, boxstyle="round,pad=0.03,rounding_size=0.2", fc="#F7F7F7", ec="#B0B0B0", lw=1.2, ls=(0, (5, 3))))
    ax.text(2.3, 2.45, "Part 1: one RoF link", ha="center", **B)
    ybox(ax, 0.4, 1.3, 0.75, 0.6, "E/O", 12)
    fib(ax, [1.15, 3.1], [1.6, 1.6])
    ax.add_patch(Circle((2.07, 1.6), 0.1, fill=False, ec=FIBER, lw=1.4, zorder=4))
    ax.add_patch(Circle((2.2, 1.6), 0.1, fill=False, ec=FIBER, lw=1.4, zorder=4))
    ax.text(2.13, 1.85, "fiber", ha="center", **L)
    ybox(ax, 3.1, 1.3, 0.75, 0.6, "O/E", 12)
    ax.plot([3.85, 4.1, 4.1], [1.6, 1.6, 1.9], color="black", lw=1.3, zorder=3)
    ax.add_patch(Polygon([[4.0, 2.12], [4.2, 2.12], [4.1, 1.9]], fc="black", zorder=4))
    ax.text(2.3, 0.75, "E/O → fiber → O/E", ha="center", **L)
    # big arrow
    ax.add_patch(matplotlib.patches.FancyArrow(4.65, 1.65, 0.8, 0, width=0.28, head_width=0.6, head_length=0.35,
                                               fc="#D9534F", ec="none", zorder=3))
    ax.text(5.15, 2.25, "deployed\nat scale", ha="center", **L)
    # right: fiber DAS (Part 2)
    ax.add_patch(FancyBboxPatch((6.0, 0.15), 4.85, 3.05, boxstyle="round,pad=0.03,rounding_size=0.2", fc="#F7F7F7", ec="#B0B0B0", lw=1.2, ls=(0, (5, 3))))
    ax.text(8.42, 2.92, "Part 2: fiber-fed DAS", ha="center", **B)
    bts(ax, 6.2, 1.25, "base station")
    coax(ax, [6.62, 7.0], [1.6, 1.6], lw=2)
    unit(ax, 7.0, 1.25, 0.85, 0.7, "Master\nunit", MU_FILL, "#6B5B00", 11)
    for k, yy in enumerate((2.45, 1.6, 0.75)):
        fib(ax, [7.85, 8.25, 8.25, 8.7], [1.6, 1.6, yy, yy])
        unit(ax, 8.7, yy - 0.25, 0.85, 0.5, "Remote\nunit", fs=10)
        for j, ax_ in enumerate((9.85, 10.35)):
            ax.plot([9.55, ax_], [yy, yy], color=COAX, lw=1.4, zorder=3)
            ceiling_antenna(ax, ax_, yy + 0.06)
    ax.text(8.42, 0.25, "one signal source → many antennas", ha="center", **L)
    save(fig, "transition.png")


# =============================================================== DAS concept
def f_das_concept():
    fig, ax = canvas(11, 4.4)
    bx, bw, fh, n = 0.3, 6.6, 0.95, 4
    for i in range(n):
        ax.add_patch(Rectangle((bx, 0.3 + i * fh), bw, fh, fc="#FAFAFA", ec="#424242", lw=1.3, zorder=1))
    ax.add_patch(Polygon([[bx - 0.1, 0.3 + n * fh], [bx + bw + 0.1, 0.3 + n * fh], [bx + bw + 0.1, 0.3 + n * fh + 0.08], [bx - 0.1, 0.3 + n * fh + 0.08]], fc="#9E9E9E", ec="#424242", lw=1))
    # ground floor equipment room
    ax.add_patch(Rectangle((bx + 0.1, 0.38), 2.4, 0.78, fc="#FFF8E1", ec="#B08900", lw=1.1, ls=(0, (4, 3)), zorder=2))
    ax.text(bx + 2.45, 0.42, "Equipment room", ha="right", va="bottom", fontsize=10, fontweight="bold", color="#8D6E00", zorder=3)
    bts(ax, bx + 0.25, 0.42, None, w=0.36, h=0.56)
    coax(ax, [bx + 0.61, bx + 1.0], [0.7, 0.7], lw=2)
    unit(ax, bx + 1.0, 0.48, 0.95, 0.45, "Head-end", MU_FILL, "#6B5B00", 10)
    rx = bx + 2.75
    fib(ax, [bx + 1.95, rx, rx], [0.7, 0.7, 0.3 + (n - 1) * fh + 0.62])
    ax.text(rx + 0.08, 1.0, "fiber riser", ha="left", rotation=90, **L)
    for i in range(1, n):
        y = 0.3 + i * fh
        fib(ax, [rx, rx + 0.3], [y + 0.62, y + 0.62])
        unit(ax, rx + 0.3, y + 0.45, 0.7, 0.34, "RU", fs=10)
        ax.plot([rx + 1.0, bx + bw - 0.4], [y + fh - 0.12, y + fh - 0.12], color=COAX, lw=1.2, zorder=2)
        ax.plot([rx + 0.65, rx + 0.65, rx + 1.0], [y + 0.79, y + fh - 0.12, y + fh - 0.12], color=COAX, lw=1.2, zorder=2)
        for xa in (rx + 1.6, rx + 2.9, bx + bw - 0.4):
            ceiling_antenna(ax, xa, y + fh - 0.12)
            waves(ax, xa, y + fh - 0.25)
        handset(ax, rx + 2.15, y + 0.12, w=0.12, h=0.22)
        handset(ax, rx + 3.5, y + 0.12, w=0.12, h=0.22)
    # outdoor macro
    mx = 9.6
    lattice_tower(ax, mx, 0.3, h=2.9)
    arrow(ax, (mx - 0.3, 3.0), (bx + bw + 0.15, 2.6), color="#707070", lw=1.5, ls=(0, (4, 3)))
    ax.plot([bx + bw + 0.25], [2.62], marker="x", color="#D9534F", ms=16, mew=3.5, zorder=8)
    ax.text(8.25, 3.3, "outdoor signal is weakened\nby walls and distance", ha="center", **L)
    ax.text(mx, 0.05, "outdoor macro site", ha="center", **L)
    # numbered steps
    steps = [((bx + 0.43, 1.05), "1"), ((bx + 1.47, 1.05), "2"), ((rx + 1.95, 0.3 + 3 * fh + 0.62), "3")]
    for (x, y), t in steps:
        ax.add_patch(Circle((x, y), 0.14, fc="#D9534F", ec="none", zorder=9))
        ax.text(x, y, t, ha="center", va="center", color="white", fontsize=11, fontweight="bold", zorder=10)
    save(fig, "das_concept.png")


# =============================================================== DAS types
def mini_bts(ax, x, y):
    bts(ax, x, y, None, w=0.3, h=0.5)


def f_das_types():
    fig, ax = canvas(11, 3.9)
    titles = ["Passive DAS", "Active (fiber) DAS", "Hybrid DAS"]
    for k, t in enumerate(titles):
        x0 = 0.1 + k * 3.65
        ax.add_patch(FancyBboxPatch((x0, 0.55), 3.45, 3.1, boxstyle="round,pad=0.02,rounding_size=0.15", fc="#FAFAFA", ec="#B0B0B0", lw=1.1))
        ax.text(x0 + 1.72, 3.38, t, ha="center", **B)
    ys = (2.75, 1.85, 0.95)
    # passive: BTS -> coax -> splitters -> antennas
    x0 = 0.1
    mini_bts(ax, x0 + 0.15, 1.6)
    coax(ax, [x0 + 0.45, x0 + 1.25], [1.85, 1.85])
    ax.add_patch(Circle((x0 + 1.35, 1.85), 0.11, fc="white", ec="black", lw=1.3, zorder=5))
    ax.text(x0 + 1.35, 1.85, "S", ha="center", va="center", fontsize=9, fontweight="bold", zorder=6)
    for yy in ys:
        coax(ax, [x0 + 1.46, x0 + 2.0, x0 + 3.0], [1.85, yy, yy])
        ceiling_antenna(ax, x0 + 3.0, yy + 0.08)
    ax.text(x0 + 1.72, 0.65, "coax + splitters", ha="center", **L)
    # active: BTS -> MU -> fiber -> RUs -> antenna
    x0 = 3.75
    mini_bts(ax, x0 + 0.1, 1.6)
    coax(ax, [x0 + 0.4, x0 + 0.6], [1.85, 1.85], lw=2)
    unit(ax, x0 + 0.6, 1.6, 0.6, 0.5, "MU", MU_FILL, "#6B5B00", 10)
    for yy in ys:
        fib(ax, [x0 + 1.2, x0 + 1.6, x0 + 1.6, x0 + 2.1], [1.85, 1.85, yy, yy])
        unit(ax, x0 + 2.1, yy - 0.18, 0.55, 0.36, "RU", fs=10)
        ax.plot([x0 + 2.65, x0 + 3.05], [yy, yy], color=COAX, lw=1.3, zorder=3)
        ceiling_antenna(ax, x0 + 3.05, yy + 0.08)
    ax.text(x0 + 1.72, 0.65, "fiber to every remote unit", ha="center", **L)
    # hybrid: BTS -> MU -> fiber -> one RU per zone -> coax -> antennas
    x0 = 7.4
    mini_bts(ax, x0 + 0.1, 1.6)
    coax(ax, [x0 + 0.4, x0 + 0.6], [1.85, 1.85], lw=2)
    unit(ax, x0 + 0.6, 1.6, 0.6, 0.5, "MU", MU_FILL, "#6B5B00", 10)
    fib(ax, [x0 + 1.2, x0 + 1.75], [1.85, 1.85])
    unit(ax, x0 + 1.75, 1.67, 0.55, 0.36, "RU", fs=10)
    ax.add_patch(Circle((x0 + 2.5, 1.85), 0.1, fc="white", ec="black", lw=1.2, zorder=5))
    ax.text(x0 + 2.5, 1.85, "S", ha="center", va="center", fontsize=8, fontweight="bold", zorder=6)
    coax(ax, [x0 + 2.3, x0 + 2.4], [1.85, 1.85], lw=2)
    for yy in ys:
        coax(ax, [x0 + 2.6, x0 + 2.85, x0 + 3.1], [1.85, yy, yy], lw=2)
        ceiling_antenna(ax, x0 + 3.1, yy + 0.08)
    ax.text(x0 + 1.72, 0.65, "fiber per zone, short coax", ha="center", **L)
    # legend
    coax(ax, [3.6, 4.2], [0.2, 0.2])
    ax.text(4.3, 0.2, "coax (RF)", va="center", **L)
    fib(ax, [5.6, 6.2], [0.2, 0.2])
    ax.text(6.3, 0.2, "fiber (RF over fiber)", va="center", **L)
    ax.text(0.15, 0.2, "MU: master unit · RU: remote unit · S: splitter", va="center", fontsize=10, color="#444444")
    save(fig, "das_types.png")


# =============================================================== coax loss bar chart
def f_coax_loss():
    # Times Microwave LMR-400 attenuation formula: dB/100 ft = 0.122290*sqrt(f) + 0.000260*f, f in MHz
    f = np.array([700, 1800, 2600, 3500])
    db100m = (0.122290 * np.sqrt(f) + 0.000260 * f) / 0.3048
    fig, ax = plt.subplots(figsize=(6.2, 4.3))
    bars = ax.bar([f"{v} MHz" for v in f], db100m, color=["#9E9E9E", "#9E9E9E", "#9E9E9E", "#D9534F"], width=0.6, zorder=3)
    for b, v in zip(bars, db100m):
        ax.text(b.get_x() + b.get_width() / 2, v + 0.6, f"{v:.1f} dB", ha="center", fontsize=12, fontweight="bold")
    ax.axhline(0.025, color=FIBER, lw=2.5, zorder=4)
    ax.text(3.45, 1.4, "single-mode fiber: ≈ 0.025 dB / 100 m\n(any RF band)", ha="right", fontsize=11, color="#B85C00", fontweight="bold")
    ax.set_ylabel("Coax loss per 100 m (dB)", fontsize=12)
    ax.set_ylim(0, 32)
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", color="#E6E6E6", zorder=0)
    ax.set_title("LMR-400 coax loss at common mobile bands", fontsize=12, fontweight="bold")
    fig.tight_layout()
    save(fig, "coax_loss.png")


# =============================================================== multi-operator DAS architecture
def f_das_arch():
    fig, ax = canvas(11, 4.2)
    # operators
    for k, (y, name) in enumerate(((2.95, "Operator A"), (1.85, "Operator B"), (0.75, "Operator C"))):
        arrow(ax, (0.15, y + 0.3), (0.55, y + 0.3), color="#707070", lw=1.2)
        bts(ax, 0.6, y, None, w=0.42, h=0.62)
        ax.text(0.81, y - 0.08, name, ha="center", va="top", **L)
        coax(ax, [1.02, 1.6], [y + 0.31, y + 0.31], lw=2)
    ax.text(0.05, 3.85, "from each operator's core (backhaul)", ha="left", **L)
    unit(ax, 1.6, 0.85, 1.05, 2.8, "POI\n\nlevel control\n& combining", "#EDE7F6", "#5E35B1", 11)
    coax(ax, [2.65, 3.15], [2.25, 2.25], lw=2.5)
    unit(ax, 3.15, 1.45, 1.15, 1.6, "Master\nunit\n\nRF ↔ optical", MU_FILL, "#6B5B00", 11)
    rus = [3.1, 1.85, 0.6]
    for k, y in enumerate(rus):
        fib(ax, [4.3, 4.7, 4.7, 6.4], [2.25, 2.25, y + 0.3, y + 0.3], lw=2.6)
        unit(ax, 6.4, y, 1.1, 0.6, "Remote unit\nO/E · E/O · amps", fs=9)
        ax.plot([7.5, 7.85], [y + 0.3, y + 0.3], color=COAX, lw=1.4, zorder=3)
        ceiling_antenna(ax, 7.95, y + 0.42)
        ax.plot([7.85, 7.85, 7.95], [y + 0.3, y + 0.36, y + 0.36], color=COAX, lw=1.4, zorder=3)
        ax.add_patch(Ellipse((9.1, y + 0.35), 2.0, 0.85, fc=["#DDEFD9", "#FBEFC9", "#E3F2FD"][k], ec="none", zorder=0))
        handset(ax, 8.6, y + 0.2, w=0.13, h=0.24)
        handset(ax, 9.5, y + 0.25, w=0.13, h=0.24)
        ax.plot([8.05, 8.66], [y + 0.36, y + 0.42], color="#707070", lw=1, ls=(0, (3, 2)), zorder=2)
        ax.plot([8.05, 9.56], [y + 0.36, y + 0.48], color="#707070", lw=1, ls=(0, (3, 2)), zorder=2)
    ax.text(9.1, 0.12, "coverage zones (floors, halls, tunnels)", ha="center", **L)
    span(ax, 4.3, 6.4, 3.85, "RoF links")
    ax.text(5.35, 0.12, "fiber: DL and UL", ha="center", **L)
    save(fig, "das_arch.png")


# =============================================================== subway case
def f_subway():
    fig, ax = canvas(11, 4.3)
    gy = 3.0                                   # street level
    ax.add_patch(Rectangle((0, gy), 11, 0.04, fc="#616161", ec="none"))
    ax.add_patch(Rectangle((0, 0.15), 11, gy - 0.15, fc="#EFEBE9", ec="none", zorder=0))
    ax.text(10.9, gy + 0.08, "street level", ha="right", va="bottom", **L)
    # base-station hotel above ground
    ax.add_patch(Rectangle((0.3, gy + 0.04), 2.6, 1.05, fc="#FFF8E1", ec="#B08900", lw=1.2, zorder=2))
    ax.text(1.6, gy + 0.98, "Base-station hotel (4 operators)", ha="center", va="top", fontsize=11, fontweight="bold", color="#8D6E00")
    for k in range(4):
        bts(ax, 0.42 + k * 0.38, gy + 0.12, None, w=0.3, h=0.5)
    unit(ax, 2.0, gy + 0.15, 0.8, 0.5, "MU", MU_FILL, "#6B5B00", 10)
    # two stations + tunnel
    stations = [(3.2, 5.7), (7.6, 10.6)]
    for x0, x1 in stations:
        ax.add_patch(Rectangle((x0, 1.0), x1 - x0, 1.35, fc="#FAFAFA", ec="#424242", lw=1.3, zorder=1))
        ax.add_patch(Rectangle((x0, 1.0), x1 - x0, 0.22, fc="#BDBDBD", ec="none", zorder=2))
        ax.text((x0 + x1) / 2, 1.06, "platform", ha="center", va="bottom", fontsize=9, color="#424242", zorder=3)
    ax.add_patch(Rectangle((5.7, 1.0), 1.9, 0.75, fc="#D7CCC8", ec="#424242", lw=1.3, zorder=1))
    ax.text(6.65, 1.38, "tunnel", ha="center", va="center", **L)
    ax.plot([0.2, 10.8], [0.95, 0.95], color="#5D4037", lw=2.2, zorder=3)          # track
    for x in (3.6, 8.1):                                                             # trains
        ax.add_patch(FancyBboxPatch((x, 1.24), 1.4, 0.42, boxstyle="round,pad=0,rounding_size=0.08", fc="#90A4AE", ec="#37474F", lw=1, zorder=4))
        for w in range(4):
            ax.add_patch(Rectangle((x + 0.1 + w * 0.33, 1.4), 0.22, 0.16, fc="#E3F2FD", ec="none", zorder=5))
    # fiber from MU down a shaft and along the stations / tunnel
    fib(ax, [2.8, 3.05, 3.05, 10.4], [gy + 0.4, gy + 0.4, 2.55, 2.55], lw=2.6)
    for x in (3.6, 4.9, 6.65, 8.1, 9.6):
        unit(ax, x - 0.22, 2.2, 0.44, 0.26, "RU", fs=8)
        fib(ax, [x, x], [2.46, 2.55], lw=2)
        ceiling_antenna(ax, x + 0.38, 2.2, 0.8)
        ax.plot([x + 0.22, x + 0.38], [2.33, 2.33], color=COAX, lw=1, zorder=3)
    for x in (4.3, 5.3, 8.9, 10.1):
        handset(ax, x, 1.7, w=0.11, h=0.2)
    ax.text(3.3, 2.65, "fiber", ha="left", fontsize=11, style="italic", color="#B85C00")
    ax.text(4.45, 0.45, "station", ha="center", **B)
    ax.text(9.1, 0.45, "station", ha="center", **B)
    save(fig, "subway.png")


# =============================================================== research demo
def f_demo():
    fig, ax = canvas(7.0, 4.0)
    ybox(ax, 0.1, 2.75, 1.4, 0.7, "5G-NR\nIF1 = 1.14 GHz", 10)
    ybox(ax, 0.1, 1.45, 1.4, 0.7, "Candidate 6G\nIF2 = 12 GHz", 10)
    arrow(ax, (1.5, 3.1), (1.95, 2.55)); arrow(ax, (1.5, 1.8), (1.95, 2.3))
    ybox(ax, 1.95, 2.1, 0.75, 0.65, "E/O", 11)
    fib(ax, [2.7, 3.6], [2.42, 2.42])
    ax.text(3.15, 2.55, "one fiber", ha="center", **L)
    ax.add_patch(Rectangle((3.6, 2.1), 0.8, 0.65, fc=LYEL, ec="#6B5B00", lw=1.2, zorder=4))
    ax.text(4.0, 2.42, "coupler", ha="center", va="center", fontsize=10, fontweight="bold", zorder=5)
    fib(ax, [4.4, 4.7, 4.7, 5.0], [2.6, 2.6, 3.3, 3.3])
    ybox(ax, 5.0, 3.0, 0.85, 0.6, "PIN PD\n+ LPF", 10)
    ax.text(6.4, 3.3, "5G RAU", ha="center", va="center", **B)
    arrow(ax, (5.85, 3.3), (6.0, 3.3))
    fib(ax, [4.4, 4.7, 4.7, 5.0], [2.25, 2.25, 1.55, 1.55])
    ybox(ax, 5.0, 1.25, 0.85, 0.6, "UTC-PD", 10)
    ybox(ax, 5.0, 0.3, 0.85, 0.5, "Laser λ2", 10)
    fib(ax, [5.42, 5.42], [0.8, 1.25])
    ax.text(6.4, 1.55, "THz\nRAU", ha="center", va="center", **B)
    arrow(ax, (5.85, 1.55), (6.0, 1.55))
    ax.text(3.5, 0.05, "laboratory demonstration", ha="center", **L)
    save(fig, "demo.png")


for fn in (f_transition, f_das_concept, f_das_types, f_coax_loss, f_das_arch, f_subway, f_demo):
    fn()
print("written to", OUT)
