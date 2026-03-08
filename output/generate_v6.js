const pptxgen = require("pptxgenjs");
const pres = new pptxgen();

pres.layout = "LAYOUT_16x9";
pres.author = "Skill-Forge";
pres.title = "Hydrogen Production Comparison";

const slide = pres.addSlide();
slide.background = { color: "FFFFFF" };

// === Title ===
slide.addText(
  "1.1/ Blue and Green hydrogen are two low-carbon production\nmethods of H2 with the highest future potential",
  {
    x: 0.4, y: 0.25, w: 8.2, h: 0.65,
    fontSize: 16, fontFace: "Georgia", bold: true,
    color: "000000", margin: 0, lineSpacingMultiple: 1.2
  }
);

// === CO2 legend (top right) ===
slide.addShape(pres.shapes.OVAL, {
  x: 8.3, y: 0.3, w: 0.22, h: 0.22,
  line: { color: "333333", width: 1 }, fill: { color: "FFFFFF" }
});
slide.addText("X", {
  x: 8.3, y: 0.3, w: 0.22, h: 0.22,
  fontSize: 7, fontFace: "Calibri", bold: true, color: "333333",
  align: "center", valign: "middle", margin: 0
});
slide.addText("CO2 emissions\nkg CO2 per kgH2 produced", {
  x: 8.55, y: 0.27, w: 1.1, h: 0.3,
  fontSize: 6.5, fontFace: "Calibri", color: "333333", margin: 0
});

// === Divider line ===
slide.addShape(pres.shapes.LINE, {
  x: 0.4, y: 0.98, w: 9.2, h: 0,
  line: { color: "333333", width: 0.75 }
});

// === "Low-carbon H2" label ===
slide.addText("Low-carbon H2", {
  x: 4.2, y: 1.03, w: 4.2, h: 0.18,
  fontSize: 8.5, fontFace: "Calibri", bold: true, color: "333333", align: "center", margin: 0
});

// === Navy header border ===
slide.addShape(pres.shapes.LINE, {
  x: 0.4, y: 1.24, w: 9.2, h: 0,
  line: { color: "1B3A5C", width: 2 }
});

// === Table ===
const noBorder = { pt: 0, color: "FFFFFF" };
const hBorder = { pt: 0.5, color: "D0D0D0" };
const hdrBorderBot = { pt: 1, color: "333333" };

const hdrW = (t) => ({ text: t, options: { bold: true, color: "000000", fill: { color: "FFFFFF" }, fontSize: 9, fontFace: "Calibri", align: "center", valign: "middle", border: [noBorder, noBorder, hdrBorderBot, noBorder] } });
const hdrB = (t) => ({ text: t, options: { bold: true, color: "000000", fill: { color: "E8F0FE" }, fontSize: 9, fontFace: "Calibri", align: "center", valign: "middle", border: [noBorder, noBorder, hdrBorderBot, noBorder] } });
const hdrG = (t) => ({ text: t, options: { bold: true, color: "000000", fill: { color: "E6F4EA" }, fontSize: 9, fontFace: "Calibri", align: "center", valign: "middle", border: [noBorder, noBorder, hdrBorderBot, noBorder] } });
const lbl = (t) => ({ text: t, options: { bold: true, color: "000000", fill: { color: "FFFFFF" }, fontSize: 8, fontFace: "Calibri", valign: "middle", border: [hBorder, noBorder, hBorder, noBorder] } });
const cW = (t) => ({ text: t, options: { color: "333333", fill: { color: "FFFFFF" }, fontSize: 8, fontFace: "Calibri", valign: "middle", border: [hBorder, noBorder, hBorder, noBorder] } });
const cB = (t) => ({ text: t, options: { color: "333333", fill: { color: "E8F0FE" }, fontSize: 8, fontFace: "Calibri", valign: "middle", border: [hBorder, noBorder, hBorder, noBorder] } });
const cG = (t) => ({ text: t, options: { color: "333333", fill: { color: "E6F4EA" }, fontSize: 8, fontFace: "Calibri", valign: "middle", border: [hBorder, noBorder, hBorder, noBorder] } });

const rows = [
  [
    { text: "", options: { fill: { color: "FFFFFF" }, fontSize: 8, border: [noBorder, noBorder, hdrBorderBot, noBorder] } },
    hdrW("Grey\nH2"),
    hdrB("Blue\nH2"),
    hdrG("Green\nH2")
  ],
  [
    lbl("Production\nprocess"),
    cW("Split\u00B9 natural gas into\nH2 and CO2"),
    cB("Similar to Grey but additionally\ncapture, use, and store CO2"),
    cG("Split water into H2 and O2 in an\nelectrolyzer powered by renewables")
  ],
  [
    lbl("CO2 emissions\nkg CO2/kgH2"),
    cW("~10"),
    cB("~1-3  Most CO2 stored"),
    cG("~0  Assuming Green elec. mix\u00B2")
  ],
  [
    lbl("Investments\nand complexity"),
    cW("Large scale, one-off facilities\nTriple-digit mn EUR CAPEX"),
    cB("Large scale, one-off facilities\nTriple-digit mn EUR CAPEX"),
    cG("Small-scale (5-10MW), replicable\u00B3\nSingle/double-digit mn EUR CAPEX\nExpecting 50-70% reduction by 2030")
  ],
  [
    lbl("EPC duration"),
    cW("3-5 years EPC"),
    cB("5-10+ years EPC, contingent on\nCO2 storage site development"),
    cG("1-3 years EPC duration")
  ],
  [
    lbl("Direct link to\npower sector"),
    cW("\u2716"),
    cB("\u2716"),
    cG("\u2714")
  ]
];

slide.addTable(rows, {
  x: 0.4, y: 1.25, w: 9.2, h: 2.45,
  border: noBorder,
  colW: [1.2, 2.65, 2.65, 2.7],
  rowH: [0.28, 0.38, 0.35, 0.52, 0.38, 0.28],
  autoPage: false
});

// === Footnotes ===
slide.addText(
  "1.  Process: Sulfur Removal, Synthesis Gas Production via Steam-Methane Reforming (SMR) or Auto-Thermal Reforming (ATR), CO Shift Reaction,\n" +
  "     Purification. The latter is expected to offer higher efficiencies in combination with CCS. Grey hydrogen can also be produced from coal gasification.\n" +
  "2.  In Australia, producing hydrogen from electrolyzers on grid electricity would lead to emission intensity of ~40 kgCO2/kgH2.\n" +
  "3.  Especially PEM electrolyzers can be largely pre-assembled, containerized, and stacked.",
  {
    x: 0.4, y: 3.85, w: 8.8, h: 0.48,
    fontSize: 6, fontFace: "Calibri", color: "555555", margin: 0,
    lineSpacingMultiple: 1.15
  }
);

// === Footer line ===
slide.addShape(pres.shapes.LINE, {
  x: 0.4, y: 5.05, w: 9.2, h: 0,
  line: { color: "333333", width: 0.5 }
});

// === Footer ===
slide.addText("McKinsey & Company    4", {
  x: 7.2, y: 5.1, w: 2.4, h: 0.2,
  fontSize: 8, fontFace: "Calibri", color: "666666", align: "right", margin: 0
});

pres.writeFile({ fileName: "/Users/lifeichen/Skill-Forge/output/slide_v6.pptx" })
  .then(() => console.log("Created slide_v6.pptx"))
  .catch(err => console.error(err));
