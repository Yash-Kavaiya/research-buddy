# Snowballing method

## 1. Two directions, two purposes

| Direction | Finds | Bias |
|---|---|---|
| Backward (references of the seed) | What the work builds on: foundations, methods, datasets | Toward older and well-known work |
| Forward (papers citing the seed) | What builds on the work: extensions, applications, critiques | Toward whatever is already cited a lot; recent papers have few citations |

A complete expansion uses both, then a dated keyword search for the last few months, which the citation graph has not caught up with.

## 2. Choosing seeds

Good seeds are on-topic, well indexed, and different from each other.

| Seed set | Result |
|---|---|
| One landmark paper | Its most-cited references, dominated by general classics |
| Two to five papers from the same subtopic, different groups | Shared references that define the subtopic |
| A recent survey | A very wide backward set; use it to find seeds, not as a seed |
| Papers from different subtopics | Shared references are generic; split into separate runs |

Use the published version's DOI where one exists. Preprint records often have incomplete reference lists.

## 3. Reading the output

**Seminal candidates** are ranked by how many seeds cite them, then by total citations. With three seeds, a paper cited by all three is a shared foundation.

Classify every paper in the backward and seminal lists:

| Role | Description | Keep? |
|---|---|---|
| Topic foundation | Introduces the problem, the core method, or the key finding | Yes |
| Direct predecessor | The approach the seeds improve on | Yes |
| General tool | Datasets, optimizers, metrics, libraries, statistical methods | Only if the user needs them |
| Background | Textbook-level context | Usually no |
| Tangential | Cited once for a passing point | No |

Classify every paper in the forward list by what it does with the seed:

| Relation | Signal in the citing paper |
|---|---|
| Extends | Builds a method on the seed |
| Applies | Uses the seed's method in another domain |
| Compares | Uses the seed as a baseline |
| Critiques or fails to replicate | Reports a problem with the seed |
| Surveys | Places the seed in a taxonomy |
| Mentions | Cites in passing |

Read the abstract, and the sentence that cites the seed if available, before assigning a relation.

## 4. How far to go

| Hop | Size | When to take it |
|---|---|---|
| 0 | the seeds | always |
| 1 | references and citing papers of the seeds | always |
| 2 | one hop from the two or three most relevant new papers | when hop 1 revealed a subtopic the user cares about |
| 3 or more | grows very fast and drifts | only inside a systematic review with screening criteria |

Stopping rule for reviews: stop when a full round adds no new paper that meets the inclusion criteria.

## 5. Finding the newest follow-ups

The forward list is sorted by citations, so a strong paper from last month is invisible. For each seed, run a keyword search on the seed's method name or dataset name with a recent year filter and sort by date.

## 6. Data problems and what to do

| Symptom | Cause | Action |
|---|---|---|
| A seed shows 0 references | The index has no reference list for that record | Use the published version's DOI |
| A classic shows an implausible year | Duplicate or republished record | Confirm the year on the publisher page before quoting it |
| The same paper twice | Preprint and published versions | Keep the published one |
| A reference list much shorter than the paper's | Partial indexing | Say so; supplement with the PDF's reference list |

## 7. Signals worth noting

- A paper cited by every seed but unknown to the user is the most valuable output.
- A highly cited paper that the seeds do not cite may belong to a neighbouring community working on the same problem under another name.
- A cluster of citing papers that criticise a seed means its claims are contested; flag it.
- Citation counts measure attention. Read before recommending.
