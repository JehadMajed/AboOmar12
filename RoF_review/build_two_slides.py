"""Two slides (DAS, C-RAN) built on images supplied by the presenter, in the v3 template.
Usage: python3 build_two_slides.py v3.pptx v4.pptx figs_v3 figures_part2 out.pptx
"""
from pathlib import Path

src = Path(__file__).with_name("build_v3_full.py").read_text()
exec(src[:src.index("# ================================================================ Part 2")])
for sid in list(prs.slides._sldIdLst):
    prs.part.drop_rel(sid.get(qn("r:id")))
    prs.slides._sldIdLst.remove(sid)
B = lambda h, t: [(h, True), (t, False)]

s = new_slide("Use 1: In-Building DAS",
              "Left: outdoor macro signal cannot penetrate the building; with DAS, many low-power antennas inside give uniform coverage. "
              "Right: the chain. Donor Unit takes the operator signal, Main Hub Unit converts RF to optical, fiber runs up the riser to "
              "Remote Optic Units on each floor, short low-loss coax and passive splitters (DSU) feed the ceiling antennas. "
              "The fiber riser is the RoF link from Part 1. Image sources: add the URLs of both images before presenting.")
figure(s, F2 / "user_das_problem_solution.png", 0.6, 1.35, 5.9, 3.9)
figure(s, F2 / "user_das_units.png", 6.8, 1.35, 5.9, 3.9)
textbox(s, 0.6, 5.45, 12.1, 1.4, [
    B("Problem → solution: ", "walls block the outdoor signal; many low-power antennas inside give uniform coverage."),
    B("Chain: ", "Donor Unit → Main Hub (RF → optical) → fiber riser (RoF) → Remote Optic Unit per floor → antennas."),
], 16, gap=6)

s = new_slide("Use 2: C-RAN with RoF Fronthaul",
              "Baseband units are pooled centrally; each remote radio head keeps only the RF part. Backhaul (core to BBU pool) is digital; "
              "fronthaul (BBU to RRH) is the RoF link. Digital fronthaul (CPRI) needs 1.23 Gb/s for 20 MHz x 1 antenna and about 315 Gb/s for "
              "100 MHz x 64 antennas; analog RoF needs up to 40x less fiber bandwidth but EVM of about 8 % fails the 3.5 % 256-QAM limit "
              "(Li et al., arXiv:2111.13851; 3GPP TS 38.104). Image source: add the URL before presenting.")
figure(s, F2 / "user_cran_rof.png", 0.6, 1.35, 12.1, 4.0)
textbox(s, 0.6, 5.55, 12.1, 1.3, [
    B("Backhaul ", "(core → BBU pool) is digital; fronthaul (BBU → RRH) is the RoF link."),
    B("Trade-off: ", "analog RoF needs up to 40× less fiber bandwidth than CPRI, at lower signal quality (EVM ≈ 8 %)."),
], 16, gap=6)

prs.save(OUT)
print("saved", OUT, len(prs.slides), "slides")
