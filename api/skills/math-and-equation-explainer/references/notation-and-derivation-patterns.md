# Notation conventions and common derivation steps

## 1. Notation that varies between papers

State which convention is in use before explaining.

| Notation | Usual meaning | Variations to check |
|---|---|---|
| bold lowercase **x** | vector | column vector by default; some papers use rows |
| bold uppercase **X** | matrix | may also be a random vector in statistics |
| calligraphic 𝒟, 𝒳 | set, dataset, space, or distribution | 𝒩 is the normal distribution; 𝒪 is order notation |
| x_i versus x^(i) | i-th component versus i-th sample | conventions swap between fields |
| E_{x~p}[f(x)] | expectation of f under p | the subscript may name the variable, the distribution, or both |
| p(x; θ) versus p(x \| θ) | parameterised by versus conditioned on | Bayesian papers use the bar for both |
| log | natural log in ML and statistics | base 2 in information theory, base 10 in some sciences |
| ∇_θ L | gradient of L with respect to θ | shape follows θ |
| ‖x‖ | Euclidean norm | may be another norm; check for a subscript |
| ⊙, ∘ | elementwise product | ∘ can also be function composition |
| ⊗ | Kronecker or tensor (outer) product | context decides |
| 1[condition] | indicator, 1 if true else 0 | also written 𝟙 or [condition] |
| x ≜ y, x := y | defined as | |
| ∝ | proportional to | constant factors dropped, often a normaliser |
| argmax, argmin | the argument achieving the optimum | may be a set if not unique |
| Hat, bar, tilde, star | estimate, mean, perturbed or alternative, optimum | papers reassign these freely |
| O(·), Θ(·), Ω(·), o(·) | upper, tight, lower, strictly smaller asymptotic bounds | Õ hides log factors |

Derivative layout: with the numerator layout, ∂y/∂x for vector y and x is the Jacobian with rows indexed by y. The denominator layout is its transpose. Papers rarely say which they use; check shapes.

## 2. Symbol table discipline

For every symbol record type, shape or domain, meaning, and source. Mark "inferred" when the paper does not define it. A shape check on both sides of each equation catches most transcription and convention errors.

## 3. Steps that papers skip, and their justifications

| Step | Rule | Needs |
|---|---|---|
| Moving a derivative inside an expectation or integral | Leibniz rule, dominated convergence | Integrand differentiable, dominated by an integrable function; distribution not depending on the variable (else use the log-derivative trick) |
| ∇_θ E_{x~p_θ}[f(x)] = E[f(x) ∇_θ log p_θ(x)] | Log-derivative (score function) trick | p_θ differentiable in θ, support not depending on θ |
| Sampling x = g(ε, θ) with ε from a fixed distribution | Reparameterisation | g differentiable in θ |
| E[log X] ≤ log E[X] | Jensen's inequality | log concave; reversed for convex functions |
| Lower bound on a log-likelihood (ELBO) | Multiply and divide by q, then Jensen | q with the same support |
| p(x, y) = p(x \| y) p(y) | Product rule | none |
| p(x) = Σ_y p(x, y) | Marginalisation | none |
| p(y \| x) = p(x \| y) p(y) / p(x) | Bayes' rule | p(x) > 0 |
| E[X] = E[E[X \| Y]] | Tower rule | integrability |
| Var(X) = E[X²] − (E[X])² | Definition expanded | finite second moment |
| Product becomes sum | Log of a product; independence gives the product | independence, often i.i.d. samples |
| f(x) ≈ f(a) + f′(a)(x − a) | First-order Taylor expansion | f differentiable; x near a; error term dropped |
| \|⟨u, v⟩\| ≤ ‖u‖‖v‖ | Cauchy-Schwarz | inner-product space |
| ‖a + b‖ ≤ ‖a‖ + ‖b‖ | Triangle inequality | norm |
| P(∪ A_i) ≤ Σ P(A_i) | Union bound | none |
| P(X ≥ a) ≤ E[X]/a | Markov's inequality | X non-negative, a > 0 |
| Completing the square | Algebra | used to recognise a Gaussian |
| Lagrangian and stationarity | Constrained optimisation | constraint qualification; convexity for sufficiency |
| ∂/∂x (xᵀAx) = (A + Aᵀ)x | Matrix calculus | = 2Ax when A is symmetric |
| ∂/∂X log det X = X⁻ᵀ | Matrix calculus | X invertible |
| Chain rule through a composition | Chain rule | each function differentiable; mind the order of Jacobians |
| Softmax derivative: ∂p_k/∂z_i = p_k(δ_ki − p_i) | Quotient rule | none |
| "Constant with respect to θ" terms dropped | Optimisation does not depend on them | Check the term truly lacks θ |

## 4. Sanity checks

| Check | How |
|---|---|
| Shapes or units | Both sides must agree; a scalar loss cannot equal a vector |
| Limiting case | Set a parameter to 0, 1, or infinity and see whether a known result appears |
| Special case | One dimension, two classes, a single sample |
| Sign and direction | Does increasing the input move the output the way the text claims? |
| Numeric | Evaluate both sides on small random values; compare a gradient with finite differences |
| Symbolic | Reproduce the algebra with a computer algebra system |

## 5. When the paper seems wrong

1. Recheck the transcription and the convention.
2. Test numerically.
3. Look for an erratum or a later version.
4. Report both versions, say which one the check supports, and classify the discrepancy: typo, missing assumption, or unresolved.

## 6. Explaining to a reader

- Say what the expression means in one plain sentence before any algebra.
- One operation per line, each with its reason.
- Define a symbol where it first appears, not in a list the reader must hold in memory.
- Keep the paper's notation; if you change it, give the mapping once.
- Separate intuition from derivation, and say where an analogy stops being accurate.
