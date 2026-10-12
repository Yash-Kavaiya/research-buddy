---
name: paper-to-explainer-video
description: "Plans an explainer video for a paper: timed narration script and scene-by-scene storyboard with visuals and animations. Use for video abstracts and explainers. Not for live talks; use paper-to-slides."
version: 1.0.0
metadata:
  author: "Yash Kavaiya <yash.kavaiya3@gmail.com>"
  tags: [video, storyboard, science-communication, animation]
---

# Paper to Explainer Video

## Purpose

Produce the two things a video is built from: what is said, second by second, and what is on screen while it is said. The script is written for the ear and budgeted to the target length, and every scene describes a visual precisely enough to build.

## When to use

- A conference or journal asks for a video abstract or presentation video.
- The user wants a YouTube explainer or a short clip for social media.
- Planning animations (Manim, After Effects, slides with motion) for a method.

Hand off instead for a live talk (`paper-to-slides`) or a written post (`paper-to-blog`). This skill produces the script and storyboard; rendering the video needs an animation or video tool, and if the session offers one, pass the storyboard to it.

## Prerequisites

- The paper and its figures.
- The target length, platform, aspect ratio, and audience.
- The production means (slides with voice-over, Manim, or other animation tool). The skill delivers a script and storyboard; rendering needs one of those tools.

## Inputs

- The paper and its figures.
- Target length and platform: video abstract (2 to 5 minutes, per the venue's rules), explainer (5 to 10 minutes), short vertical clip (30 to 90 seconds, 9:16).
- Audience: specialists, the wider field, students, or the public.
- Production means: screen-recorded slides with voice-over, animation (Manim suits mathematical and algorithmic content), talking head, or a mix. This decides what visuals are realistic.
- Narrator: the author's voice or a synthetic voice, and the language.
- The venue's technical requirements: duration, resolution, file size, captions.

## Instructions

1. **Fix the single message** and the three to five beats that deliver it. A video holds less than a talk of the same length.
2. **Budget the words.** Narration runs at about 140 to 160 words per minute; plan 150. A 3-minute video is about 450 words, less with pauses for animations. Write to the word count before anything else.
3. **Structure:**

   | Segment | Share | Purpose |
   |---|---|---|
   | Hook | first 5 to 15 s | A question, a surprising fact, or the result itself. Viewers decide here. |
   | Problem | 15% | What is hard or unknown, with a concrete example |
   | Idea | 25% | The key insight, built up visually |
   | How it works | 25% | The method in two or three steps |
   | Result | 20% | The main evidence, one or two visuals |
   | Close | 10% | What it means, limits, where to find the paper |

   For a short vertical clip: hook, one idea, one result, pointer to the paper.
4. **Write the narration** for the ear: short sentences, one idea each, active voice, the key term repeated instead of varied, numbers rounded sensibly and limited to those that matter. Read it aloud and time it.
5. **Storyboard scene by scene.** Each scene is 5 to 20 seconds. For each one specify:
   - Start time and duration.
   - The narration for that span.
   - What is on screen, described precisely enough to build: objects, layout, labels, colours.
   - The motion: what appears, moves, transforms, or is highlighted, and in what order, synchronised to which words.
   - On-screen text: a few words at most, never the narration repeated.
   - Source assets: which paper figure, dataset, or diagram it is built from.
6. **Design the visuals to explain.** Build diagrams piece by piece as they are mentioned; animate the data flow through the architecture; morph an equation term by term; show a chart drawing itself with the compared bar highlighted. Reuse one visual vocabulary (colours and shapes for the same concepts) throughout.
7. **Keep it accurate.** Simplified visuals must not misrepresent the method or exaggerate an effect; use the paper's real numbers and axes for results.
8. **Plan accessibility**: captions from the script, sufficient contrast, no information carried by colour alone, no rapid flashing.
9. **List the production assets**: figures to remake, animations to code, recordings, music (licensed or none), end card with title, authors, venue, and link.
10. **Check timing**: sum the scene durations, compare with the limit, and mark what to cut first.

## Output format

```markdown
# Explainer: <paper title>
Length: 3:00 (450 words). Format: 16:9, 1080p. Audience: ... Production: Manim + voice-over.
Message: <one sentence>

## Script (narration only)
<full text, with [pause] marks>   Word count: 447

## Storyboard
| # | Time | Narration | On screen | Motion | Text | Asset |
|---|---|---|---|---|---|---|
| 1 | 0:00–0:08 | "What if a model could ...?" | Blank dark background; question appears centre | Fade in word by word | the question | none |
| 2 | 0:08–0:25 | "..." | Three labelled boxes left to right: Input, Encoder, Output | Boxes draw in order; arrow animates between them | "Encoder" | Fig. 1 redrawn |

## Asset list
## Captions file (SRT) on request
## Cut list if over time
```

For Manim production, add per-scene implementation notes: the objects (`Text`, `MathTex`, `Axes`, `Rectangle`, `Arrow`) and animations (`Create`, `Write`, `Transform`, `FadeIn`, `Indicate`) to use.

## Examples

Requests that should trigger this skill:

- "Write a 3-minute video script explaining my paper."
- "Storyboard an explainer video for this method."
- "Create a video abstract for my journal article."
- "Plan a Manim animation of my algorithm."
- "Make a 60-second vertical clip script about my research."

Requests that belong to another skill:

- "Make slides for a live talk." → use `paper-to-slides`
- "Write a blog post." → use `paper-to-blog`
- "Draw a static architecture figure." → use `architecture-diagram-maker`

### Worked example

**Request:** "3-minute video abstract, 16:9, for researchers in neighbouring fields, on my paper about one-shot pruning that halves a model's parameters at 98% of its accuracy."

**What the agent does:**

1. Fixes the message and four beats, and budgets about 450 words.
2. Writes the narration for the ear and times it.
3. Storyboards 12 scenes with time, narration, on-screen objects, motion, and source asset.
4. Lists assets to build and what to cut first if over time.

**Result (excerpt):**

```markdown
| # | Time | Narration | On screen | Motion |
|---|---|---|---|---|
| 1 | 0:00–0:08 | "What if you could delete half of a neural network and barely notice?" | a dense grid of connected nodes | half the edges fade out together |
| 5 | 1:05–1:25 | "We score every weight once, using the data the model has already seen." | weight matrix as a heat map | cells brighten in order of score |
| 9 | 2:10–2:30 | "At half the size, accuracy stays within two percent." | bar chart from Table 1 | pruned bar grows beside the full bar |

Word count: 447. Captions: from the script.
```

## Quality bar and pitfalls

- The script contains only what the paper supports. Do not invent a demonstration, a number, or an application for the sake of the hook.
- Write narration first and fit visuals to it. A storyboard without timed words cannot be produced.
- Do not put the narration on screen as text. Viewers cannot read and listen to different words at once.
- One idea per scene; if a scene needs more than about 20 seconds, split it.
- Time it by reading aloud. Scripts that fit on paper routinely run 20% over.
- State limits in the close. A video travels further than the paper and will be seen without it.
- Use only footage, images, and music the user has rights to; credit sources on the end card.
- Follow the venue's rules on length, anonymity for review-stage videos, and file format.
- Be clear about what is delivered: a script and storyboard, not a rendered video, unless a rendering tool was actually used.

## Limitations

- The deliverable is a script and storyboard. No video is rendered unless an animation or video tool is actually used.
- Timing is estimated from word counts and must be checked by reading aloud.
- Simplified visuals risk misrepresenting a method; they are checked against the paper but remain abstractions.
- Music, footage, and images require rights the skill cannot grant.

## Troubleshooting

| Problem | Likely cause | Solution |
|---|---|---|
| The narration runs over the target length | Too many beats | Cut a beat, then trim sentences; do not speed up the read |
| A scene cannot be produced with the available tools | The visual is too elaborate | Simplify to shapes, text, and one motion per scene |
| A visual misrepresents the method | The simplification dropped a step | Check it against the method section and add the missing step or a caption |
| Manim rendering fails with an error | An object or animation name is invalid for the installed version | Check the names against the installed Manim version's documentation and render scene by scene |

## Related skills

- `paper-summarizer` to fix the message and the beats.
- `math-and-equation-explainer` for the step-by-step logic behind animated derivations.
- `architecture-diagram-maker` and `publication-figure-maker` for the visuals to animate.
- `paper-to-slides` when a recorded slide talk is enough.
- `paper-to-blog` for the description text and the post that accompanies the video.
- `paper-to-poster` to point a poster's QR code at the video.
