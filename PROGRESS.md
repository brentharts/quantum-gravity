# Progress on G0–G16

Ideas are as numbered in [docs/03-ideas.md](docs/03-ideas.md). Status as of 2026-11-01. G13–G16 come from Brent Hartshorn's quantum gravity paper (see `docs/hartshorn-bridge.md`).

| Idea | What | Status | Where |
|---|---|---|---|
| G0 | Four open problems of lattice QG | **written** | `OPEN.md` |
| G1 | A physical gap excludes a massless mode | **proved in Lean** | `QuantumGravity/NoGraviton.lean` |
| G2 | Pregeometric phase of MacDowell–Mansouri lattice gravity | group constants and **pair-action partner count 30 (42 unfixed) proved in Lean**; Lipschitz constant of a pair term and the S⁴ compensator **to do** | `GravityGroups.lean`, `MMPartners.lean`, `docs/G2-pregeometric-phase.md` |
| G3 | CDT through the transfer matrix | 2D: **spectrum proved**, λ_n = x₋^{2n+2}/g (Möbius identity and fixed-point algebra in Lean; triangular/completeness argument in the doc); 3+1 programme written | `CDT2D.lean`, `python/qg/cdt2d.py`, `docs/G3-cdt.md` |
| G4 | YM on any geometry; induced gravity | count lemma, ℤ³/ℤ⁴ reproduced, **600-cell optimum 9 proved**, general lower bound; induced-gravity cluster expansion **to do** | `ForestRowSum.lean`, `python/qg/forest_partners.py`, `docs/G4-geometry-uniform.md` |
| G5 | Stress tensor of continuum YM | programme written (4 steps), all open | `docs/G5-stress-tensor.md` |
| G6 | Gravity and asymptotic freedom | **proved in Lean** | `QuantumGravity/RunningWithGravity.lean` |
| G7 | Cosmological billiards | AE₃/E₁₀ **in Lean**; BKL = continued fractions **checked** | `Billiards.lean`, `python/qg/bkl_billiard.py` |
| G8 | Confinement of the curvature-squared sector | corollary of 4Y-M + G1 + group constants; character coefficients computed; rigorous area-law constants **to do** | `paper/`, `python/qg/lorentz_strong.py` |
| G9 | 3D: Ponzano–Regge ↔ forest gauge | exact 6j identities and PR asymptotics **checked**; **quantum 6j of SU(2)_k** (orthogonality, Biedenharn–Elliott, total dimension, q → 1 limit) **checked**; Turaev–Viro invariants and the interpolating family **to do** | `python/qg/sixj.py`, `python/qg/quantum6j.py` |
| G10 | YM₂ on Liouville quantum gravity | Brownian-disk Wilson loop **derived and checked**; sphere sectors shift μ | `python/qg/ym2_brownian.py`, `paper/` |
| G11 | Decoherence–diffusion trade-off for QGL | saturating model **built and checked**; port into QGL **to do** (Brent's repo) | `python/qg/cq_tradeoff.py` |
| G12 | Small QGL tests | Gauss–Kuzmin for BKL eras **checked** | `python/qg/bkl_billiard.py` |
| G13 | Immirzi parameter over all spins (Hartshorn's open item) | **certified to 25 digits**: 0.2375329579659206643583771 (2 states per puncture), 0.2740668582328299962167637 (2j+1) | `python/qg/immirzi.py` |
| G14 | Volume operator: prefactor and semiclassical limit (Hartshorn's open items) | closed-form tridiagonal elements **checked against brute force**; prefactor (√2/3)(8πγℓ_P²)^{3/2}√\|Q\|; ratio → 1 with **j(1 − ratio) → 3/4** (numerics to j = 65536; proof to do) | `python/qg/volume.py` |
| G15 | Harmonic gaps of plaquette clusters | **one formula** Δ = √(2 μ_min(∂∂ᵀ)); strip formula for all N **proved in Lean**; L-shape = strip explained; predictions 2×2 → 2, T → 2.12977 | `ClusterModes.lean`, `python/qg/cluster_gap.py` |
| G16 | Dimension four, twice (Hartshorn) | **Lean** | `GravityGroups.dim_four_twice` |

## Next steps, in order

1. G8: rigorous area law for SO(4) vector loops at β_W < 4/29, with explicit constants (polymer expansion), to add to
   the paper.
2. G14: prove j(1 − ratio) → 3/4 (Bohr–Sommerfeld for the tridiagonal a_k, or a WKB analysis of the Jacobi matrix).
3. G15: send the 2×2 and T-shape predictions to Brent for his full-Hamiltonian code.
4. G2: the Lipschitz constant of the pair term and Hessian bound of the MacDowell–Mansouri plaquette-pair action on the 4Y-M forest, in Lean
   like `GaugeFix.lean`.
5. G4: the induced-gravity expansion on degree-capped complexes.
6. G11: open a PR to `brentharts/Quantum_Gravity_Lab` with a `qgl_cq.py` module, if Brent wants it.
