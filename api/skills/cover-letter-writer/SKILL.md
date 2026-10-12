---
name: cover-letter-writer
description: "Writes the cover letter to a journal editor for a submission or revision: what the paper shows, fit to the journal, and declarations. Use for journal submissions. Not for reviewer responses."
version: 1.0.0
metadata:
  author: "Yash Kavaiya <yash.kavaiya3@gmail.com>"
  tags: [cover-letter, journal-submission, editor]
---

# Cover Letter Writer

## Purpose

Write a one-page letter that tells an editor what a manuscript contributes and why it belongs in their journal, and that carries every declaration the journal requires. Declarations are stated only when the author has confirmed them.

## When to use

- Submitting a manuscript to a journal.
- Resubmitting a revision, or transferring a paper after rejection elsewhere.
- Preparing the highlights, significance statement, or suggested-reviewer list the submission system asks for.

Hand off instead for the detailed response to reviewers (`rebuttal-writer`) or choosing the journal (`venue-recommender`).

## Prerequisites

- The manuscript's title, abstract, and main finding.
- The journal's aims and scope and its instructions for authors on cover letters.
- Facts for the declarations: funding, conflicts of interest, ethics approval, availability of materials, and any preprint.

## Inputs

- The manuscript: title, abstract, main finding with numbers.
- The journal, its aims and scope, and its instructions for authors on cover letters and declarations.
- The handling editor's name, from the journal's site, if a specific editor is addressed.
- Author details: corresponding author, affiliations, contact.
- Facts for the declarations: funding, conflicts of interest, ethics approval, data and code availability, preprint or prior presentation, related manuscripts under review.
- For a revision: the manuscript number and the decision letter.

## Instructions

1. **Read the journal's instructions** for what the letter must contain. Requirements differ; some journals want specific statements verbatim.
2. **Identify the fit**: which part of the journal's scope the paper serves, and one or two recent articles from the journal that the paper builds on or speaks to. Verify those articles exist and say what you describe (`paper-search`).
3. **Write the letter** in four short paragraphs:
   1. *Submission statement*: the title, the article type, and the journal.
   2. *What the paper does and finds*: the question, the approach in a clause, and the main result with a number. Two to four sentences, in plain terms an editor outside the subfield can follow.
   3. *Why it matters and why this journal*: the advance over what was known, who will use it, and the fit to scope.
   4. *Declarations*: original work, not under consideration elsewhere, all authors approve; conflicts of interest; funding; ethics approval and consent where applicable; data and code availability; preprint or conference version disclosed with its reference.
4. **Add optional elements only when the journal invites them**: suggested reviewers (names, affiliations, institutional emails, and the reason, with no recent collaborators or anyone with a conflict), opposed reviewers with a brief neutral reason, a request for a special issue, cover-art or word-count notes.
5. **For a revision**: reference the manuscript number, thank the editor and reviewers in one sentence, summarise the main changes in 3 to 5 bullets, and point to the attached point-by-point response.
6. **For a transfer after rejection**: do not hide the history if the journal asks; summarise how the paper changed in response to earlier reviews.
7. **Write the highlights or significance statement** if required, following the journal's limits (for Elsevier highlights: 3 to 5 bullets, each within the character limit stated in the guide for authors).
8. **Check** every fact in the letter against the manuscript, and keep the letter to one page.

## Output format

```text
<Date>

Dr. <Name>
Editor-in-Chief, <Journal>

Dear Dr. <Name>,

We submit our manuscript, "<Title>", for consideration as a <article type> in <Journal>.

<What the paper does and finds: 2 to 4 sentences with the main result.>

<Why it matters and why it fits this journal: 2 to 4 sentences.>

This manuscript is original, has not been published, and is not under consideration elsewhere. All authors have approved the submission. <Conflicts.> <Funding.> <Ethics.> <Data availability.> <Preprint disclosure.>

Sincerely,
<Corresponding author, affiliation, email>
```

Followed, when requested, by:

- Highlights (bulleted, within limits)
- Suggested reviewers table: name, affiliation, email, expertise, no-conflict confirmation
- A list of placeholders the author must fill: `[ethics approval number]`, `[grant number]`

## Examples

Requests that should trigger this skill:

- "Write a cover letter for my submission to the Journal of Hydrology."
- "Draft the letter to the editor for my manuscript."
- "Write a cover letter for my revised paper, manuscript ID 2025-0412."
- "Write the highlights for an Elsevier journal."
- "Suggest reviewers for my submission and format the list."

Requests that belong to another skill:

- "Write the point-by-point response to reviewers." → use `rebuttal-writer`
- "Which journal should I choose?" → use `venue-recommender`
- "Write a cold email to a professor." → use `supervisor-finder`

### Worked example

**Request:** "Cover letter to a remote-sensing journal for my paper: a method that maps flood extent from Sentinel-1 images with 91% accuracy on 14 events. No conflicts; funded by grant ABC-123; preprint on arXiv."

**What the agent does:**

1. Reads the journal's instructions and identifies the part of its scope the paper serves.
2. Writes four paragraphs: submission statement, what was done and found, why it fits, declarations.
3. States only the declarations the author confirmed and leaves a placeholder for the availability statement.
4. Checks every fact against the abstract and keeps the letter to one page.

**Result (excerpt):**

```markdown
Dear Dr. [Editor name],

We submit our manuscript, "[Title]", for consideration as a research article in [Journal].

Rapid flood mapping is limited by cloud cover in optical imagery. We present a method that maps flood extent from Sentinel-1 radar images and evaluate it on 14 flood events, where it reaches 91% overall accuracy.

... The work was funded by grant ABC-123. The authors declare no conflicts of interest. A preprint is available on arXiv ([identifier]). [Data availability statement to be confirmed.]
```

## Quality bar and pitfalls

- Declarations are statements of fact made by the authors. Never write "no conflicts of interest", "approved by the ethics committee", or "not under review elsewhere" unless the author has confirmed it. Use a bracketed placeholder and ask.
- Do not overstate the result. The letter's claims must match the abstract.
- Do not paste the abstract. The editor has it; the letter says why they should send the paper to review.
- Address the correct journal and editor. Wrong names left over from a previous submission are a common and avoidable embarrassment.
- No flattery of the journal and no claims that the work is "groundbreaking". State the advance concretely.
- Suggested reviewers must be real, independent experts with verifiable institutional emails. Never invent a reviewer or an address; fabricated reviewer contacts are grounds for retraction.
- Disclose preprints and overlapping publications. Undisclosed overlap is treated as misconduct.
- Keep it to one page.

## Limitations

- The letter relies on facts the author supplies. Declarations cannot be verified by the agent.
- Journals differ in what a cover letter must contain; the instructions for authors govern.
- Suggested reviewers must be identified and verified by retrieval; the agent cannot vouch for the absence of conflicts.
- A cover letter supports a submission; it does not change the editor's judgement of fit.

## Troubleshooting

| Problem | Likely cause | Solution |
|---|---|---|
| A required declaration is unknown | The author has not supplied it | Insert a bracketed placeholder and ask; never assert it |
| The letter repeats the abstract | It was summarised instead of argued | State the advance and the fit in new wording, two to four sentences each |
| The wrong journal or editor name appears | Text was reused from an earlier submission, which is an avoidable error | Check journal name, editor, and article type against the journal's site before sending |

## Related skills

- `venue-recommender` to choose the journal and confirm scope.
- `abstract-writer` for the main result statement.
- `rebuttal-writer` for the point-by-point response attached to a revision.
- `paper-search` to verify the journal articles mentioned for fit and to find independent reviewers.
- `ethics-irb-drafter` for the ethics and data statements.
- `camera-ready-checker` for the rest of the submission package.
