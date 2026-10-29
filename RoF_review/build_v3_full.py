"""Builds the full v3 deck: Part 1 (from restructure_v3.py) + Part 2 (DAS, deployment, limits) + backup.

Usage: python3 build_v3_full.py v3.pptx v4.pptx figs_v3 figs_part2 out.pptx
"""
import subprocess
import sys
import tempfile
from pathlib import Path

from lxml import etree
from PIL import Image
from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.dml.color import RGBColor
from pptx.enum.chart import XL_CHART_TYPE, XL_LABEL_POSITION
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR
from pptx.oxml.ns import qn
from pptx.util import Inches, Pt

V3, V4, FIGS1, FIGS2, OUT = sys.argv[1:6]
HERE = Path(__file__).resolve().parent

# ---------------------------------------------------------------- Part 1
part1 = Path(tempfile.mkdtemp()) / "part1.pptx"
subprocess.run([sys.executable, str(HERE / "restructure_v3.py"), V3, V4, str(part1), FIGS1], check=True)
prs = Presentation(str(part1))

# Part 2 starts with DAS, so the old DAS slide at the end of Part 1 is replaced by the new section.
sld_lst = prs.slides._sldIdLst
last = list(sld_lst)[-1]
prs.part.drop_rel(last.get(qn("r:id")))
sld_lst.remove(last)

INK = RGBColor(0x11, 0x11, 0x11)
GREY = RGBColor(0x59, 0x59, 0x59)
FRAME = RGBColor(0xA6, 0xA6, 0xA6)
LIGHT = RGBColor(0xF2, 0xF2, 0xF2)
HEAD = RGBColor(0xD9, 0xD9, 0xD9)
ACCENT = RGBColor(0xD9, 0x53, 0x4F)
FONT = "Arial"
blank = prs.slides[0].slide_layout


# ---------------------------------------------------------------- helpers (same style as Part 1)
def runs(p, parts, size, color=INK):
    for item in parts:
        text, bold, italic = (item + (False, False))[:3] if isinstance(item, tuple) else (item, False, False)
        r = p.add_run()
        r.text = text
        f = r.font
        f.name, f.size, f.bold, f.italic = FONT, Pt(size), bold, italic
        f.color.rgb = color


def textbox(slide, x, y, w, h, paras, size, gap=6, color=INK, anchor=MSO_ANCHOR.TOP):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = Inches(0.05)
    for i, parts in enumerate(paras):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.space_after = Pt(gap)
        runs(p, parts, size, color)
    return tb


def box(slide, x, y, w, h, fill=None, line=FRAME):
    s = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    st = s._element.find(qn("p:style"))
    if st is not None:
        s._element.remove(st)
    if fill is None:
        s.fill.background()
    else:
        s.fill.solid()
        s.fill.fore_color.rgb = fill
    s.line.color.rgb = line
    s.line.width = Pt(0.75)
    return s


def new_slide(title, notes=""):
    s = prs.slides.add_slide(blank)
    for ph in list(s.placeholders):
        ph._element.getparent().remove(ph._element)
    textbox(s, 0.6, 0.35, 12.1, 0.9, [[(title, True)]], 34)
    if notes:
        s.notes_slide.notes_text_frame.text = notes
    return s


def figure(slide, path, x, y, w, h, frame=True):
    """Place an image inside the box, keeping its aspect ratio; returns (x, y, w, h) actually used."""
    pw, ph = Image.open(path).size
    r = pw / ph
    fw, fh = w, w / r
    if fh > h:
        fh, fw = h, h * r
    fx = x + (w - fw) / 2
    pic = slide.shapes.add_picture(str(path), Inches(fx), Inches(y), Inches(fw), Inches(fh))
    if frame:
        pic.line.color.rgb = FRAME
        pic.line.width = Pt(0.75)
    return fx, y, fw, fh


def source(slide, text):
    textbox(slide, 0.6, 6.9, 12.1, 0.45, [[(text,)]], 11, color=GREY)


def table(slide, rows, x, y, w, col_w, size=14, row_h=0.5):
    shp = slide.shapes.add_table(len(rows), len(rows[0]), Inches(x), Inches(y), Inches(w), Inches(row_h * len(rows)))
    tbl = shp.table
    tblPr = tbl._tbl.tblPr
    st = tblPr.find(qn("a:tableStyleId"))
    if st is not None:
        st.text = "{5940675A-B579-460E-94D1-54222C63F5DA}"  # "No Style, Table Grid"
    for i, cw in enumerate(col_w):
        tbl.columns[i].width = Inches(cw)
    for ri, row in enumerate(rows):
        for ci, val in enumerate(row):
            c = tbl.cell(ri, ci)
            c.margin_left = c.margin_right = Inches(0.08)
            c.margin_top = c.margin_bottom = Inches(0.04)
            c.vertical_anchor = MSO_ANCHOR.MIDDLE
            tf = c.text_frame
            tf.word_wrap = True
            p = tf.paragraphs[0]
            runs(p, [(val, ri == 0 or ci == 0)], size)
            c.fill.solid()
            c.fill.fore_color.rgb = HEAD if ri == 0 else RGBColor(0xFF, 0xFF, 0xFF)
            tcPr = c._tc.get_or_add_tcPr()
            for k, tag in enumerate(("lnL", "lnR", "lnT", "lnB")):
                ln = etree.Element(qn("a:" + tag), w="9525", cap="flat", cmpd="sng", algn="ctr")
                sf = etree.SubElement(ln, qn("a:solidFill"))
                etree.SubElement(sf, qn("a:srgbClr"), val="A6A6A6")
                etree.SubElement(ln, qn("a:prstDash"), val="solid")
                tcPr.insert(k, ln)
    return tbl


F1, F2 = Path(FIGS1), Path(FIGS2)

# ================================================================ Part 2
# --- 1. Transition
s = new_slide("Part 2: Why Talk About DAS?",
              "Transition (about 0:45). Part 1 explained one RoF link. Part 2 answers: where is that link used in practice, at scale? "
              "The clearest answer is the fiber-fed distributed antenna system. Every trade-off from Part 1 (loss, noise, dynamic range, "
              "transparency to bands and operators) reappears here as a design decision.")
figure(s, F2 / "transition.png", 0.6, 1.35, 12.1, 3.75, frame=False)
textbox(s, 0.6, 5.25, 12.1, 1.6, [
    [("• A RoF link is a building block; a ", False), ("fiber-fed DAS", True), (" is where it is deployed at scale.", False)],
    [("• Every Part 1 trade-off (loss, noise, dynamic range, transparency) becomes a DAS design decision.", False)],
    [("• RoF transparency lets several operators and bands share one in-building network.", False)],
], 18, gap=6)

# --- 2. What is a DAS (students)
s = new_slide("What Is a Distributed Antenna System (DAS)?",
              "For students hearing the term for the first time: walls and distance weaken the outdoor signal (red cross). "
              "A DAS brings the base-station signal inside and spreads it over many small, low-power antennas close to the users. "
              "Walk the three numbers: (1) signal source, (2) distribution from the head-end over fiber to a remote unit on each floor, "
              "(3) ceiling antennas. For the experts: many low-power antennas close to users give a more uniform signal level than one high-power antenna far away.")
figure(s, F2 / "das_concept.png", 0.6, 1.35, 8.6, 3.6, frame=True)
steps = [("1", "Signal source", "operator base station (or repeater) in the equipment room"),
         ("2", "Distribution", "head-end sends the signal over fiber (or coax) to a remote unit on each floor"),
         ("3", "Antennas", "many low-power ceiling antennas close to the users")]
for i, (n, h, t) in enumerate(steps):
    y = 1.4 + i * 1.2
    c = s.shapes.add_shape(MSO_SHAPE.OVAL, Inches(9.45), Inches(y), Inches(0.42), Inches(0.42))
    st = c._element.find(qn("p:style"))
    if st is not None:
        c._element.remove(st)
    c.fill.solid(); c.fill.fore_color.rgb = ACCENT; c.line.fill.background()
    tf = c.text_frame; tf.margin_left = tf.margin_right = 0
    runs(tf.paragraphs[0], [(n, True)], 14, RGBColor(0xFF, 0xFF, 0xFF))
    tf.paragraphs[0].alignment = 2
    textbox(s, 10.0, y - 0.05, 2.75, 1.15, [[(h, True)], [(t,)]], 14, gap=2)
c = box(s, 0.6, 5.3, 12.1, 0.85, LIGHT)
tf = c.text_frame; tf.word_wrap = True; tf.vertical_anchor = MSO_ANCHOR.MIDDLE
tf.margin_left = tf.margin_right = Inches(0.2)
runs(tf.paragraphs[0], [("DAS: ", True), ("the signal of one or more base stations is distributed to many low-power antennas spread across a building, venue or tunnel.", False, True)], 17)

# --- 3. DAS types
s = new_slide("DAS Types: Passive, Active (Fiber) and Hybrid",
              "Passive DAS: coax and splitters only; no active equipment or power at the antennas, but loss grows with frequency and cable length. "
              "Active (fiber) DAS: the master unit converts RF to optical; fiber reaches a remote unit near every antenna; this is RoF. "
              "Hybrid DAS: fiber to one remote unit per zone or floor, then short coax to several passive antennas; the common compromise in large buildings. "
              "Digital DAS digitizes the RF at the head-end and sends samples, the same analog versus digital trade-off as Part 1.")
figure(s, F2 / "das_types.png", 0.6, 1.35, 12.1, 4.3, frame=False)
textbox(s, 0.6, 5.95, 12.1, 0.8, [[("Digital DAS: ", True), ("the head-end digitizes the RF and sends samples over fiber — the same analog vs. digital trade-off as Part 1.", False)]], 16)

# --- 4. Why fiber instead of coax
s = new_slide("Why Fiber Instead of Coax at 5G Bands?",
              "The plot uses the LMR-400 datasheet attenuation formula. Coax loss grows roughly with the square root of frequency; "
              "at 3.5 GHz (n78) it is about 2.4 times the 700 MHz value in dB. Fiber attenuation does not depend on the RF band. "
              "For the RAN and antenna experts: the cost moves to the remote unit (optoelectronics, amplifiers, local power). "
              "Uplink noise funnelling: when N remote units feed one uplink port, their noise adds and the floor rises by about 10·log10(N) dB "
              "(8 units: about 9 dB), which limits how many units share a sector. MIMO needs one RF chain per layer at every remote unit.")
figure(s, F2 / "coax_loss.png", 0.6, 1.35, 6.4, 4.6, frame=True)
textbox(s, 7.3, 1.4, 5.4, 4.8, [
    [("Coax loss grows with frequency: ", True), ("≈ 26.7 dB / 100 m at 3.5 GHz, ≈ 2.4× the 700 MHz value.", False)],
    [("Fiber loss is band-independent: ", True), ("one fiber run serves every band and operator.", False)],
    [("The cost moves to the remote unit: ", True), ("E/O, O/E, amplifiers and local power.", False)],
    [("Uplink noise rise: ", True), ("N remote units on one port raise the noise floor by ≈ 10·log10(N) dB.", False)],
    [("MIMO: ", True), ("2×2 or 4×4 needs one RF chain per layer at every remote unit.", False)],
], 16, gap=10)
source(s, "Coax: Times Microwave LMR-400 datasheet attenuation formula. Fiber: G.652.D single-mode cable, ≈ 0.25 dB/km at 1550 nm.")

# --- 5. Multi-operator architecture
s = new_slide("Multi-Operator Fiber DAS Architecture",
              "This is the most relevant slide for operators and neutral-host engineers. Each operator's base station connects to the POI, "
              "which sets each operator's RF level and combines bands. The master unit converts the combined RF to optical. "
              "Each remote unit converts back to RF and amplifies it. The fiber section is exactly the RoF link from Part 1. "
              "Downlink and uplink use separate fibers or wavelengths. Backhaul to each operator's core is separate and digital.")
figure(s, F2 / "das_arch.png", 0.6, 1.3, 12.1, 4.55, frame=True)
textbox(s, 0.6, 6.0, 12.1, 0.9, [
    [("POI ", True), ("(point of interface): sets each operator's RF level and combines bands.  ", False),
     ("Master unit: ", True), ("RF ↔ optical.  ", False), ("Remote unit: ", True), ("optical ↔ RF + amplifiers.", False)],
], 15)

# --- 6. Advantages and trade-offs
s = new_slide("DAS with RoF: Advantages and Trade-offs",
              "Each advantage is paired with the condition or cost that comes with it, so the slide can be defended in front of experts. "
              "Coverage comes from where the remote units and antennas are placed; the fiber only makes long runs possible.")
table(s, [
    ["Advantage", "Condition / trade-off"],
    ["Coverage in hard-to-reach areas (deep indoor, tunnels)", "Set by remote-unit and antenna placement, not by the fiber"],
    ["Multi-band, multi-operator on one network", "All carriers share each remote unit's output power and dynamic range"],
    ["Long runs with negligible transport loss", "Every remote unit needs power; fiber count must be planned"],
    ["Easy expansion: add remote units where fiber reaches", "Uplink noise rises with more units; capacity still set by the operators' sectors"],
    ["Fiber span immune to electromagnetic interference", "Over-the-air interference and passive intermodulation (PIM) still need managing"],
], 0.6, 1.4, 12.1, [5.6, 6.5], size=15, row_h=0.75)

# --- 7. Documented case: NYC subway
s = new_slide("Documented Case: New York City Subway",
              "Chosen because it is a well-known, publicly documented multi-operator fiber DAS. Same architecture as the previous slides, at city scale: "
              "operator base stations in a base-station hotel, a radio interface and optical distribution system, fiber along the stations and tunnels, "
              "and remote units near the antennas. Figures are as reported by the operator and trade press; carrier line-ups and totals may have changed since.")
figure(s, F2 / "subway.png", 0.6, 1.35, 7.0, 3.6, frame=True)
textbox(s, 7.85, 1.35, 4.85, 4.9, [
    [("Neutral-host DAS ", True), ("in the underground stations under a 27-year MTA agreement (Transit Wireless, now Boldyn Networks).", False)],
    [("All four Tier-1 US operators; ", True), ("their base stations sit in a base-station hotel feeding an optical distribution system.", False)],
    [("277 stations; ", True), ("DAS platform by Solid, antennas by PCTel.", False)],
    [("Reported scale: ", True), ("≈ 120 miles of fiber, ≈ 4,000 cellular antennas.", False)],
    [("2023: ", True), ("agreement expanded to double the 5G fiber network (418 track miles).", False)],
], 14, gap=8)
textbox(s, 0.6, 5.15, 7.0, 0.9, [[("Same chain as slide before: ", True), ("base stations → optical distribution → fiber → remote units → antennas, at city scale.", False)]], 15)
source(s, "Sources: RCR Wireless (Solid DAS deal, 277 stations); Fierce Network (four operators); Boldyn Networks press release (2023 expansion); WBA World Wi-Fi Day case study (2018).")

# --- 8. Application areas
s = new_slide("RoF Application Areas",
              "Five areas, one line each. Be careful with 5G fronthaul: commercial fronthaul today is mainly digital (CPRI / eCPRI); "
              "analog RoF fronthaul is mostly at research and trial stage, with requirements in ITU-T G.9803 Amendment 2.")
cards = [
    ("Cellular in-building & venues", "Buildings, stadiums, airports, tunnels and metros (fiber-fed DAS)."),
    ("5G fronthaul", "Analog RoF studied for C-RAN and mmWave; commercial fronthaul today is mainly digital (CPRI / eCPRI)."),
    ("Public safety", "In-building coverage for emergency-responder radio."),
    ("Defense & aerospace", "Antenna remoting, radar and satellite ground stations: low loss, light weight, EMI immunity."),
    ("Research", "RF-over-fiber in the SKA-low radio-telescope receiver (Perini et al., 2022)."),
]
for i, (h, t) in enumerate(cards):
    col, row = (i % 3, i // 3)
    x = 0.6 + col * 4.1 if row == 0 else 2.65 + col * 4.1
    y = 1.45 + row * 2.45
    box(s, x, y, 3.9, 2.2)
    textbox(s, x + 0.12, y + 0.1, 3.66, 2.0, [[(h, True)], [(t,)]], 16, gap=8)
source(s, "SKA-low: Perini et al., J. Astron. Telesc. Instrum. Syst. 8(1), 011016 (2022). Fronthaul requirements: ITU-T G.9803 Amd. 2 (2022).")

# --- 9. Limitations and challenges
s = new_slide("Limitations & Technical Challenges",
              "Practical limits (top four rows) and technical limits (bottom four rows) in one table, each with its mitigation. "
              "For the experts, the most important rows are noise and uplink noise rise, nonlinearity, and remote power.")
table(s, [
    ["Challenge", "Impact", "Mitigation"],
    ["Cost", "New fiber and optoelectronics raise CAPEX", "Reuse existing fiber; share one network among operators"],
    ["Fiber availability", "Civil works and permits slow deployment", "Plan routes early; hybrid DAS for the last metres"],
    ["Remote power", "Every remote unit needs power and backup", "Hybrid fiber–copper cable; local UPS"],
    ["Topology", "Point-to-point fiber per unit limits reconfiguration", "WDM; cascaded remote units"],
    ["Nonlinear distortion", "Intermodulation limits dynamic range", "Optimized drive level; predistortion"],
    ["Chromatic dispersion", "RF power fading at high RF and long fiber", "1310 nm operation; single-sideband; IFoF"],
    ["Noise / uplink noise rise", "Limits sensitivity and units per port", "Uplink gain plan; fewer units per combiner"],
    ["Interoperability", "Analog interfaces are largely vendor-specific", "ITU-T G.9803 requirements; digital DAS / eCPRI"],
], 0.6, 1.35, 12.1, [2.9, 4.5, 4.7], size=13, row_h=0.56)

# --- 10. Summary
s = new_slide("Summary",
              "Five take-aways, in the order of the talk. The last one is the boundary that experts will test: RoF moves the antenna closer to users; "
              "capacity comes from spectrum and radio design.")
figure(s, F2 / "transition.png", 6.9, 1.45, 5.8, 2.0, frame=False)
textbox(s, 0.6, 1.4, 6.0, 5.3, [
    [("• RoF carries the analog radio waveform over fiber: E/O at one end, O/E at the other.",)],
    [("• Fiber loss is low and band-independent; the link still adds conversion loss, noise and distortion.",)],
    [("• A fiber-fed DAS is RoF at scale: one signal source, many antennas, many operators.",)],
    [("• Coax suits short, low-frequency runs; fiber suits long runs, many bands and 5G frequencies.",)],
    [("• RoF moves the antenna closer to users; it does not add spectrum or air-interface capacity.", True)],
], 18, gap=12)

# --- 11. References
s = new_slide("References")
refs = [
    "ITU-T G.9803 (2018), Radio over fibre systems; Amendments 1 (2019) and 2 (2022). ITU-T G.Suppl.55 (10/2025). ITU-T G.652.",
    "C. H. Cox III, Analog Optical Links: Theory and Practice, Cambridge University Press, 2004.",
    "Y. Li, Q. Xie, M. El-Hajjar, L. Hanzo, \"Analogue Radio Over Fiber for Next-Generation RAN: Challenges and Opportunities,\" arXiv:2111.13851, 2021.",
    "\"Radio over Fiber: An Alternative Broadband Network Technology for IoT,\" Electronics 9(11), 1785, 2020. DOI: 10.3390/electronics9111785.",
    "M. U. Hadi, G. Murtaza, \"Fibre Wireless Distributed Antenna Systems for 5G and 6G Services,\" Electronics 12(1), 64, 2023. DOI: 10.3390/electronics12010064.",
    "F. Perini et al., \"Radio frequency over fiber technology for SKA-low receiver,\" J. Astron. Telesc. Instrum. Syst. 8(1), 011016, 2022.",
    "Times Microwave Systems, LMR-400 coaxial cable datasheet.",
    "NYC subway DAS: RCR Wireless; Fierce Network; Boldyn Networks (Transit Wireless) press release, 2023; WBA case study, 2018.",
    "SolFinder Research, \"Radio Over Fiber,\" video presentation (source of original material).",
]
textbox(s, 0.6, 1.35, 12.1, 5.6, [[(f"{i + 1}. {r}",)] for i, r in enumerate(refs)], 14, gap=7)

# ================================================================ Backup
s = new_slide("Backup: Research Directions & Outlook",
              "Backup slide for questions from the professors. The 40× and EVM figures are results of one modeled scenario (Li et al., 2021), not general results.")
figure(s, F2 / "demo.png", 0.6, 1.35, 6.2, 3.6, frame=True)
textbox(s, 7.1, 1.35, 5.6, 5.3, [
    [("Lab demo: ", True), ("5G-NR and a candidate 6G (THz) signal carried on one fiber (Hadi & Murtaza, 2023).", False)],
    [("Massive MIMO and mmWave ", True), ("push digital fronthaul rates up.", False)],
    [("Modeled case: ", True), ("up to 40× lower fiber bandwidth for analog RoF (16×16 MIMO, 28 GHz, 256-QAM), but analog EVM ≈ 8 % vs. the 3.5 % limit (Li et al., 2021).", False)],
    [("Silicon photonics ", True), ("may lower optoelectronic cost as it matures.", False)],
], 15, gap=10)

s = new_slide("Backup: Effect of CSR on Link Error Rate",
              "Values are approximate readings from the published plot (Hadi & Murtaza, 2023, Fig. 6) for a 10 km SMF + 3 m wireless link. "
              "Higher −log10(BER) means fewer errors. At low CSR distortion dominates; at high CSR noise dominates. Specific to the tested link.")
cd = CategoryChartData()
cd.categories = ["0", "5", "10", "15", "20", "25", "30"]
cd.add_series("−log10(BER)", (2.0, 3.0, 3.5, 3.5, 4.3, 4.4, 3.3))
gf = s.shapes.add_chart(XL_CHART_TYPE.LINE_MARKERS, Inches(0.6), Inches(1.35), Inches(7.6), Inches(5.0), cd)
ch = gf.chart
ch.has_legend = False
pl = ch.plots[0]
pl.has_data_labels = True
pl.data_labels.number_format = "0.0"
pl.data_labels.number_format_is_linked = False
pl.data_labels.position = XL_LABEL_POSITION.ABOVE
pl.data_labels.font.size = Pt(12)
ser = pl.series[0]
ser.format.line.color.rgb = RGBColor(0xD9, 0x53, 0x4F)
ser.format.line.width = Pt(2.5)
ch.value_axis.maximum_scale = 5
ch.value_axis.minimum_scale = 0
ch.value_axis.has_title = True
ch.value_axis.axis_title.text_frame.text = "−log10(BER)"
ch.category_axis.has_title = True
ch.category_axis.axis_title.text_frame.text = "CSR (dB)"
ch.font.size = Pt(12)
ch.font.name = FONT
textbox(s, 8.5, 1.5, 4.2, 4.8, [
    [("Higher value = fewer errors.",)],
    [("BER improves up to CSR ≈ 25 dB, then degrades at 30 dB.",)],
    [("Optical and RF power must be tuned together.",)],
    [("Specific to the tested link.",)],
], 16, gap=10)
source(s, "Redrawn from Hadi & Murtaza, Electronics 12(1), 64 (2023), Fig. 6; values read approximately from the published plot.")

prs.save(OUT)
print("saved", OUT, len(prs.slides), "slides")
