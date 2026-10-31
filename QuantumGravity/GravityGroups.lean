import Mathlib

/-!
# G2 / G8. Forest-gauge ranges for the gauge groups of Euclidean first-order gravity

4Y-M (forest-gauge paper, theorem on every compact simple group) proves a unique state, clustering
and a transfer-matrix gap for `N |β| < 2 Ric / 29`, i.e. `β_W = N² β < 2 N Ric / 29`. Here `N` is the
dimension of the faithful representation in the Wilson action and `Ric = c / 4`, where the Killing
form is `B = c · (trace form of the representation)`.

Euclidean gravity in first-order form is a gauge theory of
* `SO(4)` (Palatini; vector representation on the tetrad index), or its self-dual half `SU(2)`
  (Ashtekar–Plebanski), and
* `SO(5)` (MacDowell–Mansouri / Stelle–West, Euclidean de Sitter group), also `Sp(2) = Spin(5)`.

The ratio `c` is a quadratic-form identity on a Cartan subalgebra. With `H = (x, y)` (or `h` for
`SU(2)`), `B(H, H) = Σ_roots α(H)²` and the trace form is `Σ_weights μ(H)²`. The identities below hold
for every integer `H`, hence (being homogeneous quadratic) on the whole Cartan subalgebra. Spinor
weights `(±½, ±½)` are scaled by 2.

| group (rep) | `c` | `Ric` | `β_W` range |
|---|---|---|---|
| `SU(2)` (2) | 4 | 1 | 4/29 |
| `SO(4)` (4) | 2 | 1/2 | 4/29 |
| `SO(5)` (5) | 3 | 3/4 | 15/58 |
| `Sp(2)` (4) | 6 | 3/2 | 12/29 |

`SO(4)` is semisimple, not simple. Its two factors have equal Ricci constant, so the Bakry–Émery
argument of 4Y-M (which needs only a lower Ricci bound) applies unchanged. Not claimed here: the
lattice action of gravity is not the Wilson action, and this file only records the group constants
the 4Y-M theorems need.
-/

namespace QuantumGravity.Groups

/-- `Σ_{v ∈ L} (v · (x, y))²`. -/
def form (L : List (ℤ × ℤ)) (x y : ℤ) : ℤ := (L.map fun v => (v.1 * x + v.2 * y) ^ 2).sum

/-- Roots of `B₂ = so(5)`: `(±1, ±1)` and `(±1, 0), (0, ±1)`. -/
def b2Roots : List (ℤ × ℤ) :=
  [(1, 1), (1, -1), (-1, 1), (-1, -1), (1, 0), (-1, 0), (0, 1), (0, -1)]

/-- Weights of the vector representation of `so(5)`. -/
def b2Vec : List (ℤ × ℤ) := [(1, 0), (-1, 0), (0, 1), (0, -1), (0, 0)]

/-- Twice the weights of the spinor representation of `so(5)` (= fundamental of `sp(2)`). -/
def b2Spin2 : List (ℤ × ℤ) := [(1, 1), (1, -1), (-1, 1), (-1, -1)]

/-- Roots of `D₂ = so(4) = su(2) ⊕ su(2)`. -/
def d2Roots : List (ℤ × ℤ) := [(1, 1), (1, -1), (-1, 1), (-1, -1)]

/-- Weights of the vector representation of `so(4)`. -/
def d2Vec : List (ℤ × ℤ) := [(1, 0), (-1, 0), (0, 1), (0, -1)]

theorem so5_vector (x y : ℤ) : form b2Roots x y = 3 * form b2Vec x y := by
  simp [form, b2Roots, b2Vec]; ring

theorem sp2_spinor (x y : ℤ) : 4 * form b2Roots x y = 6 * form b2Spin2 x y := by
  simp [form, b2Roots, b2Spin2]; ring

theorem so4_vector (x y : ℤ) : form d2Roots x y = 2 * form d2Vec x y := by
  simp [form, d2Roots, d2Vec]; ring

/-- `su(2)` on `H = diag(h, -h)`: roots `±2h`, weights `±h`. -/
theorem su2_fundamental (h : ℤ) : (2 * h) ^ 2 + (-2 * h) ^ 2 = 4 * (h ^ 2 + (-h) ^ 2) := by ring

/-- The 4Y-M range `β_W < 2 N (c/4) / 29`. -/
def betaWmax (N c : ℚ) : ℚ := 2 * N * (c / 4) / 29

theorem range_su2 : betaWmax 2 4 = 4 / 29 := by norm_num [betaWmax]
theorem range_so4 : betaWmax 4 2 = 4 / 29 := by norm_num [betaWmax]
theorem range_so5 : betaWmax 5 3 = 15 / 58 := by norm_num [betaWmax]
theorem range_sp2 : betaWmax 4 6 = 12 / 29 := by norm_num [betaWmax]

end QuantumGravity.Groups
