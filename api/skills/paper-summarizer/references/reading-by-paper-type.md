# Reading and extracting by paper type

## 1. Three passes

| Pass | Read | Goal | Stop here if |
|---|---|---|---|
| 1 | Title, abstract, section headings, contribution list, conclusion, figure captions | What kind of paper, what it claims | The paper is not relevant |
| 2 | Introduction, figures and tables in full, method overview, results | How the claims are supported | A one-paragraph summary is all that is needed |
| 3 | Method in detail, experimental setup, limitations, appendix, footnotes | What exactly was done; where the caveats are | Never skip for a paper you will build on or cite for a specific result |

## 2. What to extract, by type

| Type | Problem section | Approach section | Evidence section | Watch for |
|---|---|---|---|---|
| Empirical study | Question, hypothesis | Design, participants, measures, procedure | Effect sizes with intervals, tests, sample sizes | Design limits on causal claims |
| Method paper (ML, engineering) | Task and gap in prior methods | Core idea, components, training and inference | Benchmarks, baselines, ablations, cost | Baseline strength; what is compared with what |
| Theory paper | Statement to be proved and why it matters | Assumptions, definitions, proof strategy | Theorems, bounds, tightness | Assumptions that restrict the result |
| Systems paper | Workload and bottleneck | Architecture and design decisions | Throughput, latency, scale, comparison | Hardware and workload specifics |
| Dataset or benchmark | Why existing data is insufficient | Collection, annotation, quality control | Statistics, baseline results | Licence, consent, annotator agreement, bias |
| Survey | Scope and inclusion | Taxonomy | Comparison tables, open problems | Date of coverage; missing areas |
| Position paper | Claim being argued | Line of argument | Examples, citations | Evidence versus opinion |
| Clinical trial | PICO | Randomisation, blinding, allocation | Primary outcome with CI, adverse events | Whether the primary outcome matches the registration |
| Qualitative study | Phenomenon and question | Sampling, data collection, analysis approach | Themes with quotes | Reflexivity, saturation, transferability |

## 3. Recording a result properly

A result needs six parts. If the paper omits one, write "not reported".

| Part | Example |
|---|---|
| Metric | top-1 accuracy |
| Value | 84.1% |
| Dataset or sample | ImageNet-1k validation |
| Comparison | ResNet-50 baseline at 81.3% |
| Uncertainty | ± 0.2 over 3 seeds |
| Location | Table 2 |

Report the difference in the paper's own terms. If the paper gives relative improvement, also give the absolute values.

## 4. The authors' claims versus yours

| Goes under | Content |
|---|---|
| The paper's sections | Only what the authors state |
| Limitations stated by the authors | Their own caveats, with location |
| Reader notes | Your observations: an untested assumption, a missing comparison, a question. Always labelled as yours |

Keep the authors' hedges. "Suggests", "may", and "in our setting" are part of the claim.

## 5. Where caveats hide

- Footnotes and table captions (different evaluation protocols, excluded data).
- The appendix (hyperparameter sensitivity, failed variants, extra datasets where the method does worse).
- The experimental setup paragraph (which baselines were rerun and which were copied from other papers).
- The limitations or broader-impact section, when the venue requires one.
- Supplementary material and the code repository's README.

## 6. Depth by purpose

| The reader wants to | Give |
|---|---|
| Decide whether to read it | One paragraph: problem, approach, main result with numbers, main limitation |
| Cite it | The exact claim and its location, with the conditions |
| Build on it | Full method detail, setup, what is unspecified, where the code is |
| Review it | Summary plus the claims-and-evidence table; then hand off to paper-critic |
| Teach it | Terms defined, intuition, one worked example |

## 7. Terms table

Define each term as the paper uses it, which may differ from common usage. Note any term the paper uses in two senses.

## 8. Checks before delivering

- Every number traced to a table, figure, or page.
- Nothing stated that is not in the paper.
- What was read is declared: full text, sections, or abstract only.
- The one-sentence takeaway matches the results, not the title.
