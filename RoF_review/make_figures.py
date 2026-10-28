"""Generates every figure used in the RoF deck as high-resolution PNG files.

Diagrams are drawn with matplotlib patches; plots are computed from the stated formulas.
Usage: python3 make_figures.py <output_dir>
"""
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Ellipse, FancyArrowPatch, Polygon, Rectangle

OUT = sys.argv[1] if len(sys.argv) > 1 else "figs"
os.makedirs(OUT, exist_ok=True)

plt.rcParams.update({
    "font.family": "Liberation Sans",
    "font.size": 14,
    "axes.edgecolor": "black",
    "axes.linewidth": 1.0,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.labelsize": 14,
    "xtick.labelsize": 12,
    "ytick.labelsize": 12,
    "legend.frameon": False,
    "legend.fontsize": 12,
})

# Okabe-Ito colours: optical = vermillion, second series = blue, wireless = grey.
OPT = "#D55E00"
BLUE = "#0072B2"
GREEN = "#009E73"
GREY = "#707070"
BLACK = "#000000"
DPI = 220


# ---------------------------------------------------------------- drawing helpers
def canvas(w, h):
    fig = plt.figure(figsize=(w, h))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, w)
    ax.set_ylim(0, h)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig, ax


def box(ax, x, y, w, h, text, kind="el", fs=13, bold=False):
    """kind: el (black outline) | eo (optoelectronic conversion, orange outline) | zone (dashed)."""
    if kind == "zone":
        ax.add_patch(Rectangle((x, y), w, h, fill=False, ec=GREY, lw=1.2, ls=(0, (5, 4))))
        ax.text(x + 0.1, y + h - 0.1, text, ha="left", va="top", fontsize=fs, color=GREY)
        return
    ec = OPT if kind == "eo" else BLACK
    lw = 2.2 if kind == "eo" else 1.2
    ax.add_patch(Rectangle((x, y), w, h, fc="white", ec=ec, lw=lw, zorder=3))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs,
            fontweight="bold" if bold else "normal", zorder=4, linespacing=1.15)


def arrow(ax, x1, y1, x2, y2, kind="el", both=False, head=True):
    style = {"opt": dict(color=OPT, lw=3.2), "el": dict(color=BLACK, lw=1.4),
             "wl": dict(color=GREY, lw=1.6, ls=(0, (4, 3)))}[kind]
    a = "<|-|>" if both else ("-|>" if head else "-")
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=a, mutation_scale=16,
                                 shrinkA=0, shrinkB=0, zorder=2, **style))


def label(ax, x, y, text, color=BLACK, fs=12, ha="center", va="bottom", italic=True, **kw):
    ax.text(x, y, text, ha=ha, va=va, fontsize=fs, color=color,
            style="italic" if italic else "normal", **kw)


def antenna(ax, x, y, s=1.0):
    ax.plot([x, x], [y, y + 0.45 * s], color=BLACK, lw=1.4, zorder=3)
    ax.add_patch(Polygon([[x - 0.17 * s, y + 0.72 * s], [x + 0.17 * s, y + 0.72 * s], [x, y + 0.45 * s]],
                         closed=True, fc="white", ec=BLACK, lw=1.4, zorder=3))


def legend_paths(ax, x, y, items=("el", "opt", "wl")):
    names = {"el": "Electrical", "opt": "Optical fiber", "wl": "Wireless"}
    for k in items:
        arrow(ax, x, y, x + 0.6, y, k, head=False)
        ax.text(x + 0.75, y, names[k], va="center", fontsize=12, color=GREY)
        x += 2.4


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=DPI, facecolor="white")
    plt.close(fig)


# ---------------------------------------------------------------- F01 title / basic link
def f_title():
    fig, ax = canvas(12, 2.2)
    y = 1.1
    box(ax, 0.1, y - 0.4, 2.2, 0.8, "Radio equipment")
    arrow(ax, 2.3, y, 3.0, y)
    box(ax, 3.0, y - 0.4, 1.0, 0.8, "E/O", "eo", bold=True)
    arrow(ax, 4.0, y, 7.4, y, "opt")
    label(ax, 5.7, y + 0.15, "optical fiber", OPT)
    box(ax, 7.4, y - 0.4, 1.0, 0.8, "O/E", "eo", bold=True)
    arrow(ax, 8.4, y, 9.1, y)
    box(ax, 9.1, y - 0.4, 1.8, 0.8, "Remote unit")
    ax.plot([10.9, 11.2], [y, y], color=BLACK, lw=1.4)
    antenna(ax, 11.2, y)
    arrow(ax, 11.45, y + 0.6, 11.95, y + 0.6, "wl")
    save(fig, "f01_title.png")


# ---------------------------------------------------------------- F02 problem: building
def f_problem():
    fig, ax = canvas(12, 4.8)
    # building
    bx, bw = 0.5, 7.2
    floors = 5
    fh = 0.78
    for i in range(floors):
        ax.add_patch(Rectangle((bx, 0.3 + i * fh), bw, fh, fill=False, ec=BLACK, lw=1.2))
    ax.text(bx + bw / 2, 0.3 + floors * fh + 0.12, "Large building / venue", ha="center", fontsize=13, color=GREY)
    # equipment room in basement (floor 0)
    box(ax, bx + 0.15, 0.38, 1.7, 0.62, "Equipment room", fs=11)
    rx = bx + 2.2  # riser
    arrow(ax, bx + 1.85, 0.69, rx, 0.69, "opt", head=False)
    arrow(ax, rx, 0.69, rx, 0.3 + (floors - 1) * fh + 0.35, "opt", head=False)
    for i in range(1, floors):
        yy = 0.3 + i * fh + 0.3
        arrow(ax, rx, yy, bx + bw - 0.4, yy, "opt", head=False)
        for xa in (rx + 1.5, rx + 3.3, bx + bw - 0.4):
            antenna(ax, xa, yy, 0.55)
    # wall attenuation note
    label(ax, rx + 0.25, 0.3 + fh + 0.02, "antenna points on every floor", GREY, fs=11, ha="left", va="bottom")
    # outdoor macro site
    mx = 10.4
    ax.plot([mx, mx], [0.3, 3.0], color=BLACK, lw=2)
    antenna(ax, mx, 3.0, 1.0)
    ax.text(mx, 0.05, "Outdoor macro site", ha="center", fontsize=12, color=GREY)
    arrow(ax, mx - 0.3, 3.4, bx + bw + 0.1, 3.0, "wl")
    ax.text(9.0, 3.65, "signal attenuated\nby walls and distance", ha="center", fontsize=12, color=GREY)
    ax.plot([bx + bw + 0.2], [3.0], marker="x", color=OPT, ms=14, mew=3)
    save(fig, "f02_problem.png")


# ---------------------------------------------------------------- F03 definition with spectra
def mini_spectrum(fig, rect, kind, title):
    ax = fig.add_axes(rect)
    f = np.linspace(-1, 1, 800)
    if kind == "rf":
        s = np.exp(-((f - 0.5) / 0.05) ** 2) * 0.8
        ax.fill_between(f[f > 0], 0, s[f > 0], color=BLACK, alpha=0.85)
        ax.set_xlim(0, 1)
        ax.set_xticks([0.5]); ax.set_xticklabels([r"$f_{RF}$"])
    else:
        s = np.exp(-((f - 0.5) / 0.04) ** 2) * 0.45 + np.exp(-((f + 0.5) / 0.04) ** 2) * 0.45
        ax.fill_between(f, 0, s, color=OPT, alpha=0.9)
        ax.plot([0, 0], [0, 1], color=OPT, lw=3)
        ax.set_xlim(-1, 1)
        ax.set_xticks([-0.5, 0, 0.5]); ax.set_xticklabels([r"$-f_{RF}$", r"$f_{opt}$", r"$+f_{RF}$"])
    ax.set_ylim(0, 1.1)
    ax.set_yticks([])
    ax.set_title(title, fontsize=12, color=GREY)
    ax.tick_params(labelsize=11, length=3)


def f_definition():
    fig, ax = canvas(12, 4.6)
    y = 1.0
    box(ax, 0.2, y - 0.45, 2.0, 0.9, "RF signal\nin")
    arrow(ax, 2.2, y, 3.0, y)
    box(ax, 3.0, y - 0.45, 1.8, 0.9, "E/O\nlaser", "eo", bold=True)
    arrow(ax, 4.8, y, 7.2, y, "opt")
    label(ax, 6.0, y + 0.15, "fiber", OPT)
    box(ax, 7.2, y - 0.45, 1.8, 0.9, "O/E\nphotodiode", "eo", bold=True)
    arrow(ax, 9.0, y, 9.8, y)
    box(ax, 9.8, y - 0.45, 2.0, 0.9, "RF signal\nout")
    mini_spectrum(fig, [0.045, 0.52, 0.16, 0.33], "rf", "electrical spectrum")
    mini_spectrum(fig, [0.42, 0.52, 0.2, 0.33], "opt", "optical spectrum")
    mini_spectrum(fig, [0.8, 0.52, 0.16, 0.33], "rf", "electrical spectrum")
    save(fig, "f03_definition.png")


# ---------------------------------------------------------------- F04 signal path DL/UL
def f_signal_path():
    fig, ax = canvas(12, 4.6)
    box(ax, 0.1, 0.3, 3.6, 4.0, "Central site", "zone")
    box(ax, 6.2, 0.3, 4.6, 4.0, "Remote antenna unit", "zone")
    dl, ul = 3.0, 1.3
    ax.text(4.95, 4.05, "fiber", ha="center", fontsize=13, color=OPT)
    # downlink
    label(ax, 4.95, dl + 0.55, "DOWNLINK", GREY, fs=11, italic=False)
    box(ax, 0.3, dl - 0.4, 1.4, 0.8, "BS RF\nout")
    arrow(ax, 1.7, dl, 2.2, dl)
    box(ax, 2.2, dl - 0.4, 1.3, 0.8, "E/O", "eo", bold=True)
    arrow(ax, 3.5, dl, 6.4, dl, "opt")
    label(ax, 4.95, dl + 0.1, r"$\lambda_1$", OPT)
    box(ax, 6.4, dl - 0.4, 1.1, 0.8, "O/E", "eo", bold=True)
    arrow(ax, 7.5, dl, 7.9, dl)
    box(ax, 7.9, dl - 0.4, 0.9, 0.8, "PA")
    arrow(ax, 8.8, dl, 9.3, dl)
    # duplexer
    box(ax, 9.3, ul - 0.4, 1.2, dl - ul + 0.8, "Duplexer", fs=12)
    ax.plot([10.5, 11.0], [(dl + ul) / 2] * 2, color=BLACK, lw=1.4)
    antenna(ax, 11.0, (dl + ul) / 2)
    arrow(ax, 11.3, 3.1, 11.95, 3.1, "wl", both=True)
    label(ax, 11.6, 3.25, "UE", GREY, italic=False)
    # uplink
    label(ax, 4.95, ul - 0.75, "UPLINK", GREY, fs=11, italic=False, va="top")
    arrow(ax, 9.3, ul, 8.8, ul)
    box(ax, 7.9, ul - 0.4, 0.9, 0.8, "LNA")
    arrow(ax, 7.9, ul, 7.5, ul)
    box(ax, 6.4, ul - 0.4, 1.1, 0.8, "E/O", "eo", bold=True)
    arrow(ax, 6.4, ul, 3.5, ul, "opt")
    label(ax, 4.95, ul + 0.1, r"$\lambda_2$ or 2nd fiber", OPT)
    box(ax, 2.2, ul - 0.4, 1.3, 0.8, "O/E", "eo", bold=True)
    arrow(ax, 2.2, ul, 1.7, ul)
    box(ax, 0.3, ul - 0.4, 1.4, 0.8, "BS RF\nin")
    save(fig, "f04_signal_path.png")


# ---------------------------------------------------------------- F05 architecture
def f_architecture():
    fig, ax = canvas(12, 4.8)
    box(ax, 0.1, 2.0, 1.5, 0.9, "Core\nnetwork")
    arrow(ax, 1.6, 2.45, 2.4, 2.45)
    label(ax, 2.0, 2.6, "backhaul", BLACK, fs=11)
    box(ax, 2.4, 0.6, 2.3, 3.7, "Base-station hotel", "zone", fs=12)
    for i, t in enumerate(["Operator A", "Operator B", "Operator C"]):
        yy = 3.2 - i * 1.0
        box(ax, 2.6, yy, 1.9, 0.7, t, fs=12)
        arrow(ax, 4.5, yy + 0.35, 5.3, yy + 0.35)
    label(ax, 4.9, 0.75, "RF", BLACK, fs=11)
    box(ax, 5.3, 1.1, 1.6, 2.9, "Head-end\n\nE/O\nO/E", "eo", fs=13, bold=True)
    ys = [3.9, 2.45, 1.0]
    for i, yy in enumerate(ys):
        arrow(ax, 6.9, 2.55, 8.6, yy + 0.35, "opt", both=True)
        box(ax, 8.6, yy, 1.4, 0.7, "RAU " + ("n" if i == 2 else str(i + 1)), fs=12)
        ax.plot([10.0, 10.3], [yy + 0.35] * 2, color=BLACK, lw=1.4)
        antenna(ax, 10.3, yy + 0.35, 0.8)
        arrow(ax, 10.55, yy + 0.65, 11.2, yy + 0.65, "wl", both=True)
    ax.text(7.75, 0.35, "fronthaul (RoF)", ha="center", fontsize=13, color=OPT)
    save(fig, "f05_architecture.png")


# ---------------------------------------------------------------- F06 RoF types
def f_types():
    fig = plt.figure(figsize=(12, 4.9))
    rows = [("RFoF", "rf"), ("IFoF", "if"), ("Digital\nfronthaul", "dig")]
    chains = [["O/E", "Amp", "PA"], ["O/E", "Mixer\n+ LO", "PA"], ["O/E +\ndeframe", "DAC", "Mixer\n+ LO", "PA"]]
    for i, ((name, kind), chain) in enumerate(zip(rows, chains)):
        y0 = 0.62 - i * 0.305
        fig.text(0.01, y0 + 0.12, name, fontsize=15, fontweight="bold", va="center")
        ax = fig.add_axes([0.13, y0, 0.3, 0.24])
        t = np.linspace(0, 1, 2000)
        if kind == "rf":
            ax.plot(t, np.sin(2 * np.pi * 60 * t) * (0.6 + 0.4 * np.sin(2 * np.pi * 3 * t)), color=OPT, lw=0.8)
        elif kind == "if":
            ax.plot(t, np.sin(2 * np.pi * 14 * t) * (0.6 + 0.4 * np.sin(2 * np.pi * 3 * t)), color=OPT, lw=1.2)
        else:
            rng = np.random.default_rng(3)
            bits = rng.integers(0, 2, 40)
            ax.step(np.linspace(0, 1, 41)[:-1], bits, where="post", color=OPT, lw=1.5)
            ax.set_ylim(-0.3, 1.3)
        ax.set_xticks([]); ax.set_yticks([])
        ax.spines["left"].set_visible(False)
        ax.set_title({"rf": "analog waveform at RF", "if": "analog waveform at IF",
                      "dig": "serial digital I/Q samples"}[kind], fontsize=12, color=GREY, loc="left")
        # chain
        axc = fig.add_axes([0.47, y0, 0.53, 0.24])
        axc.set_xlim(0, 6.36); axc.set_ylim(0, 1.18); axc.axis("off")
        x = 0.0
        for j, c in enumerate(chain):
            box(axc, x, 0.25, 1.05, 0.7, c, "eo" if j == 0 else "el", fs=12, bold=j == 0)
            if j < len(chain) - 1:
                arrow(axc, x + 1.05, 0.6, x + 1.35, 0.6)
            x += 1.35
        axc.plot([x - 0.3, x - 0.05], [0.6, 0.6], color=BLACK, lw=1.4)
        antenna(axc, x - 0.05, 0.6, 0.6)
    fig.text(0.13, 0.965, "ON THE FIBER", fontsize=13, color=GREY)
    fig.text(0.47, 0.965, "REMOTE UNIT (DOWNLINK)", fontsize=13, color=GREY)
    save(fig, "f06_types.png")


# ---------------------------------------------------------------- F07 loss comparison
def f_loss():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(12, 4.6), gridspec_kw={"width_ratios": [1, 1.6]})
    o = np.linspace(0, 10, 50)
    a1.plot(o, 2 * o, color=OPT, lw=2.5)
    a1.set_xlabel("Optical loss (dB)")
    a1.set_ylabel("RF loss (dB)")
    a1.set_title("(a) Square-law detection: RF = 2 × optical", fontsize=13, loc="left")
    a1.set_xlim(0, 10); a1.set_ylim(0, 20)
    a1.grid(color="#e6e6e6", lw=0.6)

    L = np.linspace(0, 400, 401)
    coax = 0.222 * L
    a2.plot(L, coax, color=BLACK, lw=2.5, label="Coax, LMR-400 class (22.2 dB/100 m)")
    for lc, ls in ((20, "-"), (40, "--")):
        rof = lc + 0.0005 * L
        a2.plot(L, rof, color=OPT, lw=2.5, ls=ls, label=f"RFoF, conversion loss {lc} dB (assumed)")
        lstar = lc / (0.222 - 0.0005)
        a2.plot([lstar], [0.222 * lstar], "o", color=OPT, ms=7)
        a2.annotate(f"{lstar:.0f} m", (lstar, 0.222 * lstar), xytext=(8, -18), textcoords="offset points", fontsize=12, color=OPT)
    a2.set_xlabel("Link length (m)")
    a2.set_ylabel("RF-to-RF loss (dB)")
    a2.set_title("(b) 2.5 GHz, unamplified, downlink", fontsize=13, loc="left")
    a2.set_xlim(0, 400); a2.set_ylim(0, 90)
    a2.grid(color="#e6e6e6", lw=0.6)
    a2.legend(loc="upper left")
    fig.tight_layout()
    save(fig, "f07_loss.png")


# ---------------------------------------------------------------- F08 CPRI rate
def f_cpri():
    fig, ax = plt.subplots(figsize=(12, 4.7))
    n = np.array([1, 2, 4, 8, 16, 32, 64])
    def rate(fs):  # Gb/s, 15-bit I/Q, 16/15 control, 8B/10B
        return fs * 2 * 15 * 16 / 15 * 10 / 8 / 1000
    for fs, bw, c in ((30.72, "20 MHz carrier", BLACK), (122.88, "100 MHz carrier", OPT)):
        r = rate(fs) * n
        ax.plot(n, r, "o-", color=c, lw=2.5, ms=7, label=f"Digital fronthaul (CPRI), {bw}, incl. 8B/10B")
        ax.annotate(f"{r[-1]:.0f} Gb/s", (n[-1], r[-1]), xytext=(-12, 8), textcoords="offset points", ha="right", fontsize=12, color=c)
    for v, t in ((10.1376, "CPRI option 8: 10.1 Gb/s"), (24.33024, "CPRI option 10: 24.3 Gb/s")):
        ax.axhline(v, color=GREY, lw=1, ls=":")
        ax.text(1.05, v * 1.08, t, fontsize=11, color=GREY)
    ax.set_xscale("log", base=2); ax.set_yscale("log")
    ax.set_xticks(n); ax.set_xticklabels([str(i) for i in n])
    ax.set_xlabel("Number of antennas")
    ax.set_ylabel("Required line rate (Gb/s)")
    ax.grid(color="#e6e6e6", lw=0.6, which="major")
    ax.legend(loc="upper left")
    fig.tight_layout()
    save(fig, "f08_cpri.png")


# ---------------------------------------------------------------- F09 fiber attenuation
def f_attenuation():
    fig, ax = plt.subplots(figsize=(12, 4.6))
    lam = np.linspace(1.2, 1.65, 400)
    rayleigh = 0.8 / lam ** 4
    ir = 6e11 * np.exp(-48 / lam)
    oh = 0.0  # G.652.D: low water peak
    a = rayleigh + ir + oh + 0.02
    ax.plot(lam * 1000, a, color=BLACK, lw=2.5, label="Illustrative model: Rayleigh scattering ($\\propto \\lambda^{-4}$) + infrared absorption")
    ax.plot([1310, 1550], [0.36, 0.22], "s", color=OPT, ms=9, label="G.652.D cable maximum (vendor datasheet)")
    for x, v in ((1310, 0.36), (1550, 0.22)):
        ax.annotate(f"{v} dB/km", (x, v), xytext=(10, 6), textcoords="offset points", fontsize=12, color=OPT)
    ax.set_xlabel("Wavelength (nm)")
    ax.set_ylabel("Attenuation (dB/km)")
    ax.set_ylim(0, 0.6); ax.set_xlim(1200, 1650)
    ax.grid(color="#e6e6e6", lw=0.6)
    ax.legend(loc="upper right")
    fig.tight_layout()
    save(fig, "f09_attenuation.png")


# ---------------------------------------------------------------- F10 dispersion fading
def f_dispersion():
    fig, ax = plt.subplots(figsize=(12, 4.6))
    c = 3e8
    D = 17e-6       # 17 ps/(nm km) in s/m^2
    lam = 1550e-9
    f = np.linspace(0.01e9, 40e9, 3000)
    for L, col, ls in ((5e3, BLUE, "-"), (10e3, OPT, "-"), (20e3, BLACK, "-")):
        p = np.cos(np.pi * L * D * lam ** 2 * f ** 2 / c) ** 2
        db = 10 * np.log10(np.maximum(p, 1e-4))
        ax.plot(f / 1e9, db, color=col, lw=2, ls=ls, label=f"{L/1e3:.0f} km at 1550 nm")
    ax.axhline(0, color=GREY, lw=1.5, ls="--", label="1310 nm (dispersion ≈ 0)")
    ax.axvspan(0, 6, color="#f0f0f0", zorder=0)
    ax.text(3, -36, "sub-6 GHz", ha="center", fontsize=12, color=GREY)
    ax.set_xlabel("RF frequency (GHz)")
    ax.set_ylabel("Detected RF power (dB, relative)")
    ax.set_xlim(0, 40); ax.set_ylim(-40, 3)
    ax.grid(color="#e6e6e6", lw=0.6)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.2), ncol=4)
    fig.tight_layout()
    save(fig, "f10_dispersion.png")


# ---------------------------------------------------------------- F11 SFDR
def f_sfdr():
    fig, ax = plt.subplots(figsize=(8, 4.8))
    pin = np.linspace(-60, 10, 200)
    fund = pin - 20
    imd3 = 3 * pin - 20 - 2 * 30
    nf = -110
    ax.plot(pin, fund, color=BLACK, lw=2.5, label="Fundamental (slope 1)")
    ax.plot(pin, imd3, color=OPT, lw=2.5, label="3rd-order intermodulation (slope 3)")
    ax.axhline(nf, color=GREY, lw=1.5, ls="--", label="Noise floor")
    p0 = (nf + 80) / 3
    ax.annotate("", xy=(p0, nf), xytext=(p0, p0 - 20), arrowprops=dict(arrowstyle="<|-|>", color=BLACK))
    ax.text(p0 - 2, (nf + p0 - 20) / 2, "SFDR", ha="right", fontsize=14, fontweight="bold")
    ax.set_xlabel("RF input power (dB)")
    ax.set_ylabel("RF output power (dB)")
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_xlim(-60, 10); ax.set_ylim(-130, 0)
    ax.legend(loc="upper left")
    fig.tight_layout()
    save(fig, "f11_sfdr.png")


# ---------------------------------------------------------------- F12 stadium case
def f_stadium():
    fig, ax = canvas(12, 4.8)
    cx, cy = 4.6, 2.4
    ax.add_patch(Ellipse((cx, cy), 8.4, 4.2, fill=False, ec=BLACK, lw=1.5))
    ax.add_patch(Ellipse((cx, cy), 5.0, 2.2, fill=False, ec=GREY, lw=1, ls="--"))
    ax.text(cx, cy, "pitch", ha="center", va="center", fontsize=13, color=GREY)
    ax.text(cx, cy + 1.22, "stands", ha="center", fontsize=12, color=GREY)
    box(ax, 9.6, 1.9, 2.2, 1.0, "Head-end\n(5 operators)", "eo", fs=12, bold=True)
    # fiber cable route runs around the bowl; each remote unit has its own fibers in that cable
    ax.add_patch(Ellipse((cx, cy), 6.8, 3.3, fill=False, ec=OPT, lw=3.2, zorder=2))
    arrow(ax, 9.6, 2.4, cx + 3.4, cy, "opt", head=False)
    angles = np.deg2rad([0, 45, 90, 135, 180, 225, 270, 315])
    for t in angles[1:]:
        x, y = cx + 3.4 * np.cos(t), cy + 1.65 * np.sin(t)
        ax.add_patch(Rectangle((x - 0.18, y - 0.14), 0.36, 0.28, fc="white", ec=BLACK, lw=1.2, zorder=4))
    ax.add_patch(Rectangle((cx + 3.4 - 0.18, cy + 0.25), 0.36, 0.28, fc="white", ec=BLACK, lw=1.2, zorder=4))
    ax.add_patch(Rectangle((9.6, 1.0), 0.36, 0.28, fc="white", ec=BLACK, lw=1.2))
    ax.text(10.1, 1.14, "fiber-fed remote unit", va="center", fontsize=12, color=GREY)
    ax.plot([9.6, 9.96], [0.6, 0.6], color=OPT, lw=3.2)
    ax.text(10.1, 0.6, "fiber cable route", va="center", fontsize=12, color=GREY)
    save(fig, "f12_stadium.png")


# ---------------------------------------------------------------- F13 decision flow
def f_decision():
    fig, ax = canvas(12, 4.7)
    qs = ["Fiber route\navailable?", "Length above\nbreak-even?", "Many bands or\noperators?", "Noise figure and\ndynamic range met?"]
    no = ["Passive coax\nor new fiber", "Passive coax", "Single-band\nradio or RRH", "Digital\nfronthaul"]
    x = 0.2
    for i, (q, n) in enumerate(zip(qs, no)):
        box(ax, x, 2.6, 2.1, 1.2, q, fs=13)
        arrow(ax, x + 1.05, 2.6, x + 1.05, 1.5)
        label(ax, x + 1.2, 1.95, "no", GREY, ha="left", va="center")
        box(ax, x, 0.4, 2.1, 1.1, n, fs=12)
        if i < 3:
            arrow(ax, x + 2.1, 3.2, x + 2.5, 3.2)
            label(ax, x + 2.3, 3.3, "yes", GREY)
        x += 2.5
    arrow(ax, x - 0.4, 3.2, x + 0.1, 3.2)
    label(ax, x - 0.15, 3.3, "yes", GREY)
    box(ax, x + 0.1, 2.6, 1.4, 1.2, "Analog\nRoF", "eo", fs=13, bold=True)
    save(fig, "f13_decision.png")


# ---------------------------------------------------------------- A: CSR vs BER
def f_csr():
    fig, ax = plt.subplots(figsize=(12, 4.6))
    csr = [0, 5, 10, 15, 20, 25, 30]
    v = [2.0, 3.0, 3.5, 3.5, 4.3, 4.4, 3.3]
    ax.plot(csr, v, "o-", color=OPT, lw=2.5, ms=8)
    for x, y in zip(csr, v):
        ax.annotate(f"{y:.1f}", (x, y), xytext=(0, 9), textcoords="offset points", ha="center", fontsize=12)
    ax.axhline(-np.log10(3.8e-3), color=GREY, ls="--", lw=1.2)
    ax.text(0.3, -np.log10(3.8e-3) + 0.08, "HD-FEC threshold (BER 3.8e-3)", fontsize=11, color=GREY)
    ax.set_xlabel("Carrier-to-sideband ratio (dB)")
    ax.set_ylabel(r"$-\log_{10}$(BER)   (higher = better)")
    ax.set_ylim(0, 5)
    ax.grid(color="#e6e6e6", lw=0.6)
    fig.tight_layout()
    save(fig, "a_csr.png")


# ---------------------------------------------------------------- A: RAU types
def f_rau():
    fig, ax = canvas(12, 4.6)
    rows = [("BBoF", ["PD", "TIA", "MOD", "Mixer+LO", "PA"], ["LD", "DEMOD", "Mixer+LO", "LNA"]),
            ("IFoF", ["PD", "TIA", "Mixer+LO", "PA"], ["LD", "Mixer+LO", "LNA"]),
            ("RFoF", ["PD", "TIA", "PA"], ["LD", "LNA"])]
    ax.text(1.4, 4.35, "Downlink: fiber → antenna", fontsize=13, color=GREY)
    ax.text(7.4, 4.35, "Uplink: antenna → fiber", fontsize=13, color=GREY)
    for i, (n, dlc, ulc) in enumerate(rows):
        y = 3.2 - i * 1.4
        ax.text(0.05, y + 0.35, n, fontsize=15, fontweight="bold", va="center")
        for j, t in enumerate(dlc):
            x = 1.4 + j * 1.15
            box(ax, x, y, 0.95, 0.7, t, "eo" if j == 0 else "el", fs=11, bold=j == 0)
            if j < len(dlc) - 1:
                arrow(ax, x + 0.95, y + 0.35, x + 1.15, y + 0.35)
        for j, t in enumerate(ulc):
            x = 7.4 + j * 1.15
            box(ax, x, y, 0.95, 0.7, t, "eo" if j == 0 else "el", fs=11, bold=j == 0)
            if j < len(ulc) - 1:
                arrow(ax, x + 1.15, y + 0.35, x + 0.95, y + 0.35)
    save(fig, "a_rau.png")


# ---------------------------------------------------------------- A: 5G + 6G demo
def f_demo():
    fig, ax = canvas(12, 4.6)
    box(ax, 0.1, 3.0, 2.2, 0.9, "5G-NR\nIF1 = 1.14 GHz", fs=12)
    box(ax, 0.1, 1.4, 2.2, 0.9, "Candidate 6G\nIF2 = 12 GHz", fs=12)
    arrow(ax, 2.3, 3.45, 2.8, 2.75); arrow(ax, 2.3, 1.85, 2.8, 2.45)
    box(ax, 2.8, 2.2, 1.2, 0.8, "E/O", "eo", bold=True)
    arrow(ax, 4.0, 2.6, 5.4, 2.6, "opt")
    label(ax, 4.7, 2.75, "fiber", OPT)
    box(ax, 5.4, 2.2, 1.3, 0.8, "Coupler", fs=12)
    arrow(ax, 6.7, 2.8, 7.3, 3.6, "opt")
    box(ax, 7.3, 3.3, 1.3, 0.75, "PIN PD", "eo", fs=12, bold=True)
    arrow(ax, 8.6, 3.67, 9.1, 3.67)
    box(ax, 9.1, 3.3, 0.9, 0.75, "LPF", fs=12)
    arrow(ax, 10.0, 3.67, 10.5, 3.67)
    box(ax, 10.5, 3.3, 1.4, 0.75, "5G RAU", fs=12)
    arrow(ax, 6.7, 2.4, 7.3, 1.6, "opt")
    box(ax, 7.3, 1.2, 1.0, 0.75, "BPF", fs=12)
    arrow(ax, 8.3, 1.57, 8.7, 1.57, "opt")
    box(ax, 8.7, 1.2, 1.2, 0.75, "Coupler", fs=12)
    box(ax, 8.7, 0.1, 1.2, 0.7, r"Laser $\lambda_2$", "eo", fs=12)
    arrow(ax, 9.3, 0.8, 9.3, 1.2, "opt")
    arrow(ax, 9.9, 1.57, 10.3, 1.57, "opt")
    box(ax, 10.3, 1.2, 1.6, 0.75, "UTC-PD\n→ THz", "eo", fs=12, bold=True)
    save(fig, "a_demo.png")


for fn in (f_title, f_problem, f_definition, f_signal_path, f_architecture, f_types, f_loss, f_cpri,
           f_attenuation, f_dispersion, f_sfdr, f_stadium, f_decision, f_csr, f_rau, f_demo):
    fn()
print("figures written to", OUT)
