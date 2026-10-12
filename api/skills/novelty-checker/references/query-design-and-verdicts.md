# Query design, comparison, and verdict rules

## 1. Decompose the idea

Write the idea in four slots. Novelty normally sits in one slot or in the combination.

| Slot | Question | Example |
|---|---|---|
| Problem | What is being solved or asked? | arrhythmia detection |
| Method | How? | contrastive pretraining on unlabeled signals |
| Setting | On what, for whom, under which constraint? | ECG, few labels |
| Benefit | What improves? | accuracy with 1% of labels |

## 2. Six query phrasings

Build one of each. Short keyword queries (two to five words) work best.

| # | Phrasing | Purpose | Example |
|---|---|---|---|
| 1 | The user's own words | What a similar-minded author would write | contrastive pretraining ECG arrhythmia |
| 2 | Field-standard terms | What reviewers would search | self-supervised learning electrocardiogram classification |
| 3 | Method synonyms and older names | Catches earlier vocabulary | representation learning ECG unlabeled |
| 4 | Problem only | Finds other methods for the same problem | few-label arrhythmia detection |
| 5 | Method only, adjacent setting | Finds the same method next door | contrastive learning biosignals EEG |
| 6 | Benefit or constraint | Finds work framed by the goal | label-efficient cardiac signal classification |

Vocabulary sources for phrasings 2 and 3: the keywords and titles of the two closest papers you already have, the arXiv category or MeSH heading, and the method's name in the paper that introduced it.

## 3. Where else to look

| Source | What it adds | How |
|---|---|---|
| Recent citing papers of the closest work | Follow-ups, where an idea is most often already done | citation-graph-explorer on the top two papers |
| The last two proceedings of the target venue | Work reviewers will know | Search venue name plus the problem term |
| Preprint servers sorted by date | The last three months | Sort one query by date |
| Workshop papers and theses | Early versions of ideas | Add "workshop" or search a thesis repository |
| Patents | Applied ideas, especially in engineering and biomedicine | Google Patents or Lens; state if not searched |
| Code repositories | Implementations without a paper | Search the method and task on a code host |

## 4. Component comparison

For each close paper answer four yes/partly/no questions and one free-text difference.

| Paper | Same problem | Same method | Same setting | Same evaluation | What differs |
|---|---|---|---|---|---|

Read the method section, not only the abstract, before writing "same method". Abstracts hide the details that distinguish approaches.

## 5. Verdict rules

| Verdict | Condition | What to tell the user |
|---|---|---|
| Already done | One paper is yes on problem, method, and setting | Name the paper; suggest a different angle or replication with a stated purpose |
| Incremental | Yes on problem and method; setting differs only by dataset, language, or scale | The difference must be shown to matter, or the contribution will be judged thin |
| Differentiated | A clear difference in at least one slot that would change the result or its use | State the difference in one sentence and the closest paper it distinguishes from |
| No close work found | No paper is yes on more than one slot | Report as a search result with its limits; widen the search before relying on it |

Combination novelty (known method A plus known method B) is differentiated only if the combination is non-obvious or the result is surprising. Say which.

## 6. Kinds of novelty a contribution can claim

| Kind | Claim form | What reviewers check |
|---|---|---|
| New problem | "We introduce the task of ..." | That the task is real and not a renaming |
| New method | "Unlike A and B, which ..., we ..." | The closest method and an ablation isolating the new part |
| New setting | "We are the first to study X under Y" | That Y changes something |
| New evidence | "We show, contrary to A, that ..." | The strength of the evaluation |
| New resource | "We release a dataset of ..." | How it differs from existing ones |
| New understanding | "We explain why ..." | Whether the explanation is tested |

## 7. Writing the novelty statement

Pattern: *Unlike <closest work>, which <what it does or assumes>, this work <the difference>, which <why it matters>.*

- Qualify "first" with scope and with "to our knowledge".
- Name the closest papers. Omitting them reads as not knowing them.
- State the difference as a fact about the two approaches.

## 8. Sharpening an idea that is too close

| If the overlap is in | Options |
|---|---|
| Method | Change the assumption (supervision, data, compute), or study why and when the method works |
| Setting | Move to a setting where the known method is expected to fail, and show it |
| Evaluation | Add the missing test: robustness, another population, long-term outcome, cost |
| Everything | Replicate with a clear purpose, or return to gap finding |
