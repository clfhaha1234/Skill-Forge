const pptxgen = require("pptxgenjs");
const pres = new pptxgen();

pres.layout = "LAYOUT_16x9";
pres.author = "Skill-Forge";
pres.title = "EV Market Comparison";

const slide = pres.addSlide();
slide.background = { color: "FFFFFF" };

// === Title (insight-driven, with section numbering) ===
slide.addText(
  "1.1/ China leads the global EV transition with 60% market share,\nbut Europe and the US are closing the gap rapidly",
  {
    x: 0.5, y: 0.15, w: 9, h: 0.7,
    fontSize: 20, fontFace: "Georgia", bold: true,
    color: "000000", margin: 0, lineSpacingMultiple: 1.1
  }
);

// === Divider line below title ===
slide.addShape(pres.shapes.LINE, {
  x: 0.5, y: 0.95, w: 9, h: 0,
  line: { color: "333333", width: 1 }
});

// === Subtitle ===
slide.addText("EV market comparison by region, 2024", {
  x: 0.5, y: 1.0, w: 4, h: 0.2,
  fontSize: 10, fontFace: "Calibri", color: "666666", margin: 0
});

// === Navy border above header row ===
slide.addShape(pres.shapes.LINE, {
  x: 0.5, y: 1.25, w: 9, h: 0,
  line: { color: "1B3A5C", width: 2 }
});

// === Table ===
const hdr = (t, fill) => ({ text: t, options: { bold: true, color: "000000", fill: { color: fill || "FFFFFF" }, fontSize: 10, fontFace: "Calibri", align: "center", valign: "middle" } });
const lbl = (t) => ({ text: t, options: { bold: true, color: "000000", fill: { color: "FFFFFF" }, fontSize: 9, fontFace: "Calibri", valign: "middle" } });
const cell = (t) => ({ text: t, options: { color: "333333", fill: { color: "FFFFFF" }, fontSize: 9, fontFace: "Calibri", valign: "middle" } });

const rows = [
  [
    { text: "", options: { fill: { color: "FFFFFF" }, fontSize: 9 } },
    hdr("China", "FDE8E8"),
    hdr("Europe", "DCE9F5"),
    hdr("United States", "E8F6EF")
  ],
  [
    lbl("Market size\n(2024)"),
    cell("~8.1M units sold\n(+25% YoY)"),
    cell("~3.2M units sold\n(+18% YoY)"),
    cell("~1.8M units sold\n(+35% YoY)")
  ],
  [
    lbl("Market share\nof new sales"),
    cell("~45% of all new\ncar sales"),
    cell("~24% of all new\ncar sales"),
    cell("~10% of all new\ncar sales")
  ],
  [
    lbl("Key players"),
    cell("BYD, NIO, XPeng,\nLi Auto, Tesla"),
    cell("VW Group, Stellantis,\nBMW, Mercedes, Tesla"),
    cell("Tesla, GM, Ford,\nHyundai, Rivian")
  ],
  [
    lbl("Government\nincentives"),
    cell("Purchase subsidies phasing\nout; NEV credit system;\nmanufacturing tax breaks"),
    cell("EU CO2 fleet targets;\nnational subsidies\n(varies by country)"),
    cell("$7,500 IRA tax credit;\nstate-level incentives;\ncharging infrastructure funds")
  ],
  [
    lbl("Charging\ninfrastructure"),
    cell("~2.7M public chargers\n(global leader);\nState Grid investment"),
    cell("~630K public chargers;\nEU mandate for highway\ncharging every 60 km"),
    cell("~180K public chargers;\nNEVI program $7.5B;\nlagging vs China/EU")
  ],
  [
    lbl("Market\noutlook"),
    cell("Dominant position; focus\nshifting to exports and\nnext-gen battery tech"),
    cell("Steady growth; regulatory\npressure maintains\nmomentum"),
    cell("Strong growth trajectory;\nIRA driving domestic\nmanufacturing expansion")
  ]
];

slide.addTable(rows, {
  x: 0.5, y: 1.26, w: 9, h: 3.2,
  border: { pt: 0.75, color: "C0C0C0" },
  colW: [1.4, 2.55, 2.55, 2.55],
  rowH: [0.3, 0.4, 0.4, 0.4, 0.5, 0.5, 0.5]
});

// === Footnotes ===
slide.addText(
  "Source: IEA Global EV Outlook 2024; McKinsey Center for Future Mobility; BloombergNEF EV Market Tracker",
  {
    x: 0.5, y: 4.55, w: 8, h: 0.2,
    fontSize: 6.5, fontFace: "Calibri", color: "666666", margin: 0
  }
);

// === Footer line ===
slide.addShape(pres.shapes.LINE, {
  x: 0.5, y: 5.15, w: 9, h: 0,
  line: { color: "333333", width: 0.5 }
});

// === Footer ===
slide.addText("McKinsey & Company    5", {
  x: 7, y: 5.18, w: 2.5, h: 0.2,
  fontSize: 8, fontFace: "Calibri", color: "666666", align: "right", margin: 0
});

pres.writeFile({ fileName: "/Users/lifeichen/Skill-Forge/output/slide_v3.pptx" })
  .then(() => console.log("Created slide_v3.pptx"))
  .catch(err => console.error(err));
