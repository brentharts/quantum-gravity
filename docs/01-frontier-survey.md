# The quantum gravity frontier, October 2026

A survey written so that the lattice Yang–Mills work (creelie/4Y-M v4.29.0; romanov360/yang-mills-3d-forest-gauge)
can be pointed at gravity. Searches were run on 2026-10-31. Every item says how it is backed:

- **✓ seen**: the abstract, publisher record or arXiv listing was seen in a search on 2026-10-31.
- **secondary**: seen only through a news piece, an aggregator or talk slides. Check the primary source before citing.
- **background**: standard material from before 2025, from memory. It is well established but was not re-checked today.

Full citations are in [references.md](references.md).

---

## 0. The one-paragraph picture

No approach has a nonperturbative quantum theory of four-dimensional gravity that has been **constructed** in the sense
that 2D Yang–Mills, φ⁴₂,₃ or Liouville quantum gravity have been. As a result, the field has no analogue of the Clay
problem: it has not agreed on what "solving" quantum gravity would mean. The strongest results are of four kinds.
(i) **Exactly solvable lower-dimensional models**: 2D Liouville quantum gravity (rigorous), 3D gravity through
Virasoro TQFT, and JT gravity.
(ii) **Algebraic structure**: type II von Neumann algebras of observables once an observer or clock is included.
(iii) **Numerical evidence from lattice methods** (CDT, EDT) and from the functional RG (asymptotic safety).
Both give a de Sitter-like large-scale geometry and dimensional reduction near 2 at short scales.
(iv) A **growing experimental programme** that tests whether gravity can carry quantum information. It uses
gravity-mediated entanglement (BMV), decoherence–diffusion bounds on classical gravity, interferometer noise searches,
and single-graviton sensing.
None of these experiments has yet seen a quantum-gravitational signal.

---

## 1. Nonperturbative lattice and path-integral approaches

These are the closest in spirit to our lattice Yang–Mills work.

### Causal Dynamical Triangulations (CDT)
- Review: Ambjørn & Loll, *CDT: gateway to nonperturbative quantum gravity*, arXiv:2401.09399 (2024). **✓ seen.**
  The main results are a de Sitter-like quantum universe emerging from the path integral and an anomalous spectral
  dimension at short distances.
- Spectral dimension falls from about 4 to about 3/2 (Coumbe–Jurkiewicz, arXiv:1411.7712) or about 2 (earlier work).
  The reduction starts near 40 Planck lengths (Bishop, arXiv:1812.09331). **✓ seen.**
- Quantum Ricci curvature (Klitgaard–Loll), an Ollivier-type coarse curvature, gives the first curvature observable
  on triangulations. At large scales it is compatible with S⁴ (arXiv:2006.06263; review arXiv:2306.13782). **✓ seen.**
- **Relevant structure for us:** CDT has a proper-time foliation, a transfer matrix, and (in 2D, and partially in
  higher dimensions) reflection positivity. That is the same Osterwalder–Schrader machinery the 4Y-M papers use.
  Its phase diagram has phases with no 4D geometry (branched polymer, crumpled, bifurcation) and a de Sitter phase "C".
  The de Sitter phase is separated from the others by second-order transitions, whose existence is numerical.
  **background.**
- No 2025–26 CDT paper turned up in the searches. That probably reflects search coverage rather than inactivity.

### Euclidean Dynamical Triangulations (EDT) with a measure term
- Dai, Freeman, Laiho, Schiffer, Unmuth-Yockey, Phys. Rev. D 111 (2025), arXiv:2408.08963 (Euclidean correlation
  functions). **secondary** (talk slides). Asaduzzaman–Catterall revisit EDT and find broad agreement with
  earlier models, which hints at universality. **✓ seen.**
- Open question in the field: whether the fine-tuned measure term reaches a continuum limit with a second-order
  transition. EDT without it has a first-order transition. **background.**

### Regge calculus and quantum Regge calculus
- Fixed triangulation, variable edge lengths (Hamber's programme; Dittrich and Bonzom on discretisation-independent
  actions). **background.** An October 2026 MDPI paper on induced Regge gravity is Euclidean and one-loop, and it
  assumes rather than derives the fluctuation covariance. **✓ seen.**
- The **conformal-factor problem**: the Euclidean Einstein–Hilbert/Regge action is unbounded below. This is the
  gravitational counterpart of "no uniform curvature bound", and it is why Bakry–Émery-type arguments cannot be applied
  to the raw gravity measure. **background.**

### Lattice gravity as a gauge theory of the Lorentz / de Sitter group
- Palatini or MacDowell–Mansouri gravity as a lattice gauge theory: Catterall & Ferrante, arXiv:0912.5525. Monte Carlo
  gives a vanishing vierbein in the ground state, so at that coupling there is no geometry. Lorentz-group lattice gauge
  theory: Zubkov, arXiv:1308.3406. Gravitational Wilson loops: arXiv:0907.2652. **✓ seen**, but nothing from 2024–26
  turned up.
- This is the approach where **our theorems apply literally**: Euclidean Spin(4) = SU(2)×SU(2) and the Euclidean de
  Sitter group SO(5) are compact simple (or semisimple) groups. See [03-ideas.md](03-ideas.md), idea G2.

### Spin foams / loop quantum gravity
- EPRL/FK is the standard model. Its large-spin effective action is the area-Regge action (Miković–Vojinović; Bahr,
  Dittrich, Steinhaus and collaborators on "effective spin foams" and renormalisation of the 4D EPRL model).
  **✓ seen / background.** Spin foams are lattice BF theory with simplicity constraints. Ooguri / Ponzano–Regge
  models are SU(2) lattice gauge theory with a delta-function (flatness) Boltzmann weight.
- Quasicrystalline spin foams with matter: arXiv:2306.01964. **✓ seen.** This is relevant to the aperiodic-tiling side
  of this repository.
- Alexander–Bernardo–Hui, *Cosmological constant from a quantum gravitational θ-vacuum and the gravitational Hall
  effect*, Phys. Rev. Lett. 136, 151501 (17 April 2026), arXiv:2506.14886. **✓ seen.** It argues that the
  Chern–Simons–Kodama state lives in a θ-sector with θ = 12π²/(Λℓ_P²) mod 2π, with Λ playing the role of a Hall
  resistivity. A 2025 paper (arXiv:2511.05417) treats normalisability of the Kodama state. **✓ seen.**

---

## 2. Continuum quantum field theory approaches

### Asymptotic safety (functional RG)
- 2026 review: *Asymptotically safe quantum gravity and its phenomenology*, arXiv:2606.21522. **✓ seen** (listing
  only).
- Lorentzian signature: D'Angelo (arXiv:2310.20603) gives the first background-independent Lorentzian fixed point in
  the Einstein–Hilbert truncation. D'Angelo, Ferrero and Fröb (CQG 2025) study the de Sitter graviton propagator. Assant,
  Litim and Reichert (Nov 2025 talk) report Källén–Lehmann spectral functions of all graviton modes that are compatible
  with causality and unitarity. **✓ seen / secondary.**
- **Gravity and Yang–Mills:** Folkerts–Litim–Pawlowski (arXiv:1101.5552) find that gravity does not destroy asymptotic
  freedom. The one-loop graviton contribution to the gauge β-function is scheme dependent, but every
  symmetry-preserving computation gives a contribution with the same sign or zero (arXiv:1710.04669 review).
  arXiv:2604.03033 (2026) is a heat-kernel computation of the gravitational correction to gauge couplings. **✓ seen /
  secondary.**

### Quadratic gravity (Stelle; "agravity")
- Liu, Quintin, Afshordi, Phys. Rev. Lett. 136, 111501 (18 March 2026), arXiv:2510.18733. **✓ seen.** Inflation comes
  from quantum quadratic gravity, and the paper predicts a **floor** on primordial gravitational waves. Gravity is
  asymptotically free and becomes **strongly coupled** in the IR, and that strong coupling **confines the spin-2
  ghost** (Holdom–Ren). This is the place where a "confinement / mass gap" result is wanted inside gravity itself.
- Competing treatment: Kumar–Marto, arXiv:2603.07150, where the spin-2 mode stays off-shell. Kubo–Kuntz,
  arXiv:2502.03543, on the ghost and unitarity. **✓ seen.**

### Postquantum classical gravity (Oppenheim)
- Classical gravity coupled to quantum matter forces a trade-off: stronger decoherence requires weaker diffusion
  (Nat. Commun. 2023). **✓ seen.** Oppenheim–Sajjad, arXiv:2605.05375 (May 2026): consistency requires stochastic
  spacetime evolution, and LISA Pathfinder excess noise bounds one coupling combination. **✓ seen.**
  Hirotani–Matsumura, arXiv:2603.29230: strain spectra and a transverse-projected version that satisfies the
  constraint. **secondary.** A critique of relativistic extensions is arXiv:2404.07723. **✓ seen.**

---

## 3. Holography, algebras, and string theory

- **Observer algebras.** Chandrasekaran, Longo, Penington and Witten (arXiv:2206.10780): with an observer and clock,
  the de Sitter static-patch algebra is **type II₁**, so it has a trace and a finite entropy maximised by the
  Bunch–Davies state. Black holes give type II∞. Chen–Xu, arXiv:2511.00622, JHEP 09 (2026) 240: covariant observers
  with fluctuating static patches still give type II. **✓ seen.**
- **3D gravity is (almost) solved.** Collier, Eberhardt and Zhang solve 3D gravity with Λ < 0 through Virasoro TQFT
  (arXiv:2304.13650; SciPost Phys. 17, 134 (2024)). Flat-space 3D gravity is one-loop exact through three loops
  (arXiv:2507.16141). *What's the matter with 3D gravity?* (arXiv:2607.01319, 2026) quantises a massive scalar
  coupled to 3D gravity to all orders in G_N. **✓ seen.**
- JT gravity and double-scaled SYK give exactly solvable 2D models with de Sitter versions. **background**; not
  re-searched.
- **Swampland.** Palti's review (arXiv:1903.06239); Lehnert, arXiv:2509.02632 (Sept 2025), a status review for
  cosmologists (species scale, distance conjecture, emergence). **✓ seen.** A 2026 PRL on CFTs argues that continuous
  parameters of quantum gravity are set dynamically rather than externally ("no free parameters"). **secondary.**
- **BKL / cosmological billiards.** Near a spacelike singularity, gravity becomes a billiard in the Weyl chamber of a
  hyperbolic Kac–Moody algebra: AE₃ for 4D vacuum gravity (Mixmaster) and E₁₀ for 11D supergravity
  (Damour–Henneaux–Nicolai). **background.** QGL's `qgl_bkl.py` already integrates the Mixmaster dynamics. The
  Cartan matrices are checked in `python/qg/gravity_group_checks.py`.

---

## 4. Rigorous mathematics of quantum gravity (where theorems exist)

- **2D Liouville quantum gravity is constructed.** The √(8/3)-LQG sphere equals the Brownian map (Miller–Sheffield,
  arXiv:1605.03563, 1608.05391). The DOZZ formula and conformal bootstrap for Liouville CFT were proved by
  Kupiainen–Rhodes–Vargas and Guillarmou–Kupiainen–Rhodes–Vargas (background). Ang–Remy–Sun, Ann. Sci. ENS 58 (2025):
  the moduli of the Brownian annulus. Berestycki, arXiv:2512.02538: the LQG spectrum. Miller–Tian, arXiv:2603.24473
  (2026): the conformal dimension of the Brownian sphere is 2 (secondary). Survey: *Lessons from the mathematics of 2D
  Euclidean quantum gravity*, arXiv:2212.03031. **✓ seen.**
- **2D Yang–Mills on surfaces** (Driver, Sengupta, Lévy) and its random-surface / string expansion (Park and others)
  are rigorous. **background / ✓ seen.**
- **Nothing in d ≥ 3 with local degrees of freedom is constructed.** As in Yang–Mills (problem 3 of 4Y-M
  `strong-coupling/OPEN.md`), the gap is the continuum limit.
- **Formal verification.** PhysLean (formerly HepLean) is the community Lean 4 physics library. It covers special
  relativity, Wick's theorem and parts of QFT, but searches found no general-relativity formalisation. PhysProver
  (arXiv:2601.15737) uses it as training data. **✓ seen.** Our 4Y-M Lean project is already ahead of this library
  on lattice gauge theory.

---

## 5. Experiments and observation

| Programme | What it can show | Status, Oct 2026 |
|---|---|---|
| Gravity-mediated entanglement (Bose et al.; Marletto–Vedral) | Gravity can carry a quantum channel. Whether that means "gravity is quantum" is debated (arXiv:2208.09489), and local hidden-variable loopholes exist (arXiv:2109.02616). | Proposals only. The nanodiamond interferometer design is arXiv:2405.21029. **✓ seen** |
| Caution | Many "superposed spacetime" proposals are equivalent to quantum matter on classical spacetime (npj QI 2026). | **secondary** |
| Small-source gravity | 92 mg gold sphere (Aspelmeyer group, Nature 2021); 0.43 mg levitated-particle measurement (Southampton). | **✓ seen** (dates not checked) |
| Decoherence vs diffusion | Bounds classical-gravity couplings (LISA Pathfinder, interferometry). | Bounds set in 2026. **✓ seen** |
| Interferometer noise (Verlinde–Zurek geontropic; GQuEST photon counting) | Vacuum metric fluctuations. | GQuEST design in PRX 2025. Signal-to-model map for LIGO-type interferometers in a Jan 2026 Caltech paper. No detection. **✓ seen** |
| Single-graviton sensing (Tobar, Manikandan, Beitel, Pikovski) | Stimulated absorption of gravitons from LIGO-band waves by a quantum acoustic resonator. | Nat. Commun. 15, 7229 (2024) and follow-ups. Proposal only. **✓ seen** |
| CMB B-modes | The quadratic-gravity floor on r. | Future (LiteBIRD, CMB-S4 class). **background** |
| DESI DR2 evolving dark energy | Motivates cosmologically coupled black holes and Λ-as-dynamical models. | Already cited in QGL's README. |

---

## 6. What the survey says about where a lattice-gauge group can contribute

1. **The only approaches with a lattice gauge field as the fundamental variable** are first-order (Palatini /
   MacDowell–Mansouri) lattice gravity, spin foams (constrained lattice BF), and 3D gravity (Chern–Simons / Turaev–Viro).
   In the Euclidean setting their gauge groups are compact. That is exactly the setting of the "every compact simple
   group" theorem of 4Y-M.
2. **Strong-coupling phases are well studied numerically in gravity** (branched polymer, crumpled, vanishing vierbein)
   but have **no theorems**. The 4Y-M toolkit gives theorems at strong coupling: uniqueness, decay and a gap at an
   explicit coupling.
3. In gravity, a **mass gap is the wrong target**. A massless graviton means the physical phase must have no gap. A
   strong-coupling gap theorem therefore proves that a phase is *not* the gravitational one. 4Y-M's no-go theorem
   (`SpectralNoGo.lean`) becomes, for gravity, a criterion for ruling out lattice phases. This reversal is the most
   useful single observation in this survey, and it drives ideas G1–G3 in [03-ideas.md](03-ideas.md).
4. **Gravity couples to matter through T_μν.** The continuum Yang–Mills theory must therefore supply a renormalised
   stress tensor before it can be "connected to gravity later" (Brent's question). 4Y-M already controls flowed
   observables under the Sakai–Sasaki spatial gradient flow. The gradient flow is also how Suzuki defined the lattice
   energy-momentum tensor (background).
