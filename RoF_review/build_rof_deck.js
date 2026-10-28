// Builds the Radio over Fiber (RoF) deck: one message and one figure per slide.
// Figures come from make_figures.py. Usage:
//   python3 make_figures.py figs && npm install pptxgenjs && node build_rof_deck.js figs RoF_Technical_Review.pptx
const fs = require("fs");
const path = require("path");
const pptxgen = require("pptxgenjs");

const FIGS = process.argv[2] || "figs";
const OUT = process.argv[3] || "RoF_Technical_Review.pptx";

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in
pres.title = "Radio over Fiber (RoF)";
pres.theme = { headFontFace: "Arial", bodyFontFace: "Arial" };

const FONT = "Arial";
const BLACK = "000000";
const DARK = "333333";
const GREY = "707070";

pres.defineSlideMaster({
  title: "MAIN", background: { color: "FFFFFF" },
  objects: [{ placeholder: { options: { name: "title", type: "title", x: 0.6, y: 0.4, w: 12.1, h: 0.7,
    fontFace: FONT, fontSize: 30, bold: true, color: BLACK, align: "left", valign: "middle", margin: 0 }, text: "" } }],
  slideNumber: { x: 12.2, y: 7.0, w: 0.5, h: 0.3, fontFace: FONT, fontSize: 10, color: GREY, align: "right" },
});

function pngSize(file) {
  const b = fs.readFileSync(file);
  return { w: b.readUInt32BE(16), h: b.readUInt32BE(20) };
}
// Place a figure inside the box, keeping its aspect ratio, centred horizontally.
function figure(s, name, x, y, w, h) {
  const file = path.join(FIGS, name);
  const { w: pw, h: ph } = pngSize(file);
  const r = pw / ph;
  let fw = w, fh = w / r;
  if (fh > h) { fh = h; fw = h * r; }
  s.addImage({ path: file, x: x + (w - fw) / 2, y: y + (h - fh) / 2, w: fw, h: fh });
}
function text(s, t, o) {
  s.addText(t, Object.assign({ isTextBox: true, fontFace: FONT, fontSize: 18, color: DARK, margin: 0, valign: "top" }, o));
}
// Standard slide: title, one-line message, large figure, source line.
function slide(section, title, message, fig, notes, src) {
  const s = pres.addSlide({ masterName: "MAIN", sectionTitle: section });
  s.addText(title, { placeholder: "title" });
  if (message) text(s, message, { x: 0.6, y: 1.15, w: 12.1, h: 0.5, fontSize: 18 });
  if (fig) figure(s, fig, 0.6, 1.85, 12.1, src ? 4.75 : 5.1);
  if (src) text(s, src, { x: 0.6, y: 6.75, w: 11.4, h: 0.4, fontSize: 10, color: GREY, valign: "bottom" });
  if (notes) s.addNotes(notes);
  return s;
}

const A = "Speaker A", B = "Speaker B", APP = "Appendix";

// ------------------------------------------------------------------ Speaker A
pres.addSection({ title: A });
{
  const s = pres.addSlide({ masterName: "MAIN", sectionTitle: A });
  text(s, "Radio over Fiber (RoF)", { x: 0.6, y: 1.6, w: 12.1, h: 1.0, fontSize: 44, bold: true, color: BLACK });
  text(s, "Carrying radio signals over optical fiber", { x: 0.6, y: 2.6, w: 12.1, h: 0.6, fontSize: 22, color: DARK });
  text(s, "Speaker A  ·  Speaker B  ·  15 minutes", { x: 0.6, y: 3.3, w: 12.1, h: 0.4, fontSize: 16, color: GREY });
  figure(s, "f01_title.png", 0.6, 4.6, 12.1, 2.2);
  s.addNotes("0:20, Speaker A. Introduce the topic and the split: Speaker A covers problem, definition, signal path, architecture and RoF types; Speaker B covers the comparisons, limits, the deployment case and the conclusion.");
}
slide(A, "The problem", "Large buildings and venues need many antenna points, fed from one equipment room.",
  "f02_problem.png",
  "1:00, Speaker A.\n" +
  "Outdoor macro signals are attenuated by walls and distance, so coverage inside tunnels, stadiums and large buildings is provided by many indoor antenna points.\n" +
  "The radio equipment is kept in one room (or a base-station hotel) to share power, cooling, maintenance and operator access.\n" +
  "The engineering question is therefore: how do we carry the radio signal from that room to each antenna point, over tens of metres to kilometres, within a loss, noise and distortion budget?\n" +
  "Scope: only this transport segment. Backhaul to the core network and air-interface design are out of scope.");
slide(A, "What RoF is", "The radio waveform modulates light. A photodiode turns it back into the same radio signal.",
  "f03_definition.png",
  "1:15, Speaker A.\n" +
  "Definition used in this talk: an optical link that carries an analog radio waveform, at RF or IF, with E/O conversion at one end and O/E at the other.\n" +
  "Read the spectra left to right: the RF signal at f_RF; after the laser, the optical carrier with two sidebands at ±f_RF; after the photodiode, the original RF signal again.\n" +
  "Key boundary: RoF transports a radio signal. It does not create spectrum or wireless capacity. Digitized I/Q transport (CPRI) is called digital fronthaul here, not RoF.",
  "Sources: ITU-T G.Suppl.55 (10/2025); ITU-T G.9803 (2018).");
slide(A, "Signal path: downlink and uplink", "Four optical conversions in a two-way link. Each adds noise and distortion.",
  "f04_signal_path.png",
  "1:30, Speaker A.\n" +
  "Downlink: base-station RF output → E/O at the central site → fiber → O/E at the remote unit → power amplifier → duplexer → antenna.\n" +
  "Uplink: antenna → duplexer → LNA → E/O at the remote unit → fiber → O/E at the central site → base-station RF input.\n" +
  "Downlink and uplink use separate fibers or separate wavelengths. WDM is optional; it is only needed when several links share one fiber.\n" +
  "With intensity modulation and direct detection, 1 dB of optical loss costs 2 dB of RF loss (square-law detection, Cox 2004). We use this on slide 7.",
  "Source: C. H. Cox III, Analog Optical Links, Cambridge University Press, 2004.");
slide(A, "Where it sits in the network", "RoF is the fronthaul link from head-end to remote unit. Backhaul stays digital.",
  "f05_architecture.png",
  "1:15, Speaker A.\n" +
  "Operators' radios sit in a base-station hotel. The head-end combines their RF signals and converts them to optical (and back for the uplink).\n" +
  "Fibers run in a star to the remote antenna units (RAUs). The RAU is not passive: it contains photodiode, laser, amplifiers, filters and needs power.\n" +
  "Backhaul (base station to core) is a digital packet link and is not affected by the choice of RoF.\n" +
  "Because the analog link carries whatever RF is fed into it, several operators and bands can share it, within its bandwidth and dynamic range.");
slide(A, "Three ways to use the fiber", "Simpler remote unit means analog signal on the fiber. Digital needs a full radio at the remote end.",
  "f06_types.png",
  "1:30, Speaker A. Hand over to Speaker B after this slide (about 7:00 elapsed).\n" +
  "RFoF: the fiber carries the radio signal at its final frequency. The remote unit only converts and amplifies. The optics must work at the carrier frequency.\n" +
  "IFoF: the fiber carries a lower intermediate frequency. The remote unit needs a mixer and local oscillator.\n" +
  "Digital fronthaul (CPRI): the fiber carries sampled I/Q bits. The remote unit is a complete radio with DAC, mixer and amplifier. This is not RoF, but it is the main alternative.\n" +
  "Trade-off: remote-unit complexity rises from top to bottom; fiber capacity requirement rises in the opposite direction (slide 8).");

// ------------------------------------------------------------------ Speaker B
pres.addSection({ title: B });
slide(B, "Coax or fiber? It depends on length", "Fiber has lower RF loss only beyond a break-even length set by the conversion loss.",
  "f07_loss.png",
  "1:45, Speaker B.\n" +
  "Comparison defined: passive LMR-400-class coax versus an unamplified analog RFoF link, from the head-end RF port to the remote antenna port, downlink, 2.5 GHz.\n" +
  "Coax loss: 22.2 dB per 100 m (datasheet). Fiber: 0.25 dB/km optical, which is 0.5 dB/km in RF terms (panel a).\n" +
  "The RoF link also has a fixed RF-to-RF conversion loss. 20 dB and 40 dB are assumed values for illustration; the real value comes from the equipment datasheet.\n" +
  "Break-even length = conversion loss / (0.222 − 0.0005) dB/m: about 90 m and 180 m.\n" +
  "In practice both systems use amplifiers, so the deciding metrics become noise figure, dynamic range and power consumption, not loss alone.",
  "Coax: Times Microwave LMR-400 datasheet (22.2 dB/100 m at 2500 MHz). Fiber: G.652.D cable datasheets. Conversion loss values are assumptions.");
slide(B, "Analog RoF vs digital fronthaul", "Digital fronthaul line rate grows with every antenna and every MHz of bandwidth.",
  "f08_cpri.png",
  "1:30, Speaker B.\n" +
  "CPRI rate = sample rate × 2 (I and Q) × 15 bits × 16/15 (control) × 10/8 (8B/10B line coding).\n" +
  "20 MHz LTE, one antenna: 30.72 Msps → 1228.8 Mb/s, which is CPRI option 2. 100 MHz NR at 122.88 Msps → 4.9 Gb/s per antenna, about 315 Gb/s for 64 antennas.\n" +
  "An analog link instead carries each antenna stream in roughly its radio bandwidth, so the fiber capacity needed is much smaller.\n" +
  "What analog gives up: quality degrades along the link (noise, distortion, dispersion), there is no bit-level monitoring, and interfaces are mostly vendor-specific. Digital links are robust and standardized (CPRI, eCPRI, O-RAN 7.2x).\n" +
  "eCPRI with split 7.2x reduces the digital rate; it scales with MIMO layers and traffic, not antenna count.",
  "Source: CPRI Specification V7.0 (2015). Rates computed with the formula in the notes.");
slide(B, "Benefit: low fiber loss", "Fiber loss is a fraction of a dB per km, and the fiber itself does not pick up interference.",
  "f09_attenuation.png",
  "1:00, Speaker B.\n" +
  "Standard single-mode fiber (G.652.D): cabled maximum around 0.36 dB/km at 1310 nm and 0.22 dB/km at 1550 nm (vendor datasheets). The curve is an illustrative physical model, the squares are datasheet limits.\n" +
  "Conditions on each benefit:\n" +
  "– Low loss matters only above the break-even length (slide 7).\n" +
  "– The fiber is immune to electromagnetic pickup; the remote electronics and the radio link are not.\n" +
  "– Central equipment is easier to share and maintain, but the remote unit still needs power.\n" +
  "– Cost is site-specific and is not claimed here.",
  "Datasheet points: Prysmian G.652.D cable. Model curve is illustrative (Rayleigh scattering and infrared absorption).");
slide(B, "Limit 1: chromatic dispersion", "At 1550 nm the received RF power fades at certain frequencies. Sub-6 GHz bands are barely affected.",
  "f10_dispersion.png",
  "1:00, Speaker B.\n" +
  "With double-sideband intensity modulation, the two optical sidebands travel at slightly different speeds. After detection they interfere, and the RF power drops to zero at specific frequency–length combinations.\n" +
  "Computed with P ∝ cos²(π·L·D·λ²·f²/c), D = 17 ps/(nm·km). At 10 km the first null is near 19 GHz.\n" +
  "Mitigation: operate at 1310 nm (near-zero dispersion), use single-sideband modulation, or use IFoF.\n" +
  "This matters for mmWave over km-scale fiber, not for indoor sub-6 GHz systems.",
  "Model: U. Gliese et al., IEEE Trans. Microwave Theory Tech. 44(10), 1996. Curves computed for standard SMF.");
{
  const s = pres.addSlide({ masterName: "MAIN", sectionTitle: B });
  s.addText("Limit 2: noise vs distortion", { placeholder: "title" });
  text(s, "An analog link has a limited usable power window.", { x: 0.6, y: 1.15, w: 12.1, h: 0.5 });
  figure(s, "f11_sfdr.png", 0.6, 1.85, 7.6, 4.75);
  text(s, [
    { text: "Too little signal", options: { bold: true, breakLine: true } },
    { text: "lost in noise", options: { breakLine: true } },
    { text: " ", options: { breakLine: true } },
    { text: "Too much signal", options: { bold: true, breakLine: true } },
    { text: "intermodulation appears", options: { breakLine: true } },
    { text: " ", options: { breakLine: true } },
    { text: "SFDR", options: { bold: true, breakLine: true } },
    { text: "the usable window between the two" },
  ], { x: 8.7, y: 2.4, w: 4.0, h: 3.6, fontSize: 18 });
  text(s, "Illustrative, no values. Source: C. H. Cox III, Analog Optical Links, 2004.", { x: 0.6, y: 6.75, w: 11.4, h: 0.4, fontSize: 10, color: GREY, valign: "bottom" });
  s.addNotes("1:00, Speaker B.\n" +
    "Laser noise, photodiode shot noise and receiver thermal noise set a noise floor. Laser and modulator nonlinearity creates intermodulation, which rises 3 dB for every 1 dB of input.\n" +
    "The spurious-free dynamic range is the span between the two. It limits uplink sensitivity and how many carriers can share one link.\n" +
    "Other practical limits: one fiber pair or wavelength pair per remote unit, power needed at every remote unit, and no bit-level performance monitoring on an analog link.");
}
slide(B, "Case: Maracanã and Mineirão (2014)", "Fiber-fed distributed antenna system for five operators, 2G / 3G / 4G.",
  "f12_stadium.png",
  "1:00, Speaker B.\n" +
  "Reported by the vendors: Axell Wireless (June 2014) supplied optical DAS for stadiums including Maracanã and Mineirão, combined capacity over 141,000, five operators, 2G/3G/4G. RFS (10 June 2014) supplied HYBRIFLEX hybrid fiber and DC power cable at Maracanã.\n" +
  "Not reported: link budgets, noise figures, measured capacity, cost comparison, or whether each subsystem carried analog RF or digital fronthaul.\n" +
  "So the case shows feasibility of a multi-operator fiber DAS in a large venue. It does not support performance or cost claims.\n" +
  "The figure is a schematic, not the real floor plan.",
  "Sources: Axell Wireless press release, June 2014; RFS press release, 10 June 2014. Schematic only.");
slide(B, "When to choose analog RoF", "RoF moves the antenna point closer to users. It does not add spectrum.",
  "f13_decision.png",
  "1:00, Speaker B.\n" +
  "Conclusions, each tied to a slide:\n" +
  "1. RoF transports an existing radio signal; it does not add spectrum or wireless capacity (slide 3).\n" +
  "2. Against passive coax, it has lower loss only beyond a break-even length (slide 7).\n" +
  "3. Against digital fronthaul, it needs far less fiber capacity and a simpler remote unit, at the cost of noise, distortion, dispersion and weaker monitoring (slides 8, 10, 11).\n" +
  "4. Documented use: multi-operator fiber DAS in large venues (slide 12).\n" +
  "The flow on the slide is the decision checklist that follows from these points.");
{
  const s = pres.addSlide({ masterName: "MAIN", sectionTitle: B });
  text(s, "Questions", { x: 0.6, y: 2.0, w: 12.1, h: 1.0, fontSize: 44, bold: true, color: BLACK });
  figure(s, "f01_title.png", 0.6, 4.2, 12.1, 2.2);
  s.addNotes("Appendix slides cover RAU types, a measured BER curve, a 5G/6G research demo, and references.");
}

// ------------------------------------------------------------------ Appendix
pres.addSection({ title: APP });
slide(APP, "A1  Remote unit types", "What the remote unit must contain for each signal on the fiber.", "a_rau.png",
  "BBoF here means analog baseband over fiber, as in the source figure. It is different from digital fronthaul.",
  "Redrawn from: Electronics 9(11), 1785 (2020), Fig. 3. DOI: 10.3390/electronics9111785.");
slide(APP, "A2  Measured BER vs carrier-to-sideband ratio", "One experimental link: 10 km fiber + 3 m wireless. Best result near 25 dB.", "a_csr.png",
  "Values are approximate readings from the published plot (verification against the paper required). At low CSR distortion dominates; at high CSR noise dominates. The result applies only to the tested link.",
  "Redrawn from: M. U. Hadi and G. Murtaza, Electronics 12(1), 64 (2023), Fig. 6. Values read from the published plot.");
slide(APP, "A3  Research demo: 5G + candidate 6G on one fiber", "Laboratory demonstration, not a deployed system.", "a_demo.png",
  "The 6G branch uses a second laser and a UTC photodiode to generate a THz signal by optical beating. '6G' is the authors' label.",
  "Redrawn and simplified from: M. U. Hadi and G. Murtaza, Electronics 12(1), 64 (2023), Fig. 2.");
{
  const s = pres.addSlide({ masterName: "MAIN", sectionTitle: APP });
  s.addText("A4  References", { placeholder: "title" });
  const refs = [
    "C. H. Cox III, Analog Optical Links: Theory and Practice, Cambridge University Press, 2004.",
    "U. Gliese, S. Nørskov, T. N. Nielsen, Chromatic dispersion in fiber-optic microwave and millimeter-wave links, IEEE T-MTT 44(10), 1996.",
    "ITU-T G.9803 (2018), Radio over fibre systems, with Amendments 1 (2019) and 2 (2022).",
    "ITU-T G-series Supplement 55 (10/2025), Radio-over-fibre technologies and their applications.",
    "ITU-T G.652, single-mode optical fibre and cable; Prysmian G.652.D cable datasheet.",
    "CPRI Specification V7.0 (2015); eCPRI Specification V2.0 (2019).",
    "Y. Li, Q. Xie, M. El-Hajjar, L. Hanzo, Analogue Radio Over Fiber for Next-Generation RAN, arXiv:2111.13851, 2021.",
    "Radio over Fiber: An Alternative Broadband Network Technology for IoT, Electronics 9(11), 1785, 2020.",
    "M. U. Hadi, G. Murtaza, Fibre Wireless Distributed Antenna Systems for 5G and 6G Services, Electronics 12(1), 64, 2023.",
    "Times Microwave Systems, LMR-400 datasheet.",
    "Axell Wireless press release, June 2014; RFS press release, 10 June 2014.",
  ];
  text(s, refs.map((r, i) => ({ text: r, options: { bullet: { type: "number" }, paraSpaceAfter: 4, breakLine: i < refs.length - 1 } })),
    { x: 0.6, y: 1.4, w: 12.1, h: 5.4, fontSize: 14 });
}

pres.writeFile({ fileName: OUT }).then((f) => console.log("Wrote " + f));
