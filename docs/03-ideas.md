# Ideas for progress on quantum gravity

Written in the house style of 4Y-M: finite statements, explicit constants, Lean where the arithmetic is finite, a
"what is not claimed" line for every idea, and refusals as useful as connections. The ideas are ordered by
**cost × likelihood of a clean result**. The survey behind them is [01-frontier-survey.md](01-frontier-survey.md), and
the bridge to our work is [02-where-our-work-meets-gravity.md](02-where-our-work-meets-gravity.md).

**Guiding observation.** In gravity a mass gap is not the goal but a diagnosis. The graviton is massless, so any
lattice phase with a transfer-matrix gap is **not** the gravitational phase. The strong-coupling machinery of 4Y-M
produces gaps at explicit couplings. Pointed at lattice formulations of gravity, it therefore produces **rigorous
exclusions of non-gravitational phases**. Numerics have seen these phases for 30 years, but nobody has proved anything
about them.

---

## Tier 1: quick wins (days, mostly Lean / exact arithmetic)

### G1. "A gapped lattice phase has no graviton" (Lean)
- **Statement.** If the Källén–Lehmann measure of a reflection-positive two-point function has support in [m, ∞) with
  m > 0 in physical units, then the limit has no massless pole, and in particular no spin-2 massless state in that
  channel. If the gap is uniform in lattice units, every renormalised two-point function vanishes (the 4Y-M no-go).
- **Why.** It turns every strong-coupling gap theorem into a phase-exclusion theorem for lattice gravity.
- **How.** `YangMills/SpectralNoGo.lean` already has `kallenLehmann_pos` and `nogo_no_gapped_limit`. A corollary file
  `Gravity/NoGraviton.lean` is mostly a restatement with a "massless pole" predicate (ρ has an atom at 0, or mass
  near 0).
- **Not claimed.** This identifies no gravitational phase. It only excludes phases.

### G6. Gravity cannot spoil asymptotic freedom, in `RunningCoupling.lean`
- **Statement.** With β(g) = −b₀g³ + f_g·g and f_g ≥ 0 (antiscreening, the sign found in every symmetry-preserving
  computation; Folkerts–Litim–Pawlowski), the coupling still enters every window at a spacing-independent scale
  (`window_entered`). A Lean counterexample shows the statement fails for f_g < 0 with |f_g| large.
- **Why.** This is the first formal statement about YM *plus* gravity in our library, and it answers "how does this
  connect to gravity later" at the level of the running coupling.
- **Not claimed.** The sign of f_g is scheme-dependent. The theorem is conditional on it.

### G7. Cosmological billiards: AE₃ and E₁₀ in Lean, and a QGL test
- **Done here.** `scripts/gravity_group_checks.py` verifies exactly that AE₃ has det −2 and E₁₀ has det −1, both with
  Lorentzian inertia (one negative direction).
- **Next.** (a) Do the same with `decide` / `norm_num` in Lean. (b) In QGL, add a test that the Kasner u-map of
  `qgl_bkl.py` matches the reflection sequence in the Weyl group of AE₃ (PGL(2,ℤ) acting on the upper half plane),
  epoch by epoch. (c) Add E₁₀ ⊃ E₈ to the `rosettaphys` knowledge graph as an arrow, not an equals sign.
- **Not claimed.** The billiard is a near-singularity limit of classical gravity. It is a hint about quantum gravity
  (Damour–Nicolai), not a theory.

---

## Tier 2: papers (weeks to months; our tools apply literally)

### G2. Strong-coupling theorem for first-order lattice gravity: the "pregeometric phase"
- **Setting.** Euclidean MacDowell–Mansouri / Stelle–West lattice gravity. An SO(5) link field U plus a unit SO(5)
  vector V_x (the compensator that breaks SO(5) → SO(4)). The tetrad is the covariant difference e ~ U V − V.
  Action: Wilson-type plaquette terms in the SO(4) projection of the curvature (β), plus a hopping term κ Σ V_x·U V_y.
- **Theorem target.** For |β| and |κ| below explicit constants: a unique infinite-volume state, exponential clustering,
  a transfer-matrix gap, and **⟨e⟩ = 0** (no geometry). Combined with G1, this phase has no graviton.
- **Our inputs.** The forest gauge applies to SO(5) (Ric = 3/4, so β_W < 15/58 for the pure-gauge part; see
  `scripts/gravity_group_checks.py`). The V-field is a gauge–Higgs system, as in Osterwalder–Seiler. Elitzur's theorem
  already gives ⟨V⟩ = 0 without gauge fixing. The content is the *gap* and *uniqueness*, at explicit couplings, for the
  geometric observables.
- **Why it matters.** It is the first theorem about a phase of lattice quantum gravity in four dimensions. It explains
  the vanishing vierbein that Catterall–Ferrante saw in Monte Carlo, and it gives the CDT/EDT communities a rigorous
  anchor for "phase A is not gravity".
- **Not claimed.** Nothing about the geometric phase, the Lorentzian theory or the continuum. The MacDowell–Mansouri
  plaquette action is not the Wilson action, so the Hessian count (29/2) has to be redone for it. That is a finite
  computation in the style of `GaugeFix.lean`.

### G8. Ghost confinement in quadratic gravity: a Yang–Mills-shaped question
- **Context.** Quantum quadratic gravity (Stelle; Salvio–Strumia; Holdom–Ren; Liu–Quintin–Afshordi PRL 2026) is
  asymptotically free and becomes strongly coupled in the IR. The proposal is that this strong coupling **confines the
  massive spin-2 ghost**, just as QCD confines gluons. On the lattice, a Wilson plaquette action for the Lorentz
  connection generates exactly the R_μνR^μν term (Mannion–Taylor; Zubkov). The frozen-vierbein limit is a pure
  SO(4)/Spin(4) lattice gauge theory.
- **Observation.** 4Y-M already proves a unique state and a gap for SO(4) at |β| < 1/29 (β_W < 4/29). The compact
  Euclidean Wilson action is reflection positive, so its transfer matrix is a positive operator on a Hilbert space with
  **no negative-norm states at all**, and at strong coupling the whole spectrum above the vacuum is gapped. In this
  lattice model the curvature-squared sector therefore has no ghost and no massless mode. That is the
  lattice-at-fixed-spacing analogue of the Holdom–Ren claim. The open question moves to whether the continuum limit of
  this model *is* quadratic gravity. The confinement criterion
  (area law for Lorentz Wilson loops) at strong coupling follows from standard character expansions.
- **Deliverable.** A short paper: *Confinement of the curvature-squared sector of lattice Lorentz gauge theory at
  strong coupling*. Theorems: gap and clustering (from 4Y-M), area law (character expansion, explicit constants),
  and the G1 corollary. Lean: counts and thresholds.
- **Not claimed.** Nothing about the continuum, about whether Afshordi's inflationary scenario sits in this phase, or
  about Lorentzian unitarity.

### G4. Yang–Mills on any geometry, uniformly, and induced gravity à la Sakharov
- **Statement 1 (geometry-uniform gap).** Take any 2-complex in which every link lies in at most k plaquettes. Suppose
  it has a "forest" with one fixed link per plaquette, or a quantified failure of this. Then lattice YM on it has a
  unique state and decay for β below a constant depending only on k and the per-link partner count. This is the 4Y-M
  argument with the lattice ℤ⁴ replaced by its two local counts. The deliverable is the combinatorial lemma: which
  complexes admit such forests, and the partner count for (i) CDT triangulations with a vertex-degree cap, (ii) the
  Chair44 cube complex (`qgl_tiling.py`), and (iii) the 600-cell / regular 4-polytope lattices.
- **Statement 2 (induced gravity, rigorous at strong coupling).** For such complexes T, the cluster expansion gives
  log Z_YM[T] = Σ_{local patterns P} n_P(T)·a_P(β) with absolutely summable a_P. In the annealed measure
  exp(−S_grav[T])·Z_YM[T], YM matter only **shifts the local couplings** (κ₀, κ₄, Δ of CDT/EDT) by explicit convergent
  series, and generates no non-local interaction. This is Sakharov's induced gravity at strong coupling, with error
  bounds. The October 2026 induced-Regge paper *assumes* the fluctuation covariance. This statement derives it, at
  strong coupling.
- **Not claimed.** Strong coupling only. In the scaling region of the gravity model the gauge field is weakly coupled,
  and the statement says nothing there.

### G10. Yang–Mills on a Liouville quantum gravity surface, exactly (2D)
- **Why.** 2D quantum gravity (LQG / Brownian map) is constructed, and 2D YM is constructed. Their coupling is the one
  place where "YM + quantum gravity" can be an actual theorem today.
- **Statement.** YM₂ depends on the surface only through its area: Z(Σ, A) = Σ_λ (dim λ)^{2−2g} e^{−g²A C₂(λ)/2}
  (Migdal; rigorous by Sengupta and Lévy). Averaging over the area law of the γ-LQG sphere or disk (explicit:
  Ang–Remy–Sun integrability) gives E[Z] in closed form. Wilson-loop expectations for a loop bounding a region of LQG
  area A₁ use the joint area laws. Expected output: KPZ-type dressing of the Casimir energies, and a "string tension
  on random surfaces" formula.
- **Not claimed.** YM₂ has no propagating gluons. This tests the coupling machinery, not 4D physics.

---

## Tier 3: programmes (long; this is where the Clay-sized questions sit)

### G5. The stress tensor of continuum Yang–Mills: the actual interface to gravity
- Extend 4Y-M's "renormalised flowed observables" theorem to Suzuki's flowed energy–momentum tensor T_μν(t). Steps:
  (i) reflection positivity and tightness for T_μν(t) at fixed flow time; (ii) the small-t expansion with
  renormalisation by one condition, as in the ratio condition; (iii) the trace anomaly as a theorem conditional on (E).
- Payoff: the semiclassical Einstein equation G_μν = 8πG⟨T_μν⟩_ren becomes a well-posed target conditional only on
  4Y-M's (D) and (E). If the gap m exists, the YM vacuum energy is of order m⁴. That gives a clean statement of the
  YM contribution to the cosmological-constant problem.
- **This is the answer to "how this needs to connect to gravity later":** gravity couples to T_μν, so the continuum
  YM theory has to deliver T_μν, and the gradient flow 4Y-M already uses is the standard way to build it.

### G3. CDT through the transfer matrix
- 1+1 CDT is exactly solvable: its proper-time Hamiltonian has an explicit spectrum. Use it as a calibration case for
  transfer-matrix gap tools in a model where the answer is known. Then prove uniqueness and a gap for the
  spatial-volume process of 2+1 and 3+1 CDT in the region of large bare cosmological constant (the analogue of
  strong coupling). This is a rigorous phase-A/B exclusion and pairs with G1.
- Open in the field: reflection positivity of the CDT transfer matrix in 3+1, and the order of the A–C and C–B
  transitions.

### G9. Three dimensions: from our ℤ³ theorems to 3D gravity
- Euclidean 3D gravity with Λ > 0 is SU(2)×SU(2) Chern–Simons theory, i.e. Turaev–Viro. Ponzano–Regge is SU(2)
  lattice BF, whose Boltzmann weight is the β → ∞ (flat) limit of a heat-kernel action. Romanov's ℤ³ forest-gauge
  paper covers the β → 0 end. Proposal: a one-parameter family interpolating the gapped YM end and the topological
  gravity end, with the interpolating transfer matrix studied rigorously at both ends.
- Finite, Lean-friendly piece: exact 6j-symbol identities (orthogonality, Biedenharn–Elliott) and Turaev–Viro
  invariants of small manifolds at small level, by exact cyclotomic arithmetic. Also 3D YM coupled to 3D gravity,
  matching the 2026 *What's the matter with 3D gravity?* programme from the lattice side.

### G0. Framing: "four open problems of lattice quantum gravity"
- Mirror 4Y-M `strong-coupling/OPEN.md`: (1) intermediate couplings: which phases are gapped, with proofs;
  (2) the crossover to the geometric phase; (3) a continuum limit with reflection positivity and a diffeomorphism-
  invariant replacement for the Osterwalder–Schrader axioms (the CLPW type-II observer algebra is the best candidate
  for "what the observables are"); (4) the graviton, i.e. a **massless** spin-2 pole in physical units, the mirror
  image of Yang–Mills problem 4.
- A short note stating these, with G1/G2/G8 as the first rows proved, would give Brent's paper a precise target.

---

## For QGL (Brent's lab)

### G11. Make the hybrid honest: Oppenheim's trade-off as a test
- QGL couples a classical orbit to a quantum sensor without backreaction. With backreaction switched on (sensor energy
  shifting the orbit), any consistent classical-quantum dynamics needs orbit diffusion bounded below by the
  decoherence–diffusion trade-off, D₂ ⪰ D₁ D₀⁻¹ D₁† in the notation of Oppenheim et al. (Nat. Commun. 2023; check the
  conventions there before coding). Add a `qgl_cq.py` that implements the minimal consistent master equation, plus a test that
  QGL's decoherence rate and the induced orbit diffusion satisfy the bound. Report the strain spectrum in the
  Hirotani–Matsumura form so that it can be compared with LISA Pathfinder and LIGO sensitivities.
- Retire or derive the complexity scalar C_Q(r). Either fix it from a stated principle or keep it explicitly
  phenomenological, with calibration ranges reported (it already is, in the README). G11 gives one principled
  replacement: decoherence fixed by the trade-off.

### G12. Small tests that would make QGL cite-able
- Exact Kasner and Kretschmann checks against the Einstein Toolkit `Exact` thorn (already in its reading list).
- `qgl_bkl.py` epoch statistics against the Gauss–Kuzmin distribution: the u-map is the continued-fraction map, so the
  era-length statistics are known exactly.

---

## Suggested first move

**G1 + G8 + G6 as one short paper with a Lean appendix.** The theorems already hold. What remains is the
interpretation, a character-expansion area law with explicit constants, and two small Lean files. That is the fastest
way for the group to say something correct and new about quantum gravity. G2 and G4 are the natural second paper, and
they need Lockwood's block-averaging expertise. G5 is the long-term bridge from 4Y-M to gravity.
