# G3. Causal dynamical triangulations through the transfer matrix

## 2D: the spectrum, proved

The 2D CDT one-step propagator with a marked entrance loop is G(x, y; g) = gxy/((1 − gx)(1 − gx − gy))
(Ambjørn–Loll). Its coefficients give the transfer matrix

  M(l₁, l₂) = g^{l₁+l₂−1} C(l₁+l₂−1, l₁−1),   l₁, l₂ ≥ 1,   0 < g < ½.

**Theorem.** The symmetrised transfer matrix S = D^{−1/2} M D^{1/2}, with D = diag(l), is a positive
Hilbert–Schmidt operator on ℓ²(ℕ). Its nonzero spectrum is

  λ_n = x₋^{2n+2}/g,   n = 0, 1, 2, …,   x₋ = (1 − s)/(2g),   s = √(1 − 4g²),

so λ_{n+1}/λ_n = (1 − s)/(1 + s) and the lattice gap is Δ_lat = −log x₋² = 2 artanh s. With g = ½e^{−a²Λ},
Δ_lat(a)/a → 2√(2Λ) and E_n − E₀ = 2√(2Λ)·n.

**Proof.**
1. *Möbius action* (Lean: `CDT2D.propagator_row`, from Mathlib's negative binomial series). For |gx| < 1 and
   v_x = (x^l)_{l≥1},
   v_x M = h(x) v_{φ(x)},   h(x) = x/(1 − gx),   φ(x) = g/(1 − gx).
2. *Fixed point* (Lean: `phi_xm`, `xm_pos`, `xm_lt_one`, `phi_deriv_xm`, `h_xm`). x₋ ∈ (0, 1) solves φ(x₋) = x₋,
   with φ'(x₋) = x₋² and h(x₋) = x₋²/g.
3. *Triangular action.* Differentiate the identity of step 1 n times at x = x₋, by Leibniz and Faà di Bruno.
   With w_k = ∂ᵏv_x|_{x₋}, i.e. (w_k)_l = l(l−1)⋯(l−k+1) x₋^{l−k}:
   w_n M = h(x₋)φ'(x₋)ⁿ w_n + Σ_{k<n} c_{nk} w_k.
   On span{w₀, …, w_N}, M therefore acts as a triangular matrix with diagonal λ_n = h(x₋)φ'(x₋)ⁿ = x₋^{2n+2}/g
   (Lean: `eigen_geometric`). These values are distinct, so for every n there is a left eigenvector
   u_n ∈ span{w₀, …, w_n} with u_n M = λ_n u_n.
4. *Symmetrisation.* l₂M(l₁, l₂) is symmetric, so M = BD^{−1} with B symmetric, and S = D^{−1/2}BD^{−1/2} is
   symmetric. If uM = λu then (uD^{1/2})S = λ(uD^{1/2}). The vectors u_nD^{1/2} have entries √l·poly(l)·x₋^l and
   lie in ℓ². Moreover Σ S(l₁,l₂)² ≤ Σ_n (n+1)(2g)^{2n}·poly(n) < ∞, so S is Hilbert–Schmidt and self-adjoint.
5. *Completeness.* Suppose y ∈ ℓ² is orthogonal to every √l·l^k x₋^l. Then all derivatives at x₋ of
   F(z) = Σ y_l √l z^l vanish. F is analytic on |z| < 1, so F ≡ 0 and y = 0. The eigenvectors u_nD^{1/2} span a
   dense subspace. For a compact self-adjoint operator this means they exhaust the nonzero spectrum.
6. All λ_n > 0, so S is positive: the transfer matrix is reflection positive. ∎

The numerics in `python/qg/cdt2d.py` (eigenvalue ratios equal to r(g) to ten digits) agree.

**Why it matters for the programme.** This is a solvable model of quantum gravity in which the lattice gap scales
like the spacing, Δ_lat(a) ≈ 2√(2Λ)·a. That is exactly the behaviour 4Y-M's no-go theorem demands of any theory
with a continuum gap (Hypothesis R). 2D gravity has no graviton, so G1 does not exclude this phase.

## 3+1: what can be proved next

In the region of large bare cosmological constant κ₄ (the analogue of strong coupling), the spatial-volume process
of CDT is dominated by small slices. A Dobrushin argument for the slice-volume chain (each slice conditioned on its
two neighbours) should give uniqueness and a gap there, with the transfer-matrix positivity of CDT supplying the
spectral interpretation.
- Combined with `NoGraviton.lean`, this excludes the region from being gravitational.
- Status: open. The first step is a bound on the number of 4D CDT slabs between given 3-slices, which is exponential
  in the slice volumes (Ambjørn–Jurkiewicz–Loll), with explicit constants.
