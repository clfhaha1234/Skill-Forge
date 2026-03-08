const pptxgen = require("/Users/lifeichen/Skill-Forge/node_modules/pptxgenjs");

const pres = new pptxgen();
pres.layout = "LAYOUT_16x9"; // 10" x 5.625"
pres.author = "Skill-Forge";
pres.title = "Dutch Hydrogen Strategy 2020-2035";

const slide = pres.addSlide();

// Dark background for premium feel
slide.background = { color: "0A1628" };

// --- Title ---
// Georgia 36-44pt bold, NO accent line under title
slide.addText("Dutch Hydrogen Strategy (2020\u20132035)", {
  x: 0.5, y: 0.3, w: 9, h: 0.6,
  fontFace: "Georgia",
  fontSize: 24,
  bold: true,
  color: "FFFFFF",
  margin: 0,
});

// Subtitle
slide.addText("McKinsey & Company  |  Timeline Overview", {
  x: 0.5, y: 0.85, w: 9, h: 0.3,
  fontFace: "Calibri",
  fontSize: 12,
  color: "00A896",
  margin: 0,
});

// --- Timeline ---
const milestones = [
  { year: "2020", label: "National Hydrogen\nStrategy published" },
  { year: "2022", label: "REPowerEU plan\naccelerates ambitions" },
  { year: "2025", label: "First green H2\nhubs operational" },
  { year: "2028", label: "HyNetwork backbone\npipeline live" },
  { year: "2030", label: "Scale-up phase\ncomplete" },
  { year: "2035", label: "EU hydrogen corridor\nintegration" },
];

const timelineY = 2.8; // vertical center of the timeline line
const startX = 0.8;
const endX = 9.2;
const totalW = endX - startX;
const count = milestones.length;
const spacing = totalW / (count - 1);

// Horizontal line
slide.addShape(pres.shapes.LINE, {
  x: startX,
  y: timelineY,
  w: totalW,
  h: 0,
  line: { color: "028090", width: 2.5 },
});

// Circles and labels
milestones.forEach((m, i) => {
  const cx = startX + i * spacing;
  const circleSize = 0.32;

  // Circle (oval)
  slide.addShape(pres.shapes.OVAL, {
    x: cx - circleSize / 2,
    y: timelineY - circleSize / 2,
    w: circleSize,
    h: circleSize,
    fill: { color: "028090" },
    line: { color: "02C39A", width: 1.5 },
  });

  // Year label above
  slide.addText(m.year, {
    x: cx - 0.5,
    y: timelineY - 0.75,
    w: 1.0,
    h: 0.35,
    fontFace: "Georgia",
    fontSize: 16,
    bold: true,
    color: "02C39A",
    align: "center",
    valign: "middle",
    margin: 0,
  });

  // Description below
  slide.addText(m.label, {
    x: cx - 0.7,
    y: timelineY + 0.3,
    w: 1.4,
    h: 0.75,
    fontFace: "Calibri",
    fontSize: 11,
    color: "CCCCCC",
    align: "center",
    valign: "top",
    margin: 0,
  });
});

// --- Footer bar ---
slide.addShape(pres.shapes.RECTANGLE, {
  x: 0,
  y: 5.15,
  w: 10,
  h: 0.475,
  fill: { color: "028090" },
});

slide.addText("Confidential  |  Dutch Hydrogen Strategy", {
  x: 0.5,
  y: 5.15,
  w: 9,
  h: 0.475,
  fontFace: "Calibri",
  fontSize: 10,
  color: "FFFFFF",
  align: "center",
  valign: "middle",
  margin: 0,
});

// Write file
pres.writeFile({ fileName: "/Users/lifeichen/Skill-Forge/output/slide_v0.pptx" })
  .then(() => console.log("PPTX created successfully."))
  .catch((err) => console.error("Error:", err));
