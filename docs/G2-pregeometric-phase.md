# G2. The pregeometric phase of lattice MacDowell–Mansouri gravity

## Setting

Euclidean MacDowell–Mansouri gravity is an SO(5) gauge theory, broken to SO(4) by a unit 5-vector V (Stelle–West).

- **Variables:** a link field U_xy ∈ SO(5) and a site field V_x ∈ S⁴ ⊂ ℝ⁵.
- **Tetrad:** in the gauge V = (0,0,0,0,1), the tetrad is the so(5)/so(4) part of the connection. Gauge-covariantly,
  e_xy = U_xy V_y − V_x, up to normalisation.
- **Action:** S = S_MM(U, V) + κ Σ_⟨xy⟩ V_x · U_xy V_y.
  - S_MM is a sum over pairs of plaquettes at a site: ε_abcde V^e (U_p)^{ab} (U_p')^{cd}, with p and p' in
    complementary planes. Smolin (1979) and Caselle–D'Adda–Magnea (1989) give such actions; in the continuum limit
    they reduce to the Euler term + Einstein–Hilbert + cosmological constant.
  - The κ term is a gauge–Higgs hopping term.

## Target theorem

There are explicit β₀, κ₀ > 0 such that for |β| < β₀ and |κ| < κ₀:
1. the infinite-volume Gibbs state (free boundary conditions in boxes) is unique;
2. gauge-invariant local observables cluster exponentially;
3. the transfer matrix has a gap m(β, κ) > 0;
4. ⟨e_xy · e_xy'⟩ decays exponentially in |y − y'|, and the induced metric g_μν = ⟨e_μ · e_ν⟩ averages to a multiple
   of the identity that tends to 0 as β, κ → 0. There is no macroscopic geometry.

By `NoGraviton.lean`, if the gap persists in physical units along a tuning, this phase has no graviton.

## Ingredients and status

| Step | Status |
|---|---|
| Group constants for SO(5): Ric = 3/4, pure-gauge range β_W < 15/58 | done (`GravityGroups.lean`) |
| Forest gauge for the link field | 4Y-M's straight-line forest applies verbatim, since it is a property of ℤ⁴ |
| Partner count for S_MM: a link enters plaquette *pairs*, so its conditional law depends on 1 + 2·5 plaquette products per plaquette through it | to do. It is a finite count in the style of `GaugeFix.lean`; the influence matrix has entries ≤ C|β| over a larger neighbourhood |
| Hessian bound for the pair action on the free links (Bakry–Émery route) | to do. Bilinear in curvatures, so the Hessian has cross terms between plaquettes; the bound will be of the form h|β| with h computable |
| Site field V: single-site Dobrushin with hopping κ (S⁴ is a von Mises–Fisher family) | standard. The sharp Kantorovich modulus of the vMF family on S⁴ is needed (4Y-M computed the S³ one, 1/4) |
| Combined influence matrix (links + sites) row sum < 1 | assembly |
| Gap from the transfer matrix (Osterwalder–Seiler) | standard once uniqueness and decay hold with explicit rates |

## What it would mean

It would be the first theorem about a phase of four-dimensional lattice quantum gravity. It would also explain the
vanishing tetrad seen by Catterall–Ferrante (arXiv:0912.5525) at strong coupling.

## Not claimed

Nothing here concerns the geometric phase, Lorentzian signature, or the continuum limit.
