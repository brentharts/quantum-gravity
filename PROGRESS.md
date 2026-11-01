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
| G13 | Immirzi parameter from counting punctures | three conventions **derived and checked**: 0.1274 (spin ½), 0.2375 (Domagala–Lewandowski), 0.2741 (all projections); the value 0.2375 is the middle one | `python/qg/immirzi.py`, `docs/G13-immirzi-counting.md` |
| G14 | Kerr horizons and the Penrose gap | identities (Smarr, first law at both horizons, Penrose gap M r₋/2, A₊A₋ = (8πJ)²) **checked exactly**; the heuristic composition with spin-½ area is labelled as such | `python/qg/kerr.py`, `docs/G14-kerr-horizons.md` |
| G15 | Planar maps, FK weights, SU(2)_k loop weight | Tutte and Mullin counts by brute force, FK dictionary, closed walks on A_{k+1} **checked**; no map from spin networks to maps constructed | `python/qg/planar_maps.py`, `docs/G15-planar-maps-su2k.md` |
| G16 | SU(2) strip of N = 3, 4, 5 plaquettes in the spin-network basis | N = 4, 5 levels **agree** with an independent Peter–Weyl calculation (2e-6, 1e-3) under a fitted phase rule; N = 4 weak-coupling gap ratio to N = 3 **consistent** with the formula (0.9624 vs 0.9598, two-point extrapolation); N = 5 not done | `python/qg/spin_network_strip.py`, `docs/G16-spin-network-strip.md` |
| G17 | Volume prefactor from the classical tetrahedron | c = √2/3 **fixed** by the regular tetrahedron (exact); max Q / classical → 1 with correction −3/(4j), **computed to j = 40**; smallest volume 1.777 ℓ_P³ | `python/qg/volume_tetrahedron.py`, `docs/G17-volume-prefactor.md` |

## Next steps, in order

0. G16: a faster state generator to reach g² < 0.4 at N = 4, 5 and test 2√(2 − cos(π/(N+1))); SU(2)_k deformation of the strip with quantum 6j (the link to G9's Turaev–Viro item).

1. G8: rigorous area law for SO(4) vector loops at β_W < 4/29, with explicit constants (polymer expansion), to add to
   the paper.
2. G3: prove the geometric spectrum of the 2D CDT transfer matrix (the Möbius fixed points of the propagator).
3. G2: the partner count and Hessian bound of the MacDowell–Mansouri plaquette-pair action on the 4Y-M forest, in Lean
   like `GaugeFix.lean`.
4. G4: the induced-gravity expansion on degree-capped complexes.
5. G11: open a PR to `brentharts/Quantum_Gravity_Lab` with a `qgl_cq.py` module, if Brent wants it.
