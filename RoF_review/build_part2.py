"""Part 2 only (DAS + C-RAN), condensed, in the v3 template.
Usage: python3 build_part2.py v3.pptx v4.pptx figs_v3 figures_part2 out.pptx
"""
import sys
from pathlib import Path

src = Path(__file__).with_name("build_v3_full.py").read_text()
helpers = src[:src.index("# ================================================================ Part 2")]
exec(helpers)  # builds Part 1 into `prs` and defines the slide helpers

for sid in list(prs.slides._sldIdLst):  # keep the template, drop Part 1 slides
    prs.part.drop_rel(sid.get(qn("r:id")))
    prs.slides._sldIdLst.remove(sid)

LI = "Li, Xie, El-Hajjar, Hanzo, \"Analogue Radio Over Fiber for Next-Generation RAN,\" arXiv:2111.13851 (2021)"
B = lambda h, t: [(h, True), (t, False)]

# 1. Where is RoF used
s = new_slide("Where Is RoF Used in Practice?",
              "Goal of Part 2: show where the RoF link from Part 1 is used in practice, and what it costs. Left: C-RAN fronthaul (BBU to RRH over fiber). Right: indoor DAS.")
figure(s, F2 / "hadi2023_fig1_top_crop.png", 0.6, 1.3, 12.1, 4.3)
textbox(s, 0.6, 5.75, 12.1, 0.9, [B("Two uses, one question: ", "where does the fiber carry the radio signal, and what is the trade-off?")], 17)
source(s, "Adapted from: Hadi & Murtaza, \"Fibre Wireless Distributed Antenna Systems for 5G and 6G Services,\" Electronics 12(1), 64 (2023), Fig. 1, CC BY 4.0.")

# 2. DAS: what + why fiber
s = new_slide("Use 1: In-Building DAS",
              "Students: one signal source, many low-power antennas close to users (photo: real ceiling DAS antenna). Experts: coax loss rises with frequency, so fiber feeds remote units; cost moves to remote power, and uplink noise rises ~10log10(N) when N units share a port.")
figure(s, F2 / "silva2023_mall_das_antenna.jpg", 0.6, 1.35, 3.0, 4.0)
freqs = [700, 1800, 2600, 3500]
cd = CategoryChartData(); cd.categories = [f"{f} MHz" for f in freqs]
cd.add_series("Coax loss per 100 m (dB)", [round((0.12229 * f ** 0.5 + 0.00026 * f) / 0.3048, 1) for f in freqs])
ch = s.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, Inches(3.8), Inches(1.35), Inches(4.6), Inches(4.0), cd).chart
ch.has_legend = False; pl = ch.plots[0]; pl.has_data_labels = True
pl.data_labels.number_format = '0.0" dB"'; pl.data_labels.number_format_is_linked = False; pl.data_labels.font.size = Pt(12)
pl.series[0].format.fill.solid(); pl.series[0].format.fill.fore_color.rgb = RGBColor(0x7F, 0x7F, 0x7F)
ch.font.size = Pt(11); ch.font.name = FONT
textbox(s, 8.6, 1.35, 4.1, 5.2, [
    B("DAS: ", "one base station, many low-power antennas close to users."),
    B("Coax: ", "loss grows with frequency, 26.7 dB/100 m at 3.5 GHz."),
    B("Fiber: ", "≈ 0.025 dB/100 m for every band and operator."),
    B("Cost: ", "power at every remote unit; uplink noise rises with more units."),
], 15, gap=8)
source(s, "Photo: ceiling DAS antenna, Silva et al., Sensors 23, 4579 (2023). Chart: Times Microwave LMR-400 datasheet formula.")

# 3. C-RAN
s = new_slide("Use 2: C-RAN Fronthaul",
              "Baseband moves away from the antenna site and is pooled. The price is fronthaul: CPRI 20 MHz x1 antenna = 1.23 Gb/s; 100 MHz x64 antennas ≈ 315 Gb/s (CPRI V7.0 formula).")
figure(s, F2 / "li2021_fig1_ran_evolution.png", 0.6, 1.3, 12.1, 3.4)
textbox(s, 0.6, 4.9, 12.1, 1.8, [
    B("C-RAN: ", "baseband pooled centrally; radio heads stay at the antennas."),
    B("Gain: ", "shared processing, easier cell coordination, less equipment at each site."),
    B("Price: ", "fronthaul. CPRI: 1.23 Gb/s for 20 MHz × 1 antenna; ≈ 315 Gb/s for 100 MHz × 64 antennas."),
], 16, gap=6)
source(s, "Source: " + LI + ", Fig. 1. Rates: CPRI Specification V7.0.")

# 4. Analog vs digital: the trade-off
s = new_slide("Analog vs. Digital Fronthaul: Bandwidth vs. Quality",
              "Left: aggregated fiber bandwidth, A-RoF far lower (up to 40-fold in the modeled case). Right: EVM; A-RoF ~8 % meets 64-QAM but not the 3.5 % 256-QAM limit (3GPP TS 38.104); D-RoF meets it. This is the core trade-off of the talk.")
figure(s, F2 / "li2021_fig3_bandwidth.jpg", 0.6, 1.3, 4.6, 3.5)
figure(s, F2 / "li2021_fig5_evm.jpg", 5.4, 1.3, 7.3, 3.5)
textbox(s, 0.6, 5.0, 12.1, 1.7, [
    B("Analog RoF: ", "up to 40× less fiber bandwidth, simpler radio head, but EVM ≈ 8 % (fails the 3.5 % limit for 256-QAM)."),
    B("Digital fronthaul: ", "robust and standardized (CPRI / eCPRI), but bandwidth- and power-hungry."),
], 16, gap=6)
source(s, "Source: " + LI + ", Figs. 3 and 5. EVM limit: 3GPP TS 38.104.")

# 5. Limitations
s = new_slide("Limitations & Mitigation", "Five rows only; details on request.")
table(s, [
    ["Challenge", "Impact", "Mitigation"],
    ["Fiber & remote power", "CAPEX; every remote unit needs power", "Reuse fiber; hybrid fiber–copper cable"],
    ["Noise & nonlinearity", "Limit dynamic range and EVM", "Drive-level optimization; predistortion"],
    ["Chromatic dispersion", "RF power fading at high RF, long fiber", "1310 nm; single-sideband; IFoF"],
    ["Fronthaul rate (C-RAN)", "Grows with antennas and bandwidth", "Split 7.2x (eCPRI); analog RoF"],
    ["Interoperability", "Analog interfaces are vendor-specific", "ITU-T G.9803; eCPRI / O-RAN"],
], 0.6, 1.4, 12.1, [3.4, 4.5, 4.2], size=16, row_h=0.8)

# 6. Conclusions
s = new_slide("Conclusions", "Close the talk on the boundary experts will test: RoF moves the antenna, not the spectrum.")
textbox(s, 0.6, 1.4, 12.1, 5.2, [
    [("• RoF carries the analog radio waveform over fiber: low, band-independent loss.",)],
    [("• In buildings (DAS): fiber replaces lossy coax and feeds many antennas from one source.",)],
    [("• In C-RAN: analog RoF cuts fronthaul bandwidth sharply but loses signal quality.",)],
    [("• The choice depends on fiber availability, bands, required EVM and remote power.",)],
    [("• RoF moves the antenna closer to users; it does not add spectrum or capacity.", True)],
], 20, gap=14)

# 7. References
s = new_slide("References")
refs = ["Y. Li, Q. Xie, M. El-Hajjar, L. Hanzo, arXiv:2111.13851, 2021.",
        "M. U. Hadi, G. Murtaza, Electronics 12(1), 64, 2023. DOI: 10.3390/electronics12010064.",
        "J. da L. A. Silva et al., Sensors 23, 4579, 2023.",
        "V. Quintuna Rodriguez et al., arXiv:2101.04216, 2021.",
        "CPRI V7.0 (2015); eCPRI V2.0 (2019); 3GPP TS 38.104; ITU-T G.9803 (2018) & Amd. 2 (2022).",
        "Times Microwave Systems, LMR-400 datasheet."]
textbox(s, 0.6, 1.4, 12.1, 5.3, [[(f"{k + 1}. {r}",)] for k, r in enumerate(refs)], 16, gap=8)

# Backup
s = new_slide("Backup: Functional Splits", "For RAN experts: the lower the split, the more is central and the higher the fronthaul rate. Analog RoF sits below Option 8.")
figure(s, F2 / "quintuna2021_fig_functional_splits.png", 0.6, 1.3, 6.2, 5.3)
textbox(s, 7.1, 1.4, 5.6, 5.0, [B("Option 8: ", "time-domain I/Q (CPRI), highest rate."),
        B("Option 7.2: ", "frequency-domain I/Q (eCPRI, O-RAN)."),
        B("Option 2: ", "packets; lowest rate."),
        B("Analog RoF: ", "the RF waveform itself, below Option 8.")], 16, gap=10)
source(s, "Source: Quintuna Rodriguez et al., \"Cloud-RAN functional split for an efficient fronthaul network,\" arXiv:2101.04216 (2021).")

prs.save(OUT)
print("saved", OUT, len(prs.slides), "slides")
