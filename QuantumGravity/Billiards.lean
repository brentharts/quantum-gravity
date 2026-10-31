import Mathlib

/-!
# G7. Cosmological billiards: the Cartan matrices of AE₃ and E₁₀

Near a spacelike singularity the dynamics of four-dimensional vacuum gravity (Mixmaster,
Belinski–Khalatnikov–Lifshitz) becomes a billiard in the Weyl chamber of the hyperbolic Kac–Moody
algebra `AE₃`, and that of eleven-dimensional supergravity a billiard for `E₁₀`
(Damour–Henneaux–Nicolai). The finite content is the Cartan matrices.

`leadingMinors` is the fraction-free (Bareiss) elimination without pivoting. Its `k`-th pivot is the
`k`-th leading principal minor of the matrix (Bareiss 1968), so the last entry is the determinant.
When no leading minor vanishes, Jacobi's rule says the number of negative eigenvalues equals the
number of sign changes in `1, D₁, …, Dₙ`. A single sign change means Lorentzian signature, which is
the signature of a hyperbolic Kac–Moody algebra.

What is checked here, by `decide` on integers:

* `AE₃`, with its nodes ordered so that no leading minor vanishes, has minors `2, 3, −2`: det `−2`,
  one negative direction;
* `E₁₀` has minors `2, 3, …, 10, −1`: det `−1` (unimodular), one negative direction;
* `E₈` has det `1` (unimodular, positive definite) and the affine `E₉ = E₈⁽¹⁾` has det `0`, which
  locate `E₁₀ ⊃ E₉ ⊃ E₈`;
* for `AE₃` the Bareiss value agrees with `Matrix.det` (`ae3_det`).

Not claimed: the identification of BKL dynamics with these billiards is a statement about the
classical theory near a singularity (Damour–Henneaux–Nicolai), not about quantum gravity.
-/

namespace QuantumGravity.Billiards

/-- One step of fraction-free elimination: the pivot `p` is the top-left entry, and the remaining
block becomes `(p * a - r₀ * b) / prev`. Structural recursion on `fuel` keeps it reducible by the
kernel. -/
def minorsAux : Nat → Int → List (List Int) → List Int
  | 0, _, _ => []
  | _ + 1, _, [] => []
  | fuel + 1, prev, r0 :: rest =>
    let p := r0.headD 0
    p :: minorsAux fuel p
      (rest.map fun ri => List.zipWith (fun a b => (p * a - ri.headD 0 * b) / prev) ri.tail r0.tail)

/-- The leading principal minors `D₁, …, Dₙ` (valid when none of `D₁, …, Dₙ₋₁` vanishes). -/
def leadingMinors (M : List (List Int)) : List Int := minorsAux M.length 1 M

/-- Number of sign changes in `1, D₁, …, Dₙ`: by Jacobi's rule, the number of negative eigenvalues. -/
def signChanges : List Int → Nat
  | l => ((1 :: l).zip l).countP fun (a, b) => a * b < 0

/-- Symmetric Cartan matrix of a simply laced or doubly laced diagram, from its edges `(i, j, m)`
meaning `A i j = A j i = -m`. -/
def cartan (n : Nat) (edges : List (Nat × Nat × Int)) : List (List Int) :=
  (List.range n).map fun i => (List.range n).map fun j =>
    if i = j then 2 else
      -(edges.foldl (fun acc (e : Nat × Nat × Int) =>
          if (e.1 = i ∧ e.2.1 = j) ∨ (e.1 = j ∧ e.2.1 = i) then acc + e.2.2 else acc) 0)

/-- `AE₃`, nodes ordered `(α₃, α₂, α₁)` of the usual labelling, so that the affine pair `α₁, α₂`
(with `A₁₂ = -2`) comes last and no leading minor vanishes. -/
def ae3 : List (List Int) := [[2, -1, 0], [-1, 2, -2], [0, -2, 2]]

/-- `E₁₀`: a chain `0 — 1 — ⋯ — 8` with node `9` attached to node `6`. -/
def e10 : List (List Int) := cartan 10 ((List.range 8).map (fun i => (i, i + 1, 1)) ++ [(6, 9, 1)])

/-- `E₉ = E₈⁽¹⁾`: chain `0 — ⋯ — 7`, node `8` attached to node `5`. -/
def e9 : List (List Int) := cartan 9 ((List.range 7).map (fun i => (i, i + 1, 1)) ++ [(5, 8, 1)])

/-- `E₈`: chain `0 — ⋯ — 6`, node `7` attached to node `4`. -/
def e8 : List (List Int) := cartan 8 ((List.range 6).map (fun i => (i, i + 1, 1)) ++ [(4, 7, 1)])

theorem ae3_minors : leadingMinors ae3 = [2, 3, -2] := by decide

theorem ae3_lorentzian : signChanges (leadingMinors ae3) = 1 := by decide

theorem e10_minors : leadingMinors e10 = [2, 3, 4, 5, 6, 7, 8, 9, 10, -1] := by decide

theorem e10_lorentzian : signChanges (leadingMinors e10) = 1 := by decide

theorem e9_affine : (leadingMinors e9).getLast? = some 0 := by decide

theorem e8_unimodular : leadingMinors e8 = [2, 3, 4, 5, 6, 7, 8, 1] := by decide

/-- The Bareiss value of `AE₃` is its determinant. -/
theorem ae3_det : Matrix.det !![(2 : ℤ), -1, 0; -1, 2, -2; 0, -2, 2] = -2 := by
  simp [Matrix.det_fin_three]

/-- The two `2 × 2` subdiagrams of `AE₃` containing the double bond are affine (`det = 0`) and of
finite type (`det = 3`): removing a node from a hyperbolic diagram leaves finite or affine type. -/
theorem ae3_subdiagrams :
    Matrix.det !![(2 : ℤ), -2; -2, 2] = 0 ∧ Matrix.det !![(2 : ℤ), -1; -1, 2] = 3 ∧
      Matrix.det !![(2 : ℤ), 0; 0, 2] = 4 := by
  simp [Matrix.det_fin_two]

end QuantumGravity.Billiards
