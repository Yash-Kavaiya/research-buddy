---
name: paper-to-blog
description: "Rewrites a research paper as a plain-language blog post, lay summary, or social thread for a chosen audience, keeping numbers and caveats accurate. Use to publicise a paper. Not for formal abstracts."
version: 1.0.0
metadata:
  author: "Yash Kavaiya <yash.kavaiya3@gmail.com>"
  tags: [science-communication, blog, lay-summary, social-media]
---

# Paper to Blog

Explain the research to people outside the subfield without saying anything the paper does not support. Accuracy is kept; jargon and detail are what go.

## Purpose

Explain research to people outside the subfield without saying anything the paper does not support. The finding leads, the method is explained by example or analogy, numbers are put in context, and the limits are kept.

## When to use

- Announcing or explaining a new paper on a blog, lab website, newsletter, or social platform.
- A journal or funder requires a lay or plain-language summary.
- Explaining someone else's paper to a wider audience.

Hand off instead for a talk (`paper-to-slides`) or a video (`paper-to-explainer-video`).

## Prerequisites

- The paper, including its limitations section.
- The audience and the format: blog post, lay summary, or thread, with the platform's length limits.
- Links to the paper, preprint, and code, and the journal's embargo or press policy if any.

## Inputs

- The paper, including its limitations section.
- The audience: general public, practitioners in the field's industry, researchers in neighbouring fields, students, or policymakers.
- The format and platform: blog post (600 to 1,200 words), lay summary (150 to 300 words, per the journal's rules), thread (6 to 12 posts within the platform's character limit), LinkedIn post, newsletter item.
- Voice: the author's own first person, a lab's voice, or third-person reporting.
- Links to include: paper, preprint, code, data, demo.

## Instructions

1. **Find the story.** Answer in one sentence each: What did you find? Why should this reader care? What can someone do with it? What is still unknown? The first answer is the opening.
2. **Pick the audience's level** and decide which terms must be explained and which can be dropped. Explain a term the first time or replace it with a description.
3. **Structure for the format.**

   *Blog post*
   1. Title that states the finding or asks the question it answers.
   2. Opening paragraph: the finding and why it matters, in plain words.
   3. The problem: what was unknown or hard, with a concrete example.
   4. What was done: the approach by analogy or example, no more method than the reader needs.
   5. What was found: the two or three main results, with the key numbers in context.
   6. What it means and what it does not: implications and limits.
   7. What comes next, and links.

   *Thread*
   1. Post 1: the finding and why it matters, standing alone, with the key figure.
   2. Posts 2 to 3: the problem.
   3. Posts 4 to 6: the approach and results, one idea and ideally one image each.
   4. One post on limitations.
   5. Final post: link to the paper and code, credit to co-authors and funders.

   *Lay summary*: follow the journal's headings and word limit; aim for a reading age of about 12 to 14.
4. **Translate the numbers.** Put them in context ("from 12 errors in 100 to 9") and prefer absolute figures to relative ones for risks and effects. State what was measured, on what or whom.
5. **Use analogies carefully.** An analogy should make the mechanism clearer; say where it stops being accurate if a reader might over-extend it.
6. **Keep the caveats.** State the study type and its limits in plain language: sample, setting, whether it is a preprint not yet peer reviewed, and correlation versus causation. Match the paper's verbs: if the paper says "is associated with", the post does too.
7. **Choose visuals**: one clear figure from the paper, simplified and re-captioned, or a diagram (`publication-figure-maker`, `architecture-diagram-maker`). Add alt text.
8. **Write a headline that is true.** No "breakthrough", "cure", "solves", or "proves". Check that the headline alone would not mislead.
9. **Check against the paper**, sentence by sentence, for anything stronger than the source. For a post about someone else's paper, make clear whose work it is and link to it.
10. **Give variants**: alternative titles and, for threads, a shorter version.

## Output format

```markdown
## <Title>
<post body, with subheadings for a blog post>

*Paper: <citation and link>. Code: <link>. Authors: ...*

---
## Notes
- Audience and reading level: ...
- Claims checked against: §, Table, Fig.
- Caveats included: ...
- Alternative titles: ...
- Suggested image and alt text: ...
```

For a thread: numbered posts, each within the platform's limit, with the character count.

## Examples

Requests that should trigger this skill:

- "Write a blog post about my paper for a general audience."
- "Make a LinkedIn post announcing our new publication."
- "Turn this paper into a 10-post thread."
- "Write the plain-language summary the journal requires, 250 words."
- "Explain this paper to high-school students."

Requests that belong to another skill:

- "Write the formal abstract." → use `abstract-writer`
- "Make conference slides." → use `paper-to-slides`
- "Write a video script." → use `paper-to-explainer-video`

### Worked example

**Request:** "Blog post, about 700 words, general audience, for my paper: app-based CBT reduced insomnia severity by 3.9 points more than a leaflet in a 12-week trial of 180 adults."

**What the agent does:**

1. Finds the story: what was found, why a reader should care, and what is unknown.
2. Structures the post with the finding first and explains the approach by example.
3. Translates the numbers into context and states the study's limits in plain words.
4. Writes a headline that is true and checks each sentence against the paper.

**Result (excerpt):**

```markdown
## A sleep-therapy app helped people with insomnia more than standard advice
People with insomnia who used a therapy app for 12 weeks slept noticeably better than those given a leaflet of sleep tips, our new trial shows.

... On a standard 28-point insomnia scale, app users improved by about 7 points and leaflet readers by about 3.

**What we don't know yet.** The trial lasted 12 weeks and involved 180 adults who volunteered, so we can't say how long the benefit lasts or whether it holds for everyone.

Alternative titles: ...
```

## Quality bar and pitfalls

- Never state a result, number, or implication that is not in the paper. Simplifying is allowed; changing the claim is not.
- Do not turn a study in mice, in simulation, or on one dataset into a claim about people or the real world. Say what was studied.
- Health, safety, and financial topics need extra care: no advice to readers, and the limits stated near the top.
- Keep relative and absolute effects straight; "doubles the risk" from 1 in 10,000 to 2 in 10,000 must say so.
- Label a preprint as not yet peer reviewed.
- Avoid hype words and manufactured suspense. Readers and journalists discount them, and they damage the author's credibility.
- Credit co-authors, collaborators, and funders, and check the journal's embargo and press policy before publishing.
- Check the licence before reusing any figure from the published version. If reuse is not permitted, use the author's own originals or an open-access version.
- Write in the author's voice from their material. If the user will post it under their name, they should read and own every sentence.

## Limitations

- Simplification removes detail; the post is not a substitute for the paper and links to it.
- The post reflects the paper's claims and inherits its limitations.
- Platform character limits and journal press rules change and should be confirmed.
- Health, safety, and financial topics are described, never turned into advice for readers.

## Troubleshooting

| Problem | Likely cause | Solution |
|---|---|---|
| A sentence claims more than the paper does | Simplifying dropped a condition | Restore the condition in plain words: who was studied, for how long, and under what setting |
| The post is too technical | Terms were not explained | Replace or explain each term on first use and test against the stated audience |
| A thread post exceeds the platform limit | Sentences are too long | Split the idea across two posts or cut qualifiers that repeat |
| A number fails validation against the paper | A value was rounded or converted wrongly | Recheck it against the table and correct it before publishing |

## Related skills

- `paper-summarizer` to extract the findings and limitations accurately.
- `results-interpreter` for wording that matches the strength of the evidence.
- `abstract-writer` for the formal counterpart.
- `publication-figure-maker` and `architecture-diagram-maker` for a simplified visual.
- `paper-to-explainer-video`, `paper-to-slides`, and `paper-to-poster` for other formats.
- `academic-tone-editor` is the opposite direction (formal register); do not apply it to the post.
