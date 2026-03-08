const pptxgen = require("pptxgenjs");

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.33" x 7.5"
pres.author = "McKinsey & Company";
pres.title = "Dutch Hydrogen Strategy 2020-2035";

const slide = pres.addSlide();
slide.background = { color: "FFFFFF" };

// === COLORS ===
const NAVY = "0C2340";
const CRIMSON = "C00000";
const DARK_GREY = "404040";
const LIGHT_GREY = "E8E8E8";
const MED_GREY = "999999";

// === TITLE ===
slide.addText(
  "The Netherlands aims to become Europe's green hydrogen hub, scaling from 500 MW to 3\u20134 GW by 2030",
  {
    x: 0.5, y: 0.35, w: 12.33, h: 0.85,
    fontFace: "Georgia", fontSize: 22, bold: true, color: "000000",
    valign: "top", margin: 0
  }
);

// === SUBTITLE ===
slide.addText("Dutch Hydrogen Strategy: Key milestones and targets (2020\u20132035)", {
  x: 0.5, y: 1.25, w: 12.33, h: 0.25,
  fontFace: "Calibri", fontSize: 10, color: "888888",
  valign: "top", margin: 0
});

// === CRIMSON DIVIDER ===
slide.addShape(pres.shapes.LINE, {
  x: 0.5, y: 1.55, w: 12.33, h: 0,
  line: { color: CRIMSON, width: 0.75 }
});

// === TIMELINE ===
const timelineY = 2.8;
const timelineStartX = 0.9;
const timelineEndX = 12.43;

// Timeline connector line (2pt navy)
slide.addShape(pres.shapes.LINE, {
  x: timelineStartX, y: timelineY, w: timelineEndX - timelineStartX, h: 0,
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

const nodeR = 0.13; // radius = half of 0.26"
const spacing = (timelineEndX - timelineStartX) / (milestones.length - 1);

milestones.forEach((m, i) => {
  const cx = timelineStartX + i * spacing;

  // Node circle (navy filled)
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

  // Vertical tick mark (1pt navy, 0.15" tall)
  if (m.above) {
    slide.addShape(pres.shapes.LINE, {
      x: cx, y: timelineY - nodeR - 0.15, w: 0, h: 0.15,
      line: { color: NAVY, width: 1 }
    });
    // Label above
    slide.addText(m.label, {
      x: cx - 0.7, y: timelineY - nodeR - 0.15 - 0.45, w: 1.4, h: 0.45,
      fontFace: "Calibri", fontSize: 8.5, color: DARK_GREY,
      align: "center", valign: "bottom", margin: 0
    });
  } else {
    slide.addShape(pres.shapes.LINE, {
      x: cx, y: timelineY + nodeR, w: 0, h: 0.15,
      line: { color: NAVY, width: 1 }
    });
    // Label below
    slide.addText(m.label, {
      x: cx - 0.7, y: timelineY + nodeR + 0.15, w: 1.4, h: 0.45,
      fontFace: "Calibri", fontSize: 8.5, color: DARK_GREY,
      align: "center", valign: "top", margin: 0
    });
  }
});

// === DATA TABLE ===
const tableX = 0.5;
const tableY = 3.7;
const tableW = 12.33;
const colW = [2.83, 1.9, 1.9, 1.9, 1.9, 1.9];

// Border definitions
const navyBorderTop = { pt: 1.5, color: NAVY };
const navyBorderBottom = { pt: 1.5, color: NAVY };
const navyBorderBottomThin = { pt: 1, color: NAVY };
const lightGreyBorder = { pt: 0.5, color: LIGHT_GREY };
const noBorder = { pt: 0, color: "FFFFFF" };

// Header row options (shared)
const headerOptBase = {
  fontFace: "Calibri", fontSize: 8.5, bold: true, color: NAVY, align: "center", valign: "middle",
  border: [navyBorderTop, noBorder, navyBorderBottom, noBorder]
};
const headerOptLeft = { ...headerOptBase, align: "left" };

// Body row options
const bodyOptCenter = {
  fontFace: "Calibri", fontSize: 8, color: DARK_GREY, align: "center", valign: "middle",
  border: [noBorder, noBorder, lightGreyBorder, noBorder]
};
const bodyOptLeft = {
  fontFace: "Calibri", fontSize: 8.5, bold: true, color: "333333", align: "left", valign: "middle",
  border: [noBorder, noBorder, lightGreyBorder, noBorder]
};

// Last row options (navy bottom border)
const lastRowOptCenter = {
  fontFace: "Calibri", fontSize: 8, color: DARK_GREY, align: "center", valign: "middle",
  border: [noBorder, noBorder, navyBorderBottomThin, noBorder]
};
const lastRowOptLeft = {
  fontFace: "Calibri", fontSize: 8.5, bold: true, color: "333333", align: "left", valign: "middle",
  border: [noBorder, noBorder, navyBorderBottomThin, noBorder]
};

const tableData = [
  // Header
  [
    { text: "Metric", options: headerOptLeft },
    { text: "2020", options: { ...headerOptBase } },
    { text: "2025", options: { ...headerOptBase } },
    { text: "2028", options: { ...headerOptBase } },
    { text: "2030", options: { ...headerOptBase } },
    { text: "2035", options: { ...headerOptBase } }
  ],
  // Row 1
  [
    { text: "Electrolyzer capacity (GW)", options: { ...bodyOptLeft } },
    { text: "0.0", options: { ...bodyOptCenter } },
    { text: "0.5", options: { ...bodyOptCenter } },
    { text: "2.0", options: { ...bodyOptCenter } },
    { text: "3\u20134", options: { ...bodyOptCenter } },
    { text: "6\u20138", options: { ...bodyOptCenter } }
  ],
  // Row 2
  [
    { text: "Green H\u2082 cost (\u20AC/kg)", options: { ...bodyOptLeft } },
    { text: "6.0\u20138.0", options: { ...bodyOptCenter } },
    { text: "4.0\u20135.0", options: { ...bodyOptCenter } },
    { text: "2.5\u20133.5", options: { ...bodyOptCenter } },
    { text: "1.5\u20132.5", options: { ...bodyOptCenter } },
    { text: "1.0\u20131.5", options: { ...bodyOptCenter } }
  ],
  // Row 3 (last row - navy bottom border)
  [
    { text: "H\u2082 production (kt/yr)", options: { ...lastRowOptLeft } },
    { text: "<1", options: { ...lastRowOptCenter } },
    { text: "20\u201340", options: { ...lastRowOptCenter } },
    { text: "100\u2013200", options: { ...lastRowOptCenter } },
    { text: "300\u2013500", options: { ...lastRowOptCenter } },
    { text: "800\u20131,200", options: { ...lastRowOptCenter } }
  ]
];

slide.addTable(tableData, {
  x: tableX, y: tableY, w: tableW,
  colW: colW,
  rowH: [0.3, 0.3, 0.3, 0.3],
  margin: [2, 4, 2, 4]
});

// === FOOTNOTE ===
slide.addText("Note: Capacity and cost projections are indicative targets based on national and EU policy documents; actual figures may vary.", {
  x: 0.5, y: 5.2, w: 12.33, h: 0.2,
  fontFace: "Calibri", fontSize: 6.5, italic: true, color: MED_GREY,
  valign: "top", margin: 0
});

// === FOOTER ===
// Footer rule line
slide.addShape(pres.shapes.LINE, {
  x: 0.5, y: 6.45, w: 12.33, h: 0,
  line: { color: "333333", width: 0.5 }
});

// Source text (left)
slide.addText("Source: Dutch Ministry of Economic Affairs and Climate Policy; European Commission REPowerEU; HyNetwork Services", {
  x: 0.5, y: 6.5, w: 8, h: 0.25,
  fontFace: "Calibri", fontSize: 7, color: MED_GREY,
  valign: "top", margin: 0
});

// McKinsey branding (right) + page number
slide.addText([
  { text: "McKinsey & Company", options: { bold: true, fontFace: "Calibri", fontSize: 8, color: "000000" } },
  { text: "  1", options: { fontFace: "Calibri", fontSize: 8, color: "000000" } }
], {
  x: 9.5, y: 6.5, w: 3.33, h: 0.25,
  align: "right", valign: "top", margin: 0
});

// === SAVE ===
pres.writeFile({ fileName: "/Users/lifeichen/Skill-Forge/output/slide_v4.pptx" })
  .then(() => console.log("slide_v4.pptx created successfully"))
  .catch(err => console.error("Error:", err));
