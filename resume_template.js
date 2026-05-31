const { Document, Packer, Paragraph, TextRun, AlignmentType, LevelFormat, TabStopType, ExternalHyperlink } = require('docx');
const fs = require('fs');

const FONT = "Calibri";
const NAME_SIZE = 28;
const BODY_SIZE = 20;
const SECTION_SIZE = 21;
const RIGHT = 10440;

const data = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));

function sectionTitle(text) {
  return new Paragraph({
    spacing: { before: 80, after: 40 },
    border: { bottom: { style: "single", size: 6, color: "000000", space: 1 } },
    children: [new TextRun({ text, font: FONT, size: SECTION_SIZE, bold: true, allCaps: true })]
  });
}
function bullet(text) {
  return new Paragraph({
    spacing: { after: 0 },
    numbering: { reference: "bullets", level: 0 },
    children: [new TextRun({ text, font: FONT, size: BODY_SIZE })]
  });
}
function plain(text) {
  return new Paragraph({
    spacing: { after: 0 },
    children: [new TextRun({ text, font: FONT, size: BODY_SIZE })]
  });
}
function entryHeader(left, right) {
  return new Paragraph({
    spacing: { before: 60, after: 0 },
    tabStops: [{ type: TabStopType.RIGHT, position: RIGHT }],
    children: [
      new TextRun({ text: left, font: FONT, size: BODY_SIZE, bold: true }),
      new TextRun({ text: "\t" + right, font: FONT, size: BODY_SIZE, bold: true }),
    ]
  });
}
function entryRole(role, date) {
  return new Paragraph({
    spacing: { after: 0 },
    tabStops: [{ type: TabStopType.RIGHT, position: RIGHT }],
    children: [
      new TextRun({ text: role, font: FONT, size: BODY_SIZE, italics: true }),
      new TextRun({ text: "\t" + date, font: FONT, size: BODY_SIZE, italics: true }),
    ]
  });
}

const alignmentProject = [
  entryHeader("Alignment (Behavioral Infrastructure Tool) | Founder & Product Lead", "Jan. 2026 - Present"),
  ...data.alignment_bullets.map(b => bullet(b)),
];

const kpopProject = [
  entryHeader("Cross-Border Collectibles Resale | Founder", "Apr. 2026 - Present"),
  bullet("Identified an underserved cross-border resale niche through rapid market research; validated demand within 48 hours without upfront inventory investment."),
  bullet("Iterated on content positioning, increasing organic post reach by 10x."),
  bullet("Facilitated 8 transactions within 5 days, validating cross-border demand and seller acquisition model."),
  bullet("Built automated inventory tracking and listing annotation systems to reduce buyer friction and support seller acquisition."),
  bullet("Maintained 100% 5-star rating across 76 transactions with 11.5% repeat purchase rate."),
];

const projectsInOrder = data.alignment_first
  ? [...alignmentProject, ...kpopProject]
  : [...kpopProject, ...alignmentProject];

const doc = new Document({
  numbering: {
    config: [{
      reference: "bullets",
      levels: [{
        level: 0, format: LevelFormat.BULLET, text: "\u2022", alignment: AlignmentType.LEFT,
        style: { paragraph: { indent: { left: 360, hanging: 360 } } }
      }]
    }]
  },
  sections: [{
    properties: {
      page: {
        size: { width: 12240, height: 15840 },
        margin: { top: 620, right: 900, bottom: 300, left: 900 }
      }
    },
    children: [
      new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 0 }, children: [new TextRun({ text: "Dominique (Xucen) ZHENG", font: FONT, size: NAME_SIZE, bold: true })] }),
      new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 40 }, children: [new TextRun({ text: "Los Angeles, CA | (+1)213-827-4863 | xucenzhe@usc.edu | ", font: FONT, size: BODY_SIZE }), new ExternalHyperlink({ link: "https://www.linkedin.com/in/dominique-zheng-b50559381", children: [new TextRun({ text: "LinkedIn", font: FONT, size: BODY_SIZE, style: "Hyperlink" })] }), new TextRun({ text: " | Seeking " + data.seeking, font: FONT, size: BODY_SIZE })] }),
      new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 0 }, children: [new TextRun({ text: "Summary: ", font: FONT, size: BODY_SIZE, bold: true }), new TextRun({ text: data.summary, font: FONT, size: BODY_SIZE, italics: true })] }),
      new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 60 }, children: [new TextRun({ text: "Authorized to work in the U.S. and available to continue part-time during the academic year.", font: FONT, size: BODY_SIZE })] }),

      sectionTitle("Projects"),
      ...projectsInOrder,

      entryHeader("Behavioral Campaigns | USC Annenberg", "2026"),
      bullet("Developed identity-based and behavioral activation campaigns applying friction reduction, onboarding psychology, and peer-aligned messaging; selected by professor as exemplar work for future classes."),



      sectionTitle("Education"),
      entryHeader("University of Southern California", "California, USA"),
      entryRole("M.E. Major in Integrated Design, Technology & Business", "Expected May 2027"),
      plain("Core Courses: Communication & Persuasion, Marketing & Analytics for Start-ups, Finance for Entrepreneurship"),
      entryHeader("Shanghai Jiao Tong University", "Shanghai, China"),
      entryRole("B.A. Major in Visual Communication Design with focus on Brand & Product Strategy, Minor in Entrepreneurship", "Graduated Jun. 2025"),

      sectionTitle("Internship Experience"),
      entryHeader("Moo Housing Inc.", "Los Angeles, CA"),
      entryRole("Digital Marketing Intern", "May. 2026 - Present"),
      bullet("Published 2 SEO-optimized blog posts reaching average Google ranking positions of 5.3 and 6.2 within days of launch."),
      bullet("Redesigned lease renewal email campaign, increasing open rate from 17.8% to 33.0% (+85% relative improvement)."),
      bullet("Launched re-engagement email sequence targeting unconverted leads, achieving 25.5% open rate."),
      entryHeader("SEPHORA (SHANGHAI) COSMETICS CO., LTD.", "Shanghai, China"),
      entryRole("UX Design Intern", "Jul. 2024 - Oct. 2024"),
      bullet("Mapped end-to-end mobile activation flow; surfaced 20+ friction points reducing conversion and retention signals."),
      bullet("Ran hallway usability tests to identify mental model mismatches in coupon CTA design; proposed and got approved a standardized redirect logic, resolving user confusion in the purchase flow."),
      bullet("Conducted competitive analysis of Ulta Beauty's app; developed a structured audit highlighting feature gaps to inform prioritization."),
      bullet("Partnered with PM on Member Center redesign; A/B test yielded 3% lift in engagement time and 1% reduction in task abandonment."),


      sectionTitle("Skills & Tools"),
      plain("Language: English (Proficient, TOEFL 106); Chinese (Native)"),
      plain("Growth: activation metrics, A/B testing, funnel analysis, experiment design"),
      plain("Analytics: SQL (basic), Excel (pivot tables)"),
      plain("Tools: Figma, Notion, Airtable, Zapier, Clay, HubSpot, Mailchimp, Google Analytics, Google Search Console, VS Code, ChatGPT, Claude" + (data.extra_tools.length > 0 ? ", " + data.extra_tools.join(", ") : "")),

      sectionTitle("Honors"),
      plain("Excellent Project of SJTU Undergraduate Research Program 2023  |  Fourth place, Tencent Games Peace Cup College Developer Creation Competition 2022"),
    ]
  }]
});

Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync(data.output, buffer);
  console.log("Done: " + data.output);
});
