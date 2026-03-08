const pptxgen = require("pptxgenjs");
const pres = new pptxgen();

pres.layout = "LAYOUT_16x9";
pres.author = "Skill-Forge";
pres.title = "H2 Demand and Production Costs";

const slide = pres.addSlide();
slide.background = { color: "FFFFFF" };

// === Title ===
slide.addText(
  "1.1/ Blue H2 is cheaper today, but Green H2 is the 'new solar' with costs decreasing rapidly",
  {
    x: 0.5, y: 0.2, w: 9, h: 0.65,
    fontSize: 16, fontFace: "Georgia", bold: true,
    color: "000000", margin: 0, lineSpacingMultiple: 1.15
  }
);

// === Subtitle ===
slide.addText("Global H2 demand and production costs\u00B9", {
  x: 0.5, y: 0.88, w: 5, h: 0.18,
  fontSize: 9, fontFace: "Calibri", color: "666666", margin: 0
});

// === Divider line ===
slide.addShape(pres.shapes.LINE, {
  x: 0.5, y: 1.1, w: 9, h: 0,
  line: { color: "333333", width: 1 }
});

// === Legend ===
slide.addShape(pres.shapes.RECTANGLE, {
  x: 6.8, y: 1.15, w: 0.15, h: 0.15,
  fill: { color: "000000" }
});
slide.addText("Least-cost option", {
  x: 7.0, y: 1.15, w: 1.2, h: 0.15,
  fontSize: 7, fontFace: "Calibri", color: "333333", margin: 0
});
slide.addShape(pres.shapes.RECTANGLE, {
  x: 8.3, y: 1.15, w: 0.15, h: 0.15,
  fill: { color: "FFFFFF" }, line: { color: "000000", width: 0.5 }
});
slide.addText("2nd least-cost option", {
  x: 8.5, y: 1.15, w: 1.2, h: 0.15,
  fontSize: 7, fontFace: "Calibri", color: "333333", margin: 0
});

// === Navy header border ===
slide.addShape(pres.shapes.LINE, {
  x: 0.5, y: 1.45, w: 9, h: 0,
  line: { color: "1B3A5C", width: 2 }
});

// === Table ===
const hdr = (t) => ({ text: t, options: { bold: true, color: "000000", fill: { color: "FFFFFF" }, fontSize: 9, fontFace: "Calibri", align: "center", valign: "middle" } });
const lbl = (t) => ({ text: t, options: { bold: true, color: "000000", fill: { color: "FFFFFF" }, fontSize: 10, fontFace: "Calibri", valign: "middle" } });
const cell = (t) => ({ text: t, options: { color: "333333", fill: { color: "FFFFFF" }, fontSize: 9, fontFace: "Calibri", align: "center", valign: "middle" } });

const rows = [
  [
    { text: "", options: { fill: { color: "FFFFFF" }, fontSize: 9 } },
    hdr("Global H2\ndemand\nMt p.a."),
    hdr("Thereof\nGrey H2\nMt p.a. (Share %)"),
    hdr("Thereof\nBlue+Green H2\nMt p.a."),
    hdr("Production cost\nGrey H2\n$/kg"),
    hdr("Production cost\nBlue H2\n$/kg"),
    hdr("Production cost\nGreen H2\n$/kg")
  ],
  [
    lbl("2018"),
    cell("73"),
    cell("73 (100%)"),
    cell("~0"),
    cell("\u25A0 ~1.0-2.5"),
    cell("\u25A1 ~1.5-3.0"),
    cell("4.3")
  ],
  [
    lbl("2030"),
    cell("110"),
    cell("73+X (>70%)"),
    cell("Up to 37"),
    cell("\u25A0 ~1.0-2.5"),
    cell("\u25A1 ~1.5-3.0"),
    cell("\u25A1 2.0")
  ],
  [
    lbl("2050"),
    cell("545"),
    cell("73+/-X (<20%)"),
    cell("Up to 472"),
    cell("\u201C"),
    cell("\u201C"),
    cell("\u25A0 1.3")
  ]
];

slide.addTable(rows, {
  x: 0.5, y: 1.46, w: 9, h: 1.8,
  border: { pt: 0.5, color: "D0D0D0" },
  colW: [0.7, 1.1, 1.5, 1.2, 1.1, 1.1, 1.3],
  rowH: [0.55, 0.4, 0.4, 0.4]
});

// === Additional context text ===
slide.addText(
  "Green hydrogen cost trajectory follows a similar pattern to solar PV, which saw an 89% cost\n" +
  "reduction between 2010-2020. Key drivers include falling electrolyzer costs, increasing renewable\n" +
  "energy availability, and scaling of manufacturing capacity.",
  {
    x: 0.5, y: 3.45, w: 9, h: 0.5,
    fontSize: 9, fontFace: "Calibri", color: "333333", margin: 0,
    lineSpacingMultiple: 1.3
  }
);

// === Footnotes ===
slide.addText(
  "1.  Estimates by Hydrogen Council; Grey H2 production costs assuming natural gas prices of $4-$8/mmBtu; Blue H2 costs assuming Grey costs + $0.5/kg;\n" +
  "     Green H2 costs assuming IRENA database weighted average solar PV costs (auctions and PPAs) in 2020",
  {
    x: 0.5, y: 4.55, w: 8.5, h: 0.3,
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
slide.addText("McKinsey & Company    5", {
  x: 7, y: 5.15, w: 2.5, h: 0.2,
  fontSize: 8, fontFace: "Calibri", color: "666666", align: "right", margin: 0
});

pres.writeFile({ fileName: "/Users/lifeichen/Skill-Forge/output/slide_v4.pptx" })
  .then(() => console.log("Created slide_v4.pptx"))
  .catch(err => console.error(err));
