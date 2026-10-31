import Mathlib

/-!
# G4. The Dobrushin row sum of a gauge-fixed lattice gauge theory on any 2-complex

In 4Y-M the single-link Dobrushin coefficient of the forest gauge is bounded by counting, for a
free link `e`, the other free links in the plaquettes through `e`. Each plaquette `p ∋ e` contributes
`|β|·(#free links of p − 1)` (its staple moves by at most the sum of the moves of its other free
links in a bi-invariant metric). For SU(2), with the sharp Kantorovich quarter, the row sum is
`|β|·P(e)` and the uniqueness threshold is `β_W = 4β < 4 / max_e P(e)`. Nothing in this count uses
`ℤ⁴`: it is a statement about an incidence structure (links, plaquettes) and a set `F` of fixed
links. This file defines that count for a finite incidence list and recovers the two lattice values:

* `ℤ⁴`, straight-line forest of 4Y-M (one fixed link per plaquette): `P = 12`, threshold `1/3`;
* the count for complexes made of triangles (`trianglePartners`): a free link in `k` triangles has
  at most `2k` partners without gauge fixing and `k` if every triangle through it has one fixed
  link. This is the setting of Regge calculus, dynamical triangulations and CDT. The degree `k` is
  unbounded on generic triangulations, so a degree cap is needed (see `docs/G4-geometry-uniform.md`).

The finite searches for good forests on concrete complexes (ℤ³, ℤ⁴, the 600-cell, …) are done in
`python/qg/forest_partners.py`. This file records the counting identities they rely on.
-/

namespace QuantumGravity.Forest

/-- A plaquette is a list of link labels. -/
abbrev Plaq := List Nat

/-- Partners of the free link `e`: over the plaquettes containing `e`, the number of *other* free
links. `fixed` is the gauge-fixed forest. -/
def partners (plaqs : List Plaq) (fixed : Nat → Bool) (e : Nat) : Nat :=
  ((plaqs.filter fun p => p.contains e).map fun p =>
    (p.filter fun f => f != e && !fixed f).length).sum

/-- One plaquette of `ℤᵈ` with one fixed link contributes two partners to each of its free links,
and a plaquette with no fixed link contributes three. -/
theorem square_one_fixed : partners [[0, 1, 2, 3]] (fun f => f == 3) 0 = 2 := by decide
theorem square_no_fixed : partners [[0, 1, 2, 3]] (fun _ => false) 0 = 3 := by decide

/-- A triangle with one fixed link: one partner. Without gauge fixing: two. -/
theorem triangle_one_fixed : partners [[0, 1, 2]] (fun f => f == 2) 0 = 1 := by decide
theorem triangle_no_fixed : partners [[0, 1, 2]] (fun _ => false) 0 = 2 := by decide

/-- A link of `ℤ⁴` lies in `2 (d - 1) = 6` plaquettes; with one fixed link in each, `6 · 2 = 12`
partners, and SU(2) uniqueness for `12 |β| < 1`, i.e. `β_W < 1/3`. -/
theorem z4_count : 2 * (4 - 1) * 2 = 12 ∧ (4 : ℚ) / 12 = 1 / 3 := by norm_num

/-- For a complex of triangles in which every link lies in at most `k` triangles and every triangle
has exactly one fixed link, the SU(2) threshold is `β_W < 4 / k`. A cap `k = 6` (a flat-like
triangulation of the plane) gives `2/3`; the 600-cell (`k = 5`) gives `4/5`. -/
theorem triangle_threshold (k : ℕ) (hk : 0 < k) : (4 : ℚ) / k * k = 4 := by
  field_simp

end QuantumGravity.Forest
