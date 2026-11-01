import Mathlib

/-!
# G3. The transfer matrix of two-dimensional causal dynamical triangulations

The one-step propagator of 2D CDT with a marked entrance loop (Ambjørn–Loll) has coefficients

  `M(l₁, l₂) = g^{l₁+l₂-1} · C(l₁+l₂-1, l₁-1)`,   `l₁ ≥ 1`.

**The key identity** (`propagator_row`): on the geometric sequences `v_x = (x^l)_l`,

  `Σ_{l₁ ≥ 1} x^{l₁} M(l₁, l₂) = h(x) · φ(x)^{l₂}`,   `h(x) = x / (1 - g x)`,   `φ(x) = g / (1 - g x)`,

for `|g x| < 1`, i.e. `v_x M = h(x) v_{φ(x)}`: the transfer matrix acts on generating functions through
the Möbius map `φ`. For `0 < g < 1/2`, `φ` has the fixed point `x₋ = (1 - s)/(2g)`, `s = √(1 - 4g²)`, with
`0 < x₋ < 1` (`xm_pos`, `xm_lt_one`, `phi_xm`), `φ'(x₋) = x₋²` (`phi_hasDerivAt`, `phi_deriv_xm`) and
`h(x₋) = x₋²/g` (`h_xm`).

Differentiating `v_x M = h(x) v_{φ(x)}` `n` times at `x₋` shows that `M` acts triangularly on the vectors
`w_n = ∂ⁿ v_x |_{x₋}` with diagonal `h(x₋) φ'(x₋)ⁿ`. Its eigenvalues are therefore

  `λ_n = x₋^{2n+2} / g`,   `λ_{n+1}/λ_n = x₋² = (1 - s)/(1 + s)`   (`ratio_xm`).

In `docs/G3-cdt.md` and the paper, the symmetrised matrix is shown to be Hilbert–Schmidt and the `w_n` to be
complete. That gives the whole spectrum, `{λ₀ rⁿ} ∪ {0}`, all eigenvalues positive. This file proves the
analytic identity and the algebra of the fixed point.
-/

open Real

namespace QuantumGravity.CDT

/-- The CDT transfer-matrix coefficient for `l₁ = n + 1`: `g^{n+l₂} · C(n+l₂, n)`. -/
noncomputable def M (g : ℝ) (n l2 : ℕ) : ℝ := g ^ (n + l2) * ((n + l2).choose n : ℝ)

/-- **The propagator acts on geometric sequences through a Möbius map.** -/
theorem propagator_row {g x : ℝ} (hgx : |g * x| < 1) (l2 : ℕ) :
    HasSum (fun n : ℕ => x ^ (n + 1) * M g n l2) (x / (1 - g * x) * (g / (1 - g * x)) ^ l2) := by
  have hr : ‖g * x‖ < 1 := by simpa [Real.norm_eq_abs] using hgx
  have hs := (hasSum_choose_mul_geometric_of_norm_lt_one (𝕜 := ℝ) l2 hr).mul_left (x * g ^ l2)
  have hne : 1 - g * x ≠ 0 := by
    have : g * x < 1 := (abs_lt.mp hgx).2
    linarith
  have hf : (fun n : ℕ => x ^ (n + 1) * M g n l2)
      = fun i : ℕ => x * g ^ l2 * (((i + l2).choose l2 : ℕ) * (g * x) ^ i) := by
    funext n
    unfold M
    rw [Nat.choose_symm_add]
    ring
  have hv : x / (1 - g * x) * (g / (1 - g * x)) ^ l2 = x * g ^ l2 * (1 / (1 - g * x) ^ (l2 + 1)) := by
    rw [div_pow, pow_succ]
    field_simp
  rw [hf, hv]
  exact hs

/-- `s = √(1 - 4 g²)`. -/
noncomputable def s (g : ℝ) : ℝ := Real.sqrt (1 - 4 * g ^ 2)

/-- The attracting fixed point `x₋ = (1 - s)/(2g)` of `φ(x) = g/(1 - g x)`. -/
noncomputable def xm (g : ℝ) : ℝ := (1 - s g) / (2 * g)

lemma s_nonneg (g : ℝ) : 0 ≤ s g := Real.sqrt_nonneg _

section
variable {g : ℝ} (hg : 0 < g) (hg2 : g < 1 / 2)
include hg hg2

lemma s_sq : s g ^ 2 = 1 - 4 * g ^ 2 := by
  unfold s
  rw [Real.sq_sqrt]
  nlinarith

omit hg2 in
lemma s_lt_one : s g < 1 := by
  unfold s
  rw [Real.sqrt_lt' one_pos]
  nlinarith

/-- `x₋ = 2g/(1 + s)`. -/
lemma xm_eq : xm g = 2 * g / (1 + s g) := by
  have h1 := s_sq hg hg2
  have h2 := s_nonneg g
  unfold xm
  rw [div_eq_div_iff (by positivity) (by positivity)]
  nlinarith

lemma xm_pos : 0 < xm g := by
  rw [xm_eq hg hg2]
  have := s_nonneg g
  positivity

lemma xm_lt_one : xm g < 1 := by
  rw [xm_eq hg hg2]
  have := s_nonneg g
  rw [div_lt_one (by positivity)]
  linarith

/-- `x₋` solves `g x² - x + g = 0`. -/
lemma xm_quadratic : g * xm g ^ 2 - xm g + g = 0 := by
  have h1 := s_sq hg hg2
  unfold xm
  field_simp
  nlinarith

lemma one_sub_gxm_pos : 0 < 1 - g * xm g := by
  have := xm_lt_one hg hg2
  nlinarith

/-- **`x₋` is a fixed point of `φ`.** -/
theorem phi_xm : g / (1 - g * xm g) = xm g := by
  have hq := xm_quadratic hg hg2
  have hne := (one_sub_gxm_pos hg hg2).ne'
  rw [div_eq_iff hne]
  linarith

/-- `h(x₋) = x₋² / g`. -/
theorem h_xm : xm g / (1 - g * xm g) = xm g ^ 2 / g := by
  have hne := (one_sub_gxm_pos hg hg2).ne'
  have hq := xm_quadratic hg hg2
  rw [div_eq_div_iff hne hg.ne']
  linear_combination (xm g) * hq

/-- **The eigenvalue ratio.** `x₋² = (1 - s)/(1 + s)`. -/
theorem ratio_xm : xm g ^ 2 = (1 - s g) / (1 + s g) := by
  have h1 := s_sq hg hg2
  have h2 := s_nonneg g
  rw [xm_eq hg hg2, div_pow, div_eq_div_iff (by positivity) (by positivity)]
  nlinarith

/-- `φ'(x₋) = x₋²`. -/
theorem phi_deriv_xm : g ^ 2 / (1 - g * xm g) ^ 2 = xm g ^ 2 := by
  rw [show g ^ 2 / (1 - g * xm g) ^ 2 = (g / (1 - g * xm g)) ^ 2 by rw [div_pow], phi_xm hg hg2]
end

/-- The derivative of `φ(x) = g/(1 - g x)`. -/
theorem phi_hasDerivAt {g x : ℝ} (hx : 1 - g * x ≠ 0) :
    HasDerivAt (fun y => g / (1 - g * y)) (g ^ 2 / (1 - g * x) ^ 2) x := by
  have h1 : HasDerivAt (fun y => 1 - g * y) (-g) x := by
    simpa using ((hasDerivAt_id x).const_mul g).const_sub 1
  have h2 := (hasDerivAt_const x g).div h1 hx
  have e : (0 * (1 - g * x) - g * -g) / (1 - g * x) ^ 2 = g ^ 2 / (1 - g * x) ^ 2 := by ring
  rw [e] at h2
  exact h2

/-- The eigenvalues `λ_n = x₋^{2n+2}/g` are positive and decrease geometrically with ratio
`(1 - s)/(1 + s)`. -/
theorem eigen_geometric {g : ℝ} (hg : 0 < g) (hg2 : g < 1 / 2) (n : ℕ) :
    0 < xm g ^ (2 * n + 2) / g ∧
      xm g ^ (2 * (n + 1) + 2) / g = (1 - s g) / (1 + s g) * (xm g ^ (2 * n + 2) / g) := by
  refine ⟨by have := xm_pos hg hg2; positivity, ?_⟩
  rw [← ratio_xm hg hg2]
  ring

end QuantumGravity.CDT
