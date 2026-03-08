const pptxgen = require("pptxgenjs");
const pres = new pptxgen();

pres.layout = "LAYOUT_16x9";
pres.author = "Skill-Forge";
pres.title = "Hydrogen Production Comparison";

const slide = pres.addSlide();

// === SKILL_V0 defaults: Teal Trust palette, dark premium feel ===
slide.background = { color: "1A1A2E" };

// Title
slide.addText("Hydrogen Production Methods Comparison", {
  x: 0.5, y: 0.3, w: 9, h: 0.8,
  fontSize: 36, fontFace: "Georgia", bold: true,
  color: "02C39A", margin: 0
});

// Subtitle
slide.addText("Grey, Blue, and Green H2 — Key Characteristics", {
  x: 0.5, y: 1.1, w: 9, h: 0.4,
  fontSize: 14, fontFace: "Calibri", color: "AAAAAA"
});

// Table data
const headerOpts = { bold: true, color: "FFFFFF", fill: { color: "028090" }, fontSize: 11, fontFace: "Calibri", align: "center", valign: "middle" };
const labelOpts = { bold: true, color: "00A896", fill: { color: "16213E" }, fontSize: 11, fontFace: "Calibri", valign: "middle" };
const cellOpts = { color: "CCCCCC", fill: { color: "16213E" }, fontSize: 10, fontFace: "Calibri", valign: "middle" };
const cellAltOpts = { color: "CCCCCC", fill: { color: "1A1A3E" }, fontSize: 10, fontFace: "Calibri", valign: "middle" };

const rows = [
  [
    { text: "", options: { ...headerOpts, fill: { color: "16213E" } } },
    { text: "Grey H2", options: headerOpts },
    { text: "Blue H2", options: headerOpts },
    { text: "Green H2", options: headerOpts }
  ],
  [
    { text: "Production\nprocess", options: labelOpts },
    { text: "Split natural gas\ninto H2 and CO2", options: cellOpts },
    { text: "Similar to Grey but\ncapture and store CO2", options: cellOpts },
    { text: "Split water into H2 and O2\nvia electrolysis (renewables)", options: cellOpts }
  ],
  [
    { text: "CO2 emissions\n(kg CO2/kgH2)", options: labelOpts },
    { text: "~10", options: cellAltOpts },
    { text: "~1-3\n(most CO2 stored)", options: cellAltOpts },
    { text: "~0\n(assuming green mix)", options: cellAltOpts }
  ],
  [
    { text: "Investment\nscale", options: labelOpts },
    { text: "Large scale,\none-off facilities", options: cellOpts },
    { text: "Large scale,\none-off facilities", options: cellOpts },
    { text: "Small-scale (5-10MW),\nreplicable facilities", options: cellOpts }
  ],
  [
    { text: "CAPEX per\nfacility", options: labelOpts },
    { text: "Triple-digit mn\nEUR CAPEX", options: cellAltOpts },
    { text: "Triple-digit mn\nEUR CAPEX", options: cellAltOpts },
    { text: "Single/double-digit mn\nEUR CAPEX", options: cellAltOpts }
  ],
  [
    { text: "EPC\nduration", options: labelOpts },
    { text: "3-5 years", options: cellOpts },
    { text: "5-10+ years\n(CO2 storage dev.)", options: cellOpts },
    { text: "1-3 years", options: cellOpts }
  ]
];

slide.addTable(rows, {
  x: 0.5, y: 1.7, w: 9, h: 3.2,
  border: { pt: 0.5, color: "028090" },
  colW: [1.8, 2.4, 2.4, 2.4],
  rowH: [0.4, 0.56, 0.56, 0.56, 0.56, 0.56]
});

// Footer
slide.addText("Source: McKinsey Hydrogen Council analysis, 2020", {
  x: 0.5, y: 5.05, w: 7, h: 0.3,
  fontSize: 8, fontFace: "Calibri", color: "777777"
});
slide.addText("McKinsey & Company", {
  x: 7.5, y: 5.2, w: 2, h: 0.3,
  fontSize: 8, fontFace: "Calibri", color: "777777", align: "right"
});

pres.writeFile({ fileName: "/Users/lifeichen/Skill-Forge/output/slide_v0.pptx" })
  .then(() => console.log("Created slide_v0.pptx"))
  .catch(err => console.error(err));
