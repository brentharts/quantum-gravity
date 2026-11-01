# Quantum gravity from the lattice Yang–Mills side

Tristan Romanov and Brent Hartshorn, building on the 4Y-M collaboration (Bhattacharjee, Bhattacharya, Lockwood,
Romanov) and Hartshorn's [Quantum Gravity Lab](https://github.com/brentharts/Quantum_Gravity_Lab).

The starting point is [creelie/4Y-M v4.29.0](https://github.com/creelie/4Y-M/tree/v4.29.0). In that work, lattice
Yang–Mills for every compact simple group has a unique state and a gap at strong coupling, and the continuum gap is
reduced to one cube estimate. This repository asks what that machinery can say about gravity.

**The guiding observation.** In Yang–Mills a mass gap is the goal; in gravity it is a diagnosis. The graviton is
massless, so a lattice phase with a gap in physical units is not gravitational. The strong-coupling theorems of 4Y-M
apply as stated to lattice gravity written as a gauge theory of SO(4) or SO(5). They therefore *exclude* those
phases, which simulations have seen but nobody has proved anything about.

## Contents

| Path | What |
|---|---|
| [`paper/main.pdf`](paper/main.pdf) | Draft: *A gap is not a graviton: strong-coupling exclusions for lattice gravity in first-order form* (G1, G8, G6, G4, G10, G3, G7) |
| [`PROGRESS.md`](PROGRESS.md) | Status of ideas G0–G12 |
| [`OPEN.md`](OPEN.md) | G0: four open problems of lattice quantum gravity, mirroring 4Y-M's |
| [`docs/`](docs) | Frontier survey (Oct 2026), how 4Y-M meets gravity, the ideas, references, and notes on G2, G3, G4, G5, G13–G17 |
| [`QuantumGravity/`](QuantumGravity) | Lean 4 / Mathlib (v4.33.0); no `sorry`, standard axioms only |
| [`python/qg/`](python/qg) | Numerical and exact-arithmetic checks; tests in `python/tests` |

## Lean (all compiled, `lake build`)

| File | Idea | Main statements |
|---|---|---|
| `NoGraviton.lean` | G1 | a physical gap along the tuning survives every limit; a massless mode is not exponentially decaying; **no continuum limit with a massless mode** |
| `RunningWithGravity.lean` | G6 | with antiscreening gravity asymptotic freedom survives (and the coupling is never larger than without gravity); with screening, an interacting UV fixed point g² → −f/b; the window is still entered at an explicit scale |
| `GravityGroups.lean` | G2/G8 | Killing/trace ratios for SU(2), SO(4), SO(5), Sp(2) on the whole Cartan subalgebra; ranges 4/29, 4/29, 15/58, 12/29 |
| `ForestRowSum.lean` | G4 | the partner count on any 2-complex; **the 600-cell: 9 partners is optimal** (β_W < 4/9) |
| `Billiards.lean` | G7 | AE₃ minors 2, 3, −2 and E₁₀ minors 2, …, 10, −1 by `decide` (Lorentzian); E₈ unimodular, E₉ affine |

## Python (`python3 -m pytest python/tests`)

| Module | Idea | Result |
|---|---|---|
| `forest_partners.py` | G4 | reproduces 12 (ℤ⁴) and 7 (ℤ³); period-2 forests on ℤ³ cannot beat 8 (exhaustive); 600-cell optimum 9 |
| `ym2_brownian.py` | G10 | YM₂ on the Brownian disk: area law → d_F(1 + gL√C_F)e^{−gL√C_F}; on the sphere each representation shifts μ by g²C/2, γ_str unchanged |
| `cdt2d.py` | G3 | 2D CDT transfer matrix: geometric spectrum λ_{n+1}/λ_n = (1−s)/(1+s), s = √(1−4g²); gap ∝ a |
| `lorentz_strong.py` | G8 | SO(4) character coefficient a_F = β_W/16 + O(β_W³); leading string tension 4.75 at β_W = 4/29 |
| `sixj.py` | G9 | 6j orthogonality, Biedenharn–Elliott and Racah identities exactly; Ponzano–Regge asymptotics |
| `cq_tradeoff.py` | G11 | qubit backreaction on a classical momentum: Γ·D₂ = F²/4 at every measurement strength |
| `bkl_billiard.py` | G7/G12 | BKL era lengths = continued-fraction digits; Gauss–Kuzmin statistics |
| `gravity_group_checks.py` | G2/G7 | exact rational cross-check of the Lean group constants and Cartan matrices |
| `immirzi.py` | G13 | Immirzi parameter from three counting conventions: 0.1274, 0.2375 (m = ±j), 0.2741 (all projections); renewal-equation growth checked |
| `kerr.py` | G14 | Kerr: Smarr and first law at both horizons, Penrose gap M r₋/2, A₊A₋ = (8πJ)² (exact); heuristic puncture count N ≥ 2π\|J\|/ln 2 |
| `planar_maps.py` | G15 | Tutte 2, 9, 54 and Mullin 2, 10, 70 by brute force; FK dictionary (q, κ′, γ, c, γ_str); closed walks on A_{k+1} = Catalan, growth √q_k |
| `spin_network_strip.py` | G16 | SU(2) strip of N = 3, 4, 5 plaquettes in the spin-network basis with signed 6j; levels agree with an independent Peter–Weyl calculation |
| `volume_tetrahedron.py` | G17 | volume prefactor √2/3 from the regular tetrahedron; max eigenvalue of the triple product → classical value as 1 − 3/(4j) (to j = 40); smallest volume 1.777 ℓ_P³ |

## Build

```
lake exe cache get
lake build
lake env lean scripts/Axioms.lean
pip install -r requirements.txt pytest && python3 -m pytest -q python/tests
cd paper && latexmk -pdf main.tex
```

## Not claimed

Nothing here identifies a gravitational phase, constructs a continuum limit of any 4D gravity model, or concerns
Lorentzian signature. The strong-coupling statements hold at fixed lattice spacing.
