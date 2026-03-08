const pptxgen = require("pptxgenjs");
const pres = new pptxgen();

pres.layout = "LAYOUT_16x9";
pres.author = "Skill-Forge";
pres.title = "Hydrogen Production Comparison";

const slide = pres.addSlide();
slide.background = { color: "FFFFFF" };

// === Title ===
slide.addText(
  "1.1/ Blue and Green hydrogen are two low-carbon production methods of H2 with the highest future potential",
  {
    x: 0.5, y: 0.2, w: 9, h: 0.65,
    fontSize: 16, fontFace: "Georgia", bold: true,
    color: "000000", margin: 0, lineSpacingMultiple: 1.15
  }
);

// === Divider line ===
slide.addShape(pres.shapes.LINE, {
  x: 0.5, y: 1.0, w: 9, h: 0,
  line: { color: "333333", width: 1 }
});

// === Navy header border ===
slide.addShape(pres.shapes.LINE, {
  x: 0.5, y: 1.25, w: 9, h: 0,
  line: { color: "1B3A5C", width: 2 }
});

// === "Low-carbon H2" label ===
slide.addText("Low-carbon H2", {
  x: 3.7, y: 1.05, w: 5, h: 0.2,
  fontSize: 9, fontFace: "Calibri", bold: true, color: "333333", align: "center", margin: 0
});

// === CO2 emissions legend (top right) ===
slide.addText("X    CO2 emissions\n      kg CO2 per kgH2 produced", {
  x: 7.5, y: 1.05, w: 2, h: 0.2,
  fontSize: 6.5, fontFace: "Calibri", color: "333333", margin: 0
});

// === Table with horizontal-only borders ===
const noBorder = { pt: 0, color: "FFFFFF" };
const hBorder = { pt: 0.5, color: "D0D0D0" };
const hdrBorderBot = { pt: 1, color: "333333" };

const hdr = (t) => ({
  text: t,
  options: {
    bold: true, color: "000000", fill: { color: "FFFFFF" },
    fontSize: 9, fontFace: "Calibri", align: "center", valign: "middle",
    border: [noBorder, noBorder, hdrBorderBot, noBorder]
  }
});

const lbl = (t) => ({
  text: t,
  options: {
    bold: true, color: "000000", fill: { color: "FFFFFF" },
    fontSize: 8.5, fontFace: "Calibri", valign: "middle",
    border: [hBorder, noBorder, hBorder, noBorder]
  }
});

const cell = (t) => ({
  text: t,
  options: {
    color: "333333", fill: { color: "FFFFFF" },
    fontSize: 8.5, fontFace: "Calibri", valign: "middle",
    border: [hBorder, noBorder, hBorder, noBorder]
  }
});

const rows = [
  [
    { text: "", options: { fill: { color: "FFFFFF" }, fontSize: 8.5, border: [noBorder, noBorder, hdrBorderBot, noBorder] } },
    hdr("Grey\nH2"),
    hdr("Blue\nH2"),
    hdr("Green\nH2")
  ],
  [
    lbl("Production\nprocess"),
    cell("Split\u00B9 natural gas\ninto H2 and CO2"),
    cell("Similar to Grey but additionally\ncapture, potentially use, and\nstore CO2"),
    cell("Split water into H2 and O2 in an\nelectrolyzer that is powered\nby renewables")
  ],
  [
    lbl("CO2 emissions\nkg CO2/kgH2"),
    cell("~10"),
    cell("~1-3\nMost CO2 stored"),
    cell("~0\nAssuming Green electricity mix\u00B2")
  ],
  [
    lbl("Investments\nand complexity"),
    cell("Large scale, one-off facilities\nRequiring triple-digit million\nEUR CAPEX per facility"),
    cell("Large scale and one-off facilities\nRequiring triple-digit mn EUR\nCAPEX per facility"),
    cell("Small-scale (5-10MW) facilities\nthat can be replicated\u00B3\nSingle/double-digit mn EUR CAPEX\nper facility, expecting 50-70%\nreduction until 2030")
  ],
  [
    lbl("EPC duration"),
    cell("3-5 years EPC"),
    cell("5-10+ years EPC duration,\ncontingent upon development\nof CO2 storage site"),
    cell("1-3 years EPC duration")
  ],
  [
    lbl("Direct link to\npower sector"),
    cell("X"),
    cell("X"),
    cell("\u2713")
  ]
];

slide.addTable(rows, {
  x: 0.5, y: 1.26, w: 9, h: 2.8,
  border: noBorder,
  colW: [1.5, 2.5, 2.5, 2.5],
  rowH: [0.3, 0.42, 0.42, 0.68, 0.42, 0.3],
  autoPage: false
});

// === Footnotes ===
slide.addText(
  "1.  Process: Sulfur Removal, Synthesis Gas Production via Steam-Methane Reforming (SMR) or Auto-Thermal Reforming (ATR), CO Shift Reaction,\n" +
  "     Purification. The latter is expected to offer higher efficiencies in combination with CCS. Grey hydrogen can also be produced from coal gasification.\n" +
  "2.  In Australia, producing hydrogen from electrolyzers that run on grid electricity would lead to an emission intensity of ~40 kgCO2/kgH2.\n" +
  "3.  Especially PEM electrolyzers can be largely pre-assembled, containerized, and stacked.",
  {
    x: 0.5, y: 4.2, w: 8.5, h: 0.45,
    fontSize: 6, fontFace: "Calibri", color: "666666", margin: 0,
    lineSpacingMultiple: 1.15
  }
);

// === Footer line ===
slide.addShape(pres.shapes.LINE, {
  x: 0.5, y: 5.1, w: 9, h: 0,
  line: { color: "333333", width: 0.5 }
});

// === Footer ===
slide.addText("McKinsey & Company    4", {
  x: 7, y: 5.15, w: 2.5, h: 0.2,
  fontSize: 8, fontFace: "Calibri", color: "666666", align: "right", margin: 0
});

pres.writeFile({ fileName: "/Users/lifeichen/Skill-Forge/output/slide_v5.pptx" })
  .then(() => console.log("Created slide_v5.pptx"))
  .catch(err => console.error(err));
