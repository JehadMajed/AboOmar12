"""Redraws the three technical figures of the v3 deck at high resolution, keeping their content and style.

  arch.png  - RoF network architecture (backhaul / fronthaul, BBU pool, RRH, optical access network)
  block.png - RoF link block diagram (CW laser, RF modulator, MZM, WDM MUX/DEMUX, photodiode, filter)
  rau.png   - RAU types BBoF / RFoF / IFoF (adapted from Electronics 9(11), 1785, 2020, Fig. 3)

Usage: python3 make_v3_figures.py <output_dir>
"""
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import (Circle, Ellipse, FancyArrowPatch, FancyBboxPatch, Polygon,
                                Rectangle)

OUT = sys.argv[1] if len(sys.argv) > 1 else "figs_v3"
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.family": "Liberation Sans", "font.size": 12})
DPI = 300


def canvas(w, h):
    fig = plt.figure(figsize=(w, h))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, w); ax.set_ylim(0, h); ax.set_aspect("equal"); ax.axis("off")
    return fig, ax


def arrow(ax, p, q, color="black", lw=1.4, style="-|>", ls="-", ms=14, z=3):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle=style, mutation_scale=ms, color=color, lw=lw,
                                 ls=ls, shrinkA=0, shrinkB=0, zorder=z))


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=DPI, facecolor="white")
    plt.close(fig)


# =============================================================== architecture
def cube(ax, x, y, s=0.32):
    d = s * 0.45
    ax.add_patch(Polygon([[x, y], [x + s, y], [x + s, y + s], [x, y + s]], fc="#B4B4B4", ec="#555", lw=1, zorder=4))
    ax.add_patch(Polygon([[x, y + s], [x + s, y + s], [x + s + d, y + s + d], [x + d, y + s + d]], fc="#D6D6D6", ec="#555", lw=1, zorder=4))
    ax.add_patch(Polygon([[x + s, y], [x + s + d, y + d], [x + s + d, y + s + d], [x + s, y + s]], fc="#8F8F8F", ec="#555", lw=1, zorder=4))
    return (x + (s + d) / 2, y + (s + d) / 2)


def tower(ax, x, y, h=0.75, color="#C0392B"):
    ax.plot([x - 0.1, x, x + 0.1], [y, y + h, y], color=color, lw=1.4, zorder=4)
    for k in np.linspace(0.15, 0.75, 4):
        w = 0.1 * (1 - k)
        ax.plot([x - w, x + w], [y + k * h, y + k * h], color=color, lw=0.8, zorder=4)


def phone(ax, x, y):
    ax.add_patch(Rectangle((x, y), 0.17, 0.08, angle=30, fc="#1F4E9E", ec="#0B2A5C", lw=0.8, zorder=5))


def f_arch():
    fig, ax = canvas(11, 4.1)
    # metro ring
    for dy, c in ((0.0, "#6A8FD8"), (0.03, "#E57373"), (0.06, "#F3A6C8")):
        ax.add_patch(Ellipse((1.9, 2.15 + dy), 2.9, 0.95, fill=False, ec=c, lw=1.6, zorder=2))
    n1 = cube(ax, 0.3, 2.0); n2 = cube(ax, 1.55, 2.55); n3 = cube(ax, 2.95, 1.95); n4 = cube(ax, 1.25, 1.45)
    # optical fiber to BBU pool
    bx, by = 5.0, 3.05
    ax.plot([n3[0] + 0.1, bx - 0.2], [n3[1], by], color="#333", lw=1.4, zorder=3)
    ax.text(3.75, 2.95, "Optical\nFiber", ha="center", fontsize=12, fontweight="bold")
    ax.add_patch(FancyBboxPatch((bx - 0.24, by - 0.25), 0.48, 0.58, boxstyle="round,pad=0.03", fc="white", ec="#555", lw=1.2, zorder=4))
    for k in range(3):
        ax.add_patch(Ellipse((bx, by - 0.12 + k * 0.14), 0.3, 0.1, fc="#2F6FD6", ec="#1A4A9A", lw=0.8, zorder=5))
        ax.add_patch(Rectangle((bx - 0.15, by - 0.12 + k * 0.14 - 0.05), 0.3, 0.05, fc="#2F6FD6", ec="none", zorder=5))
    ax.text(bx, by - 0.5, "BBU Pool", ha="center", fontsize=12, fontweight="bold")
    # backhaul / fronthaul labels
    for x0, t in ((3.6, "Backhaul"), (5.85, "Fronthaul")):
        ax.add_patch(Rectangle((x0, 3.7), 1.25, 0.3, fc="white", ec="#D9534F", lw=1.3, zorder=4))
        ax.text(x0 + 0.625, 3.85, t, ha="center", va="center", fontsize=12, fontweight="bold", zorder=5)
    ax.plot([4.85, 5.85], [3.85, 3.85], color="#D9534F", lw=1.2, ls=(0, (3, 2)))
    ax.plot([bx, bx], [3.85, by + 0.36], color="#D9534F", lw=1.2, ls=(0, (3, 2)))
    # RRH cells
    ax.add_patch(Ellipse((7.1, 3.3), 1.9, 0.75, fc="#DCEFD8", ec="none", zorder=1))
    ax.add_patch(Ellipse((8.55, 2.65), 1.9, 0.75, fc="#FCEFC7", ec="none", zorder=1))
    tower(ax, 6.95, 2.95); tower(ax, 8.35, 2.3)
    ax.plot([bx + 0.24, 6.95], [by, 3.3], color="#333", lw=1.4, zorder=3)
    ax.plot([bx + 0.24, 8.35], [by - 0.05, 2.75], color="#333", lw=1.4, zorder=3)
    ax.text(6.95, 2.72, "RRH", ha="center", fontsize=12, fontweight="bold")
    ax.text(8.35, 2.07, "RRH", ha="center", fontsize=12, fontweight="bold")
    phone(ax, 6.4, 3.4); phone(ax, 7.45, 3.35); phone(ax, 8.85, 2.85); phone(ax, 8.0, 2.45)
    ax.text(7.75, 3.1, "User", fontsize=12, fontweight="bold")
    ax.text(9.15, 2.55, "User", fontsize=12, fontweight="bold")
    # optical access network
    ax.add_patch(FancyBboxPatch((4.15, 0.12), 5.1, 1.75, boxstyle="round,pad=0.05,rounding_size=0.3", fill=False,
                                ec="#B57BB5", lw=1.3, ls=(0, (4, 3)), zorder=1))
    sx, sy = 5.0, 1.35
    ax.plot([n4[0], sx], [n4[1], sy], color="#333", lw=1.4, zorder=3)
    ax.add_patch(Circle((sx, sy), 0.05, fc="#2E7D32", ec="black", lw=0.8, zorder=5))
    ax.text(sx - 0.15, sy - 0.32, "Splitter", ha="center", fontsize=12, fontweight="bold")
    # building
    ax.plot([sx, 7.35], [sy, 1.5], color="#333", lw=1.2)
    ax.add_patch(Rectangle((7.35, 1.2), 0.45, 0.6, fc="#6FA8DC", ec="#2A5D8A", lw=1, zorder=4))
    for i in range(3):
        for j in range(2):
            ax.add_patch(Rectangle((7.42 + j * 0.2, 1.27 + i * 0.18), 0.1, 0.1, fc="white", ec="none", zorder=5))
    # house
    ax.plot([sx, 8.55], [sy, 0.95], color="#333", lw=1.2)
    ax.add_patch(Rectangle((8.55, 0.7), 0.5, 0.35, fc="#F4E1C1", ec="#8D6E63", lw=1, zorder=4))
    ax.add_patch(Polygon([[8.48, 1.05], [9.12, 1.05], [8.8, 1.3]], fc="#C0392B", ec="#7B241C", lw=1, zorder=4))
    # base station
    ax.plot([sx, 5.85], [sy, 0.75], color="#333", lw=1.2)
    tower(ax, 5.85, 0.3, h=0.55, color="black")
    for r in (0.12, 0.2):
        ax.add_patch(matplotlib.patches.Arc((5.85, 0.85), r * 2, r * 2, theta1=30, theta2=150, color="black", lw=1.2))
    ax.text(5.85, 0.1, "BS", ha="center", fontsize=12, fontweight="bold")
    ax.add_patch(Rectangle((6.35, 0.3), 0.32, 0.2, fc="#F4E1C1", ec="#8D6E63", lw=1, zorder=4))
    ax.add_patch(Polygon([[6.32, 0.5], [6.7, 0.5], [6.51, 0.62]], fc="#C0392B", ec="#7B241C", lw=1, zorder=4))
    ax.text(4.6, 0.35, "Optical Access\nNetwork", ha="center", fontsize=12, fontweight="bold")
    # legend
    ax.text(0.3, 0.75, "BBU: Baseband Unit\nBS: Base Station\nRRH: Remote Radio Head", fontsize=12,
            fontweight="bold", va="center", linespacing=1.3)
    save(fig, "arch.png")


# =============================================================== block diagram
YEL = "#F7C948"
LYEL = "#FFF59D"


def ybox(ax, x, y, w, h, t, fs=11):
    ax.add_patch(Rectangle((x, y), w, h, fc=YEL, ec="#6B5B00", lw=1.2, zorder=4))
    ax.text(x + w / 2, y + h / 2, t, ha="center", va="center", fontsize=fs, fontweight="bold", zorder=5)


def dashed(ax, x, y, w, h, t):
    ax.add_patch(Rectangle((x, y), w, h, fill=False, ec="#555", lw=1, ls=(0, (4, 3))))
    ax.text(x + w - 0.08, y + 0.1, t, ha="right", va="bottom", fontsize=10, fontweight="bold")


def f_block():
    fig, ax = canvas(11, 4.1)
    dashed(ax, 1.3, 1.55, 2.4, 2.1, "Central Station")
    ax.text(0.2, 2.9, "Transmitter 1", fontsize=11, fontweight="bold", va="center")
    arrow(ax, (1.0, 3.15), (1.5, 3.15))
    ybox(ax, 1.5, 2.9, 0.8, 0.5, "RF\nModulator", 9.5)
    arrow(ax, (2.3, 3.15), (2.6, 3.15))
    ybox(ax, 2.6, 2.85, 0.85, 0.6, "MZM")
    ybox(ax, 1.5, 1.8, 0.8, 0.6, "CW\nLaser")
    ax.plot([2.3, 3.02], [2.1, 2.1], color="black", lw=1.4)
    arrow(ax, (3.02, 2.1), (3.02, 2.85))
    # lambda 1 / n
    arrow(ax, (3.45, 3.15), (4.65, 3.15))
    ax.text(3.9, 3.25, r"$\lambda_1$", fontsize=11)
    ax.plot([3.9, 3.9], [1.0, 3.0], color="#555", lw=1, ls=(0, (2, 3)))
    ax.plot([2.5, 2.5], [1.0, 1.5], color="#555", lw=1, ls=(0, (2, 3)))
    ax.text(2.5, 0.75, "Transmitter n", ha="center", fontsize=11, fontweight="bold")
    arrow(ax, (3.6, 0.6), (4.65, 0.6))
    ax.text(3.9, 0.7, r"$\lambda_n$", fontsize=11)
    # MUX / DEMUX trapezoids
    ax.add_patch(Polygon([[4.65, 3.75], [5.1, 3.35], [5.1, 0.55], [4.65, 0.15]], fc=LYEL, ec="#6B5B00", lw=1.2, zorder=4))
    ax.text(4.88, 1.95, "M\nU\nX", ha="center", va="center", fontsize=11, fontweight="bold", linespacing=1.6, zorder=5)
    ax.add_patch(Polygon([[6.6, 3.35], [7.05, 3.75], [7.05, 0.15], [6.6, 0.55]], fc=LYEL, ec="#6B5B00", lw=1.2, zorder=4))
    ax.text(6.83, 1.95, "D\nE\nM\nU\nX", ha="center", va="center", fontsize=11, fontweight="bold", linespacing=1.5, zorder=5)
    ax.plot([5.1, 6.6], [1.95, 1.95], color="#444", lw=1.6)
    for dx in (-0.08, 0.08):
        ax.add_patch(Circle((5.85 + dx, 1.95), 0.11, fill=False, ec="#444", lw=1.2, zorder=4))
    ax.text(5.85, 2.25, "Optical Fiber", ha="center", fontsize=11, fontweight="bold")
    # receivers
    dashed(ax, 7.6, 2.3, 2.7, 1.55, "Base Station")
    ax.text(7.3, 3.65, "Receiver 1", fontsize=11, fontweight="bold")
    arrow(ax, (7.05, 3.15), (7.75, 3.15))
    ybox(ax, 7.75, 2.85, 1.05, 0.6, "Photodiode", 10)
    arrow(ax, (8.8, 3.15), (9.05, 3.15))
    ybox(ax, 9.05, 2.85, 0.8, 0.6, "Filter", 10)
    ax.plot([9.85, 10.55, 10.55], [3.15, 3.15, 3.7], color="black", lw=1.4)
    ax.add_patch(Polygon([[10.45, 3.95], [10.65, 3.95], [10.55, 3.7]], fc="black", ec="black", zorder=4))
    ax.plot([7.35, 7.35], [0.9, 2.95], color="#555", lw=1, ls=(0, (2, 3)))
    arrow(ax, (7.05, 0.6), (8.1, 0.6))
    ax.text(7.2, 0.72, "Receiver n", fontsize=11, fontweight="bold")
    save(fig, "block.png")


# =============================================================== RAU types
BLUE = "#5B9BD5"
GREEN = "#70AD47"
LIGHT = "#E7E7E7"
MID = "#BFBFBF"
DARK = "#7F7F7F"


def tri(ax, x, y, w, h, color, label, left=False):
    pts = [[x + w, y + h / 2], [x, y], [x, y + h]] if not left else [[x, y + h / 2], [x + w, y], [x + w, y + h]]
    ax.add_patch(Polygon(pts, fc=color, ec="#333", lw=0.8, zorder=4))
    ax.text(x + (w * 0.4 if not left else w * 0.6), y + h / 2, label, ha="center", va="center", fontsize=8, fontweight="bold", zorder=5)


def diode(ax, x, y, s, color, up=True):
    ax.add_patch(Rectangle((x, y), s, s, fc=color, ec="#333", lw=0.8, zorder=4))
    cx, cy = x + s / 2, y + s / 2
    pts = [[cx - 0.09, cy - 0.07], [cx + 0.09, cy - 0.07], [cx, cy + 0.08]] if up else [[cx - 0.09, cy + 0.07], [cx + 0.09, cy + 0.07], [cx, cy - 0.08]]
    ax.add_patch(Polygon(pts, fc="black", zorder=5))
    yb = cy + 0.08 if up else cy - 0.08
    ax.plot([cx - 0.09, cx + 0.09], [yb, yb], color="black", lw=1.2, zorder=5)


def mixer(ax, x, y, r, color):
    ax.add_patch(Circle((x, y), r, fc=color, ec="#333", lw=0.8, zorder=4))
    d = r * 0.7
    ax.plot([x - d, x + d], [y - d, y + d], color="#333", lw=0.8, zorder=5)
    ax.plot([x - d, x + d], [y + d, y - d], color="#333", lw=0.8, zorder=5)


def rect(ax, x, y, w, h, color, label):
    ax.add_patch(Rectangle((x, y), w, h, fc=color, ec="#333", lw=0.8, zorder=4))
    ax.text(x + w / 2, y + h / 2, label, ha="center", va="center", fontsize=7, fontweight="bold", zorder=5)


def spectrum(ax, x, y, w, h, kind):
    ax.add_patch(Rectangle((x, y), w, h, fc="white", ec="#333", lw=0.8, zorder=4))
    ax.plot([x + 0.05, x + 0.05, x + w - 0.04], [y + h - 0.05, y + 0.05, y + 0.05], color="black", lw=0.7, zorder=5)
    t = np.linspace(-1, 1, 60)
    if kind == "bb":
        xs = x + 0.07 + (t + 1) / 2 * w * 0.35
        ys = y + 0.05 + (h - 0.15) * np.exp(-((t + 1) * 2.2) ** 2)
    else:
        c = x + w * (0.45 if kind == "if" else 0.6)
        xs = c + t * w * 0.15
        ys = y + 0.05 + (h - 0.15) * np.clip(1 - t ** 8, 0, 1)
    ax.plot(xs, ys, color="black", lw=0.8, zorder=5)


def ant(ax, x, y):
    ax.plot([x, x], [y - 0.15, y + 0.05], color="black", lw=1, zorder=5)
    ax.add_patch(Polygon([[x - 0.08, y + 0.18], [x + 0.08, y + 0.18], [x, y + 0.05]], fc="white", ec="black", lw=1, zorder=5))


def rau_panel(ax, y0, kind, title):
    H = 1.4
    # input region (signal type on fiber)
    in_col = {"bb": LIGHT, "rf": DARK, "if": LIGHT}[kind]
    ax.add_patch(Rectangle((0.0, y0 + 0.1), 0.85, 1.25, fc=in_col, ec="none", zorder=1))
    spectrum(ax, 0.12, y0 + 0.78, 0.6, 0.32, kind)
    ax.text(0.42, y0 + 0.4, "Optical\nPower", ha="center", va="center", fontsize=8, fontweight="bold",
            color="white" if kind == "rf" else "black", zorder=5)
    ax.text(0.42, y0 + 1.14, {"bb": "Baseband", "rf": "RF", "if": "IF"}[kind], ha="center", fontsize=7, fontweight="bold",
            color="white" if kind == "rf" else "black")
    # unit body with domain shading
    x0, x1 = 0.85, 3.8
    if kind == "bb":
        ax.add_patch(Rectangle((x0, y0), 1.25, H, fc=LIGHT, ec="none", zorder=1))
        ax.add_patch(Rectangle((2.1, y0), 0.35, H, fc=MID, ec="none", zorder=1))
        ax.add_patch(Rectangle((2.45, y0), x1 - 2.45, H, fc=DARK, ec="none", zorder=1))
    elif kind == "if":
        ax.add_patch(Rectangle((x0, y0), 1.55, H, fc=LIGHT, ec="none", zorder=1))
        ax.add_patch(Rectangle((2.4, y0), x1 - 2.4, H, fc=DARK, ec="none", zorder=1))
    else:
        ax.add_patch(Rectangle((x0, y0), x1 - x0, H, fc=DARK, ec="none", zorder=1))
    ax.add_patch(Rectangle((x0, y0), x1 - x0, H, fill=False, ec="#555", lw=0.9, ls=(0, (4, 3)), zorder=2))
    ax.text(x0 + 0.05, y0 + H + 0.04, title, fontsize=10, fontweight="bold")
    # splitter + fiber
    sp = y0 + 0.66
    ax.plot([0.12, 0.85], [sp, sp], color="black", lw=0.8, zorder=3)
    ax.add_patch(Rectangle((0.85, sp - 0.065), 0.13, 0.13, fc="white", ec="#333", lw=0.8, zorder=4))
    dl, ul = y0 + 1.0, y0 + 0.32
    ax.plot([0.98, 1.08, 1.08], [sp, sp, dl], color="#333", lw=0.8, zorder=3)
    ax.plot([1.08, 1.08], [sp, ul], color="#333", lw=0.8, zorder=3)
    # chains
    s = 0.28
    diode(ax, 1.08, dl - s / 2, s, BLUE, up=True)
    diode(ax, 1.08, ul - s / 2, s, GREEN, up=False)
    tri(ax, 1.48, dl - 0.16, 0.42, 0.32, BLUE, "TIA")
    tri(ax, 1.48, ul - 0.16, 0.42, 0.32, GREEN, "LD", left=True)
    xs = 2.0
    if kind == "bb":
        rect(ax, 2.0, dl - 0.07, 0.33, 0.14, BLUE, "MOD")
        rect(ax, 1.98, ul - 0.07, 0.37, 0.14, GREEN, "DEMOD")
        xs = 2.45
    if kind in ("bb", "if"):
        mx = xs + 0.18
        mixer(ax, mx, dl, 0.17, BLUE); mixer(ax, mx, ul, 0.17, GREEN)
        ax.add_patch(Rectangle((mx - 0.09, y0 + 0.57), 0.18, 0.18, fc="white", ec="#333", lw=0.8, zorder=4))
        ax.text(mx, y0 + 0.66, "LO", ha="center", va="center", fontsize=6, fontweight="bold", zorder=5)
        xs = mx + 0.3
    tri(ax, xs, dl - 0.16, 0.42, 0.32, BLUE, "PA")
    tri(ax, xs, ul - 0.16, 0.42, 0.32, GREEN, "LNA", left=True)
    ax.plot([1.36, xs + 0.42], [dl, dl], color="#333", lw=0.6, zorder=3)
    ax.plot([1.36, xs], [ul, ul], color="#333", lw=0.6, zorder=3)
    spectrum(ax, xs + 0.5, dl + 0.1, 0.42, 0.27, "rf")
    ax.plot([xs + 0.42, 3.55, 3.55], [dl, dl, y0 + 0.72], color="#333", lw=0.8, zorder=3)
    ax.plot([xs + 0.42, 3.55, 3.55], [ul, ul, y0 + 0.6], color="#333", lw=0.8, zorder=3)
    ant(ax, 3.62, y0 + 0.8)


def f_rau():
    fig, ax = canvas(3.92, 5.4)
    rau_panel(ax, 3.7, "bb", "a) BBoF RAU")
    rau_panel(ax, 1.95, "rf", "b) RFoF RAU")
    rau_panel(ax, 0.2, "if", "c) IFoF RAU")
    save(fig, "rau.png")


f_arch(); f_block(); f_rau()
print("written to", OUT)
