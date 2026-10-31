# G4. Yang–Mills on any geometry, and induced gravity at strong coupling

## 1. The count is local

The single-link Dobrushin argument of 4Y-M uses only two things: the plaquettes through a link, and which of their
links are fixed by a forest. For any 2-complex and any forest F, a free link e has

  P(e) = Σ_{p ∋ e} (#free links of p − 1)

partners. SU(2) has uniqueness, decay and a gap for β_W < 4 / max_e P(e). For complexes of triangles,
P(e) = 2k_e − (#fixed links sharing a triangle with e), where k_e is the number of triangles through e.

## 2. Results (`python/qg/forest_partners.py`, `QuantumGravity/ForestRowSum.lean`)

| complex | max P without fixing | best forest | SU(2) range | status |
|---|---|---|---|---|
| ℤ⁴, 4Y-M straight lines | 18 | 12 | β_W < 1/3 | reproduces 4Y-M |
| ℤ³, Romanov period-3 forest | 12 | 7 | β_W < 4/7 | reproduces the 3D paper |
| ℤ³, period-2 parent-map forests | 12 | **8** | β_W < 1/2 | **exhaustive**: period 2 cannot reach 7 |
| ∂Δ⁴ (S³, 5 vertices) | 6 | 4 | β_W < 1 | search |
| ∂Δ⁵ (S⁴, 6 vertices) | 8 | 6 | β_W < 2/3 | search |
| **600-cell** (S³, 120 vertices, 720 edges, 1200 triangles, k = 5) | 10 | **9** | **β_W < 4/9** | **optimal**: greedy forest attains 9; Lean counting bound shows 8 is impossible |

**600-cell optimality.** A forest has at most 119 links. Each fixed link is a triangle neighbour of 10 others, so it
can lower at most 10 partner counts by one. Bringing every one of the ≥ 601 free links to P ≤ 8 needs 1202 such
decrements, but at most 10·119 = 1190 are available (`cell600_nine_optimal`). The general bound for a closed
complex of triangles with V vertices, E edges and k triangles per edge is

  max P ≥ 2k − ⌊2k(V − 1)/(E − V + 1)⌋.

**Lesson.** On a closed 3-manifold triangulation a forest is too small to help much: it has V − 1 links among
E ≈ 6V. On ℤᵈ, forests help because there is one fixed link per *site*. For dynamical triangulations the gain from
gauge fixing is therefore small, and the threshold is governed by the maximal edge degree k. **A degree cap is
necessary**: generic DT/CDT configurations have unbounded k, and the uniform-in-geometry statement holds only
for k ≤ k_max, with β_W < 4/(2k_max − 1) or better.

## 3. Induced gravity at strong coupling (statement to prove)

For complexes T with edge degree ≤ k_max and β below the uniqueness threshold, the polymer/cluster expansion gives

  log Z_YM[T] = Σ_{connected local patterns P} n_P(T) a_P(β),  with Σ_P |a_P| e^{c|P|} < ∞ uniformly in T.

So in the annealed measure exp(−S_grav[T]) Z_YM[T], Yang–Mills only shifts the local couplings of the gravity model:
- vertex, edge and triangle counts (the κ₀, κ₄ of DT/CDT);
- local curvature patterns (edge degrees, i.e. deficit angles).

Each shift is an explicit convergent series, and no long-range interaction is induced. This is Sakharov's induced
gravity at strong coupling, with error bounds. The 2D analogue is exact: each YM₂ representation shifts the
cosmological constant by g²C_λ/2 (`python/qg/ym2_brownian.py`).

## 4. Refused: "Yang–Mills on Chair44"

Chair44 tiles are unions of unit cubes, so the cell complex of any Chair44 tiling is ℤ³ itself. Yang–Mills on it is
ordinary ℤ³ Yang–Mills unless the action is decorated by tile data (e.g. a coupling that depends on the notch
direction from `qgl_tiling.py`). Without such a decoration there is nothing to connect. With one, the 4Y-M count goes
through with β replaced by the maximum of the local couplings.
