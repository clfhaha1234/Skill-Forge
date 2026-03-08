const pptxgen = require("pptxgenjs");

let pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.33" x 7.5"
pres.author = "McKinsey & Company";
pres.title = "Dutch Hydrogen Strategy";

let slide = pres.addSlide();
slide.background = { color: "FFFFFF" };

// ─── TITLE ───
slide.addText(
  "The Netherlands aims to become Europe's green hydrogen hub,\nscaling from 500 MW to 3-4 GW by 2030",
  {
    x: 0.5, y: 0.35, w: 12.33, h: 0.85,
    fontFace: "Georgia", fontSize: 22, bold: true, color: "000000",
    valign: "top", margin: 0
  }
);

// ─── SUBTITLE ───
slide.addText("Dutch National Hydrogen Strategy timeline, 2020-2035", {
  x: 0.5, y: 1.25, w: 12.33, h: 0.25,
  fontFace: "Calibri", fontSize: 10, color: "888888",
  valign: "top", margin: 0
});

// ─── CRIMSON DIVIDER ───
slide.addShape(pres.shapes.LINE, {
  x: 0.5, y: 1.55, w: 12.33, h: 0,
  line: { color: "C00000", width: 0.75 }
});

// ─── TIMELINE ───
const timelineY = 2.9;
const timelineStartX = 1.0;
const timelineEndX = 12.0;
const nodeCount = 6;
const spacing = (timelineEndX - timelineStartX) / (nodeCount - 1);
const nodeDiam = 0.26;

// Timeline horizontal line
slide.addShape(pres.shapes.LINE, {
  x: timelineStartX, y: timelineY, w: timelineEndX - timelineStartX, h: 0,
  line: { color: "0C2340", width: 1.5 }
});

const milestones = [
  { year: "2020", label: "National Hydrogen\nStrategy published" },
  { year: "2022", label: "REPowerEU plan\naccelerates ambitions" },
  { year: "2025", label: "First green H2\nhubs operational" },
  { year: "2028", label: "HyNetwork backbone\npipeline live" },
  { year: "2030", label: "Scale-up phase\ncomplete" },
  { year: "2035", label: "EU hydrogen corridor\nintegration" }
];

milestones.forEach((m, i) => {
  const cx = timelineStartX + i * spacing;
  const nodeX = cx - nodeDiam / 2;
  const nodeY = timelineY - nodeDiam / 2;

  // Navy circle node
  slide.addShape(pres.shapes.OVAL, {
    x: nodeX, y: nodeY, w: nodeDiam, h: nodeDiam,
    fill: { color: "0C2340" }
  });

  // Year label inside node
  slide.addText(m.year, {
    x: nodeX - 0.1, y: nodeY - 0.02, w: nodeDiam + 0.2, h: nodeDiam + 0.04,
    fontFace: "Calibri", fontSize: 7.5, bold: true, color: "FFFFFF",
    align: "center", valign: "middle", margin: 0
  });

  // Alternating above/below for milestone descriptions
  const isAbove = i % 2 === 0;
  const labelY = isAbove ? timelineY - 0.95 : timelineY + 0.3;

  // Vertical connector line
  const connStartY = isAbove ? timelineY - 0.15 : timelineY + 0.15;
  const connLen = 0.15;
  slide.addShape(pres.shapes.LINE, {
    x: cx, y: isAbove ? connStartY - connLen : connStartY,
    w: 0, h: connLen,
    line: { color: "0C2340", width: 0.75 }
  });

  slide.addText(m.label, {
    x: cx - 0.7, y: labelY, w: 1.4, h: 0.55,
    fontFace: "Calibri", fontSize: 8.5, color: "404040",
    align: "center", valign: isAbove ? "bottom" : "top", margin: 0
  });
});

// ─── DATA TABLE ───
const tableX = 0.5;
const tableY = 3.9;
const colWidths = [2.33, 2.0, 2.0, 2.0, 2.0, 2.0];

const borderNone = { pt: 0, color: "FFFFFF" };
const borderNavyTop = { pt: 1.5, color: "0C2340" };
const borderNavyBottom = { pt: 1.5, color: "0C2340" };
const borderLightGrey = { pt: 0.5, color: "E8E8E8" };
const borderNavyThin = { pt: 1, color: "0C2340" };

// Header row
const headerCells = ["Metric", "2020", "2025", "2028", "2030", "2035"].map((txt, idx) => ({
  text: txt,
  options: {
    fontFace: "Calibri", fontSize: 8.5, bold: true, color: "0C2340",
    align: idx === 0 ? "left" : "center", valign: "middle",
    border: [
      borderNavyTop,    // top
      borderNone,       // right
      borderNavyBottom, // bottom
      borderNone        // left
    ],
    margin: [2, 4, 2, 4]
  }
}));

// Data rows
const dataRows = [
  ["Electrolyzer capacity (GW)", "0.5", "1.0", "2.0", "3-4", "8+"],
  ["Green H2 cost (EUR/kg)", "5-6", "3-4", "2.5-3", "2.0", "1.5"],
  ["CO2 reduction (Mt/yr)", "0.5", "2.0", "5.0", "8.0", "15+"]
];

const tableData = [headerCells];

dataRows.forEach((row, rowIdx) => {
  const isLastRow = rowIdx === dataRows.length - 1;
  const bottomBorder = isLastRow ? borderNavyThin : borderLightGrey;

  const cells = row.map((txt, colIdx) => ({
    text: txt,
    options: {
      fontFace: "Calibri",
      fontSize: colIdx === 0 ? 8.5 : 8,
      bold: colIdx === 0,
      color: colIdx === 0 ? "333333" : "404040",
      align: colIdx === 0 ? "left" : "center",
      valign: "middle",
      border: [
        borderNone,      // top
        borderNone,      // right
        bottomBorder,    // bottom
        borderNone       // left
      ],
      margin: [2, 4, 2, 4]
    }
  }));
  tableData.push(cells);
});

slide.addTable(tableData, {
  x: tableX, y: tableY, w: 12.33,
  colW: colWidths,
  rowH: [0.3, 0.28, 0.28, 0.28]
});

// ─── FOOTNOTE ───
slide.addText("1. Capacity and cost projections based on Dutch government targets and McKinsey Energy Insights analysis", {
  x: 0.5, y: 5.5, w: 10, h: 0.25,
  fontFace: "Calibri", fontSize: 7, italic: true, color: "999999",
  valign: "top", margin: 0
});

// ─── FOOTER ───
// Footer rule line at y=6.6
slide.addShape(pres.shapes.LINE, {
  x: 0.5, y: 6.6, w: 12.33, h: 0,
  line: { color: "333333", width: 0.5 }
});

// Source text bottom-left
slide.addText("Source: Dutch National Hydrogen Strategy; REPowerEU; McKinsey Energy Insights", {
  x: 0.5, y: 6.65, w: 8, h: 0.25,
  fontFace: "Calibri", fontSize: 7, color: "999999",
  valign: "top", margin: 0
});

// McKinsey branding + page number bottom-right
slide.addText([
  { text: "McKinsey & Company", options: { bold: true, fontSize: 8, color: "000000", fontFace: "Calibri" } },
  { text: "  1", options: { bold: false, fontSize: 8, color: "000000", fontFace: "Calibri" } }
], {
  x: 9.5, y: 6.65, w: 3.33, h: 0.25,
  align: "right", valign: "top", margin: 0
});

// ─── SAVE ───
pres.writeFile({ fileName: "output/slide_v3.pptx" })
  .then(() => console.log("slide_v3.pptx created successfully"))
  .catch(err => console.error("Error:", err));
