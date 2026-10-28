// Builds the revised Radio over Fiber (RoF) technical review deck.
// All diagrams are drawn as native, editable vector shapes (no raster images).
// Usage: npm install pptxgenjs && node build_rof_deck.js [output.pptx]
const pptxgen = require("pptxgenjs");

const OUT = process.argv[2] || "RoF_Technical_Review.pptx";
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in
pres.title = "Radio over Fiber (RoF): Technical Review";
pres.subject = "Radio over Fiber transport: signal path, architectures, alternatives and limits";
pres.theme = { headFontFace: "Calibri", bodyFontFace: "Calibri" };

// ---------- Palette (corporate, restrained) ----------
const NAVY = "1F3A5F";   // titles, optical paths
const INK = "1A1A1A";    // body text, electrical paths
const GREY = "5F6670";   // captions, footers
const WL = "6E7781";     // wireless paths (dashed)
const BORDER = "AEB6C2";
const HEAD = "E6EBF2";   // table header fill
const LIGHT = "F3F5F8";  // panel fill
const EO = "DCE6F2";     // E/O and O/E conversion blocks
const FOCUS = "EEF2F8";  // highlighted region
const FONT = "Calibri";

// ---------- Layouts ----------
const titleOpts = { name: "title", type: "title", x: 0.6, y: 0.35, w: 12.1, h: 0.75,
  fontFace: FONT, fontSize: 28, bold: true, color: NAVY, align: "left", valign: "middle", margin: 0 };
pres.defineSlideMaster({
  title: "TITLE_SLIDE", background: { color: "FFFFFF" }, objects: [],
});
pres.defineSlideMaster({
  title: "CONTENT", background: { color: "FFFFFF" },
  objects: [
    { placeholder: { options: titleOpts, text: "" } },
    { text: { text: "Radio over Fiber (RoF) · Technical review",
      options: { x: 0.6, y: 7.0, w: 7, h: 0.3, fontFace: FONT, fontSize: 10, color: GREY, margin: 0 } } },
  ],
  slideNumber: { x: 12.1, y: 7.0, w: 0.6, h: 0.3, fontFace: FONT, fontSize: 10, color: GREY, align: "right" },
});
pres.defineSlideMaster({
  title: "APPENDIX", background: { color: "FFFFFF" },
  objects: [
    { placeholder: { options: titleOpts, text: "" } },
    { text: { text: "Appendix · Reference material, not presented in the 15-minute talk",
      options: { x: 0.6, y: 7.0, w: 9, h: 0.3, fontFace: FONT, fontSize: 10, color: GREY, margin: 0 } } },
  ],
  slideNumber: { x: 12.1, y: 7.0, w: 0.6, h: 0.3, fontFace: FONT, fontSize: 10, color: GREY, align: "right" },
});

// ---------- Helpers ----------
function txt(s, t, o) {
  s.addText(t, Object.assign({ isTextBox: true, fontFace: FONT, fontSize: 14, color: INK,
    margin: 0, valign: "top" }, o));
}
function source(s, t) { txt(s, t, { x: 0.6, y: 6.5, w: 12.1, h: 0.42, fontSize: 10, color: GREY, valign: "bottom" }); }
function box(s, x, y, w, h, label, o = {}) {
  s.addShape(pres.shapes.RECTANGLE, { x, y, w, h,
    fill: { color: o.fill || "FFFFFF" },
    line: { color: o.lc || BORDER, width: o.lw || 1, dashType: o.dash || "solid" } });
  if (label) txt(s, label, { x, y, w, h, fontSize: o.fs || 12, bold: !!o.bold, color: o.color || INK,
    align: o.align || "center", valign: o.valign || "middle", margin: o.margin == null ? 3 : o.margin });
}
const LINK = {
  opt: { color: NAVY, width: 3 },
  el: { color: INK, width: 1.25 },
  wl: { color: WL, width: 1.5, dashType: "dash" },
};
// Arrow from (x1,y1) to (x2,y2). kind: opt | el | wl. both: arrowheads at both ends.
function link(s, x1, y1, x2, y2, kind, o = {}) {
  const line = Object.assign({}, LINK[kind]);
  if (!o.noHead) line.endArrowType = "triangle";
  if (o.both) line.beginArrowType = "triangle";
  const shp = { x: Math.min(x1, x2), y: Math.min(y1, y2), w: Math.abs(x2 - x1), h: Math.abs(y2 - y1), line };
  if (x2 < x1) shp.flipH = true;
  if (y2 < y1) shp.flipV = true;
  s.addShape(pres.shapes.LINE, shp);
}
// Label centred above (or below) a horizontal segment.
function linkLabel(s, x1, x2, y, t, kind, below) {
  const color = kind === "opt" ? NAVY : kind === "wl" ? WL : INK;
  txt(s, t, { x: Math.min(x1, x2), y: below ? y + 0.05 : y - 0.32, w: Math.abs(x2 - x1), h: 0.27,
    fontSize: 10, italic: true, color, align: "center", valign: below ? "top" : "bottom" });
}
function antenna(s, x, y) { // x,y = feed point (bottom of mast)
  s.addShape(pres.shapes.LINE, { x, y: y - 0.32, w: 0, h: 0.32, line: { color: INK, width: 1.25 } });
  s.addShape(pres.shapes.ISOSCELES_TRIANGLE, { x: x - 0.13, y: y - 0.5, w: 0.26, h: 0.2, flipV: true,
    fill: { color: "FFFFFF" }, line: { color: INK, width: 1.25 } });
}
function legend(s, x, y, items = ["el", "opt", "wl"]) {
  const names = { el: "Electrical (RF / IF / digital)", opt: "Optical (fiber)", wl: "Wireless (over the air)" };
  let cx = x;
  items.forEach((k) => {
    link(s, cx, y + 0.13, cx + 0.5, y + 0.13, k, { noHead: true });
    txt(s, names[k], { x: cx + 0.6, y, w: 2.6, h: 0.26, fontSize: 10, color: GREY, valign: "middle" });
    cx += 3.1;
  });
}
function bullets(items, o = {}) { // items: string or [label, rest]
  return items.map((it, i) => {
    const last = i === items.length - 1;
    const base = { bullet: true, paraSpaceAfter: o.gap == null ? 6 : o.gap, breakLine: !last };
    if (Array.isArray(it)) return [
      { text: it[0] + " ", options: Object.assign({}, base, { bold: true, breakLine: false }) },
      { text: it[1], options: { breakLine: !last } },
    ];
    return [{ text: it, options: base }];
  }).flat();
}
const hc = (t) => ({ text: t, options: { bold: true, fill: { color: HEAD }, color: NAVY } });
function table(s, rows, o) {
  s.addTable(rows, Object.assign({ fontFace: FONT, fontSize: 12, color: INK, valign: "middle",
    border: { type: "solid", pt: 0.75, color: BORDER }, margin: [0.04, 0.08, 0.04, 0.08] }, o));
}
function content(title, notes, section, master = "CONTENT") {
  const s = pres.addSlide({ masterName: master, sectionTitle: section });
  s.addText(title, { placeholder: "title" });
  if (notes) s.addNotes(notes);
  return s;
}

// =====================================================================
// SECTION: Opening
// =====================================================================
const S_A = "Speaker A · Problem, definition, signal path, architectures";
const S_B = "Speaker B · Comparisons, benefits, limits, case, conclusions";
const S_APP = "Appendix";
pres.addSection({ title: S_A });

// ---- 1. Title ----
{
  const s = pres.addSlide({ masterName: "TITLE_SLIDE", sectionTitle: S_A });
  txt(s, "Radio over Fiber (RoF)", { x: 0.8, y: 1.7, w: 11.7, h: 0.9, fontSize: 40, bold: true, color: NAVY });
  txt(s, "Transport of radio waveforms over optical fiber: signal path, architectures, alternatives and limits",
    { x: 0.8, y: 2.65, w: 11.7, h: 0.9, fontSize: 20, color: INK });
  txt(s, [
    { text: "Technical review · 15 minutes · two speakers", options: { breakLine: true } },
    { text: "Speaker A: problem, definition, signal path, architectures, RoF types", options: { breakLine: true } },
    { text: "Speaker B: comparisons, benefits and conditions, limitations, case, conclusions" },
  ], { x: 0.8, y: 3.75, w: 11.7, h: 1.0, fontSize: 14, color: GREY, paraSpaceAfter: 4 });
  // Minimal schematic strip: central site -> fiber -> remote unit -> air -> UE
  const y = 5.75;
  box(s, 0.8, y - 0.3, 2.2, 0.6, "Central radio equipment", { fs: 11 });
  link(s, 3.0, y, 3.5, y, "el");
  box(s, 3.5, y - 0.3, 0.8, 0.6, "E/O", { fill: EO, fs: 11, bold: true });
  link(s, 4.3, y, 7.9, y, "opt");
  linkLabel(s, 4.3, 7.9, y, "Optical fiber: analog radio waveform", "opt");
  box(s, 7.9, y - 0.3, 0.8, 0.6, "O/E", { fill: EO, fs: 11, bold: true });
  link(s, 8.7, y, 9.2, y, "el");
  box(s, 9.2, y - 0.3, 1.7, 0.6, "Remote antenna unit", { fs: 11 });
  link(s, 10.9, y, 11.15, y, "el", { noHead: true });
  antenna(s, 11.15, y);
  link(s, 11.4, y - 0.3, 12.0, y - 0.3, "wl");
  box(s, 12.0, y - 0.55, 0.7, 0.5, "UE", { fs: 11 });
  s.addNotes(
    "Timing: 0:20 (Speaker A).\n" +
    "Purpose: state the subject and the division of work between the two speakers.\n" +
    "The strip at the bottom is the scope of the talk in one line: the optical segment between the central radio equipment and the remote antenna unit. " +
    "Everything that follows is about that segment, its alternatives, and the conditions under which it is the right choice.");
}

// ---- 2. Problem and scope ----
{
  const s = content("Problem and scope",
    "Timing: 1:15 (Speaker A).\n" +
    "Logic: start from the engineering need, not from the technology. The need is to distribute one radio signal to many antenna points that are physically far from the radio equipment. " +
    "Centralization is a design choice with its own reasons (shared power, cooling, maintenance, multi-operator hosting); it is what creates the transport problem.\n" +
    "Point out explicitly that backhaul is out of scope: RoF is not a backhaul technology, and confusing the two is a common error in the source material.\n" +
    "The three alternatives named here are the only ones compared later; microwave point-to-point links are excluded because they serve backhaul, not an antenna feeder.", S_A);
  txt(s, "Engineering problem", { x: 0.6, y: 1.35, w: 6.0, h: 0.35, fontSize: 18, bold: true, color: NAVY });
  txt(s, bullets([
    "Tunnels, stadiums and large buildings cannot be covered from one antenna site; radio power must be distributed over many antenna points.",
    "Radio equipment is often centralized (equipment room or base-station hotel) to share power, cooling, maintenance and multi-operator access.",
    "Question: how to carry the radio signal between the central equipment and each antenna point, over tens of metres to several kilometres, within a loss, noise, distortion and latency budget.",
  ]), { x: 0.6, y: 1.8, w: 6.0, h: 2.6, fontSize: 14 });
  txt(s, "Scope of this talk", { x: 7.0, y: 1.35, w: 5.7, h: 0.35, fontSize: 18, bold: true, color: NAVY });
  txt(s, bullets([
    ["In scope:", "the transport segment between central equipment and remote antenna units (fronthaul or DAS feeder), downlink and uplink."],
    ["Out of scope:", "backhaul to the core network, air-interface design, spectrum and radio planning."],
    ["Alternatives compared:", "passive coaxial feeder; digital fronthaul (CPRI / eCPRI)."],
  ]), { x: 7.0, y: 1.8, w: 5.7, h: 2.6, fontSize: 14 });

  // Diagram: core -> central equipment -> [transport segment] -> remote antenna points -> UE
  const y = 5.35;
  s.addShape(pres.shapes.RECTANGLE, { x: 5.35, y: 4.45, w: 3.0, h: 1.65, fill: { color: FOCUS }, line: { color: NAVY, width: 1, dashType: "dash" } });
  txt(s, "Transport segment: subject of this talk", { x: 5.35, y: 4.5, w: 3.0, h: 0.3, fontSize: 11, bold: true, color: NAVY, align: "center" });
  box(s, 0.6, y - 0.4, 1.7, 0.8, "Core network", { fs: 12 });
  link(s, 2.3, y, 3.4, y, "el");
  linkLabel(s, 2.3, 3.4, y, "Backhaul", "el");
  linkLabel(s, 2.3, 3.4, y, "digital, packet", "el", true);
  box(s, 3.4, y - 0.4, 1.95, 0.8, "Central radio equipment (base station / BBU)", { fs: 11 });
  link(s, 5.35, y, 8.35, y, "el");
  linkLabel(s, 5.35, 8.35, y, "RF, IF or digital samples", "el");
  linkLabel(s, 5.35, 8.35, y, "depends on transport option", "el", true);
  box(s, 8.35, y - 0.4, 2.0, 0.8, "Remote antenna points (× N)", { fs: 11 });
  antenna(s, 10.6, y - 0.05);
  link(s, 10.35, y - 0.05, 10.6, y - 0.05, "el", { noHead: true });
  link(s, 10.85, y - 0.35, 11.75, y - 0.35, "wl");
  linkLabel(s, 10.85, 11.75, y - 0.35, "Air interface", "wl", true);
  box(s, 11.75, y - 0.6, 0.95, 0.55, "UE", { fs: 11 });
  legend(s, 0.6, 6.45, ["el", "wl"]);
  txt(s, "Downlink direction shown; uplink is the reverse path.", { x: 7.0, y: 6.45, w: 5.7, h: 0.26, fontSize: 10, color: GREY, align: "right", valign: "middle" });
}

// ---- 3. Definition ----
{
  const s = content("Definition: what RoF transports, and what it does not",
    "Timing: 1:15 (Speaker A).\n" +
    "Logic: fix the vocabulary before any claim is made. Every later comparison depends on these distinctions.\n" +
    "Emphasize the boundary: in this talk 'RoF' means an analog waveform on the fiber. Digitized I/Q transport (CPRI) is called digital fronthaul. " +
    "ITU-T G.Suppl.55 also describes digitized variants, and some papers call CPRI-type links 'digital RoF'; we keep the terms separate to avoid attributing analog properties to digital links and vice versa.\n" +
    "The last line answers a frequent misconception: fiber capacity does not translate into wireless capacity. Users receive what the air interface delivers.", S_A);
  box(s, 0.6, 1.3, 12.1, 0.95,
    "Radio over Fiber (RoF): an optical link that carries an analog radio waveform, at RF or IF, using electrical-to-optical (E/O) conversion at one end and optical-to-electrical (O/E) conversion at the other. The radio signal is generated and demodulated outside the link.",
    { fill: LIGHT, lc: LIGHT, fs: 15, align: "left", margin: 10 });
  table(s, [
    [hc("Term"), hc("Meaning used in this talk")],
    ["RF", "Waveform at the air-interface carrier frequency; radiated after amplification and filtering."],
    ["IF", "Same modulation on a lower carrier; the remote unit needs a mixer and local oscillator (LO) to reach RF."],
    ["Baseband (I/Q)", "Complex envelope centred at 0 Hz; reaching RF needs a DAC and up-conversion. Digital fronthaul carries it as samples."],
    ["Fronthaul / backhaul", "Fronthaul: central baseband or radio site ↔ remote radio or antenna unit. Backhaul: base station ↔ core network."],
    ["Transport vs wireless capacity", "Transport: what the link carries (bit rate, or analog bandwidth and dynamic range). Wireless: user throughput, set by spectrum, SINR, MIMO layers and cell density."],
    ["Analog RoF vs digital fronthaul", "Analog waveform on fiber, versus serialized digital samples (CPRI) or packets (eCPRI). Some literature calls the latter \"digital RoF\"."],
  ], { x: 0.6, y: 2.45, w: 12.1, colW: [2.9, 9.2], fontSize: 13, rowH: 0.42 });
  txt(s, "RoF moves the point where the radio signal is radiated. It does not add spectrum or air-interface capacity.",
    { x: 0.6, y: 5.95, w: 12.1, h: 0.35, fontSize: 14, bold: true, color: NAVY });
  source(s, "Sources: ITU-T G.Suppl.55 (10/2025), Radio-over-fibre technologies and their applications; ITU-T G.9803 (2018), Radio over fibre systems; CPRI Specification V7.0 (2015); eCPRI Specification V2.0 (2019).");
}

// ---- 4. End-to-end signal path ----
{
  const s = content("End-to-end signal path: downlink and uplink",
    "Timing: 1:45 (Speaker A).\n" +
    "Walk the downlink left to right, then the uplink right to left. Stop at each conversion point.\n" +
    "Four optoelectronic conversions exist in a bidirectional link: two at each end. Each adds noise and distortion; this is why RoF link performance is not the same as fiber attenuation.\n" +
    "Square-law detection: the photodiode current is proportional to optical power, and RF power is proportional to current squared. Therefore 1 dB of optical loss costs 2 dB of RF power (Cox, 2004). " +
    "This is the correct way to translate fiber loss into the RF budget.\n" +
    "WDM is drawn as optional on purpose: a point-to-point link with two fibers is a complete RoF link. WDM only reduces fiber count when several links share a cable.\n" +
    "Downlink and uplink have different requirements: downlink is limited mainly by distortion at high drive levels; uplink by the link noise figure, because received signals are weak.", S_A);
  // zones
  box(s, 0.6, 1.35, 3.75, 3.2, "", { lc: GREY, dash: "dash" });
  txt(s, "Central site", { x: 0.7, y: 1.4, w: 3.5, h: 0.3, fontSize: 12, bold: true, color: GREY });
  box(s, 6.85, 1.35, 4.75, 3.2, "", { lc: GREY, dash: "dash" });
  txt(s, "Remote antenna unit (RAU)", { x: 6.95, y: 1.4, w: 4.5, h: 0.3, fontSize: 12, bold: true, color: GREY });
  txt(s, "Single-mode fiber, length L", { x: 4.35, y: 1.4, w: 2.5, h: 0.3, fontSize: 12, bold: true, color: NAVY, align: "center" });

  const dl = 2.35, ul = 3.85; // row centres
  txt(s, "Downlink", { x: 4.35, y: dl - 0.75, w: 2.5, h: 0.25, fontSize: 11, color: GREY, align: "center" });
  txt(s, "Uplink", { x: 4.35, y: ul + 0.42, w: 2.5, h: 0.25, fontSize: 11, color: GREY, align: "center" });
  // Downlink: RF port -> E/O -> fiber -> O/E -> amp/BPF -> PA -> duplexer
  box(s, 0.8, dl - 0.35, 1.35, 0.7, "Base-station RF port (DL out)", { fs: 11 });
  link(s, 2.15, dl, 2.65, dl, "el");
  box(s, 2.65, dl - 0.35, 1.5, 0.7, "E/O: laser (direct) or laser + MZM", { fill: EO, fs: 11, bold: true });
  link(s, 4.15, dl, 7.05, dl, "opt");
  linkLabel(s, 4.15, 7.05, dl, "intensity-modulated, λ1", "opt");
  box(s, 7.05, dl - 0.35, 1.05, 0.7, "O/E: photodiode", { fill: EO, fs: 11, bold: true });
  link(s, 8.1, dl, 8.4, dl, "el");
  box(s, 8.4, dl - 0.35, 0.95, 0.7, "Amp + BPF", { fs: 11 });
  link(s, 9.35, dl, 9.6, dl, "el");
  box(s, 9.6, dl - 0.35, 0.65, 0.7, "PA", { fs: 11 });
  link(s, 10.25, dl, 10.6, dl, "el");
  // Duplexer spans both rows
  box(s, 10.6, dl - 0.35, 0.8, ul - dl + 0.7, "Duplexer", { fs: 11 });
  link(s, 11.4, (dl + ul) / 2, 11.85, (dl + ul) / 2, "el", { noHead: true });
  antenna(s, 11.85, (dl + ul) / 2);
  link(s, 12.05, 2.3, 12.65, 2.3, "wl", { both: true });
  txt(s, "RF over the air to / from UE", { x: 11.75, y: 1.75, w: 1.0, h: 0.5, fontSize: 9, italic: true, color: WL, align: "center" });
  // Uplink: duplexer -> LNA -> E/O -> fiber -> O/E -> RF amp -> BS RF port
  link(s, 10.6, ul, 10.25, ul, "el");
  box(s, 9.6, ul - 0.35, 0.65, 0.7, "LNA", { fs: 11 });
  link(s, 9.6, ul, 8.1, ul, "el");
  box(s, 7.05, ul - 0.35, 1.05, 0.7, "E/O: laser diode", { fill: EO, fs: 11, bold: true });
  link(s, 7.05, ul, 4.15, ul, "opt");
  linkLabel(s, 4.15, 7.05, ul, "λ2 or second fiber", "opt");
  box(s, 2.65, ul - 0.35, 1.5, 0.7, "O/E: photodiode + RF amp", { fill: EO, fs: 11, bold: true });
  link(s, 2.65, ul, 2.15, ul, "el");
  box(s, 0.8, ul - 0.35, 1.35, 0.7, "Base-station RF port (UL in)", { fs: 11 });

  // Explanatory cells
  const cy = 4.8, cw = 3.85;
  [["Conversion points", "DL: E/O at central site, O/E at RAU. UL: E/O at RAU, O/E at central site. Each conversion adds noise and distortion."],
   ["Optical loss vs RF loss", "Intensity modulation with direct detection: RF power ∝ (optical power)². 1 dB optical loss → 2 dB RF loss."],
   ["Multiplexing", "DL and UL use separate fibers or wavelengths. WDM is optional; needed only when several links share one fiber."],
  ].forEach(([h, b], i) => {
    const x = 0.6 + i * (cw + 0.275);
    box(s, x, cy, cw, 1.25, "", { fill: LIGHT, lc: LIGHT });
    txt(s, [{ text: h, options: { bold: true, color: NAVY, breakLine: true } }, { text: b }],
      { x: x + 0.12, y: cy + 0.1, w: cw - 0.24, h: 1.1, fontSize: 12 });
  });
  legend(s, 0.6, 6.2);
  source(s, "Sources: C. H. Cox III, Analog Optical Links: Theory and Practice, Cambridge Univ. Press, 2004; ITU-T G.Suppl.55 (10/2025). MZM: Mach-Zehnder modulator; BPF: band-pass filter; PA: power amplifier; LNA: low-noise amplifier.");
}

// ---- 5. Architecture ----
{
  const s = content("Architecture: where the RoF link sits in the network",
    "Timing: 1:30 (Speaker A).\n" +
    "Logic: place the link in a real deployment so the audience can separate fronthaul from backhaul.\n" +
    "Backhaul is digital and packet-based; it is not affected by the choice of RoF. The RoF link is only the head-end-to-RAU segment.\n" +
    "The head-end combines RF from several operators and bands before E/O conversion. This is what makes the analog link format-transparent, within its bandwidth and dynamic range.\n" +
    "State the topology honestly: a star of point-to-point links. Fiber count can be reduced by WDM or by cascading remote units, but each option has its own cost and limits.\n" +
    "Do not describe the RAU as passive: it contains lasers, photodiodes, amplifiers and a power supply.\n" +
    "Same placement applies to centralized RAN (C-RAN): replace the head-end with a BBU pool and the RAU with an RRH; the link then carries digital fronthaul, not analog RoF.", S_A);
  // Core -> BS hotel -> head-end -> fibers -> RAUs
  box(s, 0.6, 3.3, 1.35, 0.8, "Core network", { fs: 12 });
  link(s, 1.95, 3.7, 2.55, 3.7, "el");
  linkLabel(s, 1.95, 2.55, 3.7, "Backhaul", "el");
  // BS hotel with operators
  box(s, 2.55, 2.25, 2.0, 2.9, "", { lc: GREY, dash: "dash" });
  txt(s, "Base-station hotel", { x: 2.6, y: 2.3, w: 1.9, h: 0.3, fontSize: 11, bold: true, color: GREY, align: "center" });
  ["Operator A radio", "Operator B radio", "Operator C radio"].forEach((t, i) => box(s, 2.75, 2.7 + i * 0.75, 1.6, 0.55, t, { fs: 11 }));
  [2.975, 3.725, 4.475].forEach((yy) => link(s, 4.35, yy, 5.05, yy, "el"));
  txt(s, "RF (coax)", { x: 4.35, y: 4.85, w: 0.75, h: 0.25, fontSize: 10, italic: true, color: INK, align: "center" });
  box(s, 5.05, 2.45, 1.6, 2.5, "Head-end: RF combining, E/O (DL), O/E (UL)", { fill: EO, fs: 11, bold: true });
  // fibers to RAUs
  const rau = [1.75, 3.3, 4.85];
  rau.forEach((yy, i) => {
    link(s, 6.65, 3.7, 7.85, yy + 0.35, "opt", { both: true });
    box(s, 7.85, yy, 1.35, 0.7, i === 2 ? "RAU n" : "RAU " + (i + 1), { fs: 11, dash: i === 2 ? "dash" : "solid" });
    link(s, 9.2, yy + 0.35, 9.55, yy + 0.35, "el", { noHead: true });
    antenna(s, 9.55, yy + 0.35);
    link(s, 9.75, yy + 0.1, 10.25, yy + 0.1, "wl", { both: true });
  });
  txt(s, "Fiber links: analog RF, downlink and uplink", { x: 5.05, y: 5.7, w: 4.2, h: 0.3, fontSize: 10, italic: true, color: NAVY });
  // Right panel
  txt(s, bullets([
    ["Fronthaul:", "head-end ↔ RAU. This is the RoF link."],
    ["Backhaul:", "base station ↔ core; digital, packet. Not RoF."],
    ["Topology:", "star; one fiber pair or wavelength pair per RAU. WDM or cascaded RAUs reduce fiber count."],
    ["RAU contents:", "O/E, E/O, RF amplifiers, filters, duplexer, power supply, alarms."],
    ["C-RAN variant:", "BBU pool and RRHs; the link carries digital fronthaul instead."],
  ], { gap: 8 }), { x: 10.45, y: 1.45, w: 2.3, h: 4.9, fontSize: 12 });
  legend(s, 0.6, 6.2);
  source(s, "Generic multi-operator fiber DAS / centralized radio architecture. Sources: ITU-T G.Suppl.55 (10/2025); ITU-T G.9803 (2018).");
}

// ---- 6. RoF types ----
{
  const s = content("RoF types: what is on the fiber sets what the remote unit contains",
    "Timing: 1:30 (Speaker A). Handover to Speaker B after this slide (target elapsed time ≈ 7:15).\n" +
    "Logic: the functional split decides two opposite quantities: remote-unit complexity and fiber transport requirement.\n" +
    "RFoF: simplest remote downlink chain, but the optoelectronics must operate at the carrier frequency, which becomes difficult and costly at mmWave; dispersion effects also grow with RF frequency.\n" +
    "IFoF: optoelectronics run at a lower frequency; the price is a mixer and a stable LO at every RAU.\n" +
    "Digital fronthaul: robust to fiber impairments because it is digital, but the remote unit is a full radio (RRH) and the bit rate is high. This row is not RoF in the strict sense; it is shown because it is the main alternative.\n" +
    "Analog baseband-over-fiber also appears in research literature (e.g. Electronics 9(11), 1785, 2020); it is listed in the appendix, not used in the main argument.", S_A);
  const cols = [[0.6, 1.65, "Option"], [2.35, 3.15, "Central site"], [5.6, 1.95, "Signal on fiber"], [7.65, 5.05, "Remote unit: downlink functions"]];
  cols.forEach(([x, w, t]) => box(s, x, 1.35, w, 0.4, t, { fill: HEAD, lc: HEAD, color: NAVY, bold: true, fs: 12 }));
  const rows = [
    { name: "RFoF", sub: "analog RF", c: ["Radio: DAC + up-conversion to RF", "E/O"], f: "Analog RF waveform",
      r: ["O/E", "Amp + BPF", "PA"] },
    { name: "IFoF", sub: "analog IF", c: ["Radio: DAC + up-conversion to IF", "E/O"], f: "Analog IF waveform",
      r: ["O/E", "Mixer + LO", "Amp + BPF", "PA"] },
    { name: "Digital fronthaul", sub: "CPRI; not analog RoF", c: ["BBU: PHY → I/Q samples", "Framer + optical TRx"], f: "Serial digital I/Q samples",
      r: ["Optical TRx + deframer", "DAC", "Up-conv. + LO", "PA"] },
  ];
  rows.forEach((rw, i) => {
    const y = 1.95 + i * 1.12, h = 0.8, cy = y + h / 2;
    txt(s, [{ text: rw.name, options: { bold: true, breakLine: true } }, { text: rw.sub, options: { fontSize: 10, color: GREY } }],
      { x: 0.6, y, w: 1.65, h, fontSize: 13, valign: "middle" });
    box(s, 2.35, y, 1.85, h, rw.c[0], { fs: 11 });
    link(s, 4.2, cy, 4.4, cy, "el");
    box(s, 4.4, y, 1.1, h, rw.c[1], { fill: EO, fs: 11, bold: true });
    link(s, 5.5, cy, 7.75, cy, "opt");
    linkLabel(s, 5.5, 7.75, cy, rw.f, "opt", true);
    const n = rw.r.length, bw = 0.98, gap = 0.22;
    rw.r.forEach((t, j) => {
      const x = 7.75 + j * (bw + gap);
      box(s, x, y, bw, h, t, { fill: j === 0 ? EO : "FFFFFF", bold: j === 0, fs: 11 });
      if (j < n - 1) link(s, x + bw, cy, x + bw + gap, cy, "el");
    });
    const endX = 7.75 + n * bw + (n - 1) * gap;
    link(s, endX, cy, endX + 0.2, cy, "el", { noHead: true });
    antenna(s, endX + 0.2, cy);
  });
  // Trend arrows / summary
  box(s, 0.6, 5.35, 6.0, 0.95, "", { fill: LIGHT, lc: LIGHT });
  txt(s, [{ text: "Remote-unit complexity ", options: { bold: true, color: NAVY } },
    { text: "increases from RFoF to digital fronthaul (frequency conversion, then DAC/ADC and framing)." }],
    { x: 0.72, y: 5.45, w: 5.8, h: 0.8, fontSize: 12, valign: "middle" });
  box(s, 6.7, 5.35, 6.0, 0.95, "", { fill: LIGHT, lc: LIGHT });
  txt(s, [{ text: "Fiber transport requirement ", options: { bold: true, color: NAVY } },
    { text: "increases in the opposite direction: digitized samples need far more capacity than the analog waveform (slide 8)." }],
    { x: 6.82, y: 5.45, w: 5.8, h: 0.8, fontSize: 12, valign: "middle" });
  legend(s, 0.6, 6.4, ["el", "opt"]);
  txt(s, "Uplink chains (LNA, E/O at remote; O/E at central) omitted for clarity.", { x: 6.7, y: 6.4, w: 6.0, h: 0.26, fontSize: 10, color: GREY, align: "right", valign: "middle" });
}

// =====================================================================
// SECTION: Speaker B
// =====================================================================
pres.addSection({ title: S_B });

// ---- 7. Comparison 1: coax vs RFoF ----
{
  const s = content("Comparison 1: passive coaxial feeder vs analog RFoF link",
    "Timing: 1:45 (Speaker B).\n" +
    "Logic: replace the original 'fiber loses 0.2 dB/km, coax loses 22 dB/100 m' argument, which compared a cable with a cable and ignored the conversion loss of the RoF link.\n" +
    "Model: coax loss = 0.222 dB/m × L. RoF RF loss = Lc + 2 × 0.25 dB/km × L. The factor 2 is square-law detection.\n" +
    "Lc (RF-to-RF conversion loss of an unamplified link) is device-specific. The 20–40 dB range is an assumption for illustration and must be replaced with the datasheet value of the equipment under evaluation. " +
    "Cox (2004) treats link gain in detail; do not quote a single number without the device parameters.\n" +
    "Break-even L* = Lc / (0.222 − 0.0005) ≈ 90 m for 20 dB and ≈ 180 m for 40 dB.\n" +
    "Key message: loss alone does not decide. Commercial fiber DAS units include RF gain at both ends, so the decisive metrics are noise figure (uplink), dynamic range (multi-carrier downlink) and power consumption.", S_B);
  table(s, [
    [hc("Item"), hc("Definition")],
    ["Systems", "(1) Passive coax, LMR-400 class, 50 Ω. (2) Analog RFoF link, no RF amplifiers."],
    ["Endpoints", "Head-end RF output port → remote antenna port (downlink)"],
    ["Signal", "RF passband at 2.5 GHz"],
    ["Medium", "Coax; G.652.D single-mode fiber at 1550 nm"],
    ["Criterion", "RF-to-RF insertion loss versus length"],
    ["Assumptions", "Coax 22.2 dB/100 m. Fiber 0.25 dB/km optical = 0.5 dB/km RF. RoF conversion loss Lc = 20–40 dB (assumed)."],
  ], { x: 0.6, y: 1.35, w: 5.0, colW: [1.25, 3.75], fontSize: 12 });
  const L = [0, 50, 100, 150, 200, 250, 300, 350, 400];
  const r1 = (v) => Math.round(v * 10) / 10;
  s.addChart(pres.charts.LINE, [
    { name: "Coax, LMR-400 class", labels: L.map(String), values: L.map((l) => r1(0.222 * l)) },
    { name: "RFoF, Lc = 20 dB (assumed)", labels: L.map(String), values: L.map((l) => r1(20 + 0.0005 * l)) },
    { name: "RFoF, Lc = 40 dB (assumed)", labels: L.map(String), values: L.map((l) => r1(40 + 0.0005 * l)) },
  ], {
    x: 5.9, y: 1.3, w: 6.8, h: 3.75,
    chartColors: ["1A1A1A", "1F3A5F", "7C93B5"], lineSize: 2, lineDataSymbol: "none",
    showLegend: true, legendPos: "b", legendFontSize: 11, legendFontFace: FONT, legendColor: "1A1A1A",
    showTitle: true, title: "RF-to-RF loss vs length at 2.5 GHz (downlink, unamplified)", titleFontSize: 12, titleFontFace: FONT, titleColor: "1F3A5F",
    catAxisTitle: "Link length (m)", showCatAxisTitle: true, catAxisTitleFontSize: 11, catAxisTitleColor: "5F6670",
    valAxisTitle: "RF loss (dB)", showValAxisTitle: true, valAxisTitleFontSize: 11, valAxisTitleColor: "5F6670",
    catAxisLabelFontSize: 10, valAxisLabelFontSize: 10, catAxisLabelColor: "5F6670", valAxisLabelColor: "5F6670",
    catAxisLabelFontFace: FONT, valAxisLabelFontFace: FONT,
    valAxisMinVal: 0, valAxisMaxVal: 90, valAxisMajorUnit: 10,
    valGridLine: { color: "E3E7ED", size: 0.5 }, catGridLine: { style: "none" },
  });
  box(s, 0.6, 5.25, 12.1, 1.1, "", { fill: LIGHT, lc: LIGHT });
  txt(s, [
    { text: "Result under these assumptions: ", options: { bold: true, color: NAVY } },
    { text: "break-even length L* = Lc / (0.222 − 0.0005 dB/m) ≈ 90 m (Lc = 20 dB) to 180 m (Lc = 40 dB). Below L*, passive coax has lower RF loss; above L*, RFoF does. " },
    { text: "Practical fiber DAS equipment adds RF gain at both ends, so the deciding metrics become noise figure, dynamic range and power consumption, not loss alone." },
  ], { x: 0.75, y: 5.32, w: 11.8, h: 0.98, fontSize: 13, valign: "middle" });
  source(s, "Coax: Times Microwave LMR-400 datasheet, 22.2 dB/100 m at 2500 MHz. Fiber: G.652.D cable datasheets, ≤ 0.22–0.25 dB/km at 1550 nm. Lc range is an assumption: verify against the datasheet of the equipment under evaluation.");
}

// ---- 8. Comparison 2: A-RoF vs digital fronthaul ----
{
  const s = content("Comparison 2: analog RoF vs digital fronthaul (CPRI)",
    "Timing: 1:30 (Speaker B).\n" +
    "Logic: this is the comparison that matters for mobile networks, because digital fronthaul is the incumbent for C-RAN.\n" +
    "CPRI rate, worked: 20 MHz LTE uses 30.72 Msample/s. 30.72 × 2 (I and Q) × 15 bits × 16/15 (control words) × 10/8 (8B/10B line code) = 1228.8 Mb/s, which is CPRI line-rate option 2.\n" +
    "Scaling example (computed with the same formula, no compression, before line coding): 100 MHz NR at 122.88 Msample/s gives 3.93 Gb/s per antenna; 64 antennas give about 252 Gb/s. This scaling is the argument for analog transport or for eCPRI splits.\n" +
    "Fairness: digital fronthaul quality is set by quantization and is independent of fiber length until bit errors appear; analog quality degrades along the link. Analog links also lack bit-level monitoring.\n" +
    "Li et al. (2021) report a modeled case in which A-RoF needs much less fiber bandwidth but exceeds the 3GPP EVM limit for 256-QAM; see appendix A6. Those figures are scenario-specific.", S_B);
  txt(s, "Systems: analog RFoF / IFoF vs CPRI-type digital fronthaul · Endpoints: central site ↔ remote unit · Medium: single-mode fiber · Assumption: same radio carrier and antenna count",
    { x: 0.6, y: 1.3, w: 12.1, h: 0.45, fontSize: 12, color: GREY, italic: true });
  table(s, [
    [hc("Criterion"), hc("Analog RoF (RFoF / IFoF)"), hc("Digital fronthaul (CPRI)")],
    ["Signal on fiber", "Analog RF or IF waveform", "Serialized time-domain I/Q samples (CPRI); packets (eCPRI)"],
    ["Transport requirement", "Analog bandwidth ≈ radio channel bandwidth per antenna stream, plus required dynamic range",
      "Bit rate = sample rate × 2 × bits per sample × overheads. 20 MHz LTE, 1 antenna: 1228.8 Mb/s (CPRI option 2)"],
    ["Scaling", "One RF / IF channel (subcarrier or wavelength) per antenna stream",
      "Linear in antenna count and sample rate. 100 MHz, 64 antennas ≈ 252 Gb/s before line coding (computed)"],
    ["Remote unit", "O/E, E/O, amplifiers, filters (+ mixer and LO for IFoF)", "DAC / ADC, framing, up / down-conversion, LO, amplifiers (RRH)"],
    ["Dominant impairments", "Noise, nonlinear distortion, dispersion-induced RF power fading; accumulate along the link",
      "Quantization noise, fixed by bit width; independent of length while bit errors are negligible"],
    ["Monitoring and interoperability", "No native bit-level monitoring; largely vendor-specific. ITU-T G.9803 sets system requirements",
      "Bit-level monitoring; CPRI / eCPRI specifications; O-RAN split 7.2x for multi-vendor"],
    ["Added latency", "Fiber propagation ≈ 5 µs/km; no sampling or framing", "Fiber propagation ≈ 5 µs/km + framing and buffering (implementation-specific)"],
  ], { x: 0.6, y: 1.8, w: 12.1, colW: [2.3, 4.7, 5.1], fontSize: 13, rowH: 0.56 });
  source(s, "Sources: CPRI Specification V7.0 (2015); eCPRI Specification V2.0 (2019); ITU-T G.9803 (2018) and Amd. 2 (2022); Y. Li et al., arXiv:2111.13851 (2021). Propagation delay from group index ≈ 1.47. eCPRI split 7.2x rate scales with MIMO layers and load, not antenna count.");
}

// ---- 9. Benefits and conditions ----
{
  const s = content("Benefits, and the conditions under which they hold",
    "Timing: 1:00 (Speaker B).\n" +
    "Logic: each benefit is stated with its condition and with what it does not imply. This directly corrects the original slides, which attributed fiber properties to the whole RoF system.\n" +
    "Row 1 connects to slide 7: low fiber attenuation helps only once the link is longer than the break-even length.\n" +
    "Row 3: centralization is real, but the RAU still has active optoelectronics and needs power. 'Simple RAU' is true only relative to an RRH, and only for RFoF.\n" +
    "Row 4: transparency is the main practical reason fiber DAS is used for multi-operator venues. All carriers share one link's dynamic range, so adding carriers reduces per-carrier headroom.\n" +
    "Row 5: cost is site-specific. No general cost claim is made; it requires a bill of materials for a given site.", S_B);
  table(s, [
    [hc("Benefit"), hc("Holds when"), hc("Does not imply")],
    ["Low fiber attenuation (≈ 0.2–0.25 dB/km cabled SMF at 1550 nm)", "Link is longer than the break-even length set by conversion loss (slide 7)", "Low RF-to-RF loss for short links; conversion loss is fixed"],
    ["Fiber span immune to electromagnetic pickup; galvanic isolation", "Dielectric cable is used", "Immunity of RAU electronics or of the air interface"],
    ["Centralized radio equipment (base-station hotel, multi-operator)", "RFoF or IFoF; head-end hosts all baseband and radio processing", "No remote power or maintenance: RAU has lasers, amplifiers, power supply"],
    ["Format transparency: multi-band, multi-operator, multi-technology on one link", "Within optoelectronic bandwidth, linearity and dynamic range", "Any number of bands: all carriers share one link's dynamic range"],
    ["Small, light cable", "Compared with coax of similar loss over the same route", "Lower total installed cost: site-specific, not established here"],
    ["Low added transport latency (≈ 5 µs/km, no sampling or framing)", "Analog link", "Lower end-to-end RAN latency, which baseband processing dominates"],
  ], { x: 0.6, y: 1.35, w: 12.1, colW: [4.1, 4.0, 4.0], fontSize: 14, rowH: 0.7 });
  source(s, "Sources: G.652.D cable datasheets (attenuation); ITU-T G.Suppl.55 (10/2025); C. H. Cox III, Analog Optical Links, 2004.");
}

// ---- 10. Limitations and trade-offs ----
{
  const s = content("Limitations and engineering trade-offs",
    "Timing: 1:15 (Speaker B).\n" +
    "Logic: the limitations are physical mechanisms, not general disadvantages.\n" +
    "Noise vs distortion is the central analog trade-off. The figure is the standard spurious-free dynamic range construction: the fundamental rises 1 dB per dB of input, third-order intermodulation rises 3 dB per dB. " +
    "SFDR is the input range between the noise floor and the point where IMD3 reaches the noise floor. It is illustrative and has no values.\n" +
    "Dispersion: with double-sideband intensity modulation, the two optical sidebands experience different phase shifts in a dispersive fiber; after detection they interfere and the RF power fades at specific frequency-length combinations (Gliese et al., 1996). " +
    "This is a design constraint at mmWave on 1550 nm, not a reason to avoid RoF at sub-6 GHz over short indoor runs.\n" +
    "Remote power is often underestimated in venue projects; hybrid fiber-copper cables are one documented solution (slide 11).", S_B);
  txt(s, bullets([
    ["Noise and dynamic range:", "laser RIN, shot noise and receiver thermal noise set a noise floor; the link noise figure limits uplink sensitivity and the number of carriers per link."],
    ["Nonlinear distortion:", "laser and modulator nonlinearity creates intermodulation; higher drive improves SNR until distortion dominates (SFDR)."],
    ["Chromatic dispersion:", "with double-sideband intensity modulation, RF power fades at frequency- and length-dependent nulls. Mitigation: 1310 nm, single-sideband modulation, IFoF."],
    ["Fiber and topology:", "one fiber pair or wavelength pair per RAU; new fiber needs civil works and permits."],
    ["Remote power:", "RAU lasers and amplifiers need local power or hybrid fiber–copper cable."],
    ["Operations:", "no bit-level performance monitoring on the analog link; interfaces largely vendor-specific."],
  ], { gap: 9 }), { x: 0.6, y: 1.35, w: 7.2, h: 5.0, fontSize: 14 });
  // SFDR construction
  const X = (u) => 8.55 + u * 0.4, Y = (v) => 5.35 - v * 0.36;
  box(s, 8.2, 1.3, 4.5, 4.75, "", { fill: "FFFFFF", lc: BORDER });
  txt(s, "Noise vs distortion: SFDR (illustrative, no values)", { x: 8.3, y: 1.35, w: 4.3, h: 0.3, fontSize: 11, bold: true, color: NAVY, align: "center" });
  s.addShape(pres.shapes.LINE, { x: X(0), y: Y(9.5), w: 0, h: Y(0) - Y(9.5), line: { color: GREY, width: 1, endArrowType: "none", beginArrowType: "triangle" } });
  s.addShape(pres.shapes.LINE, { x: X(0), y: Y(0), w: X(9.8) - X(0), h: 0, line: { color: GREY, width: 1, endArrowType: "triangle" } });
  const seg = (u1, v1, u2, v2, line) => s.addShape(pres.shapes.LINE, { x: X(u1), y: Y(v2), w: X(u2) - X(u1), h: Y(v1) - Y(v2), flipV: true, line });
  seg(0, 1, 8.5, 9.5, { color: NAVY, width: 2 });                 // fundamental, slope 1
  seg(5, 0, 8.3, 9.9, { color: "8C3B32", width: 2 });             // IMD3, slope 3
  s.addShape(pres.shapes.LINE, { x: X(0), y: Y(2), w: X(9.5) - X(0), h: 0, line: { color: GREY, width: 1.25, dashType: "dash" } });
  const u0 = 17 / 3; // IMD3 meets noise floor
  s.addShape(pres.shapes.LINE, { x: X(u0), y: Y(u0 + 1), w: 0, h: Y(2) - Y(u0 + 1), line: { color: INK, width: 1, beginArrowType: "triangle", endArrowType: "triangle" } });
  txt(s, "SFDR", { x: X(u0) - 0.75, y: Y(4.6), w: 0.7, h: 0.25, fontSize: 11, bold: true, align: "right" });
  txt(s, "Fundamental (slope 1)", { x: X(0.15), y: Y(4.9), w: 1.8, h: 0.25, fontSize: 10, color: NAVY });
  txt(s, "IMD3 (slope 3)", { x: X(7.35), y: Y(4.3), w: 1.3, h: 0.25, fontSize: 10, color: "8C3B32" });
  txt(s, "Noise floor", { x: X(7.3), y: Y(2) + 0.04, w: 1.4, h: 0.25, fontSize: 10, color: GREY });
  txt(s, "RF input power (dB)", { x: X(2), y: Y(0) + 0.08, w: 2.6, h: 0.25, fontSize: 10, color: GREY, align: "center" });
  txt(s, "RF output (dB)", { x: 8.3, y: 1.7, w: 1.4, h: 0.25, fontSize: 10, color: GREY });
  source(s, "Sources: C. H. Cox III, Analog Optical Links, 2004; U. Gliese et al., IEEE Trans. Microwave Theory Tech. 44(10), 1996 (dispersion-induced RF power fading); D. Wake et al., J. Lightwave Technol. 28(16), 2010.");
}

// ---- 11. Application case ----
{
  const s = content("Documented case: Maracanã and Mineirão stadiums (2014)",
    "Timing: 1:00 (Speaker B).\n" +
    "Logic: one documented deployment, with a clear statement of what the sources do and do not show.\n" +
    "Facts as reported by the vendors: Axell Wireless (June 2014) supplied optical DAS for venues including Maracanã and Mineirão, combined capacity over 141,000, five operators, 2G/3G/4G. " +
    "RFS (10 June 2014) reported its HYBRIFLEX hybrid fiber and DC power cable at Maracanã, feeding remote radio units, for 2G, 3G, 4G and iDEN.\n" +
    "The PBE Axell case study cited in the original deck names Optical Master Units converting RF to optical; that page could not be retrieved during this review, so treat equipment model names as requiring verification.\n" +
    "Do not claim performance from this case. The sources are vendor press releases; they contain no link budgets, noise figures or capacity measurements. " +
    "They also do not state whether every subsystem used analog RF transport or digital fronthaul to the remote radios.", S_B);
  const y0 = 2.0;
  box(s, 0.6, y0, 1.9, 1.5, "Base-station hotel: 5 operators, 2G / 3G / 4G", { fs: 11 });
  link(s, 2.5, y0 + 0.75, 3.2, y0 + 0.75, "el");
  linkLabel(s, 2.5, 3.2, y0 + 0.75, "RF", "el");
  box(s, 3.2, y0, 1.7, 1.5, "Optical master units: RF ↔ optical", { fill: EO, fs: 11, bold: true });
  [y0 + 0.1, y0 + 0.75, y0 + 1.4].forEach((yy, i) => {
    const ty = 1.45 + i * 0.85;
    link(s, 4.9, y0 + 0.75, 6.1, ty + 0.3, "opt", { both: true });
    box(s, 6.1, ty, 1.5, 0.6, "Fiber-fed remote unit", { fs: 10 });
    link(s, 7.6, ty + 0.3, 7.85, ty + 0.3, "el", { noHead: true });
    antenna(s, 7.85, ty + 0.3);
  });
  txt(s, "Fiber (hybrid fiber + DC power cable at Maracanã)", { x: 3.2, y: 3.75, w: 3.0, h: 0.5, fontSize: 10, italic: true, color: NAVY });
  txt(s, "Stands, concourses, public areas", { x: 6.0, y: 4.05, w: 2.3, h: 0.3, fontSize: 10, italic: true, color: WL });
  legend(s, 0.6, 4.6, ["el", "opt"]);

  txt(s, "Reported", { x: 8.6, y: 1.35, w: 4.1, h: 0.3, fontSize: 15, bold: true, color: NAVY });
  txt(s, bullets([
    "Optical DAS for five mobile operators, 2G / 3G / 4G; combined stadium capacity over 141,000 (Axell Wireless, June 2014).",
    "Maracanã: hybrid fiber + DC power cable feeding remote radio units; 2G, 3G, 4G and iDEN (RFS, 10 June 2014).",
  ], { gap: 6 }), { x: 8.6, y: 1.7, w: 4.1, h: 2.1, fontSize: 12 });
  txt(s, "Not reported", { x: 8.6, y: 3.85, w: 4.1, h: 0.3, fontSize: 15, bold: true, color: NAVY });
  txt(s, bullets([
    "Link budgets, noise figure, measured capacity, cost against alternatives.",
    "Transport format per subsystem (analog RF or digital).",
  ], { gap: 6 }), { x: 8.6, y: 4.2, w: 4.1, h: 1.2, fontSize: 12 });
  box(s, 0.6, 5.35, 12.1, 0.85, "", { fill: LIGHT, lc: LIGHT });
  txt(s, [{ text: "What the case supports: ", options: { bold: true, color: NAVY } },
    { text: "feasibility of a multi-operator, multi-technology fiber-fed DAS in large venues. It does not support quantitative performance or cost claims." }],
    { x: 0.75, y: 5.4, w: 11.8, h: 0.75, fontSize: 13, valign: "middle" });
  source(s, "Sources: Axell Wireless press release, June 2014 (prnewswire.co.uk); RFS press release, 10 June 2014 (globenewswire.com); PBE Axell case study \"Brazilian Sports Stadiums\" (equipment names: verification required).");
}

// ---- 12. Conclusions ----
{
  const s = content("Conclusions",
    "Timing: 1:00 (Speaker B). Then open questions.\n" +
    "Logic: each conclusion is traceable to a slide. If challenged, go back to that slide.\n" +
    "Avoid generalizing beyond the evidence: the break-even length depends on the assumed conversion loss; the deployment case is evidence of feasibility only.\n" +
    "The final row is a decision checklist, not a recommendation: whether RoF is appropriate depends on the site.", S_B);
  table(s, [
    [hc("#"), hc("Conclusion"), hc("Evidence")],
    ["1", "RoF transports an existing radio signal. It does not add spectrum or air-interface capacity.", "Slide 3"],
    ["2", "Against passive coax at 2.5 GHz, unamplified RFoF has lower RF loss only beyond a break-even length set by conversion loss (≈ 90–180 m under the stated assumptions).", "Slide 7"],
    ["3", "Against digital fronthaul, analog RoF needs far less fiber capacity and no DAC/ADC at the remote unit, at the cost of noise, distortion, dispersion and weaker monitoring.", "Slides 8, 10"],
    ["4", "Documented deployments include multi-operator fiber-fed DAS in large venues; vendor sources support feasibility, not performance.", "Slide 11"],
    ["5", "Selection criteria: fiber availability, link length, number of bands and operators, required noise figure and dynamic range, remote power, monitoring needs.", "Slides 7–10"],
  ], { x: 0.6, y: 1.35, w: 12.1, colW: [0.5, 9.9, 1.7], fontSize: 14, rowH: 0.75 });
}

// ---- 13. Questions ----
{
  const s = content("Questions", "Use appendix slides A1–A8 for detailed answers. Expected questions and bounded answers are in the review report, section H.", S_B);
  txt(s, "Reference material in the appendix:", { x: 0.6, y: 1.5, w: 12.1, h: 0.4, fontSize: 16, bold: true, color: NAVY });
  txt(s, bullets([
    "A1 Glossary", "A2 Loss figures at 100 m, 1 km and 10 km", "A3 Remote antenna unit types (BBoF, IFoF, RFoF)",
    "A4 Measured BER versus carrier-to-sideband ratio", "A5 Research demonstration: 5G-NR and a candidate 6G signal on one fiber",
    "A6 Fronthaul bit-rate calculation and reported analog vs digital comparison", "A7 Standards and specifications", "A8 References",
  ], { gap: 4 }), { x: 0.6, y: 2.0, w: 12.1, h: 4.2, fontSize: 15 });
}

// =====================================================================
// SECTION: Appendix
// =====================================================================
pres.addSection({ title: S_APP });

// ---- A1 Glossary ----
{
  const s = content("A1 Glossary", "Reference only.", S_APP, "APPENDIX");
  const L = [["BBU", "Baseband unit: PHY / MAC processing at the central site"],
    ["RRH / RRU", "Remote radio head / unit: DAC/ADC, frequency conversion, PA/LNA; fed by digital fronthaul"],
    ["RAU", "Remote antenna unit of an analog RoF link: O/E, E/O, RF amplifiers, filters"],
    ["DAS", "Distributed antenna system: one signal source, many antenna points"],
    ["WDM", "Wavelength-division multiplexing: several wavelengths on one fiber"],
    ["MZM", "Mach-Zehnder modulator: external intensity modulator"],
    ["IM/DD", "Intensity modulation, direct detection"],
    ["LO", "Local oscillator, used for frequency conversion"],
    ["SMF", "Single-mode fiber (ITU-T G.652 family)"]];
  const R = [["TIA / PA / LNA", "Transimpedance / power / low-noise amplifier"],
    ["RIN", "Relative intensity noise of the laser"],
    ["SFDR", "Spurious-free dynamic range"],
    ["CSR", "Optical carrier-to-sideband power ratio"],
    ["BER", "Bit error ratio"],
    ["EVM", "Error vector magnitude; 3GPP limit for 256-QAM: 3.5 %"],
    ["CPRI", "Common Public Radio Interface: serial digital I/Q fronthaul"],
    ["eCPRI", "Packet-based fronthaul; supports intra-PHY splits"],
    ["C-RAN", "Centralized RAN: baseband pooled at a central site"]];
  table(s, [[hc("Term"), hc("Meaning")], ...L], { x: 0.6, y: 1.35, w: 5.95, colW: [1.25, 4.7], fontSize: 12 });
  table(s, [[hc("Term"), hc("Meaning")], ...R], { x: 6.75, y: 1.35, w: 5.95, colW: [1.45, 4.5], fontSize: 12 });
  source(s, "EVM limit: 3GPP TS 38.104, base-station transmitter EVM requirements.");
}

// ---- A2 Loss table ----
{
  const s = content("A2 Loss figures at 100 m, 1 km and 10 km (2.5 GHz)",
    "Corrects the original table, which compared cable loss only and omitted the RoF conversion loss Lc.\n" +
    "The coax values at 1 km and 10 km are linear extrapolations; such runs are not built with passive coax. Coax systems over such distances (e.g. HFC cable TV) use in-line amplifiers, so 'no amplifier could recover it' is not a valid statement; the valid statement is that a passive coax feeder is impractical at these lengths.", S_APP, "APPENDIX");
  table(s, [
    [hc("Length"), hc("Coax, LMR-400 class (22.2 dB/100 m)"), hc("Fiber, optical loss (0.25 dB/km)"), hc("RFoF, RF loss = Lc + 2 × optical loss")],
    ["100 m", "22.2 dB", "0.025 dB", "Lc + 0.05 dB"],
    ["1 km", "222 dB (extrapolated; not built passively)", "0.25 dB", "Lc + 0.5 dB"],
    ["10 km", "2,220 dB (extrapolated; not built passively)", "2.5 dB", "Lc + 5 dB"],
  ], { x: 0.6, y: 1.4, w: 12.1, colW: [1.4, 3.9, 3.0, 3.8], fontSize: 14, rowH: 0.55 });
  txt(s, bullets([
    "Lc: fixed RF-to-RF conversion loss of the unamplified RoF link; device-specific. Verification required against equipment datasheets.",
    "Optical-to-RF factor of 2 applies to intensity modulation with direct detection (square-law photodetection).",
    "Splice and connector losses are excluded from both columns.",
  ], { gap: 6 }), { x: 0.6, y: 4.0, w: 12.1, h: 2.0, fontSize: 14 });
  source(s, "Sources: Times Microwave LMR-400 datasheet; G.652.D cable datasheets; C. H. Cox III, Analog Optical Links, 2004.");
}

// ---- A3 RAU types ----
{
  const s = content("A3 Remote antenna unit types: BBoF, IFoF, RFoF",
    "Redrawn from Electronics 9(11), 1785 (2020), Fig. 3, with downlink and uplink chains separated.\n" +
    "In this figure, BBoF denotes analog baseband over fiber: the RAU needs a modulator, mixer and LO. This differs from digital fronthaul, which carries sampled baseband.\n" +
    "RFoF has no frequency conversion at the RAU but still contains a photodiode, TIA, PA, LNA and a laser diode, plus power supply.", S_APP, "APPENDIX");
  const rows = [
    ["BBoF", "Baseband", ["PD", "TIA", "MOD", "Mixer + LO", "PA"], ["LD", "DEMOD", "Mixer + LO", "LNA"]],
    ["IFoF", "IF", ["PD", "TIA", "Mixer + LO", "PA"], ["LD", "Mixer + LO", "LNA"]],
    ["RFoF", "RF", ["PD", "TIA", "PA"], ["LD", "LNA"]],
  ];
  txt(s, "Downlink: fiber → antenna", { x: 2.6, y: 1.35, w: 4.9, h: 0.3, fontSize: 12, bold: true, color: NAVY, align: "center" });
  txt(s, "Uplink: antenna → fiber", { x: 7.8, y: 1.35, w: 4.9, h: 0.3, fontSize: 12, bold: true, color: NAVY, align: "center" });
  rows.forEach(([n, sig, dlc, ulc], i) => {
    const y = 1.8 + i * 1.45, h = 0.6, cy = y + h / 2;
    txt(s, [{ text: n, options: { bold: true, breakLine: true } }, { text: "On fiber: " + sig, options: { fontSize: 10, color: GREY } }],
      { x: 0.6, y, w: 1.8, h, fontSize: 14, valign: "middle" });
    const bw = 0.82, g = 0.2;
    dlc.forEach((t, j) => {
      const x = 2.6 + j * (bw + g);
      box(s, x, y, bw, h, t, { fill: j === 0 ? EO : "FFFFFF", bold: j === 0, fs: 10 });
      if (j < dlc.length - 1) link(s, x + bw, cy, x + bw + g, cy, "el");
    });
    // uplink drawn left (fiber side) to right with arrows pointing toward fiber
    const ulr = ulc.slice();
    ulr.forEach((t, j) => {
      const x = 7.8 + j * (bw + g);
      box(s, x, y, bw, h, t, { fill: j === 0 ? EO : "FFFFFF", bold: j === 0, fs: 10 });
      if (j < ulr.length - 1) link(s, x + bw + g, cy, x + bw, cy, "el");
    });
    if (i < 2) s.addShape(pres.shapes.LINE, { x: 0.6, y: y + 1.05, w: 12.1, h: 0, line: { color: "E3E7ED", width: 0.75 } });
  });
  txt(s, "PD: photodiode · TIA: transimpedance amplifier · MOD / DEMOD: modulator / demodulator · LO: local oscillator · PA: power amplifier · LNA: low-noise amplifier · LD: laser diode. Shaded blocks are O/E (downlink) and E/O (uplink).",
    { x: 0.6, y: 6.0, w: 12.1, h: 0.45, fontSize: 11, color: GREY });
  source(s, "Redrawn from: \"Radio over Fiber: An Alternative Broadband Network Technology for IoT,\" Electronics 9(11), 1785 (2020), Fig. 3. DOI: 10.3390/electronics9111785.");
}

// ---- A4 CSR vs BER ----
{
  const s = content("A4 Measured BER versus carrier-to-sideband ratio (one experimental link)",
    "Values are approximate readings from the published plot, carried over from the original deck. They were not re-checked against the paper during this review: verification required.\n" +
    "Interpretation: at low CSR the optical sidebands are strong relative to the carrier and distortion dominates; at high CSR most optical power is in the unmodulated carrier and the detected signal is weak relative to noise. " +
    "The optimum is specific to the tested link (10 km SMF plus 3 m wireless).\n" +
    "Note that −log10(BER) ≈ 2 corresponds to BER ≈ 1e-2, above common hard-decision FEC thresholds (≈ 3.8e-3).", S_APP, "APPENDIX");
  s.addChart(pres.charts.LINE, [
    { name: "−log10(BER)", labels: ["0", "5", "10", "15", "20", "25", "30"], values: [2.0, 3.0, 3.5, 3.5, 4.3, 4.4, 3.3] },
  ], {
    x: 0.6, y: 1.35, w: 7.4, h: 4.9, chartColors: ["1F3A5F"], lineSize: 2, lineDataSymbol: "circle", lineDataSymbolSize: 7,
    showLegend: false, showValue: true, dataLabelPosition: "t", dataLabelFormatCode: "0.0", dataLabelFontSize: 10, dataLabelColor: "1A1A1A", dataLabelFontFace: FONT,
    showTitle: true, title: "Higher value = lower BER", titleFontSize: 12, titleFontFace: FONT, titleColor: "1F3A5F",
    catAxisTitle: "CSR (dB)", showCatAxisTitle: true, catAxisTitleFontSize: 11, catAxisTitleColor: "5F6670",
    valAxisTitle: "−log10(BER)", showValAxisTitle: true, valAxisTitleFontSize: 11, valAxisTitleColor: "5F6670",
    catAxisLabelFontSize: 10, valAxisLabelFontSize: 10, catAxisLabelColor: "5F6670", valAxisLabelColor: "5F6670",
    catAxisLabelFontFace: FONT, valAxisLabelFontFace: FONT,
    valAxisMinVal: 0, valAxisMaxVal: 5, valAxisMajorUnit: 1, valGridLine: { color: "E3E7ED", size: 0.5 }, catGridLine: { style: "none" },
  });
  txt(s, bullets([
    ["Setup:", "10 km SMF plus 3 m wireless link (as reported)."],
    ["Trend:", "BER improves up to CSR ≈ 25 dB, then degrades at 30 dB."],
    ["Mechanism:", "distortion dominates at low CSR; noise dominates at high CSR."],
    ["Limit:", "result applies to the tested link only."],
    ["Status:", "values read from the published plot; verification required."],
  ], { gap: 8 }), { x: 8.3, y: 1.5, w: 4.4, h: 4.6, fontSize: 13 });
  source(s, "Redrawn from: M. U. Hadi and G. Murtaza, \"Fibre Wireless Distributed Antenna Systems for 5G and 6G Services,\" Electronics 12(1), 64 (2023), Fig. 6. DOI: 10.3390/electronics12010064.");
}

// ---- A5 5G + 6G demo ----
{
  const s = content("A5 Research demonstration: 5G-NR and a candidate 6G signal on one fiber",
    "Laboratory demonstration, not a deployed system. '6G' is the authors' label for a candidate THz signal.\n" +
    "Mechanism of the 6G branch: the IF2 signal is carried on the optical sideband; a second laser at λ2 is combined, and a uni-travelling-carrier photodiode (UTC-PD) mixes the two optical tones so that the beat frequency falls in the THz range (photonic up-conversion).\n" +
    "Block names follow the published figure.", S_APP, "APPENDIX");
  // Inputs
  box(s, 0.6, 1.7, 1.9, 0.8, "5G-NR: 5 × 50 MHz at IF1 = 1.14 GHz", { fs: 11 });
  box(s, 0.6, 2.9, 1.9, 0.8, "Candidate 6G at IF2 = 12 GHz", { fs: 11 });
  link(s, 2.5, 2.1, 2.9, 2.55, "el"); link(s, 2.5, 3.3, 2.9, 2.75, "el");
  box(s, 2.9, 2.25, 1.2, 0.8, "Tx (E/O)", { fill: EO, fs: 11, bold: true });
  link(s, 4.1, 2.65, 5.4, 2.65, "opt");
  linkLabel(s, 4.1, 5.4, 2.65, "fiber", "opt");
  box(s, 5.4, 2.25, 1.3, 0.8, "Optical coupler", { fs: 11 });
  // 5G branch
  link(s, 6.7, 2.45, 7.3, 1.8, "opt");
  box(s, 7.3, 1.45, 1.4, 0.7, "PIN photodiode (O/E)", { fill: EO, fs: 10, bold: true });
  link(s, 8.7, 1.8, 9.1, 1.8, "el");
  box(s, 9.1, 1.45, 0.9, 0.7, "LPF", { fs: 11 });
  link(s, 10.0, 1.8, 10.4, 1.8, "el");
  box(s, 10.4, 1.45, 2.3, 0.7, "5G RAU (antenna side)", { fs: 11 });
  // 6G branch
  link(s, 6.7, 2.85, 7.3, 3.8, "opt");
  box(s, 7.3, 3.45, 0.9, 0.7, "BPF (optical)", { fs: 10 });
  link(s, 8.2, 3.8, 8.6, 3.8, "opt");
  box(s, 8.6, 3.45, 1.2, 0.7, "Optical coupler", { fs: 10 });
  box(s, 8.6, 4.6, 1.2, 0.6, "Laser λ2", { fill: EO, fs: 10, bold: true });
  link(s, 9.2, 4.6, 9.2, 4.15, "opt");
  link(s, 9.8, 3.8, 10.2, 3.8, "opt");
  box(s, 10.2, 3.45, 1.0, 0.7, "UTC-PD (O/E)", { fill: EO, fs: 10, bold: true });
  link(s, 11.2, 3.8, 11.5, 3.8, "el");
  box(s, 11.5, 3.45, 1.2, 0.7, "6G RAU: THz output (f_THz)", { fs: 10 });
  txt(s, "Beat of λ1 sideband and λ2 → f_THz", { x: 9.9, y: 4.25, w: 2.8, h: 0.3, fontSize: 10, italic: true, color: GREY });
  legend(s, 0.6, 5.5, ["el", "opt"]);
  txt(s, "Research demonstration of simultaneous transport. No deployment, cost or capacity conclusion follows from it.",
    { x: 0.6, y: 5.9, w: 12.1, h: 0.35, fontSize: 13, bold: true, color: NAVY });
  source(s, "Redrawn and simplified from: M. U. Hadi and G. Murtaza, Electronics 12(1), 64 (2023), Fig. 2. DOI: 10.3390/electronics12010064.");
}

// ---- A6 Fronthaul rate ----
{
  const s = content("A6 Fronthaul bit-rate calculation and reported analog vs digital comparison",
    "The CPRI calculation uses the specification's sample rates and overheads; check figures before quoting a different configuration.\n" +
    "Li et al. figures were carried over from the original deck; the arXiv full text could not be retrieved during this review. Verify the 40× and 8 % values against the paper before presenting them.", S_APP, "APPENDIX");
  txt(s, "CPRI-type rate per antenna-carrier", { x: 0.6, y: 1.35, w: 6, h: 0.35, fontSize: 16, bold: true, color: NAVY });
  box(s, 0.6, 1.8, 12.1, 0.6, "R = fs × 2 (I, Q) × N bits × 16/15 (control words) × line-code factor (10/8 for 8B/10B)", { fill: LIGHT, lc: LIGHT, fs: 15 });
  table(s, [
    [hc("Case"), hc("fs"), hc("N"), hc("Antennas"), hc("Result")],
    ["LTE 20 MHz", "30.72 Msample/s", "15", "1", "1228.8 Mb/s with 8B/10B (CPRI option 2)"],
    ["NR 100 MHz", "122.88 Msample/s", "15", "1", "3.93 Gb/s before line coding"],
    ["NR 100 MHz", "122.88 Msample/s", "15", "64", "≈ 252 Gb/s before line coding"],
  ], { x: 0.6, y: 2.6, w: 12.1, colW: [1.9, 2.1, 0.8, 1.3, 6.0], fontSize: 13 });
  txt(s, "Reported modeled comparison (Li et al., 2021)", { x: 0.6, y: 4.35, w: 12, h: 0.35, fontSize: 16, bold: true, color: NAVY });
  txt(s, bullets([
    "Up to 40× lower fiber bandwidth for analog RoF than digital RoF in one modeled case: 16 × 16 MIMO, 28 GHz carrier, 256-QAM.",
    "In a modeled 256-QAM case, analog RoF EVM ≈ 8 % against the 3.5 % 3GPP limit; the digital case met the limit.",
    "Both results are scenario-specific. Values carried over from the original deck: verification against the paper required.",
  ], { gap: 5 }), { x: 0.6, y: 4.75, w: 12.1, h: 1.6, fontSize: 13 });
  source(s, "Sources: CPRI Specification V7.0 (2015); 3GPP TS 38.104; Y. Li, Q. Xie, M. El-Hajjar, L. Hanzo, \"Analogue Radio Over Fiber for Next-Generation RAN: Challenges and Opportunities,\" arXiv:2111.13851 (2021).");
}

// ---- A7 Standards ----
{
  const s = content("A7 Standards and specifications", "Reference only. CPRI and eCPRI are industry specifications, not ITU-T standards.", S_APP, "APPENDIX");
  table(s, [
    [hc("Document"), hc("Body"), hc("Scope relevant to this talk")],
    ["G.9803 (2018), Amd. 1 (2019), Amd. 2 (2022)", "ITU-T", "Radio over fibre systems: system requirements; Amd. 2 covers RoF architectures and requirements for IMT-2020 mobile fronthaul"],
    ["G.Suppl.55 (10/2025)", "ITU-T", "Radio-over-fibre technologies and their applications; earlier editions 07/2015, 12/2021, 12/2023"],
    ["G.652", "ITU-T", "Characteristics of standard single-mode optical fibre and cable"],
    ["CPRI Specification V7.0 (2015)", "CPRI industry consortium", "Serial digital I/Q interface between baseband and radio equipment"],
    ["eCPRI Specification V2.0 (2019)", "CPRI industry consortium", "Packet-based fronthaul with intra-PHY functional splits"],
    ["O-RAN fronthaul (split 7.2x)", "O-RAN Alliance", "Multi-vendor control, user and synchronization plane specification"],
    ["TS 38.104", "3GPP", "NR base-station RF requirements, including transmitter EVM limits"],
  ], { x: 0.6, y: 1.35, w: 12.1, colW: [3.6, 2.2, 6.3], fontSize: 13 });
  source(s, "Edition dates of G.Suppl.55 from the ITU-T recommendation page. Amendment content of G.9803 as cited in the original deck: verification against ITU-T text recommended.");
}

// ---- A8 References ----
{
  const s = content("A8 References", "The SolFinder Research video used in the original deck is a secondary source; it is not cited for any technical claim in this revision.", S_APP, "APPENDIX");
  const refs = [
    "C. H. Cox III, Analog Optical Links: Theory and Practice, Cambridge University Press, 2004.",
    "U. Gliese, S. Nørskov, T. N. Nielsen, \"Chromatic dispersion in fiber-optic microwave and millimeter-wave links,\" IEEE Trans. Microwave Theory Tech., 44(10), 1996.",
    "D. Wake, A. Nkansah, N. J. Gomes, \"Radio over fiber link design for next generation wireless systems,\" J. Lightwave Technol., 28(16), 2010.",
    "ITU-T G.9803 (2018), Radio over fibre systems; Amendment 1 (2019); Amendment 2 (2022).",
    "ITU-T G-series Supplement 55 (10/2025), Radio-over-fibre (RoF) technologies and their applications.",
    "ITU-T G.652, Characteristics of a single-mode optical fibre and cable.",
    "CPRI Specification V7.0 (2015); eCPRI Specification V2.0 (2019).",
    "3GPP TS 38.104, NR; Base Station (BS) radio transmission and reception.",
    "Y. Li, Q. Xie, M. El-Hajjar, L. Hanzo, \"Analogue Radio Over Fiber for Next-Generation RAN: Challenges and Opportunities,\" arXiv:2111.13851, 2021.",
    "\"Radio over Fiber: An Alternative Broadband Network Technology for IoT,\" Electronics 9(11), 1785, 2020. DOI: 10.3390/electronics9111785.",
    "M. U. Hadi, G. Murtaza, \"Fibre Wireless Distributed Antenna Systems for 5G and 6G Services,\" Electronics 12(1), 64, 2023. DOI: 10.3390/electronics12010064.",
    "Times Microwave Systems, LMR-400 coaxial cable datasheet.",
    "Axell Wireless press release on Brazilian stadium coverage, June 2014; RFS press release on Maracanã, 10 June 2014; PBE Axell case study \"Brazilian Sports Stadiums\".",
  ];
  txt(s, refs.map((r, i) => ({ text: r, options: { bullet: { type: "number" }, paraSpaceAfter: 3, breakLine: i < refs.length - 1 } })),
    { x: 0.6, y: 1.3, w: 12.1, h: 5.55, fontSize: 13 });
}

pres.writeFile({ fileName: OUT }).then((f) => console.log("Wrote " + f));
