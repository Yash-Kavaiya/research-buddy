# Gap types, evidence standards, and how to word a gap

## 1. Seven kinds of gap

| Type | What it is | Where it shows up in papers | Evidence needed to report it |
|---|---|---|---|
| Stated | Authors name it as a limitation or future work | Limitations, conclusion, survey "open challenges" | Two or more independent papers stating it, or one recent survey |
| Contradiction | Studies answer the same question differently | Results sections, meta-analyses, replication papers | Both sides named, with their sample, measure, and setting |
| Population or coverage | A group, language, region, domain, scale, or period nobody evaluated | Datasets and participants sections | A search for the missing group that returns nothing or very little, with the query shown |
| Methodological | A shared design weakness: no control, one dataset, a flawed metric, no variance | Methods and evaluation sections | Three or more papers with the same weakness, plus a reason the weakness could change conclusions |
| Measurement | The construct is measured by a proxy nobody has validated | Instruments, metrics | Evidence the proxy diverges from the construct (a paper showing it, or a clear argument) |
| Theoretical | Findings exist without an explanation, or a theory is untested in this setting | Discussion sections | The theory and the setting named, and a search showing no test |
| Transfer | A method proven nearby has not been tried here | Related work of neighbouring fields | The source result, and a reason it should (or might not) carry over |

A practical-relevance gap (results exist, but nothing usable in practice) is a variant of coverage. Report it only if the user's field values applied work.

## 2. Tests a candidate must pass

Apply all four before a gap goes in the report.

1. **Specific.** It can be written as one question with named variables or a named phenomenon and a named setting. "More work on fairness" fails.
2. **Evidenced.** At least one retrieved paper is cited for it, with what that paper says.
3. **Still open.** A targeted search of the last 18 months found nothing that closes it. Record the query and the count.
4. **Worth closing.** You can say what would change (for theory, practice, or method) if it were answered.

Then judge feasibility for this user: data access, time, skills, equipment, ethics.

## 3. Reading for gaps: where to look and what to mark

| Section | Phrases that signal a gap |
|---|---|
| Limitations | "we did not", "was limited to", "only", "small sample", "single site", "may not generalise" |
| Future work | "future work should", "remains to be", "an open question", "we leave" |
| Results | "unexpectedly", "in contrast to", "did not replicate", "inconsistent with" |
| Related work | "little attention", "few studies", "to our knowledge no" (check these; authors overstate) |
| Survey challenge sections | Read in full; each numbered challenge is a candidate cluster |

Mark in your working table: paper, section, the sentence, and your gap type. Quote the sentence so the evidence can be checked later.

## 4. Wording

Write the gap as a question, then as a statement for the proposal.

| Weak | Strong |
|---|---|
| "There is a lack of research on X." | "No study has tested whether X holds for Y; the six studies to date all use Z (A 2021; B 2022; ...)." |
| "X is under-explored." | "X has been evaluated on English text only; whether the effect survives in morphologically rich languages is unknown." |
| "More data is needed." | "The largest sample to date is 48 participants at one site (A 2023), too small to detect the moderate effect B (2022) predicts." |

Hedge to match the search: "we found no study that" is accurate; "no study exists" is a claim about the world.

## 5. Ranking

Score each surviving gap 1 to 3 on three axes and sort by the total, breaking ties by feasibility.

| Axis | 1 | 2 | 3 |
|---|---|---|---|
| Evidence | one paper | two or three papers | survey plus several papers, or a documented contradiction |
| Importance | incremental detail | changes how a method is used or a finding is read | changes a conclusion the field relies on |
| Feasibility for this user | needs resources they lack | possible with effort or a collaborator | doable with what they have |

## 6. Traps

- A gap that exists because the question is uninteresting or already known to be a dead end. Check whether anyone tried and reported a negative result.
- "Nobody has applied method M to dataset D." This is a gap only if the result would tell us something.
- Gaps taken from papers more than three years old without the still-open check.
- Treating a search miss as proof. Different communities use different words for the same problem; rerun with synonyms from the neighbouring field.
- Gaps too large for the user's project. Split them and keep the piece that fits.
