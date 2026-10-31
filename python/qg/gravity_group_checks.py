#!/usr/bin/env python3
"""Exact checks behind research/gravity/03-ideas.md (ideas G2 and G7).

1. Gauge groups of Euclidean first-order gravity, run through the forest-gauge range of 4Y-M
   (every compact simple group: N|beta| < 2 Ric/29 with Ric = c/4, B = c * trace form,
   so beta_W = N^2 beta < 2 N Ric / 29).  The groups are
     SU(2)            self-dual half of Spin(4) (Ashtekar / Plebanski)
     SO(5)            Euclidean de Sitter group of MacDowell-Mansouri, vector rep (N = 5)
     Sp(2) = Spin(5)  the same algebra in its 4-dim spinor rep (N = 4)
   The ratio c is computed from roots and weights in exact rational arithmetic, the same method as
   4Y-M strong-coupling/gauge-fixed/checks/groups/ricci.py, but written independently here.

2. The Cartan matrices of the BKL billiards (Damour-Henneaux-Nicolai): AE3 for vacuum 4D gravity
   (Mixmaster, qgl_bkl.py) and E10 for 11D supergravity.  Hyperbolic means: indefinite,
   determinant < 0, exactly one negative eigenvalue.  AE3 has det -2 and E10 has det -1.

Run: python3 research/gravity/scripts/gravity_group_checks.py
"""
from fractions import Fraction as Fr
from itertools import combinations, product


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def unit(n, i, s=1):
    return tuple(Fr(s) if k == i else Fr(0) for k in range(n))


def add(a, b, s=1):
    return tuple(x + s * y for x, y in zip(a, b))


def pm_pairs(n):
    return [add(unit(n, i, s), unit(n, j, t)) for i, j in combinations(range(n), 2)
            for s, t in product((1, -1), repeat=2)]


def killing_over_trace(roots, weights, H):
    return sum(dot(a, H) ** 2 for a in roots) / sum(dot(m, H) ** 2 for m in weights)


def groups():
    # SU(2) in R^2 on the sum-zero plane
    su2_roots = [(Fr(1), Fr(-1)), (Fr(-1), Fr(1))]
    su2_wts = [(Fr(1, 2), Fr(-1, 2)), (Fr(-1, 2), Fr(1, 2))]
    # B2 = so(5): vector rep, weights +-e_i and 0
    b2_roots = pm_pairs(2) + [unit(2, i, s) for i in range(2) for s in (1, -1)]
    b2_vec = [unit(2, i, s) for i in range(2) for s in (1, -1)] + [(Fr(0), Fr(0))]
    # spinor rep of so(5) = fundamental of sp(2): weights (+-1/2, +-1/2)
    b2_spin = [(Fr(s, 2), Fr(t, 2)) for s, t in product((1, -1), repeat=2)]
    # D2 = so(4) = su(2)+su(2): vector rep (the Euclidean Lorentz group acting on the tetrad index).
    # Not simple, but both factors have the same Ricci constant, so Ric is still a scalar.
    d2_roots = pm_pairs(2)
    d2_vec = [unit(2, i, s) for i in range(2) for s in (1, -1)]
    return [
        ("SU(2)  (self-dual Spin(4))", 2, su2_roots, su2_wts, [(Fr(1), Fr(-1)), (Fr(3), Fr(-3))]),
        ("SO(4)  (Euclidean Lorentz, vector)", 4, d2_roots, d2_vec, [(Fr(1), Fr(0)), (Fr(2), Fr(7))]),
        ("SO(5)  (MacDowell-Mansouri, vector)", 5, b2_roots, b2_vec, [(Fr(1), Fr(0)), (Fr(2), Fr(7))]),
        ("Sp(2)=Spin(5) (spinor)", 4, b2_roots, b2_spin, [(Fr(1), Fr(0)), (Fr(2), Fr(7))]),
    ]


def det(M):
    M = [[Fr(x) for x in row] for row in M]
    n, d = len(M), Fr(1)
    for c in range(n):
        p = next((r for r in range(c, n) if M[r][c] != 0), None)
        if p is None:
            return Fr(0)
        if p != c:
            M[c], M[p] = M[p], M[c]
            d = -d
        d *= M[c][c]
        for r in range(c + 1, n):
            f = M[r][c] / M[c][c]
            M[r] = [x - f * y for x, y in zip(M[r], M[c])]
    return d


def inertia(M):
    """(positive, negative) counts of a symmetric rational matrix, by leading principal minors with
    Jacobi's rule (valid here because no leading minor vanishes; asserted)."""
    minors = [Fr(1)] + [det([row[:k] for row in M[:k]]) for k in range(1, len(M) + 1)]
    assert all(m != 0 for m in minors), "a leading minor vanishes"
    neg = sum(1 for a, b in zip(minors, minors[1:]) if a * b < 0)
    return len(M) - neg, neg


def cartan_from_edges(n, edges):
    A = [[2 if i == j else 0 for j in range(n)] for i in range(n)]
    for i, j, a in edges:
        A[i][j] = A[j][i] = -a
    return A


def main():
    print("Forest-gauge range of 4Y-M for the gauge groups of Euclidean first-order gravity")
    for name, N, roots, wts, Hs in groups():
        cs = {killing_over_trace(roots, wts, H) for H in Hs}
        assert len(cs) == 1
        c = cs.pop()
        ric = c / 4
        nbeta = 2 * ric / 29
        bw = N * nbeta
        print(f"  {name:38s} N={N}  c={c}  Ric={ric}  N|beta| < {nbeta}  beta_W < {bw} = {float(bw):.4f}")
    # sanity: SU(2) must reproduce the 4Y-M value beta_W < 4/29
    su2 = groups()[0]
    assert 2 * (killing_over_trace(su2[2], su2[3], su2[4][0]) / 4) / 29 * 2 == Fr(4, 29)

    print("\nBKL billiard Cartan matrices")
    ae3 = [[2, -2, 0], [-2, 2, -1], [0, -1, 2]]
    # E10: chain 0-1-...-8 with node 9 attached to node 6 (T-shape 1-2-7), Bourbaki-free labelling
    e10 = cartan_from_edges(10, [(i, i + 1, 1) for i in range(8)] + [(6, 9, 1)])
    for name, A in (("AE3 (vacuum 4D gravity, Mixmaster)", ae3), ("E10 (11D supergravity)", e10)):
        d = det(A)
        if name.startswith("AE3"):
            # leading 1x1 and 2x2 minors of AE3 are 2 and 0; reorder to (2,1,0) for Jacobi's rule
            P = [2, 1, 0]
            A2 = [[A[i][j] for j in P] for i in P]
            pos, neg = inertia(A2)
        else:
            pos, neg = inertia(A)
        print(f"  {name:38s} det={d}  inertia (+,-)=({pos},{neg})  hyperbolic-signature={neg == 1}")
    assert det(ae3) == -2 and det(e10) == -1


if __name__ == "__main__":
    main()
