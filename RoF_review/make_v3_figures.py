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
if __name__ == "__main__":
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
def server(ax, x, y, w=0.36, h=0.5, d=0.16):
    """Grey 3-D network node, (x, y) = front-bottom-left corner. Returns a connection point."""
    ax.add_patch(Polygon([[x, y], [x + w, y], [x + w, y + h], [x, y + h]], fc="#A9A9A9", ec="#5A5A5A", lw=1, zorder=4))
    ax.add_patch(Polygon([[x, y + h], [x + w, y + h], [x + w + d, y + h + d * 0.7], [x + d, y + h + d * 0.7]],
                         fc="#D3D3D3", ec="#5A5A5A", lw=1, zorder=4))
    ax.add_patch(Polygon([[x + w, y], [x + w + d, y + d * 0.7], [x + w + d, y + h + d * 0.7], [x + w, y + h]],
                         fc="#7E7E7E", ec="#5A5A5A", lw=1, zorder=4))
    return x + w / 2, y + h / 2


def lattice_tower(ax, x, y, h=0.9, color="#C0392B", lw=1.3):
    w = 0.13
    ax.plot([x - w, x, x + w], [y, y + h, y], color=color, lw=lw, zorder=5)
    n = 5
    for k in range(1, n):
        f = k / n
        yy = y + f * h
        ww = w * (1 - f)
        ax.plot([x - ww, x + ww], [yy, yy], color=color, lw=lw * 0.6, zorder=5)
        f2 = (k + 1) / n
        ax.plot([x - ww, x + w * (1 - f2)], [yy, y + f2 * h], color=color, lw=lw * 0.4, zorder=5)
    # antenna panels near the top
    for s in (-1, 1):
        ax.add_patch(Rectangle((x + s * 0.05 - 0.02, y + h * 0.72), 0.04, 0.16, fc="white", ec=color, lw=0.9, zorder=6))


def handset(ax, x, y, w=0.15, h=0.27):
    """Upright mobile phone (user equipment); (x, y) = bottom-left corner."""
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.03",
                                fc="#1E3F8A", ec="#0B1F4D", lw=1, zorder=6))
    ax.add_patch(Rectangle((x + 0.018, y + 0.05), w - 0.036, h - 0.09, fc="#9CC3F5", ec="none", zorder=7))
    ax.plot([x + w * 0.35, x + w * 0.65], [y + h - 0.02, y + h - 0.02], color="#9CC3F5", lw=1, zorder=7)
    ax.add_patch(Circle((x + w / 2, y + 0.025), 0.012, fc="#9CC3F5", ec="none", zorder=7))


def database(ax, x, y):
    ax.add_patch(FancyBboxPatch((x - 0.3, y - 0.32), 0.6, 0.66, boxstyle="round,pad=0.02,rounding_size=0.08",
                                fc="white", ec="#4A4A4A", lw=1.4, zorder=4))
    w, t = 0.36, 0.12
    for k in range(3):
        yy = y - 0.2 + k * 0.14
        ax.add_patch(Rectangle((x - w / 2, yy), w, t, fc="#2F6FD6", ec="none", zorder=5))
        ax.add_patch(Ellipse((x, yy), w, 0.08, fc="#2457B0", ec="#1A3F86", lw=0.6, zorder=5))
    ax.add_patch(Ellipse((x, y - 0.2 + 2 * 0.14 + t), w, 0.08, fc="#7FA8EE", ec="#1A3F86", lw=0.6, zorder=6))


def office(ax, x, y):
    w, h, d = 0.42, 0.62, 0.14
    ax.add_patch(Polygon([[x, y], [x + w, y], [x + w, y + h], [x, y + h]], fc="#5DA9E9", ec="#2B6CB0", lw=1, zorder=4))
    ax.add_patch(Polygon([[x + w, y], [x + w + d, y + 0.08], [x + w + d, y + h + 0.08], [x + w, y + h]], fc="#3B82C4", ec="#2B6CB0", lw=1, zorder=4))
    ax.add_patch(Polygon([[x, y + h], [x + w, y + h], [x + w + d, y + h + 0.08], [x + d, y + h + 0.08]], fc="#A7D3F5", ec="#2B6CB0", lw=1, zorder=4))
    for i in range(4):
        for j in range(3):
            ax.add_patch(Rectangle((x + 0.05 + j * 0.12, y + 0.07 + i * 0.14), 0.08, 0.09, fc="#E8F4FD", ec="none", zorder=5))


def house(ax, x, y, s=1.0, wall="#F6E3C6", roof="#C0392B"):
    w, h = 0.55 * s, 0.38 * s
    ax.add_patch(Rectangle((x, y), w, h, fc=wall, ec="#8D6E63", lw=1, zorder=4))
    ax.add_patch(Polygon([[x - 0.07 * s, y + h], [x + w + 0.07 * s, y + h], [x + w / 2, y + h + 0.3 * s]],
                         fc=roof, ec="#7B241C", lw=1, zorder=4))
    ax.add_patch(Rectangle((x + w * 0.4, y), w * 0.2, h * 0.55, fc="#8D6E63", ec="none", zorder=5))
    for xx in (x + w * 0.1, x + w * 0.7):
        ax.add_patch(Rectangle((xx, y + h * 0.45), w * 0.2, h * 0.3, fc="#BFE1F7", ec="#8D6E63", lw=0.6, zorder=5))


def shop(ax, x, y):
    ax.add_patch(Rectangle((x, y), 0.42, 0.26, fc="#F6E3C6", ec="#8D6E63", lw=1, zorder=4))
    for k in range(4):
        ax.add_patch(Polygon([[x - 0.03 + k * 0.12, y + 0.26], [x + 0.09 + k * 0.12, y + 0.26], [x + 0.09 + k * 0.12, y + 0.34], [x - 0.03 + k * 0.12, y + 0.34]],
                             fc="#D9534F" if k % 2 == 0 else "white", ec="#A93226", lw=0.6, zorder=5))
    ax.add_patch(Rectangle((x + 0.06, y), 0.12, 0.17, fc="#8D6E63", ec="none", zorder=5))
    ax.add_patch(Rectangle((x + 0.24, y + 0.08), 0.12, 0.1, fc="#BFE1F7", ec="#8D6E63", lw=0.6, zorder=5))


def span(ax, x1, x2, y, text, color="#D9534F"):
    """Dashed bracket over a link segment with a boxed label (Backhaul / Fronthaul)."""
    ax.plot([x1, x1, x2, x2], [y - 0.12, y, y, y - 0.12], color=color, lw=1.3, ls=(0, (3, 2)), zorder=3)
    xm = (x1 + x2) / 2
    ax.add_patch(Rectangle((xm - 0.65, y - 0.02), 1.3, 0.32, fc="white", ec=color, lw=1.4, zorder=4))
    ax.text(xm, y + 0.14, text, ha="center", va="center", fontsize=13, fontweight="bold", zorder=5)


def f_arch():
    fig, ax = canvas(11, 4.1)
    B = dict(fontsize=13, fontweight="bold")
    L = dict(fontsize=11, style="italic", color="#444444")
    FIB = dict(color="#2B2B2B", lw=1.6, zorder=3)

    # ---------------- core / metro ring (left)
    cx, cy = 1.45, 2.15
    for dy, c in ((-0.035, "#5B7FD6"), (0.0, "#E06666"), (0.035, "#C27BD1")):
        ax.add_patch(Ellipse((cx, cy + dy), 2.4, 1.05, fill=False, ec=c, lw=1.6, zorder=2))
    server(ax, 0.07, 1.9)               # left
    server(ax, 1.2, 2.45)               # top  -> backhaul
    server(ax, 2.38, 1.9)               # right
    server(ax, 1.2, 1.3)                # bottom -> feeder
    ax.text(cx + 0.08, cy + 0.02, "Core\nnetwork", ha="center", va="center", linespacing=1.1, **L)

    # ---------------- mobile lane (top): backhaul -> BBU pool -> fronthaul -> RRHs
    yt = 3.0
    ax.add_patch(FancyBboxPatch((3.75, 2.2), 6.95, 1.3, boxstyle="round,pad=0.03,rounding_size=0.25",
                                fc="#F7F7F7", ec="#B0B0B0", lw=1.1, ls=(0, (5, 3)), zorder=0))
    ax.plot([1.48, 1.48, 4.9], [2.96, 3.15, 3.15], **FIB)
    ax.plot([4.9, 4.9], [3.15, yt], **FIB)
    ax.text(3.0, 3.21, "optical fiber", ha="center", **L)
    bx = 5.2
    database(ax, bx, yt)
    ax.text(bx, yt - 0.55, "BBU Pool", ha="center", **B)
    # RRH cells
    cells = [(6.6, "#DDEFD9"), (8.85, "#FBEFC9")]
    for x, col in cells:
        ax.add_patch(Ellipse((x + 0.25, 2.95), 1.95, 0.85, fc=col, ec="none", zorder=1))
        lattice_tower(ax, x, 2.55, h=0.8)
        ax.text(x, 2.32, "RRH", ha="center", va="bottom", **B)
        for px in (x - 0.75, x + 0.55):
            handset(ax, px, 3.07)
            ax.plot([x, px + 0.075], [3.25, 3.2], color="#707070", lw=1.1, ls=(0, (3, 2)), zorder=2)
        ax.text(x + 0.3, 2.62, "User (UE)", ha="left", **B)
    ax.plot([bx + 0.3, 6.6], [yt, yt], **FIB)
    ax.plot([6.6, 8.85], [yt, yt], **FIB)
    ax.text(5.95, yt - 0.25, "optical fiber", ha="center", **L)
    span(ax, 1.48, bx - 0.32, 3.62, "Backhaul")
    span(ax, bx + 0.32, 9.6, 3.62, "Fronthaul")

    # ---------------- access lane (bottom): feeder -> splitter -> fibers fanned out to premises (as in source figure)
    ax.add_patch(FancyBboxPatch((3.75, 0.05), 6.95, 1.85, boxstyle="round,pad=0.03,rounding_size=0.25",
                                fill=False, ec="#C48BC4", lw=1.3, ls=(0, (5, 3)), zorder=0))
    ax.text(3.88, 1.66, "Optical Access Network", ha="left", va="bottom", **B)
    sx, sy = 4.9, 1.15
    ax.plot([1.48, 1.48, sx], [1.3, 1.22, sy], **FIB)
    ax.text(2.95, 1.33, "optical fiber", ha="center", **L)
    # premises
    bs = (5.9, 0.32)
    lattice_tower(ax, bs[0], bs[1], h=0.55, color="black", lw=1.4)
    for r in (0.13, 0.22):
        ax.add_patch(matplotlib.patches.Arc((bs[0], 0.82), r * 2, r * 2, theta1=135, theta2=225, color="black", lw=1.3))
        ax.add_patch(matplotlib.patches.Arc((bs[0], 0.82), r * 2, r * 2, theta1=-45, theta2=45, color="black", lw=1.3))
    office(ax, 7.8, 0.95)
    house(ax, 9.3, 0.42)
    shop(ax, 7.2, 0.3)
    for tx, ty in ((bs[0], 0.87), (7.8, 1.27), (9.3, 0.6)):
        ax.plot([sx, tx], [sy, ty], color="#2B2B2B", lw=1.3, zorder=3)
    ax.add_patch(Circle((sx, sy), 0.07, fc="#2E7D32", ec="black", lw=0.8, zorder=6))
    ax.text(sx - 0.05, sy - 0.33, "Splitter", ha="center", **B)
    ax.text(bs[0], 0.1, "Base station (BS)", ha="center", **L)
    ax.text(7.41, 0.1, "Small business", ha="center", **L)
    ax.text(8.45, 1.27, "Office building", ha="left", va="center", **L)
    ax.text(9.57, 0.12, "Home", ha="center", **L)

    # ---------------- legend
    ax.text(0.1, 0.62, "BBU: Baseband Unit\nBS: Base Station\nRRH: Remote Radio Head", va="center", linespacing=1.35, **B)
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


if __name__ == "__main__":
    f_arch(); f_block(); f_rau()
    print("written to", OUT)
