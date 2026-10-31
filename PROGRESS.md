# Progress on G0–G12

Ideas are as numbered in [docs/03-ideas.md](docs/03-ideas.md). Status as of 2026-10-31.

| Idea | What | Status | Where |
|---|---|---|---|
| G0 | Four open problems of lattice QG | **written** | `OPEN.md` |
| G1 | A physical gap excludes a massless mode | **proved in Lean** | `QuantumGravity/NoGraviton.lean` |
| G2 | Pregeometric phase of MacDowell–Mansouri lattice gravity | group constants **proved in Lean**; theorem programme written; partner/Hessian count for the plaquette-pair action and the S⁴ compensator **to do** | `GravityGroups.lean`, `docs/G2-pregeometric-phase.md` |
| G3 | CDT through the transfer matrix | 2D: exact transfer matrix, geometric spectrum **found numerically** (proof to do); 3+1 programme written | `python/qg/cdt2d.py`, `docs/G3-cdt.md` |
| G4 | YM on any geometry; induced gravity | count lemma, ℤ³/ℤ⁴ reproduced, **600-cell optimum 9 proved**, general lower bound; induced-gravity cluster expansion **to do** | `ForestRowSum.lean`, `python/qg/forest_partners.py`, `docs/G4-geometry-uniform.md` |
| G5 | Stress tensor of continuum YM | programme written (4 steps), all open | `docs/G5-stress-tensor.md` |
| G6 | Gravity and asymptotic freedom | **proved in Lean** | `QuantumGravity/RunningWithGravity.lean` |
| G7 | Cosmological billiards | AE₃/E₁₀ **in Lean**; BKL = continued fractions **checked** | `Billiards.lean`, `python/qg/bkl_billiard.py` |
| G8 | Confinement of the curvature-squared sector | corollary of 4Y-M + G1 + group constants; character coefficients computed; rigorous area-law constants **to do** | `paper/`, `python/qg/lorentz_strong.py` |
| G9 | 3D: Ponzano–Regge ↔ forest gauge | exact 6j identities and PR asymptotics **checked**; quantum 6j / Turaev–Viro and the interpolating family **to do** | `python/qg/sixj.py` |
| G10 | YM₂ on Liouville quantum gravity | Brownian-disk Wilson loop **derived and checked**; sphere sectors shift μ | `python/qg/ym2_brownian.py`, `paper/` |
| G11 | Decoherence–diffusion trade-off for QGL | saturating model **built and checked**; port into QGL **to do** (Brent's repo) | `python/qg/cq_tradeoff.py` |
| G12 | Small QGL tests | Gauss–Kuzmin for BKL eras **checked** | `python/qg/bkl_billiard.py` |

## Next steps, in order

1. G8: rigorous area law for SO(4) vector loops at β_W < 4/29, with explicit constants (polymer expansion), to add to
   the paper.
2. G3: prove the geometric spectrum of the 2D CDT transfer matrix (the Möbius fixed points of the propagator).
3. G2: the partner count and Hessian bound of the MacDowell–Mansouri plaquette-pair action on the 4Y-M forest, in Lean
   like `GaugeFix.lean`.
4. G4: the induced-gravity expansion on degree-capped complexes.
5. G11: open a PR to `brentharts/Quantum_Gravity_Lab` with a `qgl_cq.py` module, if Brent wants it.
