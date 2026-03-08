const pptxgen = require("pptxgenjs");
const pres = new pptxgen();

pres.layout = "LAYOUT_16x9";
pres.author = "Skill-Forge";
pres.title = "Hydrogen Production Comparison";

const slide = pres.addSlide();
slide.background = { color: "FFFFFF" };

// === Title (insight-driven, with section numbering) ===
slide.addText(
  "1.1/ Blue and Green hydrogen are two low-carbon production\nmethods of H2 with the highest future potential",
  {
    x: 0.5, y: 0.15, w: 9, h: 0.9,
    fontSize: 22, fontFace: "Georgia", bold: true,
    color: "000000", margin: 0, lineSpacingMultiple: 1.1
  }
);

// === Divider line below title ===
slide.addShape(pres.shapes.LINE, {
  x: 0.5, y: 1.15, w: 9, h: 0,
  line: { color: "333333", width: 1 }
});

// === "Low-carbon H2" label above table columns ===
slide.addText("Low-carbon H2", {
  x: 3.5, y: 1.25, w: 5.5, h: 0.25,
  fontSize: 10, fontFace: "Calibri", bold: true, color: "333333", align: "center", margin: 0
});

// === Navy border above header row ===
slide.addShape(pres.shapes.LINE, {
  x: 2.0, y: 1.52, w: 7.5, h: 0,
  line: { color: "1B3A5C", width: 2 }
});

// === Table ===
const hdr = (t) => ({ text: t, options: { bold: true, color: "000000", fill: { color: "FFFFFF" }, fontSize: 11, fontFace: "Calibri", align: "center", valign: "middle" } });
const hdrBlue = (t) => ({ text: t, options: { bold: true, color: "000000", fill: { color: "DCE9F5" }, fontSize: 11, fontFace: "Calibri", align: "center", valign: "middle" } });
const hdrGreen = (t) => ({ text: t, options: { bold: true, color: "000000", fill: { color: "E8F6EF" }, fontSize: 11, fontFace: "Calibri", align: "center", valign: "middle" } });
const lbl = (t) => ({ text: t, options: { bold: true, color: "000000", fill: { color: "FFFFFF" }, fontSize: 10, fontFace: "Calibri", valign: "middle" } });
const cell = (t) => ({ text: t, options: { color: "333333", fill: { color: "FFFFFF" }, fontSize: 10, fontFace: "Calibri", valign: "middle" } });

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
    cell("Similar to Grey but additionally\ncapture, potentially use, and\nstore CO2"),
    cell("Split water into H2 and O2 in\nan electrolyzer that is powered\nby renewables")
  ],
  [
    lbl("CO2 emissions\n(kg CO2/kgH2)"),
    cell("~10"),
    cell("~1-3\nMost CO2 stored"),
    cell("~0\nAssuming Green electricity mix\u00B2")
  ],
  [
    lbl("Investments\nand complexity"),
    cell("Large scale, one-off facilities\n\nRequiring triple-digit million\nEUR CAPEX per facility"),
    cell("Large scale and one-off facilities\n\nRequiring triple-digit mn EUR\nCAPEX per facility"),
    cell("Small-scale (5-10MW) facilities\nthat can be replicated, similar\nto utility-scale batteries\u00B3\n\nRequiring single/double-digit mn\nEUR CAPEX per facility, expecting\n50-70% reduction until 2030")
  ],
  [
    lbl("EPC\nduration"),
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
  x: 0.5, y: 1.53, w: 9, h: 3.3,
  border: { pt: 0.75, color: "C0C0C0" },
  colW: [1.5, 2.5, 2.5, 2.5],
  rowH: [0.35, 0.5, 0.45, 0.85, 0.5, 0.35]
});

// === Footnotes (compact, inline) ===
slide.addText(
  "1.  Process: Sulfur Removal, Synthesis Gas Production via Steam-Methane Reforming (SMR) or Auto-Thermal Reforming (ATR), CO Shift Reaction,\n" +
  "     Purification. The latter is expected to offer higher efficiencies in combination with CCS. Grey hydrogen can also be produced from coal gasification.\n" +
  "2.  In Australia, producing hydrogen from electrolyzers that run on grid electricity would lead to an emission intensity of ~40 kgCO2/kgH2.\n" +
  "3.  Especially PEM electrolyzers can be largely pre-assembled, containerized, and stacked.",
  {
    x: 0.5, y: 4.88, w: 8.5, h: 0.42,
    fontSize: 6.5, fontFace: "Calibri", color: "666666", margin: 0,
    lineSpacingMultiple: 1.15
  }
);

// === Footer line ===
slide.addShape(pres.shapes.LINE, {
  x: 0.5, y: 5.32, w: 9, h: 0,
  line: { color: "333333", width: 0.5 }
});

// === Footer ===
slide.addText("McKinsey & Company    4", {
  x: 7, y: 5.35, w: 2.5, h: 0.2,
  fontSize: 8, fontFace: "Calibri", color: "666666", align: "right", margin: 0
});

pres.writeFile({ fileName: "/Users/lifeichen/Skill-Forge/output/slide_v2.pptx" })
  .then(() => console.log("Created slide_v2.pptx"))
  .catch(err => console.error(err));
