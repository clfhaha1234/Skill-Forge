const pptxgen = require("pptxgenjs");

let pres = new pptxgen();
pres.layout = "LAYOUT_16x10"; // 10" x 6.25" -- more vertical room
pres.author = "McKinsey & Company";
pres.title = "Dutch Hydrogen Strategy";

let slide = pres.addSlide();
slide.background = { color: "FFFFFF" };

// ── COLORS ──
const NAVY = "0C2340";
const CRIMSON = "C00000";
const BODY_GREY = "404040";
const SUBTLE_GREY = "E8E8E8";
const FOOTNOTE_GREY = "999999";
const SUBTITLE_GREY = "888888";

// ══════════════════════════════════════════════
// TITLE — insight / conclusion style
// ══════════════════════════════════════════════
slide.addText(
  "The Netherlands aims to become Europe's green hydrogen hub, scaling from 500 MW to 3\u20134 GW by 2030",
  {
    x: 0.5, y: 0.35, w: 9.0, h: 0.8,
    fontFace: "Georgia", fontSize: 22, bold: true,
    color: "000000", align: "left", valign: "top",
    margin: 0
  }
);

// ── SUBTITLE ──
slide.addText(
  "Dutch Hydrogen Strategy timeline and key capacity milestones, 2020\u20132035",
  {
    x: 0.5, y: 1.2, w: 9.0, h: 0.3,
    fontFace: "Calibri", fontSize: 10,
    color: SUBTITLE_GREY, align: "left",
    margin: 0
  }
);

// ── CRIMSON DIVIDER (0.75pt) ──
slide.addShape(pres.shapes.LINE, {
  x: 0.5, y: 1.5, w: 9.0, h: 0,
  line: { color: CRIMSON, width: 0.75 }
});

// ══════════════════════════════════════════════
// TIMELINE
// ══════════════════════════════════════════════

const milestones = [
  { year: "2020", label: "National Hydrogen\nStrategy published", above: true },
  { year: "2022", label: "REPowerEU plan\naccelerates ambitions", above: false },
  { year: "2025", label: "First green H2\nhubs operational", above: true },
  { year: "2028", label: "HyNetwork backbone\npipeline live", above: false },
  { year: "2030", label: "Scale-up phase\ncomplete", above: true },
  { year: "2035", label: "EU hydrogen corridor\nintegration", above: false }
];

const timelineY = 2.9;
const timelineStartX = 1.0;
const timelineEndX = 9.0;
const timelineW = timelineEndX - timelineStartX;
const nodeSize = 0.28;

// Horizontal timeline line
slide.addShape(pres.shapes.LINE, {
  x: timelineStartX, y: timelineY, w: timelineW, h: 0,
  line: { color: NAVY, width: 1.5 }
});

// Nodes and labels
milestones.forEach((m, i) => {
  const cx = timelineStartX + (i / (milestones.length - 1)) * timelineW;
  const nodeX = cx - nodeSize / 2;
  const nodeY = timelineY - nodeSize / 2;

  // Navy circle node
  slide.addShape(pres.shapes.OVAL, {
    x: nodeX, y: nodeY, w: nodeSize, h: nodeSize,
    fill: { color: NAVY }
  });

  // Year text inside node
  slide.addText(m.year, {
    x: nodeX, y: nodeY, w: nodeSize, h: nodeSize,
    fontFace: "Calibri", fontSize: 8, bold: true,
    color: "FFFFFF", align: "center", valign: "middle",
    margin: 0
  });

  // Milestone description — alternate above/below
  const labelW = 1.3;
  if (m.above) {
    slide.addText(m.label, {
      x: cx - labelW / 2, y: timelineY - 0.95, w: labelW, h: 0.55,
      fontFace: "Calibri", fontSize: 8.5,
      color: BODY_GREY, align: "center", valign: "bottom",
      margin: 0
    });
  } else {
    slide.addText(m.label, {
      x: cx - labelW / 2, y: timelineY + 0.22, w: labelW, h: 0.55,
      fontFace: "Calibri", fontSize: 8.5,
      color: BODY_GREY, align: "center", valign: "top",
      margin: 0
    });
  }
});

// ══════════════════════════════════════════════
// DATA TABLE
// ══════════════════════════════════════════════

const tableX = 0.5;
const tableY = 3.9;
const tableW = 9.0;
const colW = [2.2, 1.36, 1.36, 1.36, 1.36, 1.36]; // label col + 5 data cols

const headerOpts = {
  fontFace: "Calibri", fontSize: 8.5, bold: true,
  color: NAVY, align: "center", valign: "middle",
  margin: [2, 4, 2, 4]
};

const bodyOpts = {
  fontFace: "Calibri", fontSize: 8,
  color: BODY_GREY, align: "center", valign: "middle",
  margin: [2, 4, 2, 4]
};

const labelOpts = {
  fontFace: "Calibri", fontSize: 8.5, bold: true,
  color: "333333", align: "left", valign: "middle",
  margin: [2, 4, 2, 4]
};

// Header row — navy border top+bottom, NO fill
const headerRow = [
  { text: "Metric", options: { ...headerOpts, align: "left" } },
  { text: "2020", options: { ...headerOpts } },
  { text: "2025", options: { ...headerOpts } },
  { text: "2028", options: { ...headerOpts } },
  { text: "2030", options: { ...headerOpts } },
  { text: "2035", options: { ...headerOpts } }
];

// Data rows
const row1 = [
  { text: "Electrolyzer Capacity (GW)", options: { ...labelOpts } },
  { text: "0.5", options: { ...bodyOpts } },
  { text: "1.0", options: { ...bodyOpts } },
  { text: "2.0", options: { ...bodyOpts } },
  { text: "3\u20134", options: { ...bodyOpts } },
  { text: "6\u20138", options: { ...bodyOpts } }
];

const row2 = [
  { text: "Green H\u2082 Cost (\u20AC/kg)", options: { ...labelOpts } },
  { text: "6.0", options: { ...bodyOpts } },
  { text: "3.5", options: { ...bodyOpts } },
  { text: "2.5", options: { ...bodyOpts } },
  { text: "2.0", options: { ...bodyOpts } },
  { text: "1.5", options: { ...bodyOpts } }
];

const row3 = [
  { text: "H\u2082 Production (kt/yr)", options: { ...labelOpts } },
  { text: "~10", options: { ...bodyOpts } },
  { text: "~80", options: { ...bodyOpts } },
  { text: "~200", options: { ...bodyOpts } },
  { text: "~400", options: { ...bodyOpts } },
  { text: "~800", options: { ...bodyOpts } }
];

const tableRows = [headerRow, row1, row2, row3];

// Build per-cell borders
// Header: top 1.5pt navy, bottom 1.5pt navy, no left/right
const headerBorder = [
  { pt: 1.5, color: NAVY },   // top
  { pt: 0, color: "FFFFFF" },  // right
  { pt: 1.5, color: NAVY },   // bottom
  { pt: 0, color: "FFFFFF" }   // left
];

// Body rows 1,2: subtle bottom border
const bodyBorder = [
  { pt: 0, color: "FFFFFF" },
  { pt: 0, color: "FFFFFF" },
  { pt: 0.5, color: SUBTLE_GREY },
  { pt: 0, color: "FFFFFF" }
];

// Last row: navy bottom border to close table
const lastRowBorder = [
  { pt: 0, color: "FFFFFF" },
  { pt: 0, color: "FFFFFF" },
  { pt: 1, color: NAVY },
  { pt: 0, color: "FFFFFF" }
];

// Apply borders to cells
headerRow.forEach(cell => { cell.options.border = headerBorder; });
row1.forEach(cell => { cell.options.border = bodyBorder; });
row2.forEach(cell => { cell.options.border = bodyBorder; });
row3.forEach(cell => { cell.options.border = lastRowBorder; });

slide.addTable(tableRows, {
  x: tableX, y: tableY, w: tableW,
  colW: colW,
  rowH: [0.3, 0.28, 0.28, 0.28],
  margin: 0
});

// ══════════════════════════════════════════════
// FOOTNOTE
// ══════════════════════════════════════════════
slide.addText(
  "Note: Capacity targets based on Dutch National Hydrogen Strategy and EU REPowerEU plan; cost projections are indicative estimates.",
  {
    x: 0.5, y: 5.3, w: 9.0, h: 0.25,
    fontFace: "Calibri", fontSize: 7, italic: true,
    color: FOOTNOTE_GREY, align: "left",
    margin: 0
  }
);

// ══════════════════════════════════════════════
// FOOTER
// ══════════════════════════════════════════════

// Footer rule
slide.addShape(pres.shapes.LINE, {
  x: 0.5, y: 6.85, w: 9.0, h: 0,
  line: { color: "333333", width: 0.5 }
});

// Source (left)
slide.addText(
  "Source: Dutch Ministry of Economic Affairs; European Commission; McKinsey analysis",
  {
    x: 0.5, y: 6.9, w: 6.0, h: 0.25,
    fontFace: "Calibri", fontSize: 7,
    color: FOOTNOTE_GREY, align: "left",
    margin: 0
  }
);

// Branding (right)
slide.addText([
  { text: "McKinsey & Company", options: { bold: true, fontSize: 8, color: "000000" } },
  { text: "  1", options: { fontSize: 8, color: FOOTNOTE_GREY } }
], {
  x: 7.0, y: 6.9, w: 2.5, h: 0.25,
  fontFace: "Calibri", align: "right",
  margin: 0
});

// ── SAVE ──
pres.writeFile({ fileName: "output/slide_v2.pptx" })
  .then(() => console.log("Created slide_v2.pptx"))
  .catch(err => console.error(err));
