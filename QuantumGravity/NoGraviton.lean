import Mathlib

/-!
# G1. A gapped lattice phase has no graviton

In Yang–Mills a mass gap is the goal; in gravity it is a diagnosis. A graviton is massless, so in
a reflection-positive theory a spatially smeared field coupling to it has temporal two-point
function `S(t) = ∫ exp (-E t) dσ(E)` whose spectral measure `σ` has weight at arbitrarily small
energies: `σ (Iio ε) > 0` for every `ε > 0` (the packet contains momenta `|p| < ε`, and a massless
particle has `E = |p|`). This file proves that such a two-point function cannot arise as the limit of
a family of lattice theories with a gap in *physical* units along the continuum tuning, and that it
decays more slowly than any exponential.

Setting (as in 4Y-M `SpectralNoGo.lean`): at spacing `a` the lattice two-point function is
`S_a(t) = ∫ exp (-(E t / a)) dρ_a(E)` with `ρ_a` the finite spectral measure of `-log T_a` in lattice
units. A physical gap `m` along the tuning means `ρ_a (Iio (m a)) = 0`.

* `physicalGap_ratio_le`: `S_a(t₂) ≤ exp (-m (t₂ - t₁)) S_a(t₁)`, uniformly in `a`;
* `limit_ratio_of_physicalGap`: any limit of renormalised `Z_a S_a` keeps that bound;
* `massless_not_expDecay`: if `σ (Iio ε) > 0` for every `ε > 0`, then `∫ exp (-E t) dσ` is not
  `O(exp (-Δ t))` for any `Δ > 0`;
* `no_massless_limit_of_physicalGap`: **a lattice family with a physical gap has no continuum limit
  with a massless mode.**

Together with the strong-coupling gap theorems of 4Y-M, applied to lattice gravity in first-order
form (gauge groups `SO(4)`, `SO(5)`; see `GravityGroups.lean`), this proves that those phases are not
gravitational *as long as the gap persists in physical units along the tuning*. The 4Y-M no-go covers
the other case, a gap uniform in lattice units, where every renormalised two-point function vanishes.

Not claimed: nothing here identifies a gravitational phase. The statements only exclude phases.
-/

open MeasureTheory Filter Topology Real Set

namespace QuantumGravity

/-- Lattice two-point function at spacing `a`, from a spectral measure in lattice units. -/
noncomputable def twoPointLat (ρ : Measure ℝ) (a t : ℝ) : ℝ := ∫ E, Real.exp (-(E * t / a)) ∂ρ

/-- Continuum two-point function from a spectral measure in physical units. -/
noncomputable def twoPoint (σ : Measure ℝ) (t : ℝ) : ℝ := ∫ E, Real.exp (-(E * t)) ∂σ

lemma ae_ge_of_Iio_null {ρ : Measure ℝ} {δ : ℝ} (h : ρ (Iio δ) = 0) : ∀ᵐ E ∂ρ, δ ≤ E := by
  rw [ae_iff]
  have : {E : ℝ | ¬δ ≤ E} = Iio δ := by ext E; simp
  rw [this]; exact h

lemma integrable_expDecay {ρ : Measure ℝ} [IsFiniteMeasure ρ] {δ c : ℝ} (hδ : 0 ≤ δ) (hc : 0 ≤ c)
    (h : ρ (Iio δ) = 0) : Integrable (fun E => Real.exp (-(E * c))) ρ := by
  refine Integrable.of_bound (C := 1) ?_ ?_
  · exact (Real.continuous_exp.comp (continuous_id.mul continuous_const).neg).aestronglyMeasurable
  · filter_upwards [ae_ge_of_Iio_null h] with E hE
    rw [Real.norm_eq_abs, abs_of_pos (Real.exp_pos _)]
    apply Real.exp_le_one_iff.mpr
    have : 0 ≤ E * c := mul_nonneg (hδ.trans hE) hc
    linarith

lemma twoPointLat_nonneg (ρ : Measure ℝ) (a t : ℝ) : 0 ≤ twoPointLat ρ a t :=
  integral_nonneg fun _ => (Real.exp_pos _).le

/-- **The physical-gap ratio bound**, uniform in the spacing. -/
theorem physicalGap_ratio_le {ρ : Measure ℝ} [IsFiniteMeasure ρ] {m a t₁ t₂ : ℝ}
    (hm : 0 ≤ m) (ha : 0 < a) (ht₁ : 0 ≤ t₁) (ht : t₁ ≤ t₂) (h : ρ (Iio (m * a)) = 0) :
    twoPointLat ρ a t₂ ≤ Real.exp (-(m * (t₂ - t₁))) * twoPointLat ρ a t₁ := by
  have hma : 0 ≤ m * a := mul_nonneg hm ha.le
  have int : ∀ s, 0 ≤ s → Integrable (fun E => Real.exp (-(E * s / a))) ρ := by
    intro s hs
    have := integrable_expDecay (ρ := ρ) hma (div_nonneg hs ha.le) h
    refine this.congr (Eventually.of_forall fun E => ?_)
    simp only [mul_div_assoc]
  unfold twoPointLat
  rw [← integral_const_mul]
  apply integral_mono_ae (int t₂ (ht₁.trans ht)) ((int t₁ ht₁).const_mul _)
  filter_upwards [ae_ge_of_Iio_null h] with E hE
  rw [← Real.exp_add]
  apply Real.exp_le_exp.mpr
  have hdt : 0 ≤ t₂ - t₁ := sub_nonneg.mpr ht
  have key : m * a * (t₂ - t₁) ≤ E * (t₂ - t₁) := mul_le_mul_of_nonneg_right hE hdt
  have key' : m * (t₂ - t₁) ≤ E * (t₂ - t₁) / a := by
    rw [le_div_iff₀ ha]; nlinarith
  have e1 : E * t₂ / a = E * (t₂ - t₁) / a + E * t₁ / a := by ring
  rw [e1]; linarith

/-- **The bound passes to every limit**, whatever the renormalisation. -/
theorem limit_ratio_of_physicalGap {ι : Type*} {l : Filter ι} [l.NeBot] {a : ι → ℝ}
    (ha : ∀ i, 0 < a i) {ρ : ι → Measure ℝ} [∀ i, IsFiniteMeasure (ρ i)] {m : ℝ} (hm : 0 ≤ m)
    (hsupp : ∀ i, ρ i (Iio (m * a i)) = 0) {Z : ι → ℝ} (hZ : ∀ i, 0 < Z i)
    {t₁ t₂ : ℝ} (ht₁ : 0 ≤ t₁) (ht : t₁ ≤ t₂) {L₁ L₂ : ℝ}
    (h₁ : Tendsto (fun i => Z i * twoPointLat (ρ i) (a i) t₁) l (𝓝 L₁))
    (h₂ : Tendsto (fun i => Z i * twoPointLat (ρ i) (a i) t₂) l (𝓝 L₂)) :
    L₂ ≤ Real.exp (-(m * (t₂ - t₁))) * L₁ := by
  refine le_of_tendsto_of_tendsto' h₂ (h₁.const_mul _) fun i => ?_
  have := physicalGap_ratio_le (ρ := ρ i) hm (ha i) ht₁ ht (hsupp i)
  calc Z i * twoPointLat (ρ i) (a i) t₂
      ≤ Z i * (Real.exp (-(m * (t₂ - t₁))) * twoPointLat (ρ i) (a i) t₁) :=
        mul_le_mul_of_nonneg_left this (hZ i).le
    _ = _ := by ring

/-- A massless mode: spectral weight at arbitrarily small energy. -/
def HasMasslessMode (σ : Measure ℝ) : Prop := ∀ ε > 0, 0 < σ (Iio ε)

/-- Lower bound by the low-energy weight: `∫ exp (-E t) dσ ≥ σ(Iio ε) · exp (-ε t)`. -/
lemma twoPoint_ge_lowWeight {σ : Measure ℝ} [IsFiniteMeasure σ] (h0 : σ (Iio 0) = 0)
    {ε t : ℝ} (ht : 0 ≤ t) :
    (σ (Iio ε)).toReal * Real.exp (-(ε * t)) ≤ twoPoint σ t := by
  have hint : Integrable (fun E => Real.exp (-(E * t))) σ :=
    integrable_expDecay (le_refl 0) ht h0
  have hind : Integrable ((Iio ε).indicator (fun _ => Real.exp (-(ε * t)))) σ :=
    (integrable_const _).indicator measurableSet_Iio
  have hle : (fun E => (Iio ε).indicator (fun _ => Real.exp (-(ε * t))) E)
      ≤ᵐ[σ] fun E => Real.exp (-(E * t)) := by
    filter_upwards [ae_ge_of_Iio_null h0] with E hE
    by_cases hEε : E < ε
    · rw [indicator_of_mem (show E ∈ Iio ε from hEε)]
      apply Real.exp_le_exp.mpr
      have : E * t ≤ ε * t := mul_le_mul_of_nonneg_right hEε.le ht
      linarith
    · rw [indicator_of_notMem (show E ∉ Iio ε from hEε)]
      exact (Real.exp_pos _).le
  have := integral_mono_ae hind hint hle
  rw [integral_indicator_const _ measurableSet_Iio] at this
  simpa [twoPoint, Measure.real, smul_eq_mul] using this

/-- **A massless mode is not exponentially decaying.** -/
theorem massless_not_expDecay {σ : Measure ℝ} [IsFiniteMeasure σ] (h0 : σ (Iio 0) = 0)
    (hml : HasMasslessMode σ) {Δ : ℝ} (hΔ : 0 < Δ) :
    ¬ ∃ C, ∀ t ≥ 1, twoPoint σ t ≤ C * Real.exp (-(Δ * t)) := by
  rintro ⟨C, hC⟩
  set ε := Δ / 2 with hε
  have hεpos : 0 < ε := by positivity
  set c := (σ (Iio ε)).toReal with hc
  have hcpos : 0 < c := ENNReal.toReal_pos (hml ε hεpos).ne' (measure_ne_top _ _)
  -- c ≤ C exp (-(ε t)) for all t ≥ 1
  have hbound : ∀ t ≥ (1 : ℝ), c ≤ C * Real.exp (-(ε * t)) := by
    intro t ht
    have h1 := twoPoint_ge_lowWeight (σ := σ) (ε := ε) h0 (by linarith : (0 : ℝ) ≤ t)
    have h2 := hC t ht
    have e : Real.exp (-(Δ * t)) = Real.exp (-(ε * t)) * Real.exp (-(ε * t)) := by
      rw [← Real.exp_add]; congr 1; rw [hε]; ring
    have hpos := Real.exp_pos (-(ε * t))
    have : c * Real.exp (-(ε * t)) ≤ C * Real.exp (-(ε * t)) * Real.exp (-(ε * t)) := by
      calc c * Real.exp (-(ε * t)) ≤ twoPoint σ t := h1
        _ ≤ C * Real.exp (-(Δ * t)) := h2
        _ = C * Real.exp (-(ε * t)) * Real.exp (-(ε * t)) := by rw [e]; ring
    exact le_of_mul_le_mul_right this hpos
  -- but C exp (-(ε t)) → 0
  have hlim : Tendsto (fun t : ℝ => C * Real.exp (-(ε * t))) atTop (𝓝 0) := by
    have h1 : Tendsto (fun t : ℝ => ε * t) atTop atTop := tendsto_id.const_mul_atTop hεpos
    have h2 := Real.tendsto_exp_neg_atTop_nhds_zero.comp h1
    simpa using h2.const_mul C
  have hev : ∀ᶠ t in atTop, C * Real.exp (-(ε * t)) < c := (hlim.eventually (gt_mem_nhds hcpos))
  obtain ⟨t, ht⟩ := (hev.and (eventually_ge_atTop (1 : ℝ))).exists
  exact absurd (hbound t ht.2) (not_le.mpr ht.1)

/-- **No graviton from a physical gap.** If a family of lattice theories has a gap `m > 0` in
physical units along the tuning, and its renormalised two-point functions converge at every `t > 0`
to the two-point function of a continuum spectral measure `σ` supported on `[0, ∞)`, then `σ` has
no massless mode. -/
theorem no_massless_limit_of_physicalGap {ι : Type*} {l : Filter ι} [l.NeBot] {a : ι → ℝ}
    (ha : ∀ i, 0 < a i) {ρ : ι → Measure ℝ} [∀ i, IsFiniteMeasure (ρ i)] {m : ℝ} (hm : 0 < m)
    (hsupp : ∀ i, ρ i (Iio (m * a i)) = 0) {Z : ι → ℝ} (hZ : ∀ i, 0 < Z i)
    {σ : Measure ℝ} [IsFiniteMeasure σ] (h0 : σ (Iio 0) = 0)
    (hlim : ∀ t > 0, Tendsto (fun i => Z i * twoPointLat (ρ i) (a i) t) l (𝓝 (twoPoint σ t))) :
    ¬ HasMasslessMode σ := by
  intro hml
  apply massless_not_expDecay h0 hml hm
  refine ⟨Real.exp m * twoPoint σ 1, fun t ht => ?_⟩
  have := limit_ratio_of_physicalGap ha hm.le hsupp hZ zero_le_one ht (hlim 1 one_pos)
    (hlim t (by linarith))
  calc twoPoint σ t ≤ Real.exp (-(m * (t - 1))) * twoPoint σ 1 := this
    _ = Real.exp m * twoPoint σ 1 * Real.exp (-(m * t)) := by
      rw [show -(m * (t - 1)) = m + -(m * t) by ring, Real.exp_add]; ring

end QuantumGravity
