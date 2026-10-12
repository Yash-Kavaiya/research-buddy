# Question frameworks, wording patterns, and hypothesis forms

## 1. Choosing the framework

| Framework | Elements | Use for | Example |
|---|---|---|---|
| PICO(T) | Population, Intervention, Comparison, Outcome, (Time) | Interventions and comparisons | In adults with insomnia (P), does app-based CBT (I), compared with a sleep-hygiene leaflet (C), reduce insomnia severity (O) at 12 weeks (T)? |
| PECO | Population, Exposure, Comparison, Outcome | Observational studies of an exposure | In factory workers (P), is night-shift work (E), compared with day work (C), associated with hypertension (O)? |
| SPIDER | Sample, Phenomenon of Interest, Design, Evaluation, Research type | Qualitative and mixed methods | How do newly qualified nurses (S) experience their first night shifts (PI), explored through interviews (D), in terms of coping strategies (E), in a qualitative study (R)? |
| PCC | Population, Concept, Context | Scoping reviews | What is known about digital literacy (C) among older adults (P) in rural health services (C)? |
| SPICE | Setting, Perspective, Intervention, Comparison, Evaluation | Service and policy evaluation | In district hospitals (S), for patients (P), does nurse-led discharge (I), compared with doctor-led (C), change satisfaction (E)? |
| Task, Method, Baseline, Metric, Setting | as named | Computational and engineering work | For low-resource translation (T), does subword regularisation (M) improve BLEU (Mt) over standard BPE (B) with under 100k sentence pairs (S)? |

## 2. Question types and the verbs that fit them

| Type | Stem | Design it implies |
|---|---|---|
| Descriptive | What is the prevalence, level, or distribution of ...? | Survey, records analysis |
| Comparative | Does X differ between A and B? | Group comparison |
| Relational | Is X associated with Y? To what extent does X predict Y? | Correlational, regression |
| Causal | Does X cause, increase, or reduce Y? | Experiment or strong quasi-experiment |
| Exploratory | How do ... experience ...? What factors shape ...? | Qualitative |
| Evaluative | How well does X meet goal G under conditions C? | Evaluation study, benchmark |

Use a causal verb only if the design can support it. "Effect of" in the question promises an experiment.

## 3. FINER, with the question to ask for each letter

| Criterion | Ask | Typical failure |
|---|---|---|
| Feasible | Can this person get the participants, data, time, and skills? | Needs a sample or access they do not have |
| Interesting | Would the answer matter to anyone besides the researcher? | A result that is obvious in either direction |
| Novel | Does it confirm, refute, or extend what is known? Checked by search? | Already answered; novelty asserted without a search |
| Ethical | Would a committee approve it? Are risks proportionate? | Vulnerable group without safeguards |
| Relevant | Does it advance knowledge, practice, or policy? | No path from answer to use |

## 4. From question to objectives

One aim, then three or four objectives, each starting with a measurable verb.

| Level | Verbs |
|---|---|
| Describe | identify, describe, estimate, characterise, map |
| Compare or relate | compare, examine the association, assess the difference |
| Explain or test | test, evaluate, determine whether |
| Build | develop, design, implement, validate |

Avoid "understand", "explore" (in quantitative work), "look at", and "study": they cannot be checked off.

Pattern: *To <verb> <variable or phenomenon> in <population or setting> using <measure or method>.*

## 5. Hypotheses

| Form | Template | Example |
|---|---|---|
| Null | There is no difference in O between I and C. | H0: Mean ISI at 12 weeks does not differ between groups. |
| Directional alternative | O is lower (or higher) in I than in C. | H1: Mean ISI at 12 weeks is lower in the app group. |
| Non-directional | O differs between I and C. | Use when theory gives no direction. |
| Associative | X is positively (negatively) associated with Y. | Longer screen time is associated with shorter sleep duration. |
| Moderation | The effect of X on Y is stronger when Z is high. | The benefit is larger for participants under 30. |
| Mediation | X affects Y through M. | Feedback raises grades by increasing time on task. |

State one primary hypothesis per primary outcome. List the variable type for each side (continuous, ordinal, binary, count), because that decides the test.

Qualitative studies have no hypotheses. They have a central question and sub-questions, usually starting with "how" or "what".

## 6. Operational definitions

For each term in the question give: the conceptual definition with its source, the measure (instrument or metric), the unit or scale, and when it is measured.

| Term | Conceptual definition | Measure | Scale | Timing |
|---|---|---|---|---|
| exam stress | perceived stress related to examinations | Perceived Stress Scale, 10 items | 0 to 40 | week 0 and week 4 |

## 7. Faults and fixes

| Fault | Example | Fix |
|---|---|---|
| Too broad | How does social media affect teenagers? | Name the platform or behaviour, the outcome, the age band, the setting |
| Double-barrelled | Does the app improve sleep and mood? | Split; pick one as primary |
| Yes/no for an exploratory aim | Do nurses cope with night shifts? | How do nurses cope with ...? |
| Solution in the question | How can gamification fix low engagement? | Does gamification, compared with X, change engagement measured by Y? |
| Unmeasurable term | effective, better, successful | Replace with the measure that defines it |
| Value judgement | Should schools ban phones? | What is the association between phone bans and attainment? |
