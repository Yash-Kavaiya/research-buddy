---
name: academic-tone-editor
description: "Edits academic prose for clarity, concision, hedging, and formal register while preserving meaning, terms, numbers, and citations. Use for language edits of a draft. Not for fixing the argument."
version: 1.0.0
metadata:
  author: "Yash Kavaiya <yash.kavaiya3@gmail.com>"
  tags: [editing, academic-writing, proofreading, style]
---

# Academic Tone Editor

Make the writing clearer and tighter without changing what it says. The author's claims, numbers, terms, and citations stay exactly as they are.

## Purpose

Make academic writing clearer and tighter without changing what it says. The author's claims, numbers, defined terms, and citations stay as written, and any sentence whose meaning is unclear is returned as a question instead of being rewritten.

## When to use

- A draft section needs a language edit before submission or supervisor review.
- Prose is wordy, vague, informal, over-hedged, or formulaic.
- A non-native English writer wants idiom and grammar corrected.

Hand off instead when the problem is structure or argument (`paper-outline-generator`, `self-peer-reviewer`), or when text is too close to a source (`plagiarism-and-paraphrase-checker`).

## Prerequisites

- The text to edit, as plain text, Markdown, or LaTeX.
- The spelling variant (British or American), the field, and the edit depth: proofread, copyedit, or substantive.
- No scripts or API keys are required.

## Inputs

- The text.
- Field and venue, and British or American spelling.
- Edit depth: *proofread* (grammar, spelling, punctuation only), *copyedit* (also wording and sentence structure; default), or *substantive* (also paragraph order and flow, with suggestions flagged).
- Anything that must not change: defined terms, quoted material, a required phrase.
- The venue's or institution's policy on AI-assisted editing, if the user knows it.

## Instructions

1. **Read the whole passage** before changing anything. Note the argument, the defined terms, and the author's voice.
2. **Protect the content.** Mark what will not be altered: technical terms, numbers and units, citations, equations, quotations, and the strength of each claim.
3. **Edit in passes:**
   1. *Clarity*: one idea per sentence; subject and verb close together; the actor named where it matters ("we measured", not "measurements were performed" when who did it matters); pronouns with a clear referent; terms used consistently (do not alternate "method", "approach", "technique" for the same thing).
   2. *Concision*: cut openers that carry nothing ("It is worth noting that", "In order to", "It can be seen that"); replace nominalisations with verbs ("perform an analysis of" becomes "analyse"); remove repeated statements and summaries of what was just said.
   3. *Hedging*: one hedge per claim, matched to the evidence. "May possibly suggest" becomes "suggests". Remove hedges from things that are simply true; keep them where the evidence is partial. Never strengthen a claim beyond what the author wrote.
   4. *Register*: no contractions or colloquialisms; no intensifiers ("very", "extremely", "clearly", "obviously"); no promotional words ("groundbreaking", "remarkable", "cutting-edge"); plain words over ornate ones ("use" over "utilise", "show" over "showcase").
   5. *Formulaic patterns*: vary sentence openings and length; remove signposting that announces instead of saying ("This section will discuss"); break up automatic triplets and paired contrasts used for rhythm; cut closing sentences that only restate the paragraph; remove stock transitions ("Moreover", "Furthermore", "Additionally") where the logic is already clear.
   6. *Mechanics*: grammar, articles, agreement, tense (past for what was done, present for general truths and what the paper shows), punctuation, spelling variant, number and unit style.
4. **Check meaning.** Compare each edited sentence with the original. If an edit changed the claim, its strength, or its scope, revert it or flag it as a question.
5. **Query, do not guess.** Where a sentence is ambiguous, give both readings and ask. Do not pick one and rewrite.
6. **Return** the edited text, a short change summary, and the queries.

## Output format

```markdown
## Edited text
<the full passage, ready to paste>

## What changed
- Concision: <N> words to <M> words
- Main edits: <three to six bullets with a before/after example each>

## Queries for the author
1. "<original sentence>": did you mean A or B?

## Left unchanged on purpose
- <terms, quotes, or sentences kept as written, and why>
```

For LaTeX input, return valid LaTeX and leave commands, labels, citations, and maths untouched. Offer a tracked-changes view (`latexdiff`, or bold and strikethrough) when asked.

## Examples

Requests that should trigger this skill:

- "Improve the academic tone of this paragraph."
- "Proofread my methods section."
- "Make this more concise; I need to cut 100 words."
- "This reads like AI wrote it. Make it read naturally without changing the content."
- "Fix grammar and articles; English is my second language."

Requests that belong to another skill:

- "Review my paper's argument and experiments." → use `self-peer-reviewer`
- "Is this paraphrase too close to the source?" → use `plagiarism-and-paraphrase-checker`
- "Rewrite my abstract from scratch." → use `abstract-writer`

### Worked example

**Request:** "Copyedit this sentence: "It is important to note that our proposed novel approach may possibly be able to potentially achieve a significant enhancement in terms of the accuracy.""

**What the agent does:**

1. Marks what will not change: the claim's strength (tentative) and the term accuracy.
2. Removes the empty opener and the stacked hedges, keeping one hedge.
3. Queries "significant", which may mean statistically significant.
4. Returns the edit with a change summary and the query.

**Result (excerpt):**

```markdown
## Edited text
Our approach may improve accuracy.

## What changed
- 26 words to 5. Removed "It is important to note that", "proposed novel", and three of four hedges.

## Queries for the author
1. "significant enhancement": do you mean statistically significant (then report the test) or large (then give the size)? I removed the word until you confirm.
```

## Quality bar and pitfalls

- Do not change the meaning, add content, or introduce a claim, number, example, or citation that was not in the original.
- Do not weaken or strengthen claims. Hedging edits adjust wording to evidence the author already described.
- Keep technical terms and defined notation even when a synonym would read better.
- Preserve the author's voice. An edit that makes every paragraph sound the same has gone too far.
- The purpose of removing formulaic phrasing is readability. This skill is for improving the author's own writing; it is not a tool for disguising the origin of text or evading detection software. If the user asks about AI-use rules, tell them to follow their venue's or institution's disclosure policy.
- Do not rewrite quotations or reference-list entries.
- When the passage has a problem that editing cannot fix (a missing step in the argument, an unsupported claim), say so instead of smoothing over it.

## Limitations

- Editing improves expression only. It cannot repair a missing argument, weak evidence, or an unsupported claim; those are reported.
- Field-specific phrasing can be misjudged; terms the author marks as required are kept.
- The skill is not a means of hiding the origin of text or evading detection software, and does not replace disclosure required by a venue.
- For LaTeX input, commands and maths are left untouched, so problems inside them are not fixed.

## Troubleshooting

| Problem | Likely cause | Solution |
|---|---|---|
| An edit changed the meaning | A hedge or qualifier was removed | Compare with the original, restore the qualifier, and treat the sentence as a query |
| The text became too uniform | Every sentence was restructured | Use a lighter edit depth and keep sentences that were already clear |
| LaTeX fails to compile after editing | A command, label, or brace was altered, producing an error | Diff against the original and restore the command; edits must leave LaTeX syntax unchanged |

## Related skills

- `self-peer-reviewer` for problems of argument and evidence.
- `plagiarism-and-paraphrase-checker` when wording is too close to a source.
- `abstract-writer` and `introduction-writer` when a section needs rewriting, not editing.
- `thesis-chapter-writer` for terminology consistency across chapters.
- `latex-paper-formatter` for formatting after the language is settled.
- `citation-style-converter` for reference formatting.
