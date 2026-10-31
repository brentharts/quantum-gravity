# Where the Yang–Mills work meets gravity

Answers Brent's two questions ("gravity is next" and "have you talked with Lockwood on how this needs to connect to
gravity later?"). It also corrects the paragraph his AI drafted about our work.

## 1. A correction to the drafted paragraph

Brent's draft says:

> Romanov (forest gauge): I say it fixes forest links to the identity, as our spanning-tree gauge does. I also
> summarise its strong-coupling SU(2) results: a unique state, a gap m ≥ −log(7β_W/4) for β_W < 4/7, and a Hessian
> bound of 9.599991. […]

**The numbers are right, but they belong to the three-dimensional paper.** They come from Romanov, *Three-dimensional
lattice Yang–Mills theory in a forest gauge* (github.com/romanov360/yang-mills-3d-forest-gauge, Zenodo
10.5281/zenodo.23783316), Theorems A and B on **ℤ³**. None of 4/7, 7β_W/4 or 9.599991 appears in the four-dimensional
paper that went into creelie/4Y-M v4.29.0. This was checked by searching the text of `YangMillsForestGauge.pdf`
(dated 30 October 2026) and the repository sources. Because Brent's opening line is about Yang–Mills *in 4d*, a reader
would assume these are 4D constants.

A second, smaller point: a forest of straight lines with one fixed link in every plaquette is **not** a spanning
(maximal) tree. The 4D paper explains the difference in footnote 5. In a maximal tree the number of free partners per
link is not uniform, and the temporal gauge leaves 14 partners per link. The straight-line forest leaves 12 in d = 4
and 7 in d = 3. If Brent's paper uses a spanning tree, "as our spanning-tree gauge does" is only approximately true.

A version Brent could use (please check it against his own conventions):

> **Romanov (forest gauge).** Fixes the links of a forest of straight lines to the identity, so that every plaquette
> contains exactly one fixed link. This is a partial gauge fixing, related to but not the same as a spanning-tree gauge.
> On ℤ³ (Romanov 2026) it gives, for SU(2), a unique state and a gap m ≥ −log(7β_W/4) for β_W < 4/7, and for every
> compact group a gauge-fixed Hessian bound h = 9.599991. On ℤ⁴ (Bhattacharjee, Bhattacharya, Lockwood, Romanov 2026,
> creelie/4Y-M v4.29.0) it gives, for SU(2), m ≥ −log(3β_W) for β_W < 1/3, extended by plaquette blocks to
> β_W ≤ 0.345. For SU(3) the range reaches β_W ≤ 0.76. For every compact simple group it gives a Hessian bound 29/2
> (14.420001 by a computer-assisted certificate). It also reduces a continuum mass gap to one cube estimate, which is
> unproved. All of this is Euclidean, at fixed lattice spacing, and not yet refereed. No number of ours is compared
> with it, because its couplings and gaps are not the same objects as our Hamiltonian g² and gaps.

The last sentence of Brent's draft (keeping the Hamiltonian g² separate from β_W) is correct and should stay.

## 2. What "connecting to gravity later" has to mean

Brent's claim that "Yang–Mills in 4d completes quantum theory, it's just missing gravity" is the right way to frame the
**standard model side** (gauge fields plus matter). Note, though, that 4Y-M proves lattice statements at strong
coupling, not the continuum theory. Gravity enters at three distinct levels, and each one asks something different of
the Yang–Mills work:

| Level | What gravity needs from YM | What 4Y-M has now | Gap |
|---|---|---|---|
| **A. YM on a fixed curved background** | A lattice measure on a non-flat cell complex (a triangulation or a curved lattice) with the same estimates. | Proofs use only local counts: plaquettes per link, partners per free link, and a forest with one fixed link per plaquette. | A forest-gauge pattern and partner count on *irregular* complexes. This is idea G4. |
| **B. YM as a source (semiclassical gravity)** | A renormalised stress tensor ⟨T_μν⟩, including the trace anomaly ⟨T^μ_μ⟩ = (β(g)/2g)⟨F²⟩, i.e. the YM vacuum energy that feeds Λ. | Flowed observables (Sakai–Sasaki spatial flow) have continuum limits along subsequences. The gradient flow is also how Suzuki builds a lattice T_μν. | Flowed T_μν and its renormalisation. Depends on (E). Idea G5. |
| **C. YM and gravity in one path integral** | A joint measure over geometries and connections, plus running couplings with gravitational corrections. | `RunningCoupling.lean` (one loop) and strong-coupling estimates. | Everything. The cleanest route is first-order lattice gravity, whose variables are themselves gauge fields (G2, G8). |

**Lockwood's block-averaging programme is the piece most likely to carry over.** Gravity on a lattice needs
coarse-graining that commutes with the local symmetry. Bałaban-type averaging that is covariant and composes across
scales (Theorems "cutoff", "torusscales", "smallscales", and the no-go "nomean") is exactly the missing ingredient in
CDT/EDT and spin-foam renormalisation. Those programmes coarse-grain numerically, or with tensor-network methods,
without covariance control. Proposition "nomean" already says that **no continuous covariant block map treats the
transverse positions alike, for any compact connected group**. Applied to the Euclidean Lorentz group SO(4) or Spin(4),
it is a theorem about the coarse-graining of lattice gravity in first-order form. Spin-foam renormalisation
(Bahr–Steinhaus, Dittrich) would benefit from hearing it.

## 3. What transfers directly, and what reverses

**Transfers.** Every theorem of 4Y-M stated "for every compact (simple) group" applies to the Euclidean gauge groups of
first-order gravity: Spin(4) = SU(2)×SU(2) (Palatini or Plebanski, with self-dual SU(2) Ashtekar variables) and SO(5)
or Sp(2) (MacDowell–Mansouri, Euclidean de Sitter). The ranges, computed exactly by
`scripts/gravity_group_checks.py` with the 4Y-M formula β_W < 2N·Ric/29:

| group (rep) | role in gravity | Ric | range |
|---|---|---|---|
| SU(2) (fundamental) | self-dual half of Spin(4) | 1 | β_W < 4/29 ≈ 0.138 |
| SO(4) (vector) | Euclidean Lorentz group on the tetrad index | 1/2 | β_W < 4/29, i.e. \|β\| < 1/29 |
| SO(5) (vector) | Euclidean de Sitter group (MacDowell–Mansouri) | 3/4 | β_W < 15/58 ≈ 0.259 |
| Sp(2) = Spin(5) (spinor) | the same group in its 4-dim rep | 3/2 | β_W < 12/29 ≈ 0.414 |

The SU(2) row reproduces the 4Y-M value 4/29 as a sanity check.

**Reverses.** In Yang–Mills, a gap is the goal. In gravity, a gap is a **diagnosis**: a phase with a transfer-matrix
gap has no massless graviton. 4Y-M's spectral no-go (`SpectralNoGo.lean`: a gap uniform in lattice units forces every
renormalised two-point function to vanish) and the gap theorems together become a rigorous way to **rule out**
strong-coupling phases of lattice gravity. This matches what simulations see: the vierbein vanishes at strong coupling
(Catterall–Ferrante), and CDT phases A and B are not 4D. Nobody has proved any of this, and our tools can.

## 4. Where QGL (Brent's Quantum_Gravity_Lab) fits

QGL is a semiclassical sandbox: a GR-like orbit, a Jaynes–Cummings sensor in proper time, a phenomenological complexity
scalar, Kasner/BKL/FLRW modules, and a Chair44 tiling sensor. Its README already says it is not a theory of quantum
gravity. It lines up with the frontier in three places:

1. **QGL is a classical-quantum hybrid without backreaction.** Oppenheim's theorem says that a hybrid *with*
   backreaction must obey the decoherence–diffusion trade-off. Adding backreaction (the sensor's energy shifting the
   orbit) therefore forces diffusion of the orbit. That makes a sharp, testable addition, and the bound applies as soon
   as backreaction is on. Idea G11.
2. **`qgl_bkl.py` is a cosmological billiard.** Its u-map is the Gauss map of continued fractions, i.e. a billiard in
   the Weyl chamber of the hyperbolic Kac–Moody algebra AE₃. That links QGL to the E₈ material in `rosettaphys` through
   E₁₀ ⊃ E₈. Idea G7.
3. **`qgl_tiling.py` (Chair44)** gives an aperiodic background on which lattice YM could be put (idea G4). Quasicrystal
   spin foams (arXiv:2306.01964) are prior art.
