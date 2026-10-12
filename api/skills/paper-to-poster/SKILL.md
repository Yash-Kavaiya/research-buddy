---
name: paper-to-poster
description: "Designs an academic poster from a paper: headline finding, column layout at the conference's size, trimmed text, and enlarged figures. Use for poster sessions. Not for talks; use paper-to-slides."
version: 1.0.0
metadata:
  author: "Yash Kavaiya <yash.kavaiya3@gmail.com>"
  tags: [poster, conference, tikzposter, research-communication]
---

# Paper to Poster

A poster is read from two metres away, in under a minute, by someone deciding whether to stop. Design for that reader first, then for the one who stays to talk.

## Purpose

Turn a paper into a poster that someone two metres away can understand in under a minute, and that supports a conversation with those who stop. Content is cut to a headline finding, one approach diagram, and two or three results.

## When to use

- A paper or abstract was accepted as a poster.
- A departmental or symposium poster session.
- Redesigning a text-heavy poster.

Hand off instead for a talk (`paper-to-slides`) or a written summary (`paper-to-blog`).

## Prerequisites

- The paper and its figures as vector files or source values.
- The conference's poster instructions: size, orientation, and any template.
- LaTeX (`tikzposter` or `beamerposter`) or PowerPoint for the build, and institution logos.

## Inputs

- The paper, and its figures as vector files or source data.
- The conference's poster instructions: size (A0, A1, 36 × 48 in, or other), orientation, and any template or logo rules. Sizes differ by event; get them from the instructions.
- Institution logos and branding requirements.
- Output format: LaTeX or PowerPoint.
- Whether it will be printed on paper or fabric, or shown on a screen.

## Instructions

1. **Confirm size and orientation** from the conference. A portrait A0 and a landscape 48 × 36 in board need different layouts.
2. **Write the headline finding**: one sentence in plain language stating the main result ("A 10-minute warm-up cuts injury rates by a third in amateur runners"). It is the most prominent text after the title, or it is the title.
3. **Choose the content.** A poster holds about 300 to 800 words in total. Select:
   - The problem and why it matters: 2 to 3 sentences or bullets.
   - The approach: one diagram with a short caption.
   - The 2 or 3 key results: one figure each, each with a caption that states the finding.
   - Conclusions: 3 bullets.
   - Reference to the paper, QR code, contact, acknowledgements, funding.

   Leave out the literature review, full methods, and most tables. The presenter and the paper supply those.
4. **Lay out the grid.** Three columns for landscape, two or three for portrait, with reading order top to bottom, then left to right. Number the sections or use clear headings. Give the results the largest area and the centre position. Keep 30 to 40% of the area as white space.

   ```
   +--------------------------------------------------------------+
   | TITLE (or headline finding)            authors | logos | QR  |
   +------------------+-----------------------+-------------------+
   | 1 Problem        | 3 Key result          | 4 Second result   |
   | 2 Approach       |   (largest figure)    | 5 Conclusions     |
   |   (diagram)      |                       | Refs, contact     |
   +------------------+-----------------------+-------------------+
   ```

5. **Set type sizes for distance** (for A0; scale for other sizes): title 85 to 120 pt, headline finding 60 to 80 pt, section headings 44 to 60 pt, body text 28 to 36 pt, captions and references 20 to 24 pt. Sans-serif for body text, left-aligned, in short lines and bullets.
6. **Remake the figures** for the poster: large fonts, thick lines, few series, direct labels, a finding-stating caption (`publication-figure-maker`, `architecture-diagram-maker`). Vector graphics, or raster at 150 to 300 dpi at final printed size.
7. **Choose a restrained palette**: one or two accent colours on a light background, strong contrast between text and background, and colour-blind-safe series colours. No background photos behind text.
8. **Add a QR code** to the paper, code, or a project page, with a short readable URL beside it. Test that it scans.
9. **Build it** with `tikzposter` or `beamerposter` in LaTeX, or a single custom-sized slide in PowerPoint (Design → Slide Size → Custom). Use the conference or institution template if one is required.
10. **Check a proof.** View at 100% zoom, and print on A4: if body text is readable at arm's length on A4, it will read at A0. Check logos, names, affiliations, and that images are not pixelated. Export to PDF with fonts embedded.
11. **Prepare the pitch**: a 30-second and a 2-minute spoken summary for people who stop.

## Output format

- A content plan:

```markdown
## Poster plan: <title> (<size>, <orientation>)
Headline: <one sentence>
| Block | Content | Words | Visual |
Total words: <n>
```

- The poster source (`.tex` or `.pptx`) and the PDF at final size.
- The 30-second and 2-minute pitch scripts.
- A print checklist: size, bleed if the printer needs it, file format, deadline.

## Examples

Requests that should trigger this skill:

- "Make an A0 poster for my accepted paper."
- "Design a conference poster from this manuscript."
- "What should go on my research poster?"
- "My poster has too much text. Redesign it."
- "Create a 36 by 48 inch landscape poster in PowerPoint layout."

Requests that belong to another skill:

- "Make slides for my talk." → use `paper-to-slides`
- "Write a blog post about my paper." → use `paper-to-blog`
- "Make a publication figure." → use `publication-figure-maker`

### Worked example

**Request:** "A0 portrait poster for my paper showing that a 10-minute warm-up reduced injuries among 400 amateur runners over a season."

**What the agent does:**

1. Confirms size and orientation from the conference instructions.
2. Writes the headline finding and selects content totalling about 450 words.
3. Lays out a two-column grid with the main result largest and sets type sizes for A0.
4. Plans remade figures, a QR code to the paper, and a 30-second pitch.

**Result (excerpt):**

```markdown
Headline: A 10-minute warm-up cut injuries by a third in amateur runners.

| Block | Content | Words | Visual |
|---|---|---|---|
| 1 Problem | why injuries matter for new runners | 50 | none |
| 2 Approach | randomised, 400 runners, one season | 60 | study flow diagram |
| 3 Key result | injury rate by group | 40 | large bar chart with interval |
| 5 Conclusions | 3 bullets | 60 | QR code |
Total words: 450. Body text 32 pt, headings 54 pt.
```

## Quality bar and pitfalls

- Take the dimensions from the conference instructions. A poster of the wrong size or orientation may not fit the board.
- The content comes from the paper. Do not round a result favourably for the headline or drop the condition it depends on.
- A shrunken paper is the most common bad poster. If it has paragraphs, cut more.
- Do not paste the abstract. The headline and conclusions replace it.
- Every figure needs a caption that says what it shows; viewers will not ask.
- Body text below about 24 pt at A0 cannot be read from where people stand.
- Use logos and images you are permitted to use, and follow the institution's branding rules.
- Compile or open the file and inspect it before delivering; say so if it could not be rendered.
- Printing takes time. Tell the user to check the print shop's turnaround before the travel date.

## Limitations

- Dimensions and template rules come from the conference; a wrong size cannot be fixed after printing.
- A poster carries a fraction of the paper. Methods detail and secondary results are left to the presenter and the paper.
- Print colour and resolution depend on the print shop and cannot be verified on screen.
- Rendering is confirmed only where LaTeX or PowerPoint is available.

## Troubleshooting

| Problem | Likely cause | Solution |
|---|---|---|
| Text is too small to read at distance | Too much content for the area | Cut words until body text can be 28 pt or larger at A0 |
| Figures print blurred | Low-resolution raster images were enlarged | Use vector figures, or raster at 150 to 300 dpi at final printed size |
| The LaTeX poster fails to compile | A missing poster class or an oversized image triggers an error | Install `tikzposter` or `beamerposter` and check image paths and sizes |
| The QR code does not scan | It is too small or low contrast | Print it at 4 cm or larger in black on white and test it on the proof |

## Related skills

- `paper-summarizer` and `abstract-writer` to distil the headline and conclusions.
- `publication-figure-maker` and `architecture-diagram-maker` to remake visuals at poster scale.
- `paper-to-slides` for the talk version, and `paper-to-blog` for a page the QR code can point to.
- `latex-paper-formatter` for LaTeX build problems.
- `viva-defense-prep` to rehearse answers to questions at the poster.
