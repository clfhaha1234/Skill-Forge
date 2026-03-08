const pptxgen = require("pptxgenjs");
const pres = new pptxgen();

pres.layout = "LAYOUT_16x9";
pres.author = "Skill-Forge";
pres.title = "EV Market Comparison";

const slide = pres.addSlide();
slide.background = { color: "FFFFFF" };

// === Title ===
slide.addText(
  "1.2/ China leads the global EV transition with 60% market share,\nbut Europe and the US are closing the gap rapidly",
  {
    x: 0.4, y: 0.25, w: 8.2, h: 0.65,
    fontSize: 16, fontFace: "Georgia", bold: true,
    color: "000000", margin: 0, lineSpacingMultiple: 1.2
  }
);

// === Divider line ===
slide.addShape(pres.shapes.LINE, {
  x: 0.4, y: 0.98, w: 9.2, h: 0,
  line: { color: "333333", width: 0.75 }
});

// === Subtitle ===
slide.addText("EV market comparison by region, 2024", {
  x: 0.4, y: 1.03, w: 4, h: 0.17,
  fontSize: 8.5, fontFace: "Calibri", color: "666666", margin: 0
});

// === Navy header border ===
slide.addShape(pres.shapes.LINE, {
  x: 0.4, y: 1.25, w: 9.2, h: 0,
  line: { color: "1B3A5C", width: 2 }
});

// === Table ===
const noBorder = { pt: 0, color: "FFFFFF" };
const hBorder = { pt: 0.5, color: "D0D0D0" };
const hdrBBot = { pt: 1, color: "333333" };

const CHINA = "FCE4E4";
const EUROPE = "DDEAF6";
const US = "D5EDDB";

const hdrW = (t) => ({ text: t, options: { bold: true, color: "000000", fill: { color: "FFFFFF" }, fontSize: 9, fontFace: "Calibri", align: "center", valign: "middle", border: [noBorder, noBorder, hdrBBot, noBorder] } });
const hdrC = (t) => ({ text: t, options: { bold: true, color: "000000", fill: { color: CHINA }, fontSize: 9, fontFace: "Calibri", align: "center", valign: "middle", border: [noBorder, noBorder, hdrBBot, noBorder] } });
const hdrE = (t) => ({ text: t, options: { bold: true, color: "000000", fill: { color: EUROPE }, fontSize: 9, fontFace: "Calibri", align: "center", valign: "middle", border: [noBorder, noBorder, hdrBBot, noBorder] } });
const hdrU = (t) => ({ text: t, options: { bold: true, color: "000000", fill: { color: US }, fontSize: 9, fontFace: "Calibri", align: "center", valign: "middle", border: [noBorder, noBorder, hdrBBot, noBorder] } });
const lbl = (t) => ({ text: t, options: { bold: true, color: "000000", fill: { color: "FFFFFF" }, fontSize: 8, fontFace: "Calibri", valign: "middle", border: [hBorder, noBorder, hBorder, noBorder] } });
const cC = (t) => ({ text: t, options: { color: "333333", fill: { color: CHINA }, fontSize: 8, fontFace: "Calibri", valign: "middle", border: [hBorder, noBorder, hBorder, noBorder] } });
const cE = (t) => ({ text: t, options: { color: "333333", fill: { color: EUROPE }, fontSize: 8, fontFace: "Calibri", valign: "middle", border: [hBorder, noBorder, hBorder, noBorder] } });
const cU = (t) => ({ text: t, options: { color: "333333", fill: { color: US }, fontSize: 8, fontFace: "Calibri", valign: "middle", border: [hBorder, noBorder, hBorder, noBorder] } });

const rows = [
  [
    { text: "", options: { fill: { color: "FFFFFF" }, fontSize: 8, border: [noBorder, noBorder, hdrBBot, noBorder] } },
    hdrC("China"),
    hdrE("Europe"),
    hdrU("United States")
  ],
  [
    lbl("Market size\n(2024)"),
    cC("~8.1M units sold (+25% YoY)"),
    cE("~3.2M units sold (+18% YoY)"),
    cU("~1.8M units sold (+35% YoY)")
  ],
  [
    lbl("Market share\nof new sales"),
    cC("~45% of all new car sales"),
    cE("~24% of all new car sales"),
    cU("~10% of all new car sales")
  ],
  [
    lbl("Key players"),
    cC("BYD, NIO, XPeng,\nLi Auto, Tesla"),
    cE("VW Group, Stellantis,\nBMW, Mercedes, Tesla"),
    cU("Tesla, GM, Ford,\nHyundai, Rivian")
  ],
  [
    lbl("Government\nincentives"),
    cC("NEV credit system;\nmanufacturing tax breaks"),
    cE("EU CO2 fleet targets;\nnational subsidies"),
    cU("$7,500 IRA tax credit;\nstate-level incentives")
  ],
  [
    lbl("Charging\ninfrastructure"),
    cC("~2.7M public chargers\n(global leader)"),
    cE("~630K public chargers;\nEU highway mandate"),
    cU("~180K public chargers;\nNEVI program $7.5B")
  ],
  [
    lbl("Market\noutlook"),
    cC("Dominant; shifting to\nexports and next-gen tech"),
    cE("Steady growth driven\nby regulatory pressure"),
    cU("Strong trajectory; IRA\ndriving domestic mfg.")
  ]
];

slide.addTable(rows, {
  x: 0.4, y: 1.26, w: 9.2, h: 2.95,
  border: noBorder,
  colW: [1.2, 2.65, 2.65, 2.7],
  rowH: [0.28, 0.32, 0.32, 0.42, 0.42, 0.42, 0.42],
  autoPage: false
});

// === Source ===
slide.addText(
  "Source: IEA Global EV Outlook 2024; McKinsey Center for Future Mobility; BloombergNEF EV Market Tracker",
  {
    x: 0.4, y: 4.3, w: 8.8, h: 0.2,
    fontSize: 6.5, fontFace: "Calibri", color: "555555", margin: 0
  }
);

// === Footer line ===
slide.addShape(pres.shapes.LINE, {
  x: 0.4, y: 5.05, w: 9.2, h: 0,
  line: { color: "333333", width: 0.5 }
});

// === Footer ===
slide.addText("McKinsey & Company    5", {
  x: 7.2, y: 5.1, w: 2.4, h: 0.2,
  fontSize: 8, fontFace: "Calibri", color: "666666", align: "right", margin: 0
});

pres.writeFile({ fileName: "/Users/lifeichen/Skill-Forge/output/slide_v7_ev.pptx" })
  .then(() => console.log("Created slide_v7_ev.pptx"))
  .catch(err => console.error(err));
