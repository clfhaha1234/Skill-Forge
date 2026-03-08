const pptxgen = require("pptxgenjs");

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.33" x 7.5"
pres.author = "McKinsey & Company";
pres.title = "Dutch Hydrogen Strategy";

const slide = pres.addSlide();
slide.background = { color: "FFFFFF" };

// === COLORS ===
const NAVY = "0C2340";
const BLACK = "000000";
const DARK_GREY = "333333";
const BODY_GREY = "404040";
const LIGHT_GREY = "E8E8E8";
const MED_GREY = "999999";
const SUBTITLE_GREY = "888888";

// === TITLE ===
slide.addText(
  "The Netherlands aims to become Europe's green hydrogen hub, scaling from 500 MW to 3\u20134 GW by 2030",
  {
    x: 0.5, y: 0.3, w: 12.33, h: 0.85,
    fontFace: "Georgia", fontSize: 22, bold: true, color: BLACK,
    valign: "top", margin: 0, wrap: true
  }
);

// === SUBTITLE ===
slide.addText("Dutch National Hydrogen Strategy timeline and key capacity milestones (2020\u20132035)", {
  x: 0.5, y: 1.2, w: 12.33, h: 0.25,
  fontFace: "Calibri", fontSize: 10, color: SUBTITLE_GREY,
  valign: "top", margin: 0
});

// === DIVIDER LINE (DARK GREY, NOT RED) ===
slide.addShape(pres.shapes.LINE, {
  x: 0.5, y: 1.45, w: 12.33, h: 0,
  line: { color: DARK_GREY, width: 0.75 }
});

// === TIMELINE ===
const timelineY = 2.5; // y position for the horizontal line
const timelineStartX = 1.0;
const timelineEndX = 12.0;
const timelineW = timelineEndX - timelineStartX;

// Horizontal navy line
slide.addShape(pres.shapes.LINE, {
  x: timelineStartX, y: timelineY, w: timelineW, h: 0,
  line: { color: NAVY, width: 2 }
});

// Milestones
const milestones = [
  { year: "2020", label: "National Hydrogen\nStrategy published", above: true },
  { year: "2022", label: "REPowerEU plan\naccelerates ambitions", above: false },
  { year: "2025", label: "First green H2\nhubs operational", above: true },
  { year: "2028", label: "HyNetwork backbone\npipeline live", above: false },
  { year: "2030", label: "Scale-up phase\ncomplete", above: true },
  { year: "2035", label: "EU hydrogen corridor\nintegration", above: false }
];

const nodeR = 0.13; // radius = 0.26/2
const spacing = timelineW / (milestones.length - 1);

milestones.forEach((m, i) => {
  const cx = timelineStartX + i * spacing;

  // Vertical tick mark
  const tickLen = 0.3;
  if (m.above) {
    slide.addShape(pres.shapes.LINE, {
      x: cx, y: timelineY - tickLen, w: 0, h: tickLen,
      line: { color: NAVY, width: 1 }
    });
  } else {
    slide.addShape(pres.shapes.LINE, {
      x: cx, y: timelineY, w: 0, h: tickLen,
      line: { color: NAVY, width: 1 }
    });
  }

  // Circle node
  slide.addShape(pres.shapes.OVAL, {
    x: cx - nodeR, y: timelineY - nodeR, w: 0.26, h: 0.26,
    fill: { color: NAVY }
  });

  // Year label inside node
  slide.addText(m.year, {
    x: cx - nodeR, y: timelineY - nodeR, w: 0.26, h: 0.26,
    fontFace: "Calibri", fontSize: 7.5, bold: true, color: "FFFFFF",
    align: "center", valign: "middle", margin: 0
  });

  // Milestone description
  const labelW = 1.6;
  if (m.above) {
    slide.addText(m.label, {
      x: cx - labelW / 2, y: timelineY - tickLen - 0.55, w: labelW, h: 0.5,
      fontFace: "Calibri", fontSize: 8.5, color: BODY_GREY,
      align: "center", valign: "bottom", margin: 0
    });
  } else {
    slide.addText(m.label, {
      x: cx - labelW / 2, y: timelineY + tickLen + 0.05, w: labelW, h: 0.5,
      fontFace: "Calibri", fontSize: 8.5, color: BODY_GREY,
      align: "center", valign: "top", margin: 0
    });
  }
});

// === DATA TABLE ===
const tableX = 0.5;
const tableY = 3.5;
const tableW = 12.33;
const colW = [2.33, 2.0, 2.0, 2.0, 2.0, 2.0];

// Border helpers
const navyBorderTop = { pt: 1.5, color: NAVY };
const navyBorderBot = { pt: 1.5, color: NAVY };
const navyBorderBotThin = { pt: 1, color: NAVY };
const lightBorderBot = { pt: 0.5, color: LIGHT_GREY };
const noBorder = { pt: 0, color: "FFFFFF" };

// Header row
const headerRow = [
  { text: "Metric", options: { fontFace: "Calibri", fontSize: 9, bold: true, color: NAVY, align: "left", border: [navyBorderTop, noBorder, navyBorderBot, noBorder] } },
  { text: "2020", options: { fontFace: "Calibri", fontSize: 9, bold: true, color: NAVY, align: "center", border: [navyBorderTop, noBorder, navyBorderBot, noBorder] } },
  { text: "2025", options: { fontFace: "Calibri", fontSize: 9, bold: true, color: NAVY, align: "center", border: [navyBorderTop, noBorder, navyBorderBot, noBorder] } },
  { text: "2028", options: { fontFace: "Calibri", fontSize: 9, bold: true, color: NAVY, align: "center", border: [navyBorderTop, noBorder, navyBorderBot, noBorder] } },
  { text: "2030", options: { fontFace: "Calibri", fontSize: 9, bold: true, color: NAVY, align: "center", border: [navyBorderTop, noBorder, navyBorderBot, noBorder] } },
  { text: "2035", options: { fontFace: "Calibri", fontSize: 9, bold: true, color: NAVY, align: "center", border: [navyBorderTop, noBorder, navyBorderBot, noBorder] } }
];

// Data rows
function dataRow(label, values, isLast) {
  const botBorder = isLast ? navyBorderBotThin : lightBorderBot;
  const cells = [
    { text: label, options: { fontFace: "Calibri", fontSize: 9, bold: true, color: "222222", align: "left", border: [noBorder, noBorder, botBorder, noBorder] } }
  ];
  values.forEach(v => {
    cells.push({
      text: v, options: { fontFace: "Calibri", fontSize: 8, color: BODY_GREY, align: "center", border: [noBorder, noBorder, botBorder, noBorder] }
    });
  });
  return cells;
}

const tableData = [
  headerRow,
  dataRow("Electrolyzer capacity (GW)", ["~0.01", "0.5", "2.0", "3\u20134", "8+"], false),
  dataRow("Green H2 production (kt/yr)", ["<1", "~50", "~200", "~500", "~1,200"], false),
  dataRow("Infrastructure investment (\u20ACbn)", ["0.5", "3.5", "9", "15", "25+"], true)
];

slide.addTable(tableData, {
  x: tableX, y: tableY, w: tableW, colW: colW,
  rowH: [0.35, 0.32, 0.32, 0.32],
  margin: [2, 4, 2, 4]
});

// === FOOTNOTE ===
slide.addText("Note: Capacity targets reflect government ambitions as of 2024; actual deployment subject to policy and market conditions.", {
  x: 0.5, y: 5.0, w: 12.33, h: 0.2,
  fontFace: "Calibri", fontSize: 6.5, italic: true, color: MED_GREY,
  valign: "top", margin: 0
});

// === FOOTER RULE ===
slide.addShape(pres.shapes.LINE, {
  x: 0.5, y: 6.4, w: 12.33, h: 0,
  line: { color: DARK_GREY, width: 0.5 }
});

// === FOOTER TEXT ===
slide.addText("Source: Government of the Netherlands, National Hydrogen Strategy; European Commission, REPowerEU Plan (2022).", {
  x: 0.5, y: 6.45, w: 8, h: 0.2,
  fontFace: "Calibri", fontSize: 7, color: MED_GREY,
  valign: "top", margin: 0
});

slide.addText([
  { text: "McKinsey & Company", options: { bold: true, fontFace: "Calibri", fontSize: 8, color: BLACK } },
  { text: "  1", options: { fontFace: "Calibri", fontSize: 8, color: BLACK } }
], {
  x: 8.5, y: 6.45, w: 4.33, h: 0.2,
  align: "right", valign: "top", margin: 0
});

// === SAVE ===
pres.writeFile({ fileName: "/Users/lifeichen/Skill-Forge/output/slide_v5.pptx" })
  .then(() => console.log("slide_v5.pptx created successfully"))
  .catch(err => console.error("Error:", err));
