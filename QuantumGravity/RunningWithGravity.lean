import Mathlib

/-!
# G6. Gravity does not spoil asymptotic freedom if it antiscreens

Above the Planck scale, gravitational fluctuations add a term linear in `g` to the Yang–Mills
β-function (Robinson–Wilczek; Folkerts–Litim–Pawlowski; the asymptotic-safety literature):

  `dg/dt = -b g³ - f g`,   `t = log (μ / μ₀)`,

with `b = b₀ > 0` the one-loop Yang–Mills coefficient (`11 N / (48 π²)` in 4Y-M's
`RunningCoupling.lean`) and `f` the gravitational coefficient. Its sign is scheme dependent, but
every symmetry-preserving computation gives `f ≥ 0` (antiscreening). In `u = 1 / g²` the flow is
linear:

  `du/dt = 2 b + 2 f u`,   so   `u(t) = (u₀ + b/f) e^{2 f t} - b/f`   (`f ≠ 0`).

Proved here:

* `uSol_hasDerivAt`: the closed form solves the flow;
* `uSol_ge_ym` (`f > 0`): `u(t) ≥ u₀ + 2 b t`, so the gauge coupling with gravity is never larger
  than the pure Yang–Mills one-loop coupling at the same scale;
* `gsq_tendsto_zero_of_antiscreening` (`f > 0`): asymptotic freedom survives;
* `gsq_tendsto_fixedPoint_of_screening` (`f < 0`, `b > 0`): instead `g² → -f/b > 0`, an interacting
  ultraviolet fixed point, so asymptotic freedom is lost and the sign of `f` decides between the two;
* `window_entered_with_gravity` (`f > 0`): every coupling `g_*² < g₀²` is reached at an explicit
  scale `t_*`, so 4Y-M's "the intermediate window is always entered" survives the gravitational
  correction.

Not claimed: the value or the sign of `f`. Both depend on the scheme, and this file is conditional
on them.
-/

open Real Filter Topology

namespace QuantumGravity.Running

/-- Closed-form solution of `du/dt = 2 b + 2 f u`, `u(0) = u₀`, for `f ≠ 0`. -/
noncomputable def uSol (b f u0 t : ℝ) : ℝ := (u0 + b / f) * Real.exp (2 * f * t) - b / f

theorem uSol_zero (b f u0 : ℝ) : uSol b f u0 0 = u0 := by
  simp [uSol]

theorem uSol_hasDerivAt (b f u0 t : ℝ) (hf : f ≠ 0) :
    HasDerivAt (uSol b f u0) (2 * b + 2 * f * uSol b f u0 t) t := by
  have h1 : HasDerivAt (fun t => 2 * f * t) (2 * f) t := by
    simpa using (hasDerivAt_id t).const_mul (2 * f)
  have h2 := (h1.exp).const_mul (u0 + b / f)
  have h3 := h2.sub_const (b / f)
  have e : (u0 + b / f) * (Real.exp (2 * f * t) * (2 * f)) = 2 * b + 2 * f * uSol b f u0 t := by
    unfold uSol
    field_simp
    ring
  rw [← e]
  exact h3

/-- Antiscreening only helps: the inverse coupling grows at least as fast as without gravity. -/
theorem uSol_ge_ym {b f u0 t : ℝ} (hb : 0 ≤ b) (hf : 0 < f) (hu : 0 ≤ u0) (ht : 0 ≤ t) :
    u0 + 2 * b * t ≤ uSol b f u0 t := by
  unfold uSol
  have hA : 0 ≤ u0 + b / f := by positivity
  have hexp : 1 + 2 * f * t ≤ Real.exp (2 * f * t) := by
    have := Real.add_one_le_exp (2 * f * t); linarith
  have h := mul_le_mul_of_nonneg_left hexp hA
  have e : (u0 + b / f) * (1 + 2 * f * t) - b / f = u0 + 2 * b * t + 2 * f * u0 * t := by
    field_simp
    ring
  have : 0 ≤ 2 * f * u0 * t := by positivity
  linarith

theorem uSol_tendsto_atTop {b f u0 : ℝ} (hb : 0 ≤ b) (hf : 0 < f) (hu : 0 < u0) :
    Tendsto (uSol b f u0) atTop atTop := by
  have hA : 0 < u0 + b / f := by positivity
  have h1 : Tendsto (fun t : ℝ => 2 * f * t) atTop atTop :=
    tendsto_id.const_mul_atTop (by positivity)
  have h2 : Tendsto (fun t : ℝ => (u0 + b / f) * Real.exp (2 * f * t)) atTop atTop :=
    (Real.tendsto_exp_atTop.comp h1).const_mul_atTop hA
  exact tendsto_atTop_add_const_right _ _ h2

/-- **Asymptotic freedom with antiscreening gravity.** -/
theorem gsq_tendsto_zero_of_antiscreening {b f u0 : ℝ} (hb : 0 ≤ b) (hf : 0 < f) (hu : 0 < u0) :
    Tendsto (fun t => 1 / uSol b f u0 t) atTop (𝓝 0) := by
  exact (uSol_tendsto_atTop hb hf hu).inv_tendsto_atTop.congr fun t => by simp [one_div]

/-- **Screening gravity gives a fixed point instead.** For `f < 0` the inverse coupling tends to
`-b/f`, so `g² → -f/b > 0`. -/
theorem uSol_tendsto_of_screening {b f u0 : ℝ} (hf : f < 0) :
    Tendsto (uSol b f u0) atTop (𝓝 (-(b / f))) := by
  have h1 : Tendsto (fun t : ℝ => 2 * f * t) atTop atBot :=
    tendsto_id.const_mul_atTop_of_neg (by linarith)
  have h2 : Tendsto (fun t : ℝ => Real.exp (2 * f * t)) atTop (𝓝 0) :=
    Real.tendsto_exp_atBot.comp h1
  have h3 : Tendsto (fun t : ℝ => (u0 + b / f) * Real.exp (2 * f * t) - b / f) atTop
      (𝓝 ((u0 + b / f) * 0 - b / f)) :=
    (h2.const_mul _).sub_const _
  have e : (u0 + b / f) * 0 - b / f = -(b / f) := by ring
  rw [e] at h3
  exact h3

theorem gsq_tendsto_fixedPoint_of_screening {b f u0 : ℝ} (hb : 0 < b) (hf : f < 0) :
    Tendsto (fun t => 1 / uSol b f u0 t) atTop (𝓝 (-f / b)) := by
  have hne : -(b / f) ≠ 0 := by
    have : b / f < 0 := div_neg_of_pos_of_neg hb hf
    linarith
  have h := (uSol_tendsto_of_screening (b := b) (u0 := u0) hf).inv₀ hne
  have e : (-(b / f))⁻¹ = -f / b := by
    field_simp
  rw [e] at h
  simpa [one_div] using h

/-- The scale at which the inverse coupling reaches `u*`. -/
noncomputable def tStar (b f u0 ustar : ℝ) : ℝ :=
  Real.log ((ustar + b / f) / (u0 + b / f)) / (2 * f)

/-- **Every weaker coupling is reached, at an explicit scale**, with antiscreening gravity. -/
theorem window_entered_with_gravity {b f u0 ustar : ℝ} (hb : 0 ≤ b) (hf : 0 < f) (hu : 0 < u0)
    (hs : u0 ≤ ustar) :
    0 ≤ tStar b f u0 ustar ∧ uSol b f u0 (tStar b f u0 ustar) = ustar := by
  have hA : 0 < u0 + b / f := by positivity
  have hB : 0 < ustar + b / f := by linarith
  have hq : 1 ≤ (ustar + b / f) / (u0 + b / f) := by
    rw [le_div_iff₀ hA]; linarith
  have hqpos : 0 < (ustar + b / f) / (u0 + b / f) := by positivity
  refine ⟨div_nonneg (Real.log_nonneg hq) (by positivity), ?_⟩
  unfold uSol tStar
  have e : 2 * f * (Real.log ((ustar + b / f) / (u0 + b / f)) / (2 * f))
      = Real.log ((ustar + b / f) / (u0 + b / f)) := by
    field_simp
  rw [e, Real.exp_log hqpos]
  field_simp
  ring

end QuantumGravity.Running
