const pptxgen = require("pptxgenjs");

const pres = new pptxgen();
pres.layout = "LAYOUT_16x10"; // 10" x 6.25" — more vertical space for table+footer
pres.author = "McKinsey & Company";
pres.title = "Dutch Hydrogen Strategy";

const slide = pres.addSlide();
slide.background = { color: "FFFFFF" };

// ── Colors ──
const NAVY = "0C2340";
const CRIMSON = "C00000";
const BLACK = "000000";
const DARK_GREY = "404040";
const MID_GREY = "666666";
const LIGHT_GREY = "E8E8E8";
const FOOTNOTE_GREY = "999999";

// ── Title (insight, not topic label) ──
slide.addText(
  "The Netherlands aims to become Europe's green hydrogen hub, scaling from 500 MW to 3\u20134 GW by 2030",
  {
    x: 0.5, y: 0.4, w: 9.0, h: 0.7,
    fontFace: "Georgia", fontSize: 22, bold: true,
    color: BLACK, align: "left", valign: "top",
    margin: 0,
  }
);

// ── Subtitle ──
slide.addText(
  "Dutch National Hydrogen Strategy timeline and key metrics (2020\u20132035)",
  {
    x: 0.5, y: 1.15, w: 9.0, h: 0.25,
    fontFace: "Calibri", fontSize: 11,
    color: MID_GREY, align: "left", valign: "top",
    margin: 0,
  }
);

// ── Crimson divider line ──
slide.addShape(pres.shapes.LINE, {
  x: 0.5, y: 1.5, w: 9.0, h: 0,
  line: { color: CRIMSON, width: 1 },
});

// ── Timeline ──
const timelineY = 2.6;
const timelineStartX = 0.8;
const timelineEndX = 9.2;
const timelineW = timelineEndX - timelineStartX;

// Horizontal navy line
slide.addShape(pres.shapes.LINE, {
  x: timelineStartX, y: timelineY, w: timelineW, h: 0,
  line: { color: NAVY, width: 1.5 },
});

// Milestones
const milestones = [
  { year: "2020", desc: "National Hydrogen\nStrategy published" },
  { year: "2022", desc: "REPowerEU plan\naccelerates ambitions" },
  { year: "2025", desc: "First green H2\nhubs operational" },
  { year: "2028", desc: "HyNetwork backbone\npipeline live" },
  { year: "2030", desc: "Scale-up phase\ncomplete" },
  { year: "2035", desc: "EU hydrogen corridor\nintegration" },
];

const nodeD = 0.3; // diameter
const spacing = timelineW / (milestones.length - 1);

milestones.forEach((m, i) => {
  const cx = timelineStartX + i * spacing;
  const nodeX = cx - nodeD / 2;
  const nodeY = timelineY - nodeD / 2;

  // Navy circle node
  slide.addShape(pres.shapes.OVAL, {
    x: nodeX, y: nodeY, w: nodeD, h: nodeD,
    fill: { color: NAVY },
  });

  // Year label inside node
  slide.addText(m.year, {
    x: nodeX, y: nodeY, w: nodeD, h: nodeD,
    fontFace: "Calibri", fontSize: 7, color: "FFFFFF",
    align: "center", valign: "middle", margin: 0,
  });

  // Milestone description — alternate above/below
  const isAbove = i % 2 === 0;
  const descY = isAbove ? timelineY - 0.7 : timelineY + 0.25;

  slide.addText(m.desc, {
    x: cx - 0.65, y: descY, w: 1.3, h: 0.45,
    fontFace: "Calibri", fontSize: 8.5, color: DARK_GREY,
    align: "center", valign: isAbove ? "bottom" : "top",
    margin: 0,
  });
});

// ── Data Table ──
const tableX = 0.5;
const tableY = 3.55;
const tableW = 9.0;
const colW = [2.0, 1.4, 1.4, 1.4, 1.4, 1.4]; // metric + 5 year cols

const headerStyle = {
  fontFace: "Calibri", fontSize: 8, bold: true, color: "FFFFFF",
  fill: { color: NAVY }, align: "center", valign: "middle",
  border: [
    { pt: 1.5, color: NAVY }, // top
    { pt: 0, color: "FFFFFF" }, // right
    { pt: 1.5, color: NAVY }, // bottom
    { pt: 0, color: "FFFFFF" }, // left
  ],
};

const headerLabelStyle = Object.assign({}, headerStyle, { align: "left" });

const cellStyle = {
  fontFace: "Calibri", fontSize: 8, color: DARK_GREY,
  align: "center", valign: "middle",
  border: [
    { pt: 0, color: LIGHT_GREY },
    { pt: 0, color: "FFFFFF" },
    { pt: 0.5, color: LIGHT_GREY },
    { pt: 0, color: "FFFFFF" },
  ],
};

const labelStyle = Object.assign({}, cellStyle, { align: "left", bold: true });

const tableRows = [
  // Header
  [
    { text: "Metric", options: headerLabelStyle },
    { text: "2020", options: Object.assign({}, headerStyle) },
    { text: "2025", options: Object.assign({}, headerStyle) },
    { text: "2028", options: Object.assign({}, headerStyle) },
    { text: "2030", options: Object.assign({}, headerStyle) },
    { text: "2035", options: Object.assign({}, headerStyle) },
  ],
  // Electrolyzer Capacity
  [
    { text: "Electrolyzer Capacity (GW)", options: Object.assign({}, labelStyle) },
    { text: "~0.5", options: Object.assign({}, cellStyle) },
    { text: "1.0", options: Object.assign({}, cellStyle) },
    { text: "2.0", options: Object.assign({}, cellStyle) },
    { text: "3\u20134", options: Object.assign({}, cellStyle) },
    { text: "6\u20138", options: Object.assign({}, cellStyle) },
  ],
  // Green H2 Cost
  [
    { text: "Green H2 Cost (\u20AC/kg)", options: Object.assign({}, labelStyle) },
    { text: "5.0\u20136.0", options: Object.assign({}, cellStyle) },
    { text: "3.5\u20134.0", options: Object.assign({}, cellStyle) },
    { text: "2.5\u20133.0", options: Object.assign({}, cellStyle) },
    { text: "2.0\u20132.5", options: Object.assign({}, cellStyle) },
    { text: "1.5\u20132.0", options: Object.assign({}, cellStyle) },
  ],
  // H2 Production
  [
    { text: "H2 Production (kt/yr)", options: Object.assign({}, labelStyle) },
    { text: "< 10", options: Object.assign({}, cellStyle) },
    { text: "80\u2013100", options: Object.assign({}, cellStyle) },
    { text: "200\u2013300", options: Object.assign({}, cellStyle) },
    { text: "400\u2013500", options: Object.assign({}, cellStyle) },
    { text: "800\u20131,000", options: Object.assign({}, cellStyle) },
  ],
];

slide.addTable(tableRows, {
  x: tableX, y: tableY, w: tableW,
  colW: colW,
  rowH: [0.3, 0.28, 0.28, 0.28],
  margin: [2, 4, 2, 4],
});

// ── Footnote ──
slide.addText(
  "1. Capacity and cost projections based on Dutch Government targets and IEA estimates; actual figures may vary depending on policy and market conditions.",
  {
    x: 0.5, y: 4.85, w: 9.0, h: 0.25,
    fontFace: "Calibri", fontSize: 7, italic: true,
    color: FOOTNOTE_GREY, align: "left", valign: "top",
    margin: 0,
  }
);

// ── Footer ──
// Thin dark rule line
slide.addShape(pres.shapes.LINE, {
  x: 0.5, y: 5.75, w: 9.0, h: 0,
  line: { color: DARK_GREY, width: 0.75 },
});

// Source (left)
slide.addText(
  "Source: Dutch National Hydrogen Strategy; REPowerEU; McKinsey Energy Insights",
  {
    x: 0.5, y: 5.8, w: 6.5, h: 0.25,
    fontFace: "Calibri", fontSize: 7,
    color: FOOTNOTE_GREY, align: "left", valign: "top",
    margin: 0,
  }
);

// McKinsey & Company (right) + page number
slide.addText(
  [
    { text: "McKinsey & Company", options: { bold: true, fontSize: 8, color: BLACK } },
    { text: "   1", options: { bold: false, fontSize: 8, color: FOOTNOTE_GREY } },
  ],
  {
    x: 7.0, y: 5.8, w: 2.5, h: 0.25,
    fontFace: "Calibri", align: "right", valign: "top",
    margin: 0,
  }
);

// ── Write file ──
pres.writeFile({ fileName: "output/slide_v1.pptx" })
  .then(() => console.log("Created slide_v1.pptx"))
  .catch((err) => console.error(err));
