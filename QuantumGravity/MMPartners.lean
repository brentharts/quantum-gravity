/-!
# G2. Partner counts of the MacDowell–Mansouri plaquette-pair action in the 4Y-M forest gauge

The lattice MacDowell–Mansouri action (Smolin; Caselle–D'Adda–Magnea) is a sum over sites `x` and the three
splittings `{μ, ν} ⊔ {ρ, σ} = {0, 1, 2, 3}` of a bilinear term in the curvatures of two plaquettes based at `x`
in complementary planes, `ε_{abcde} V^e R^{ab}(U_{x;μν}) R^{cd}(U_{x;ρσ})`. A link therefore interacts with:
* the other links of each plaquette through it, as in the Wilson action;
* all links of that plaquette's complementary partner at the same base.

We use the straight-line forest of 4Y-M (`YangMills/StrongCoupling/GaugeFix.lean`; the table and the conventions
are copied from there, MIT licence, © D. Bhattacharjee et al.). Sites of `ℤ⁴` are read modulo 2 as `Fin 16`; at
each site the forward link in direction `sig x` is fixed.

Checked by `decide`:
* every free link has exactly **30** free partners with multiplicity, `6 × (2 + 3)`: in each of its six plaquettes,
  two from the plaquette and three from the complementary one, since every plaquette has exactly one fixed link;
* without gauge fixing the count is `6 × (3 + 4) = 42`;
* for comparison, the Wilson action has 12 partners in this gauge (4Y-M).

The Dobrushin row sum of the pair action is at most `C |β| · 30`, with `C` the Lipschitz constant of a pair term in
one link. That constant (from `‖R‖ ≤ 2` and the S⁴ compensator) is the remaining analytic input
(`docs/G2-pregeometric-phase.md`).
-/

namespace QuantumGravity.MM

/-- The fixed direction at a site (4Y-M `GaugeFix.table`), indexed by `x₀ + 2 x₁ + 4 x₂ + 8 x₃` mod 2. -/
def table : List Nat := [0, 0, 2, 3, 3, 1, 2, 1, 1, 2, 1, 3, 3, 2, 0, 0]

def sig (x : Fin 16) : Nat := table.getD x.val 0

/-- Move by `e_μ` (modulo 2): flip bit `μ`. -/
def step (x : Fin 16) (μ : Nat) : Fin 16 := ⟨(x.val ^^^ (1 <<< μ)) % 16, Nat.mod_lt _ (by decide)⟩

def fixedLink (x : Fin 16) (μ : Nat) : Bool := sig x == μ

/-- The four links of the plaquette based at `b` in the plane `(μ, ν)`. -/
def plaq (b : Fin 16) (μ ν : Nat) : List (Fin 16 × Nat) :=
  [(b, μ), (step b μ, ν), (step b ν, μ), (b, ν)]

/-- The complementary plane of `(μ, ν)` in `{0, 1, 2, 3}`. -/
def comp (μ ν : Nat) : Nat × Nat :=
  match (([0, 1, 2, 3].filter fun a => a != μ && a != ν)) with
  | [ρ, σ] => (ρ, σ)
  | _ => (0, 0)

def freeCount (l : List (Fin 16 × Nat)) : Nat := l.countP fun e => !fixedLink e.1 e.2

def fixedCountP (l : List (Fin 16 × Nat)) : Nat := l.countP fun e => fixedLink e.1 e.2

/-- The six plaquettes through the forward link `(x, μ)`: bases `x` and `x − e_ν` (= `x + e_ν` mod 2) for each
`ν ≠ μ`, each with its plane. -/
def plaqsThrough (x : Fin 16) (μ : Nat) : List (Fin 16 × Nat × Nat) :=
  ([0, 1, 2, 3].filter (· != μ)).flatMap fun ν => [(x, μ, ν), (step x ν, μ, ν)]

/-- Partners with multiplicity of the free link `(x, μ)` under the pair action, with the forest. -/
def pairPartners (x : Fin 16) (μ : Nat) : Nat :=
  ((plaqsThrough x μ).map fun (b, a, c) =>
    (freeCount (plaq b a c) - 1) + freeCount (plaq b (comp a c).1 (comp a c).2)).sum

/-- The same count with no gauge fixing. -/
def pairPartnersNoFix (x : Fin 16) (μ : Nat) : Nat :=
  ((plaqsThrough x μ).map fun _ => 3 + 4).sum

/-- Every plaquette (any base, any plane) has exactly one fixed link: 4Y-M's property, rechecked here. -/
theorem one_fixed_per_plaquette :
    ∀ b : Fin 16, ∀ μ ν : Fin 4, μ.val < ν.val → fixedCountP (plaq b μ.val ν.val) = 1 := by decide

theorem pair_partners_thirty :
    ∀ x : Fin 16, ∀ μ : Fin 4, fixedLink x μ.val = false → pairPartners x μ.val = 30 := by decide

theorem pair_partners_nofix : ∀ x : Fin 16, ∀ μ : Fin 4, pairPartnersNoFix x μ.val = 42 := by decide

end QuantumGravity.MM
