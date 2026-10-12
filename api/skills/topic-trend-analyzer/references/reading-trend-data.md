# Reading bibliometric trend data

## 1. Getting the query right

The query decides every number. Test it before trusting the output.

| Problem | Symptom in the output | Fix |
|---|---|---|
| Ambiguous phrase | Unrelated fields in rising subtopics (a search for "transformer" returns power engineering) | Add a qualifier or use the full term: "transformer language model" |
| Phrase too narrow | Counts in single digits, or sudden zeros | Use the broader established term; check the acronym |
| Synonyms split the topic | A plateau that coincides with a newer name appearing | Run each name separately and report them side by side |
| Renaming over time | Apparent birth of a topic in a given year | Run the older name as well ("neural networks" before "deep learning") |
| Acronym collision | Counts far above expectation | Use the expanded form |

Report the exact phrase and whether title and abstract or full text was searched. Full-text search inflates counts with passing mentions.

## 2. Three signals and what each one cannot tell you

| Signal | Meaning | Blind spot |
|---|---|---|
| Papers per year | Volume of activity | The whole literature grows every year, so rising counts are the default |
| Share per 10,000 indexed papers | Activity relative to everything indexed | Changes in what the index covers shift the denominator |
| Compound annual growth rate | One number for the range | Hides the shape; sensitive to a small first-year count |

Read the yearly table first and use the growth rate as a summary only.

## 3. Stage classification

| Stage | Pattern | Typical implication for a newcomer |
|---|---|---|
| Emerging | Under roughly 100 papers a year, share rising fast, few surveys | Room for foundational work; terminology unstable; fewer baselines to compare with |
| Rapid growth | Count and share both rising steeply for three or more years | High attention and competition; work dates quickly |
| Maturing | Count rising, share flattening | Benchmarks and standards exist; contributions need rigour or a niche |
| Plateau | Share flat for two or more years | Look for subtopics still rising inside the plateau |
| Decline | Share falling for three or more years | Check whether the topic was renamed or absorbed before calling it dead |

The thresholds are guides. A field's size matters: 100 papers a year is large in a small discipline.

## 4. Rising subtopics and keywords

- The script compares two windows of equal length. A ratio of 3 means three times as many papers in the recent window.
- "under N" in the earlier column means the group was outside the 200 largest groups then. Its true earlier count is unknown and below N. Report these as new or emerging, never as growth from zero.
- Ignore groups with small recent counts; ratios on small numbers are noise.
- Topic and keyword labels are assigned by the index automatically. Treat a surprising label as a prompt to look at the papers.

## 5. Explaining an inflection

A jump in a given year usually follows something. Candidates to check, and verify by retrieval before stating:

| Cause | How to check |
|---|---|
| A landmark paper | Most-cited paper on the topic from the one or two years before the jump |
| A dataset, benchmark, or shared task | Search the topic with "dataset" or "benchmark" for that period |
| A tool or library release | Release date from the project's own page |
| A funding programme or policy change | Funder announcements for that year |
| An external event | For example a pandemic year for health topics |
| An indexing change | A jump across many unrelated topics in the same year points to the index, not the field |

If nothing can be verified, write "no clear cause identified".

## 6. Caveats to report every time

- The last complete year is provisional; indexing lags by months, more for journals than preprints.
- Coverage differs by field. Humanities, books, and non-English work are under-represented.
- Volume measures attention, not quality, and not the number of open problems.
- Counts from different databases are not comparable with each other.

## 7. Comparing topics

When comparing two or more topics, use the same year range and the same search mode for each, show them in one table by year, and compare shares. A small topic growing fast and a large topic growing slowly can both be good choices for different reasons; say which reason applies.

## 8. From trend to decision

| The user wants to | Read the data for |
|---|---|
| Pick a thesis topic | A rising subtopic inside a field that is growing or maturing, with at least one survey to learn from |
| Motivate a proposal | Share growth and a verified cause, in one sentence with the numbers and the source |
| Avoid a crowded area | Rapid growth plus many recent surveys signals crowding |
| Time a submission | Whether the topic's venues are still expanding their tracks |
