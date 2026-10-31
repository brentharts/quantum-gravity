# G5. The stress tensor of continuum Yang–Mills: the interface to gravity

Gravity couples to matter through T_μν. "Connecting Yang–Mills to gravity later" (Brent's question) therefore means
one thing first: **the continuum Yang–Mills theory has to come with a renormalised energy–momentum tensor.**

## What 4Y-M already has

- Flowed observables under the Sakai–Sasaki *spatial* gradient flow. This flow is reflection positive and leaves the
  transfer matrix unchanged up to unitary equivalence.
- After renormalisation by one condition at a single physical separation, these observables have continuum limits
  along subsequences for every tuning (Theorem "renormalised flowed observables").
- A nontrivial limit exists if and only if the ratio C(σ)/C(0) does not tend to zero.

## What gravity needs

Suzuki (2013) defines the lattice energy–momentum tensor through the (full, 4D) Yang–Mills gradient flow:

  T_μν(x) = lim_{t→0} { c₁(t) [G_μρ G_νρ − ¼ δ_μν G_ρσ G_ρσ](t, x) + c₂(t) δ_μν [G_ρσ G_ρσ − ⟨G²⟩](t, x) },

with c₁, c₂ computable from the small-t expansion (asymptotic freedom makes them perturbative as t → 0).

## Programme (each step a theorem to prove)

1. **Flowed T_μν at fixed flow time.** Show that T_μν(t) at fixed physical t is in the class covered by "renormalised
   flowed observables": reflection positivity, tightness, and continuum limits along subsequences. *Obstacle:* the
   4Y-M flow is spatial, while Suzuki's is four-dimensional. The 4D flow is not reflection positive in the time
   direction, so either the spatial flow must be used (losing T_0i and T_00 manifest covariance) or positivity must
   be recovered at fixed t.
2. **Small-t expansion with error bounds.** Conditional on (E), show that T_μν(t) − T_μν(0) = O(t·log t) inside
   correlation functions at separated points. This is where asymptotic freedom (Bałaban's ultraviolet stability)
   enters.
3. **Trace anomaly.** ⟨T^μ_μ⟩ = (β(g)/2g)⟨F²⟩_ren. With a gap m (4Y-M's (D) along the tuning), the vacuum energy
   density is of order m⁴. This is the Yang–Mills contribution to the cosmological constant, ≈ Λ_QCD⁴ for QCD, stated
   as a theorem conditional on (D) and (E).
4. **Semiclassical Einstein equation.** G_μν + Λg_μν = 8πG⟨T_μν⟩_ren becomes a well-posed equation for a background
   metric once steps 1–3 hold. Its Euclidean form on a fixed curved background needs YM on curved lattices; G4 does
   the strong-coupling part.

## Not claimed

Every step is open. This document records what "connecting to gravity" has to mean in the 4Y-M framework, and which
existing theorems it builds on.
