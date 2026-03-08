const pptxgen = require("pptxgenjs");
const pres = new pptxgen();

pres.layout = "LAYOUT_16x9";
pres.author = "Skill-Forge";
pres.title = "Hydrogen Production Comparison";

const slide = pres.addSlide();
slide.background = { color: "FFFFFF" };

// === Title (insight-driven) ===
slide.addText(
  "Blue and Green hydrogen are two low-carbon production\nmethods of H2 with the highest future potential",
  {
    x: 0.5, y: 0.2, w: 9, h: 0.9,
    fontSize: 22, fontFace: "Georgia", bold: true,
    color: "000000", margin: 0, lineSpacingMultiple: 1.1
  }
);

// === Subtitle ===
slide.addText("Low-carbon H2", {
  x: 3.5, y: 1.35, w: 3, h: 0.3,
  fontSize: 11, fontFace: "Calibri", bold: true, color: "333333", align: "center"
});

// === Divider line ===
slide.addShape(pres.shapes.LINE, {
  x: 0.5, y: 1.2, w: 9, h: 0,
  line: { color: "333333", width: 1 }
});

// === Table ===
const hdr = (t) => ({ text: t, options: { bold: true, color: "000000", fill: { color: "FFFFFF" }, fontSize: 12, fontFace: "Calibri", align: "center", valign: "middle" } });
const hdrBlue = (t) => ({ text: t, options: { bold: true, color: "000000", fill: { color: "D6EAF8" }, fontSize: 12, fontFace: "Calibri", align: "center", valign: "middle" } });
const hdrGreen = (t) => ({ text: t, options: { bold: true, color: "000000", fill: { color: "D5F5E3" }, fontSize: 12, fontFace: "Calibri", align: "center", valign: "middle" } });
const lbl = (t) => ({ text: t, options: { bold: true, color: "000000", fill: { color: "FFFFFF" }, fontSize: 10, fontFace: "Calibri", valign: "middle" } });
const cell = (t) => ({ text: t, options: { color: "333333", fill: { color: "FFFFFF" }, fontSize: 10, fontFace: "Calibri", valign: "middle" } });
const cellBlue = (t) => ({ text: t, options: { color: "333333", fill: { color: "EBF5FB" }, fontSize: 10, fontFace: "Calibri", valign: "middle" } });
const cellGreen = (t) => ({ text: t, options: { color: "333333", fill: { color: "EAFAF1" }, fontSize: 10, fontFace: "Calibri", valign: "middle" } });

const rows = [
  [
    { text: "", options: { fill: { color: "FFFFFF" }, fontSize: 10 } },
    hdr("Grey\nH2"),
    hdrBlue("Blue\nH2"),
    hdrGreen("Green\nH2")
  ],
  [
    lbl("Production\nprocess"),
    cell("Split\u00B9 natural gas\ninto H2 and CO2"),
    cellBlue("Similar to Grey but additionally\ncapture, potentially use, and store CO2"),
    cellGreen("Split water into H2 and O2 in an\nelectrolyzer powered by renewables")
  ],
  [
    lbl("CO2 emissions\n(kg CO2/kgH2)"),
    cell("~10"),
    cellBlue("~1-3\n(most CO2 stored)"),
    cellGreen("~0\n(assuming green electricity mix\u00B2)")
  ],
  [
    lbl("Investments\nand complexity"),
    cell("Large scale, one-off facilities\nRequiring triple-digit million\nEUR CAPEX per facility"),
    cellBlue("Large scale and one-off facilities\nRequiring triple-digit mn EUR\nCAPEX per facility"),
    cellGreen("Small-scale (5-10MW) facilities\nthat can be replicated\u00B3\nSingle/double-digit mn EUR CAPEX")
  ],
  [
    lbl("EPC\nduration"),
    cell("3-5 years EPC"),
    cellBlue("5-10+ years EPC duration,\ncontingent upon development\nof CO2 storage site"),
    cellGreen("1-3 years EPC duration")
  ],
  [
    lbl("Direct link to\npower sector"),
    cell("X"),
    cellBlue("X"),
    cellGreen("\u2713")
  ]
];

slide.addTable(rows, {
  x: 0.5, y: 1.55, w: 9, h: 3.3,
  border: { pt: 0.5, color: "E0E0E0" },
  colW: [1.5, 2.5, 2.5, 2.5],
  rowH: [0.4, 0.55, 0.55, 0.7, 0.6, 0.4]
});

// === Footnotes ===
slide.addText([
  { text: "1. ", options: { fontSize: 7, bold: true } },
  { text: "Process: Sulfur Removal, Synthesis Gas Production via Steam-Methane Reforming (SMR) or Auto-Thermal Reforming (ATR), CO Shift Reaction, Purification.", options: { fontSize: 7 } },
  { text: "\n2. ", options: { fontSize: 7, bold: true, breakLine: true } },
  { text: "In Australia, producing hydrogen from electrolyzers that run on grid electricity would lead to an emission intensity of ~40 kgCO2/kgH2.", options: { fontSize: 7 } },
  { text: "\n3. ", options: { fontSize: 7, bold: true, breakLine: true } },
  { text: "Especially PEM electrolyzers can be largely pre-assembled, containerized, and stacked.", options: { fontSize: 7 } }
], {
  x: 0.5, y: 4.95, w: 8.5, h: 0.45,
  color: "666666", fontFace: "Calibri", margin: 0
});

// === Footer line ===
slide.addShape(pres.shapes.LINE, {
  x: 0.5, y: 5.35, w: 9, h: 0,
  line: { color: "333333", width: 0.5 }
});

// === Footer ===
slide.addText("McKinsey & Company    4", {
  x: 7, y: 5.38, w: 2.5, h: 0.2,
  fontSize: 8, fontFace: "Calibri", color: "666666", align: "right", margin: 0
});

pres.writeFile({ fileName: "/Users/lifeichen/Skill-Forge/output/slide_v1.pptx" })
  .then(() => console.log("Created slide_v1.pptx"))
  .catch(err => console.error(err));
