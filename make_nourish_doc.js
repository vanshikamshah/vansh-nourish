const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  Header, Footer, AlignmentType, HeadingLevel, BorderStyle, WidthType,
  ShadingType, VerticalAlign, PageNumber, PageBreak, LevelFormat,
  ImageRun, ExternalHyperlink
} = require('docx');
const fs = require('fs');

// ── COLOUR PALETTE ───────────────────────────────────────────────────────────
const NAVY   = "0B1D3A";
const TEAL   = "00A896";
const CORAL  = "E8472A";
const MINT   = "D0F0EB";
const GOLD   = "F7B731";
const LIGHT  = "F0F9F7";
const LGRAY  = "F4F6F8";
const WHITE  = "FFFFFF";
const DARK   = "1A1A2E";

// ── HELPERS ──────────────────────────────────────────────────────────────────
const noBorder = { style: BorderStyle.NONE, size: 0, color: WHITE };
const noBorders = { top: noBorder, bottom: noBorder, left: noBorder, right: noBorder };

function hRule(color = TEAL) {
  return new Paragraph({
    children: [],
    border: { bottom: { style: BorderStyle.SINGLE, size: 12, color, space: 1 } },
    spacing: { before: 80, after: 80 },
  });
}

function spacer(pts = 80) {
  return new Paragraph({ children: [], spacing: { before: pts, after: 0 } });
}

function headingPara(text, color = WHITE, size = 44, bold = true) {
  return new Paragraph({
    children: [new TextRun({ text, color, size, bold, font: "Calibri" })],
    spacing: { before: 60, after: 60 },
  });
}

function bodyPara(text, color = DARK, size = 19, bold = false, italic = false, before = 80, after = 80) {
  return new Paragraph({
    children: [new TextRun({ text, color, size, bold, italic, font: "Calibri" })],
    spacing: { before, after },
  });
}

function tagline(text) {
  return new Paragraph({
    children: [new TextRun({ text, color: GOLD, size: 26, bold: true, italics: true, font: "Calibri" })],
    spacing: { before: 60, after: 60 },
  });
}

function sectionTitle(text) {
  return new Paragraph({
    children: [new TextRun({ text: text.toUpperCase(), color: NAVY, size: 28, bold: true, font: "Calibri" })],
    spacing: { before: 160, after: 60 },
    border: { bottom: { style: BorderStyle.SINGLE, size: 8, color: TEAL, space: 1 } },
  });
}

function subTitle(text, color = TEAL) {
  return new Paragraph({
    children: [new TextRun({ text, color, size: 22, bold: true, font: "Calibri" })],
    spacing: { before: 120, after: 40 },
  });
}

function bullet(text, bold = false) {
  return new Paragraph({
    numbering: { reference: "bullets", level: 0 },
    children: [new TextRun({ text, color: DARK, size: 18, bold, font: "Calibri" })],
    spacing: { before: 40, after: 40 },
  });
}

// ── COLOURED STAT BOX (single cell table) ────────────────────────────────────
function statBox(stat, label, fill = CORAL) {
  const b = { style: BorderStyle.NONE, size: 0, color: fill };
  const borders = { top: b, bottom: b, left: b, right: b };
  return new Table({
    width: { size: 2800, type: WidthType.DXA },
    columnWidths: [2800],
    rows: [
      new TableRow({
        children: [new TableCell({
          borders,
          shading: { fill, type: ShadingType.CLEAR },
          margins: { top: 120, bottom: 120, left: 160, right: 160 },
          verticalAlign: VerticalAlign.CENTER,
          children: [
            new Paragraph({
              alignment: AlignmentType.CENTER,
              children: [new TextRun({ text: stat, color: WHITE, size: 36, bold: true, font: "Calibri" })],
            }),
            new Paragraph({
              alignment: AlignmentType.CENTER,
              children: [new TextRun({ text: label, color: WHITE, size: 16, font: "Calibri" })],
            }),
          ],
        })],
      }),
    ],
  });
}

// ── ROW OF 3 STAT BOXES ──────────────────────────────────────────────────────
function threeStatRow(stats) {
  // stats = [{stat, label, fill}, ...]
  const b = { style: BorderStyle.NONE, size: 0, color: WHITE };
  const outer = { top: b, bottom: b, left: b, right: b };
  const innerW = 2800;
  const gapW   = 280;
  const cols   = [innerW, gapW, innerW, gapW, innerW];

  return new Table({
    width: { size: cols.reduce((a,c) => a+c, 0), type: WidthType.DXA },
    columnWidths: cols,
    rows: [
      new TableRow({
        children: stats.flatMap((s, i) => {
          const cells = [];
          // stat cell
          const ib = { style: BorderStyle.NONE, size: 0, color: s.fill || CORAL };
          const iBorders = { top: ib, bottom: ib, left: ib, right: ib };
          cells.push(new TableCell({
            borders: iBorders,
            shading: { fill: s.fill || CORAL, type: ShadingType.CLEAR },
            margins: { top: 120, bottom: 120, left: 160, right: 160 },
            verticalAlign: VerticalAlign.CENTER,
            width: { size: innerW, type: WidthType.DXA },
            children: [
              new Paragraph({
                alignment: AlignmentType.CENTER,
                children: [new TextRun({ text: s.stat, color: WHITE, size: 40, bold: true, font: "Calibri" })],
                spacing: { before: 0, after: 20 },
              }),
              new Paragraph({
                alignment: AlignmentType.CENTER,
                children: [new TextRun({ text: s.label, color: WHITE, size: 15, font: "Calibri" })],
                spacing: { before: 0, after: 0 },
              }),
            ],
          }));
          // gap cell (except after last)
          if (i < stats.length - 1) {
            cells.push(new TableCell({
              borders: outer,
              shading: { fill: WHITE, type: ShadingType.CLEAR },
              width: { size: gapW, type: WidthType.DXA },
              children: [new Paragraph({ children: [] })],
            }));
          }
          return cells;
        }),
      }),
    ],
  });
}

// ── SOURCE FOOTNOTE ───────────────────────────────────────────────────────────
function sourceNote(text) {
  return new Paragraph({
    children: [new TextRun({ text: `Source: ${text}`, color: "888888", size: 14, italics: true, font: "Calibri" })],
    spacing: { before: 40, after: 40 },
  });
}

// ── COMPARISON TABLE ──────────────────────────────────────────────────────────
function compTable() {
  const hBorder = { style: BorderStyle.SINGLE, size: 4, color: TEAL };
  const bBorder = { style: BorderStyle.SINGLE, size: 2, color: "CCDDDD" };
  const hBorders = { top: hBorder, bottom: hBorder, left: hBorder, right: hBorder };
  const bBorders = { top: bBorder, bottom: bBorder, left: bBorder, right: bBorder };
  const COL = [3000, 3120, 3120];

  function hCell(text, fill = NAVY) {
    return new TableCell({
      borders: hBorders,
      shading: { fill, type: ShadingType.CLEAR },
      margins: { top: 80, bottom: 80, left: 120, right: 120 },
      verticalAlign: VerticalAlign.CENTER,
      width: { size: COL[0], type: WidthType.DXA },
      children: [new Paragraph({
        alignment: AlignmentType.CENTER,
        children: [new TextRun({ text, color: WHITE, size: 18, bold: true, font: "Calibri" })],
      })],
    });
  }

  function bCell(text, fill = WHITE, textColor = DARK, bold = false, width = COL[0]) {
    return new TableCell({
      borders: bBorders,
      shading: { fill, type: ShadingType.CLEAR },
      margins: { top: 60, bottom: 60, left: 120, right: 120 },
      verticalAlign: VerticalAlign.CENTER,
      width: { size: width, type: WidthType.DXA },
      children: [new Paragraph({
        children: [new TextRun({ text, color: textColor, size: 17, bold, font: "Calibri" })],
      })],
    });
  }

  const rows = [
    ["Dimension", "Traditional Delivery", "Nourish"],
    ["Order Trigger", "User impulse / hunger", "Biometric signal (automatic)"],
    ["Menu", "500+ options, choice overload", "Zero choices — body decides"],
    ["Incentive", "Commission per order (15-30%)", "Subscription + hardware"],
    ["Food Quality", "Optimised for indulgence", "Calibrated to precise needs"],
    ["Data Used", "Order history", "Live biometrics + circadian data"],
    ["Compounding Effect", "Engagement algorithms deepen", "Personalisation improves with data"],
    ["Fulfilment", "Partner restaurants", "Proprietary neighbourhood nodes"],
    ["Health Outcome", "84% higher obesity risk", "Measurable metabolic improvement"],
  ];

  return new Table({
    width: { size: 9240, type: WidthType.DXA },
    columnWidths: [3000, 3120, 3120],
    rows: rows.map((row, i) =>
      new TableRow({
        children: row.map((cell, j) => {
          if (i === 0) return hCell(cell, NAVY);
          if (j === 0) return bCell(cell, LGRAY, NAVY, true, 3000);
          if (j === 2) return bCell(cell, MINT, "005F54", true, 3120);
          return bCell(cell, WHITE, DARK, false, 3120);
        }),
      })
    ),
  });
}

// ── BOS FRAMEWORK TABLE ───────────────────────────────────────────────────────
function bosTable() {
  const b = { style: BorderStyle.SINGLE, size: 4, color: TEAL };
  const bLight = { style: BorderStyle.SINGLE, size: 2, color: "C0DDD8" };
  const borders = { top: bLight, bottom: bLight, left: bLight, right: bLight };
  const hBorders = { top: b, bottom: b, left: b, right: b };

  const rows = [
    ["BOS Criterion", "Nourish Response"],
    ["① Magnitude of Disruption", "Eliminates the browse–choose–order behaviour entirely. Food delivery becomes invisible infrastructure — like electricity. Users never open an app."],
    ["② Customer Painkiller", "Solves decision fatigue, removes commission-driven junk-food nudges, eliminates meal-timing chaos, and delivers physiologically-correct nutrition automatically."],
    ["③ Compounding Loop", "Every meal generates richer biometric data → sharper AI predictions → better health outcomes → stronger user lock-in. A late-mover starting from zero can never replicate 2 years of accumulated physiological history."],
    ["④ Tailwinds", "Convergence of: continuous glucose monitors (CGM), miniaturised biosensors, AI/ML in healthcare, preventive-health consciousness, wearable adoption (1.5 Bn units by 2026), and rising metabolic disease burden."],
    ["⑤ New Customer Behaviour", "\"My body decides what I eat.\" In 2030 this will feel as natural as streaming music on demand felt in 2015. The customer's only action is wearing the device."],
  ];

  return new Table({
    width: { size: 9240, type: WidthType.DXA },
    columnWidths: [2800, 6440],
    rows: rows.map((row, i) =>
      new TableRow({
        children: row.map((cell, j) => {
          if (i === 0) {
            return new TableCell({
              borders: hBorders,
              shading: { fill: NAVY, type: ShadingType.CLEAR },
              margins: { top: 80, bottom: 80, left: 120, right: 120 },
              verticalAlign: VerticalAlign.CENTER,
              width: { size: j === 0 ? 2800 : 6440, type: WidthType.DXA },
              children: [new Paragraph({
                alignment: AlignmentType.CENTER,
                children: [new TextRun({ text: cell, color: WHITE, size: 18, bold: true, font: "Calibri" })],
              })],
            });
          }
          return new TableCell({
            borders,
            shading: { fill: j === 0 ? MINT : WHITE, type: ShadingType.CLEAR },
            margins: { top: 80, bottom: 80, left: 120, right: 120 },
            verticalAlign: VerticalAlign.CENTER,
            width: { size: j === 0 ? 2800 : 6440, type: WidthType.DXA },
            children: [new Paragraph({
              children: [new TextRun({ text: cell, color: j === 0 ? "005F54" : DARK, size: 17, bold: j === 0, font: "Calibri" })],
            })],
          });
        }),
      })
    ),
  });
}

// ── HOW IT WORKS FLOW TABLE ───────────────────────────────────────────────────
function flowTable() {
  const steps = [
    { num: "1", icon: "⌚", title: "Body Sends Signal", desc: "Wearable continuously reads blood glucose, hydration, stress & energy markers", fill: "005F8A" },
    { num: "2", icon: "🧠", title: "AI Decides", desc: "Algorithm fuses biometrics + circadian time + mood state → selects precise dish", fill: "006B6B" },
    { num: "3", icon: "🏭", title: "Kitchen Prepares", desc: "Nearest proprietary prep node receives the calibrated recipe and cooks fresh", fill: "007A40" },
    { num: "4", icon: "🚴", title: "Doorstep Delivery", desc: "Meal arrives — no order placed, no decision made, no app opened", fill: "6B5B00" },
    { num: "5", icon: "📊", title: "Weekly Insight", desc: "Health summary shows glucose stability, hydration trend & energy data", fill: "7A0040" },
  ];

  const b = { style: BorderStyle.NONE, size: 0, color: WHITE };
  const nb = { top: b, bottom: b, left: b, right: b };
  const COL_W = 1720;
  const GAP_W = 60;
  const COLS = [COL_W, GAP_W, COL_W, GAP_W, COL_W, GAP_W, COL_W, GAP_W, COL_W];

  return new Table({
    width: { size: COLS.reduce((a, c) => a + c, 0), type: WidthType.DXA },
    columnWidths: COLS,
    rows: [
      new TableRow({
        children: steps.flatMap((s, i) => {
          const ib = { style: BorderStyle.NONE, size: 0, color: s.fill };
          const iBorders = { top: ib, bottom: ib, left: ib, right: ib };
          const cells = [
            new TableCell({
              borders: iBorders,
              shading: { fill: s.fill, type: ShadingType.CLEAR },
              margins: { top: 100, bottom: 100, left: 80, right: 80 },
              verticalAlign: VerticalAlign.CENTER,
              width: { size: COL_W, type: WidthType.DXA },
              children: [
                new Paragraph({
                  alignment: AlignmentType.CENTER,
                  children: [new TextRun({ text: s.icon, size: 36, font: "Calibri" })],
                  spacing: { before: 0, after: 20 },
                }),
                new Paragraph({
                  alignment: AlignmentType.CENTER,
                  children: [new TextRun({ text: `STEP ${s.num}`, color: "FFFF99", size: 14, bold: true, font: "Calibri" })],
                  spacing: { before: 0, after: 20 },
                }),
                new Paragraph({
                  alignment: AlignmentType.CENTER,
                  children: [new TextRun({ text: s.title, color: WHITE, size: 17, bold: true, font: "Calibri" })],
                  spacing: { before: 0, after: 20 },
                }),
                new Paragraph({
                  alignment: AlignmentType.CENTER,
                  children: [new TextRun({ text: s.desc, color: "E0F0FF", size: 14, font: "Calibri" })],
                  spacing: { before: 0, after: 0 },
                }),
              ],
            }),
          ];
          if (i < steps.length - 1) {
            cells.push(new TableCell({
              borders: nb,
              shading: { fill: WHITE, type: ShadingType.CLEAR },
              width: { size: GAP_W, type: WidthType.DXA },
              children: [new Paragraph({
                alignment: AlignmentType.CENTER,
                children: [new TextRun({ text: "▶", color: TEAL, size: 20, bold: true, font: "Calibri" })],
              })],
            }));
          }
          return cells;
        }),
      }),
    ],
  });
}

// ── REVENUE MODEL TABLE ───────────────────────────────────────────────────────
function revenueTable() {
  const b = { style: BorderStyle.SINGLE, size: 3, color: TEAL };
  const bLight = { style: BorderStyle.SINGLE, size: 2, color: "C0DDD8" };
  const cols = [2200, 3600, 3440];
  const rows = [
    ["Stream", "Description", "Why It Matters"],
    ["Hardware", "Proprietary wearable device (~₹8,000–12,000 one-time)", "Creates sticky, high-intent user from day one"],
    ["Subscription", "Monthly plan covering meals + AI service (~₹4,500/mo)", "Recurring revenue; no per-order margin pressure"],
    ["Data Intelligence", "Anonymised population-level health insights (B2B)", "High-margin, builds over time as dataset grows"],
  ];

  return new Table({
    width: { size: 9240, type: WidthType.DXA },
    columnWidths: cols,
    rows: rows.map((row, i) =>
      new TableRow({
        children: row.map((cell, j) =>
          new TableCell({
            borders: i === 0 ? { top: b, bottom: b, left: b, right: b } : { top: bLight, bottom: bLight, left: bLight, right: bLight },
            shading: { fill: i === 0 ? TEAL : (i % 2 === 0 ? LIGHT : WHITE), type: ShadingType.CLEAR },
            margins: { top: 70, bottom: 70, left: 120, right: 120 },
            verticalAlign: VerticalAlign.CENTER,
            width: { size: cols[j], type: WidthType.DXA },
            children: [new Paragraph({
              children: [new TextRun({ text: cell, color: i === 0 ? WHITE : DARK, size: 17, bold: i === 0 || j === 0, font: "Calibri" })],
            })],
          })
        ),
      })
    ),
  });
}

// ─────────────────────────────────────────────────────────────────────────────
// DOCUMENT ASSEMBLY
// ─────────────────────────────────────────────────────────────────────────────

const doc = new Document({
  numbering: {
    config: [
      {
        reference: "bullets",
        levels: [{
          level: 0,
          format: LevelFormat.BULLET,
          text: "•",
          alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 560, hanging: 280 } } },
        }],
      },
    ],
  },
  styles: {
    default: {
      document: { run: { font: "Calibri", size: 19 } },
    },
  },

  sections: [
    // ════════════════════════════════════════════════════════════════════
    // PAGE 1 – COVER
    // ════════════════════════════════════════════════════════════════════
    {
      properties: {
        page: {
          size: { width: 12240, height: 15840 },
          margin: { top: 0, right: 0, bottom: 1440, left: 0 },
        },
      },
      children: [
        // Navy banner header
        new Table({
          width: { size: 12240, type: WidthType.DXA },
          columnWidths: [12240],
          rows: [new TableRow({
            children: [new TableCell({
              borders: noBorders,
              shading: { fill: NAVY, type: ShadingType.CLEAR },
              margins: { top: 1200, bottom: 600, left: 1440, right: 1440 },
              children: [
                new Paragraph({
                  children: [new TextRun({ text: "NOURISH", color: WHITE, size: 96, bold: true, font: "Calibri" })],
                  spacing: { before: 0, after: 80 },
                }),
                new Paragraph({
                  children: [new TextRun({
                    text: "Your Body. Your Food. No Decision.",
                    color: GOLD, size: 36, bold: true, italics: true, font: "Calibri",
                  })],
                  spacing: { before: 0, after: 160 },
                }),
                // Teal divider
                new Paragraph({
                  children: [],
                  border: { bottom: { style: BorderStyle.SINGLE, size: 12, color: TEAL, space: 1 } },
                  spacing: { before: 0, after: 160 },
                }),
                new Paragraph({
                  children: [new TextRun({ text: "Blue Ocean Strategy — Rebel Foods Challenge", color: MINT, size: 26, font: "Calibri" })],
                  spacing: { before: 0, after: 80 },
                }),
                new Paragraph({
                  children: [new TextRun({ text: "SP Jain School of Global Management · Global MBA · Dubai", color: "88C8BE", size: 22, font: "Calibri" })],
                  spacing: { before: 0, after: 80 },
                }),
                new Paragraph({
                  children: [new TextRun({ text: "Submitted by: Vansh  |  Instructor: Dr. Umesh Kothari", color: "88C8BE", size: 22, font: "Calibri" })],
                  spacing: { before: 0, after: 200 },
                }),
              ],
            })],
          })],
        }),

        spacer(240),

        // Three pillars
        new Table({
          width: { size: 10240, type: WidthType.DXA },
          columnWidths: [3200, 240, 3200, 240, 3200],
          rows: [new TableRow({
            children: [
              ...[
                { icon: "🔬", title: "Biometric Intelligence", text: "Continuous physiological reading — glucose, hydration, stress, energy" },
                null,
                { icon: "🤖", title: "Autonomous AI Kitchen", text: "Zero-input meal decision made by your body's live signals" },
                null,
                { icon: "📍", title: "Hyperlocal Prep Nodes", text: "Proprietary neighbourhood kitchens delivering precise nutrition, fast" },
              ].map((item, idx) => {
                if (!item) return new TableCell({
                  borders: noBorders,
                  shading: { fill: WHITE, type: ShadingType.CLEAR },
                  width: { size: 240, type: WidthType.DXA },
                  children: [new Paragraph({ children: [] })],
                });
                return new TableCell({
                  borders: noBorders,
                  shading: { fill: LIGHT, type: ShadingType.CLEAR },
                  margins: { top: 160, bottom: 160, left: 200, right: 200 },
                  verticalAlign: VerticalAlign.CENTER,
                  width: { size: 3200, type: WidthType.DXA },
                  children: [
                    new Paragraph({
                      alignment: AlignmentType.CENTER,
                      children: [new TextRun({ text: item.icon, size: 52, font: "Calibri" })],
                      spacing: { before: 0, after: 80 },
                    }),
                    new Paragraph({
                      alignment: AlignmentType.CENTER,
                      children: [new TextRun({ text: item.title, color: NAVY, size: 22, bold: true, font: "Calibri" })],
                      spacing: { before: 0, after: 80 },
                    }),
                    new Paragraph({
                      alignment: AlignmentType.CENTER,
                      children: [new TextRun({ text: item.text, color: "444444", size: 17, font: "Calibri" })],
                      spacing: { before: 0, after: 0 },
                    }),
                  ],
                });
              }),
            ],
          })],
        }),

        spacer(240),

        new Paragraph({
          alignment: AlignmentType.CENTER,
          children: [new TextRun({
            text: "\"In 2030, letting your body automatically order its own nutrition will feel as natural as streaming music did in 2015.\"",
            color: TEAL, size: 22, italics: true, font: "Calibri",
          })],
          spacing: { before: 120, after: 60 },
        }),

        new Paragraph({ children: [new PageBreak()] }),
      ],
    },

    // ════════════════════════════════════════════════════════════════════
    // PAGES 2-5 – CONTENT
    // ════════════════════════════════════════════════════════════════════
    {
      properties: {
        page: {
          size: { width: 12240, height: 15840 },
          margin: { top: 1080, right: 1080, bottom: 1080, left: 1080 },
        },
      },
      headers: {
        default: new Header({
          children: [
            new Table({
              width: { size: 10080, type: WidthType.DXA },
              columnWidths: [6000, 4080],
              rows: [new TableRow({
                children: [
                  new TableCell({
                    borders: noBorders,
                    shading: { fill: WHITE, type: ShadingType.CLEAR },
                    width: { size: 6000, type: WidthType.DXA },
                    children: [new Paragraph({
                      children: [new TextRun({ text: "NOURISH  ·  Blue Ocean Strategy Challenge", color: TEAL, size: 18, bold: true, font: "Calibri" })],
                    })],
                  }),
                  new TableCell({
                    borders: noBorders,
                    shading: { fill: WHITE, type: ShadingType.CLEAR },
                    width: { size: 4080, type: WidthType.DXA },
                    children: [new Paragraph({
                      alignment: AlignmentType.RIGHT,
                      children: [new TextRun({ text: "SP Jain GMBA  ·  Dr. Umesh Kothari", color: "888888", size: 16, font: "Calibri" })],
                    })],
                  }),
                ],
              })],
            }),
            new Paragraph({
              children: [],
              border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: TEAL, space: 1 } },
              spacing: { before: 0, after: 0 },
            }),
          ],
        }),
      },
      footers: {
        default: new Footer({
          children: [
            new Paragraph({
              children: [],
              border: { top: { style: BorderStyle.SINGLE, size: 4, color: TEAL, space: 1 } },
              spacing: { before: 0, after: 40 },
            }),
            new Paragraph({
              children: [
                new TextRun({ text: "Nourish — Autonomous Nutrition Platform  |  Page ", color: "888888", size: 15, font: "Calibri" }),
                new TextRun({ children: [PageNumber.CURRENT], color: "888888", size: 15, font: "Calibri" }),
                new TextRun({ text: " of ", color: "888888", size: 15, font: "Calibri" }),
                new TextRun({ children: [PageNumber.TOTAL_PAGES], color: "888888", size: 15, font: "Calibri" }),
              ],
              alignment: AlignmentType.CENTER,
            }),
          ],
        }),
      },
      children: [
        // ── SECTION 1: THE PROBLEM ─────────────────────────────────────
        sectionTitle("The Problem: Why Today's Food Delivery Is Broken"),

        new Paragraph({
          children: [new TextRun({
            text: "Two structural failures are silently damaging the health of millions of food delivery users every day.",
            color: DARK, size: 20, bold: true, font: "Calibri",
          })],
          spacing: { before: 80, after: 100 },
        }),

        // Pain Point 1
        subTitle("Pain Point 1  ·  The Disrupted Meal Rhythm", CORAL),
        bodyPara(
          "Modern food delivery has decoupled eating from biology. We eat when the app suggests, when a discount expires, or when the craving strikes — not when our body needs fuel. " +
          "Science is unambiguous about the consequences.",
          DARK, 18, false, false, 40, 100,
        ),

        threeStatRow([
          { stat: ">50%", label: "of adults spread eating over 15+ hours daily, never giving the body a true rest window", fill: "C0392B" },
          { stat: "74%", label: "higher odds of metabolic syndrome in people with irregular meal timing (27-yr cohort study)", fill: "00838A" },
          { stat: "84%", label: "higher likelihood of obesity in daily food delivery app users vs non-users (BMJ, 2024)", fill: "D35400" },
        ]),
        sourceNote("PMC Meal Timing Review 2024; Cambridge Public Health Nutrition Cohort; BMJ Public Health 2024"),

        spacer(80),
        bullet("A delay of just 1 hour at dinner impairs glucose tolerance in otherwise healthy adults (NIH/PMC10804920)."),
        bullet("22.4% of food delivery users in a clinical study reported irregular meal timing as a perceived health problem."),
        bullet("Eating >45% of daily calories after 5 pm is linked to higher risk of type 2 diabetes and cardiovascular disease."),
        bullet("Only ~10% of adults naturally maintain a ≥12-hour overnight fast — the norm set by human biology."),

        spacer(100),

        // Pain Point 2
        subTitle("Pain Point 2  ·  The Rigged Choice Architecture", CORAL),
        bodyPara(
          "Food delivery platforms earn 15–30% commission on every order. This one fact determines everything about how their apps are designed. " +
          "Bestseller badges, countdown timers, and discount bubbles are not helping you eat well — they are structurally engineered to maximise basket size and reorder frequency.",
          DARK, 18, false, false, 40, 100,
        ),

        threeStatRow([
          { stat: "360%", label: "more likely to consume fast food if you regularly use food delivery apps (KSA Research 2024)", fill: "8E44AD" },
          { stat: "47%", label: "of items sold via cloud kitchens are fast food or dessert — the highest-commission categories", fill: "1A5276" },
          { stat: "40%", label: "of food delivery platform users across 5 countries are overweight or obese (multi-country analysis)", fill: "117A65" },
        ]),
        sourceNote("Saudi Arabia Food Delivery Study 2024; PMC Dark Kitchens Analysis; Obesity Reviews 2024"),

        spacer(80),
        bullet("Platforms use visual cues, price discounts, and 'trending' badges to promote energy-dense, nutrient-poor foods."),
        bullet("High-commission items (burgers, fried chicken, desserts) are algorithmically surfaced ahead of healthier options."),
        bullet("There is zero structural incentive for any incumbent platform to prioritise your health — their revenue goes up when yours goes down."),
        bullet("Food app users in a Kolkata clinical study reported weight gain (23.6%) and indigestion (23.6%) as top perceived health effects."),

        new Paragraph({ children: [new PageBreak()] }),

        // ── SECTION 2: THE SOLUTION ────────────────────────────────────
        sectionTitle("The Solution: Nourish — Autonomous Nutrition, Not Delivery"),

        bodyPara(
          "Nourish does not improve food delivery. It makes the concept of 'ordering food' irrelevant. " +
          "Instead of asking what you want to eat, Nourish reads what your body needs to eat — and handles everything else automatically.",
          DARK, 18, false, false, 40, 120,
        ),

        subTitle("How It Works — The 5-Step Autonomous Journey"),
        spacer(60),
        flowTable(),
        spacer(100),

        // The Device
        subTitle("The Nourish Wearable"),
        new Table({
          width: { size: 9080, type: WidthType.DXA },
          columnWidths: [4400, 4680],
          rows: [new TableRow({
            children: [
              new TableCell({
                borders: noBorders,
                shading: { fill: NAVY, type: ShadingType.CLEAR },
                margins: { top: 160, bottom: 160, left: 200, right: 200 },
                verticalAlign: VerticalAlign.CENTER,
                width: { size: 4400, type: WidthType.DXA },
                children: [
                  new Paragraph({
                    alignment: AlignmentType.CENTER,
                    children: [new TextRun({ text: "⌚", size: 96, font: "Calibri" })],
                    spacing: { before: 0, after: 80 },
                  }),
                  new Paragraph({
                    alignment: AlignmentType.CENTER,
                    children: [new TextRun({ text: "NOURISH BAND", color: GOLD, size: 22, bold: true, font: "Calibri" })],
                    spacing: { before: 0, after: 80 },
                  }),
                  ...[
                    "📡  Continuous Glucose Monitor (CGM)",
                    "💧  Skin Hydration Sensor",
                    "❤️  Heart Rate Variability (HRV)",
                    "🌡️  Skin Temperature + GSR",
                    "🔋  7-day battery, waterproof",
                  ].map(s => new Paragraph({
                    alignment: AlignmentType.CENTER,
                    children: [new TextRun({ text: s, color: MINT, size: 17, font: "Calibri" })],
                    spacing: { before: 30, after: 30 },
                  })),
                ],
              }),
              new TableCell({
                borders: noBorders,
                shading: { fill: LIGHT, type: ShadingType.CLEAR },
                margins: { top: 160, bottom: 160, left: 240, right: 120 },
                verticalAlign: VerticalAlign.CENTER,
                width: { size: 4680, type: WidthType.DXA },
                children: [
                  new Paragraph({
                    children: [new TextRun({ text: "Built from the ground up for one question:", color: NAVY, size: 22, bold: true, font: "Calibri" })],
                    spacing: { before: 0, after: 80 },
                  }),
                  new Paragraph({
                    children: [new TextRun({ text: "\"What does this body need to eat, right now?\"", color: TEAL, size: 24, bold: true, italics: true, font: "Calibri" })],
                    spacing: { before: 0, after: 120 },
                  }),
                  bodyPara("Unlike Apple Watch (fitness) or Whoop (recovery), the Nourish Band is purpose-engineered for nutritional intelligence — a single-function device with medical-grade sensors.", "444444", 17, false, false, 0, 80),
                  bodyPara("No app. No menu. No decision. The band reads you silently, all day. When a meaningful nutritional signal is detected — blood sugar drifting low, dehydration setting in, an energy crash approaching — it triggers the chain automatically.", "444444", 17, false, false, 0, 0),
                ],
              }),
            ],
          })],
        }),

        spacer(120),

        // The AI Layer
        subTitle("The AI Layer — Three Inputs, One Perfect Dish"),
        new Table({
          width: { size: 9080, type: WidthType.DXA },
          columnWidths: [2900, 200, 2900, 200, 2880],
          rows: [new TableRow({
            children: [
              ...[
                { icon: "🩸", title: "Live Biometrics", items: ["Blood glucose trend", "Hydration index", "Stress & HRV score", "Nutrient deficit markers"] },
                null,
                { icon: "🕐", title: "Time & Circadian State", items: ["Time of day", "Sleep quality last night", "Activity since last meal", "Upcoming calendar signals"] },
                null,
                { icon: "😌", title: "Inferred Mood / Energy", items: ["Derived from biometrics", "Never asked — just read", "Ensures variety", "No decision fatigue"] },
              ].map((item, idx) => {
                if (!item) return new TableCell({
                  borders: noBorders,
                  shading: { fill: WHITE, type: ShadingType.CLEAR },
                  width: { size: 200, type: WidthType.DXA },
                  children: [new Paragraph({ children: [new TextRun({ text: "→", color: TEAL, size: 24, bold: true, font: "Calibri" })], alignment: AlignmentType.CENTER })],
                });
                return new TableCell({
                  borders: noBorders,
                  shading: { fill: idx === 0 ? "E8F4FD" : idx === 4 ? "EAF5EA" : "FEF9E7", type: ShadingType.CLEAR },
                  margins: { top: 120, bottom: 120, left: 160, right: 160 },
                  verticalAlign: VerticalAlign.TOP,
                  width: { size: 2900, type: WidthType.DXA },
                  children: [
                    new Paragraph({
                      alignment: AlignmentType.CENTER,
                      children: [new TextRun({ text: item.icon, size: 40, font: "Calibri" })],
                      spacing: { before: 0, after: 60 },
                    }),
                    new Paragraph({
                      alignment: AlignmentType.CENTER,
                      children: [new TextRun({ text: item.title, color: NAVY, size: 19, bold: true, font: "Calibri" })],
                      spacing: { before: 0, after: 80 },
                    }),
                    ...item.items.map(it => new Paragraph({
                      numbering: { reference: "bullets", level: 0 },
                      children: [new TextRun({ text: it, color: DARK, size: 16, font: "Calibri" })],
                      spacing: { before: 20, after: 20 },
                    })),
                  ],
                });
              }),
            ],
          })],
        }),

        spacer(100),

        // Fulfilment
        subTitle("The Fulfilment Network"),
        bodyPara(
          "Nourish operates a proprietary network of small, hyperlocal Prep Nodes — not full cloud kitchens, but dense neighbourhood units designed to cook fresh, fast, and to a precise nutritional spec. " +
          "For simple hydration items (juices, infused water), the system can route to a trusted partner nearby. " +
          "Every calibrated meal stays in-house — because that is the one thing Swiggy, Zomato, or any incumbent can never replicate.",
          DARK, 17, false, false, 40, 60,
        ),

        new Paragraph({ children: [new PageBreak()] }),

        // ── SECTION 3: COMPARISON & BOS ───────────────────────────────
        sectionTitle("Nourish vs Traditional Food Delivery"),
        spacer(60),
        compTable(),

        spacer(120),

        sectionTitle("Blue Ocean Strategy Framework"),
        bodyPara(
          "Nourish does not compete in the food delivery red ocean. It creates an entirely new market space where the rules of the incumbent game are irrelevant.",
          DARK, 18, false, false, 40, 100,
        ),
        bosTable(),

        new Paragraph({ children: [new PageBreak()] }),

        // ── SECTION 4: BUSINESS MODEL & CONCLUSION ────────────────────
        sectionTitle("Business Model & Compounding Flywheel"),

        subTitle("Three Revenue Streams"),
        revenueTable(),

        spacer(120),

        subTitle("The Compounding Personalisation Loop"),
        new Table({
          width: { size: 9080, type: WidthType.DXA },
          columnWidths: [9080],
          rows: [new TableRow({
            children: [new TableCell({
              borders: { top: { style: BorderStyle.SINGLE, size: 6, color: TEAL }, bottom: { style: BorderStyle.SINGLE, size: 6, color: TEAL }, left: { style: BorderStyle.NONE, size: 0, color: WHITE }, right: { style: BorderStyle.NONE, size: 0, color: WHITE } },
              shading: { fill: LIGHT, type: ShadingType.CLEAR },
              margins: { top: 100, bottom: 100, left: 200, right: 200 },
              width: { size: 9080, type: WidthType.DXA },
              children: [new Paragraph({
                alignment: AlignmentType.CENTER,
                children: [new TextRun({
                  text: "User wears device  →  Biometrics collected  →  AI predicts need  →  Meal delivered  →  Health improves  →  Data richer  →  Predictions sharper  →  User trust deepens  →  Subscription renews",
                  color: NAVY, size: 18, bold: true, font: "Calibri",
                })],
              })],
            })],
          })],
        }),

        spacer(80),
        bodyPara(
          "Every meal makes the system smarter. A competitor starting from zero cannot replicate two years of accumulated physiological history. " +
          "This is a data moat — not a technology moat — and it compounds silently with every meal served.",
          DARK, 17, false, false, 0, 120,
        ),

        subTitle("Tailwinds Making This Possible Now"),
        new Table({
          width: { size: 9080, type: WidthType.DXA },
          columnWidths: [2200, 2200, 2200, 2480],
          rows: [new TableRow({
            children: [
              { icon: "📡", text: "Miniaturised CGM sensors now wearable-grade & affordable" },
              { icon: "🤖", text: "LLM + predictive AI mature enough for real-time nutrition logic" },
              { icon: "🏥", text: "Preventive health mainstream — 1.5 Bn wearable units shipped by 2026" },
              { icon: "💰", text: "Metabolic disease costs driving consumer willingness to pay for solutions" },
            ].map((item, i) => new TableCell({
              borders: noBorders,
              shading: { fill: i % 2 === 0 ? MINT : LIGHT, type: ShadingType.CLEAR },
              margins: { top: 100, bottom: 100, left: 140, right: 140 },
              verticalAlign: VerticalAlign.CENTER,
              width: { size: i === 3 ? 2480 : 2200, type: WidthType.DXA },
              children: [
                new Paragraph({
                  alignment: AlignmentType.CENTER,
                  children: [new TextRun({ text: item.icon, size: 40, font: "Calibri" })],
                  spacing: { before: 0, after: 60 },
                }),
                new Paragraph({
                  alignment: AlignmentType.CENTER,
                  children: [new TextRun({ text: item.text, color: NAVY, size: 16, font: "Calibri" })],
                }),
              ],
            })),
          })],
        }),

        spacer(120),

        subTitle("The New Customer Behaviour — What 2030 Looks Like"),
        new Table({
          width: { size: 9080, type: WidthType.DXA },
          columnWidths: [9080],
          rows: [new TableRow({
            children: [new TableCell({
              borders: noBorders,
              shading: { fill: NAVY, type: ShadingType.CLEAR },
              margins: { top: 200, bottom: 200, left: 400, right: 400 },
              width: { size: 9080, type: WidthType.DXA },
              children: [
                new Paragraph({
                  alignment: AlignmentType.CENTER,
                  children: [new TextRun({ text: "\"My body decides what I eat.\"", color: GOLD, size: 36, bold: true, italics: true, font: "Calibri" })],
                  spacing: { before: 0, after: 120 },
                }),
                new Paragraph({
                  alignment: AlignmentType.CENTER,
                  children: [new TextRun({
                    text: "In 2010, few believed millions would order from kitchens they'd never seen. In 2026 it's mainstream. " +
                          "In 2030, letting your wearable autonomously handle your nutrition will feel equally obvious — " +
                          "because it removes the last thing no one wanted to do: decide what to eat.",
                    color: MINT, size: 18, font: "Calibri",
                  })],
                }),
              ],
            })],
          })],
        }),

        spacer(120),

        new Paragraph({
          alignment: AlignmentType.CENTER,
          children: [new TextRun({
            text: "Nourish doesn't improve food delivery. It makes food delivery irrelevant.",
            color: TEAL, size: 22, bold: true, italics: true, font: "Calibri",
          })],
          spacing: { before: 120, after: 0 },
        }),
      ],
    },
  ],
});

Packer.toBuffer(doc).then(buf => {
  fs.writeFileSync('nourish_bos.docx', buf);
  console.log('Done: nourish_bos.docx');
}).catch(e => { console.error(e); process.exit(1); });
