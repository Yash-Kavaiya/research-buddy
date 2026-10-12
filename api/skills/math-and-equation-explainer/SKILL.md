---
name: math-and-equation-explainer
description: "Explains equations, derivations, proofs, and notation from research papers step by step. Use when the maths in a paper is unclear. Not for whole-paper summaries; use paper-summarizer."
version: 1.0.0
metadata:
  author: "Yash Kavaiya <yash.kavaiya3@gmail.com>"
  tags: [mathematics, derivation, notation, latex]
---

# Math and Equation Explainer

## Purpose

Make a piece of mathematics understandable to a particular reader: what each symbol is, what the expression says, why each step follows, and which assumptions it needs. Skipped steps are filled in and marked.

## When to use

- A paper's equation, derivation, or proof is blocking the user.
- Notation is unfamiliar or inconsistent between papers.
- The user needs to re-derive a result to trust or extend it.

Hand off instead for understanding the paper as a whole (`paper-summarizer`) or for implementing the maths (`paper-to-code-reproducer`).

## Prerequisites

- The equation or derivation with its surrounding text, as LaTeX, pasted text, or a screenshot.
- The reader's mathematical background.
- Optional: a Python environment with SymPy or NumPy to verify algebra numerically.

## Inputs

- The equation or derivation, with surrounding text. Context decides what symbols mean; ask for the paragraph before and after if it is missing.
- The paper or source, to check its notation section and conventions.
- The reader's level: what they already know (calculus, linear algebra, probability, measure theory). Ask if unclear.

## Instructions

1. **Transcribe the equation** in LaTeX and confirm it matches the source, especially for screenshots. Subscripts, superscripts, and bold or calligraphic letters change meaning.
2. **Build the symbol table.** For each symbol: name, type (scalar, vector, matrix, set, function, random variable, operator), shape or domain, and meaning here. Mark any symbol whose meaning you inferred from context.
3. **Say what the equation states in one plain sentence** before any algebra.
4. **Explain the structure**: which term does what, and what happens when each grows or vanishes.
5. **For a derivation, show every step.** One operation per line, each with its justification: the rule, identity, or assumption used (chain rule, Jensen's inequality, independence, a Taylor expansion to first order). Fill in the steps the paper skipped, and flag each one you supplied.
6. **Name the assumptions** each step needs (differentiability, interchange of limit and integral, i.i.d. samples, positive definiteness). Note any the paper does not state.
7. **Sanity-check:**
   - Dimensions or shapes agree on both sides.
   - A special or limiting case gives a known result.
   - A small numeric example works; compute it with code when the arithmetic is non-trivial.
8. **Give the intuition** last: a geometric picture, an analogy, or the reason the form is natural. Label analogies as such.
9. **If a step does not follow**, say so. State what you tried, where it breaks, and whether it looks like a typo, a missing assumption, or a gap in your reading.

## Output format

```markdown
## The equation
$$ ... $$   (source: <paper>, Eq. <n>)

## In one sentence
...

## Symbols
| Symbol | Type and shape | Meaning | Source |
|---|---|---|---|
| $\theta$ | vector in $\mathbb{R}^d$ | model parameters | §2 |
| $\lambda$ | scalar > 0 | regularisation weight | inferred from context |

## Term by term
- $...$: ...

## Derivation
1. Start from ... $$ ... $$
2. Apply <rule> because <reason>: $$ ... $$
3. *(step not shown in the paper)* ...

## Assumptions used
- ...

## Checks
- Shapes: ...
- Limiting case: as $\lambda \to 0$, ...
- Numeric example: ...

## Intuition
...
```

Use `$...$` and `$$...$$` so the maths renders. Match the paper's notation; if you must change it, say so once and keep a mapping.

## Reference files

Open these only when the step calls for them; they are not needed for every request.

- `references/notation-and-derivation-patterns.md`: Read at steps 2, 5, and 6, when decoding notation, justifying derivation steps, and naming the assumptions each step needs.
- `assets/derivation-walkthrough-template.md`: Copy and fill for a step-by-step explanation of an equation or derivation.

## Examples

Requests that should trigger this skill:

- "Explain this equation from the paper: the ELBO in variational autoencoders."
- "How did they get from equation 3 to equation 4?"
- "What does this notation mean: E_{x~p}[log q(z|x)]?"
- "Derive the gradient of the cross-entropy loss with softmax."
- "Walk me through the proof of this lemma."

Requests that belong to another skill:

- "Summarise the paper." → use `paper-summarizer`
- "Implement this method in PyTorch." → use `paper-to-code-reproducer`
- "Typeset my derivation in the IEEE template." → use `latex-paper-formatter`

### Worked example

**Request:** "Explain why the gradient of softmax cross-entropy with respect to the logits is (p - y). I know the chain rule."

**What the agent does:**

1. Writes the loss and softmax in LaTeX and builds the symbol table with shapes.
2. States the result in one plain sentence before the algebra.
3. Derives it one operation per line with the rule used, marking the steps a paper would skip.
4. Checks shapes and verifies numerically on a three-class example.

**Result (excerpt):**

```markdown
## In one sentence
The gradient is the predicted probability vector minus the one-hot label, so each logit is pushed down in proportion to its excess probability.

## Derivation
1. Loss: $L = -\sum_k y_k \log p_k$, with $p_k = e^{z_k} / \sum_j e^{z_j}$.
2. Chain rule: $\partial L / \partial z_i = -\sum_k (y_k / p_k)\, \partial p_k / \partial z_i$.
3. *(step not shown in most papers)* Softmax derivative: $\partial p_k / \partial z_i = p_k(\delta_{ki} - p_i)$.
4. Substitute and use $\sum_k y_k = 1$: $\partial L / \partial z_i = p_i - y_i$.

## Checks
- Numeric: $z = (1, 2, 3)$, $y = (0, 0, 1)$ gives $p - y = (0.090, 0.245, -0.335)$, matching finite differences.
```

## Quality bar and pitfalls

- Do not skip steps the reader cannot do in their head. "It can be shown that" is what they came to get past.
- Do not guess a symbol's meaning silently. Mark inferences, and check the paper's notation section first.
- Verify algebra you produce. Recompute a derivation numerically or symbolically (for example with SymPy) when it is long or error-prone.
- Papers contain typos and sign errors. If the derived result differs from the printed one, show both and say which you believe and why.
- Conventions differ across fields: row versus column vectors, numerator versus denominator layout for derivatives, log base, expectation subscripts. State the convention in use.
- Intuition is not proof. Keep the two separate.

## Limitations

- Symbols are interpreted from the context supplied. Without the paper's notation section some meanings are inferred, and inferred meanings are marked.
- Screenshots can be misread; the transcription should be confirmed with the user.
- Long or novel proofs cannot always be verified. Steps that could not be confirmed are flagged, not asserted.

## Troubleshooting

| Problem | Likely cause | Solution |
|---|---|---|
| A derivation step does not follow | The paper has a typo, or an assumption is unstated | Show both versions, test numerically, and state which is believed and why |
| The derived result differs from the paper by a sign or factor | A different convention is in use, such as layout of derivatives or log base | State the convention explicitly and redo the step under the paper's convention |
| A symbol's meaning is unclear | It is defined elsewhere in the paper | Ask for the notation section or the paragraph where the symbol first appears |

## Related skills

- `paper-summarizer` for the context the equation sits in.
- `paper-critic` when a derivation's assumptions look unrealistic.
- `paper-to-code-reproducer` to turn the explained maths into an implementation.
- `latex-paper-formatter` to typeset derivations the user writes.
- `viva-defense-prep` when the user must explain the derivation aloud.
