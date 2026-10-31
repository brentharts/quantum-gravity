# G0. Four open problems of lattice quantum gravity

This list mirrors 4Y-M's `strong-coupling/OPEN.md` for Yang–Mills. A problem counts as solved only when every case
under it is proved. Normalisation for gauge-theoretic formulations: weight exp(Nβ Σ_p Re Tr Q_p), β_W = N²β.

The difference from Yang–Mills is in problem 4. **Yang–Mills wants a mass gap. Gravity wants a massless spin-2 pole.**
A gap in physical units therefore *rules out* a phase (`QuantumGravity/NoGraviton.lean`).

## 1. Which phases are gapped, at fixed lattice spacing

| Formulation | Range | Status | Where |
|---|---|---|---|
| First-order lattice gravity, frozen tetrad: pure Lorentz gauge theory SO(4) (vector rep) | β_W < 4/29 | **proved** (4Y-M every-group theorem; SO(4) has Ric = 1/2) | `QuantumGravity/GravityGroups.lean`, 4Y-M forest paper |
| Euclidean de Sitter gauge field SO(5), no compensator | β_W < 15/58 | **proved** (same theorem, Ric = 3/4) | same |
| SO(5) with the Stelle–West compensator V (MacDowell–Mansouri gravity), small β and small hopping κ | uniqueness, gap, ⟨e⟩ = 0 | **open**: needs the Hessian/partner count of the MM plaquette-pair action and the gauge–Higgs Dobrushin step | [docs/G2-pregeometric-phase.md](docs/G2-pregeometric-phase.md) |
| SU(2) Yang–Mills on a fixed triangulation with every link in ≤ k triangles | β_W < 4/k at best; the 600-cell: β_W < 4/9 (optimal for single-link forests) | **proved** for the counts; the analytic step is 4Y-M's | `ForestRowSum.lean`, `python/qg/forest_partners.py` |
| CDT / EDT, large bare cosmological constant (phases A, B) | uniqueness of the slice-volume process | **open** | [docs/G3-cdt.md](docs/G3-cdt.md) |
| 2D CDT | exact geometric spectrum λ_n = λ_0 rⁿ, gap 2 artanh √(1−4g²) | **numerical check** of the exact solution | `python/qg/cdt2d.py` |

## 2. The crossover to the geometric phase

CDT phase C and the EDT fine-tuned line are the candidate geometric phases. Their transitions to the non-geometric
phases are numerically second order (CDT) or first order (plain EDT). No criterion that a finite box can verify is
known on either side. **Open.**

## 3. A continuum limit, and what replaces the Osterwalder–Schrader axioms

For gauge theories the target is the OS axioms. Diffeomorphism invariance removes local gauge-invariant observables,
so for gravity there is no agreed axiom system. Candidates:
- relational observables (fields at points defined by other fields);
- the type II observer algebras of Chandrasekaran–Longo–Penington–Witten (an observer with a clock in de Sitter space);
- the CDT transfer matrix, which is reflection positive in proper time.

In 2D, Liouville quantum gravity is constructed, and YM₂ on it is exactly computable (`python/qg/ym2_brownian.py`).
**Open in d ≥ 3.**

## 4. The graviton

A massless spin-2 pole in physical units along a continuum tuning: the mirror image of Yang–Mills problem 4.
- If the gap is uniform in lattice units: every renormalised two-point function vanishes (4Y-M `SpectralNoGo`).
- If the gap is uniform in physical units: there is no massless mode (`no_massless_limit_of_physicalGap`).
- A graviton therefore requires Δ_lat(a)/a → 0.

**Open.**
