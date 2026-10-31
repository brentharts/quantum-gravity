#!/usr/bin/env python3
"""G9. SU(2) 6j symbols: exact identities and the Ponzano-Regge limit (3D gravity from SU(2) lattice BF theory).

The Ponzano-Regge state sum of Euclidean 3D gravity is SU(2) lattice BF theory: in the character expansion of the
flatness weight every representation enters with weight its dimension, and each tetrahedron of the triangulation
gives a 6j symbol.  Romanov's Z^3 forest-gauge theorems control the opposite end of the same SU(2) lattice theory
(small beta, Wilson weight).  This module checks the finite algebra of the gravity end exactly:

  * orthogonality      sum_x (2x+1)(2f+1) {a b x; c d f}{a b x; c d f'} = delta_{f f'}
  * Biedenharn-Elliott (pentagon), the identity behind the triangulation independence of the state sum
  * Racah's sum rule   sum_x (-1)^(f + g + x) (2x+1) {a b x; c d f}{a b x; d c g} = {a d f; b c g}
all in exact arithmetic (sympy), and the Ponzano-Regge asymptotics
    {6j} ~ cos(S_Regge + pi/4) / sqrt(12 pi V),   S_Regge = sum_e (j_e + 1/2) theta_e,
for a tetrahedron with edge lengths j_e + 1/2, volume V and exterior dihedral angles theta_e (Roberts 1999).

Run: python3 python/qg/sixj.py
"""
from __future__ import annotations

import itertools
import math

import numpy as np
from sympy import Rational, S, simplify
from sympy.physics.wigner import wigner_6j


def half_range(lo, hi):
    x = S(lo)
    while x <= hi:
        yield x
        x += Rational(1, 2)


def triangle_ok(a, b, c):
    return abs(a - b) <= c <= a + b and (a + b + c) % 1 == 0


def w6(a, b, c, d, e, f):
    """6j symbol {a b c; d e f}, zero unless all four triangles are admissible."""
    if not (triangle_ok(a, b, c) and triangle_ok(a, e, f) and triangle_ok(d, b, f) and triangle_ok(d, e, c)):
        return S(0)
    return wigner_6j(a, b, c, d, e, f)


def orthogonality(a, b, c, d):
    fs = [f for f in half_range(0, 4) if triangle_ok(a, d, f) and triangle_ok(b, c, f)]
    xs = [x for x in half_range(0, 6) if triangle_ok(a, b, x) and triangle_ok(c, d, x)]
    worst = S(0)
    for f, fp in itertools.product(fs, fs):
        s = sum((2 * x + 1) * (2 * f + 1) * w6(a, b, x, c, d, f) * w6(a, b, x, c, d, fp) for x in xs)
        worst = max(worst, abs(simplify(s - (1 if f == fp else 0))))
    return worst, len(fs)


def biedenharn_elliott(j1, j2, j3, j4, j5, j6, j7, j8, j9):
    """sum_x (-1)^(S+x) (2x+1) {j1 j2 x; j3 j4 j7}{j3 j4 x; j5 j6 j8}{j5 j6 x; j2 j1 j9}
         = {j7 j8 j9; j5 j1 j4}{j7 j8 j9; j6 j2 j3},  S = sum j1..j9."""
    Ssum = j1 + j2 + j3 + j4 + j5 + j6 + j7 + j8 + j9
    lhs = S(0)
    for x in half_range(0, 8):
        lhs += (-1) ** int(Ssum + x) * (2 * x + 1) * (w6(j1, j2, x, j3, j4, j7)
                                                     * w6(j3, j4, x, j5, j6, j8)
                                                     * w6(j5, j6, x, j2, j1, j9))
    rhs = w6(j7, j8, j9, j5, j1, j4) * w6(j7, j8, j9, j6, j2, j3)
    return simplify(lhs - rhs), rhs


def racah_sum_rule(a, b, c, d, f, g):
    lhs = S(0)
    for x in half_range(0, 8):
        lhs += (-1) ** int(f + g + x) * (2 * x + 1) * w6(a, b, x, c, d, f) * w6(a, b, x, d, c, g)
    return simplify(lhs - w6(a, d, f, b, c, g))


def tetra_geometry(L):
    """Edge lengths L = (l12, l13, l14, l23, l24, l34) of a tetrahedron with vertices 1..4.
    Returns (volume, exterior dihedral angles in the same edge order)."""
    l12, l13, l14, l23, l24, l34 = L
    d2 = {(0, 1): l12 ** 2, (0, 2): l13 ** 2, (0, 3): l14 ** 2, (1, 2): l23 ** 2, (1, 3): l24 ** 2, (2, 3): l34 ** 2}
    # embed by Cayley-Menger / coordinates
    p = [np.zeros(3)]
    p.append(np.array([l12, 0, 0]))
    x = (d2[(0, 2)] + d2[(0, 1)] - d2[(1, 2)]) / (2 * l12)
    p.append(np.array([x, math.sqrt(d2[(0, 2)] - x * x), 0]))
    x4 = (d2[(0, 3)] + d2[(0, 1)] - d2[(1, 3)]) / (2 * l12)
    y4 = (d2[(0, 3)] + d2[(0, 2)] - d2[(2, 3)] - 2 * x4 * p[2][0]) / (2 * p[2][1])
    p.append(np.array([x4, y4, math.sqrt(d2[(0, 3)] - x4 * x4 - y4 * y4)]))
    V = abs(np.dot(p[1], np.cross(p[2], p[3]))) / 6
    edges = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
    th = []
    for i, j in edges:
        k, l = [v for v in range(4) if v not in (i, j)]
        e = p[j] - p[i]
        e /= np.linalg.norm(e)

        def perp(v):
            w = p[v] - p[i]
            return w - np.dot(w, e) * e
        u, w = perp(k), perp(l)
        interior = math.acos(np.dot(u, w) / (np.linalg.norm(u) * np.linalg.norm(w)))
        th.append(math.pi - interior)
    return V, th


def ponzano_regge(js):
    """js = (j12, j13, j14, j23, j24, j34). The 6j symbol {j12 j13 j23; j34 j24 j14} has the triangles
    (j12 j13 j23), (j12 j24 j14), (j34 j13 j14), (j34 j24 j23)."""
    L = [j + 0.5 for j in js]
    V, th = tetra_geometry(L)
    Sr = sum(l * t for l, t in zip(L, th))
    return math.cos(Sr + math.pi / 4) / math.sqrt(12 * math.pi * V)


def main():
    for args in ((1, 1, 1, 1), (Rational(1, 2), Rational(3, 2), 1, 2), (2, 2, 2, 2)):
        w, n = orthogonality(*args)
        print(f"orthogonality {args}: {n}x{n} block, max deviation {w}")
    for args in ((1, 1, 1, 1, 1, 1, 1, 1, 1), (Rational(1, 2), Rational(1, 2), 1, Rational(1, 2), Rational(1, 2), 1, 1, 1, 1),
                 (2, 1, 1, 2, 1, 2, 1, 2, 2)):
        diff, rhs = biedenharn_elliott(*args)
        print(f"Biedenharn-Elliott {args}: lhs - rhs = {diff}  (rhs = {rhs})")
    print("Racah sum rule (1,1,1,1,1,2):", racah_sum_rule(1, 1, 1, 1, 1, 2))
    print("Ponzano-Regge, scaled tetrahedra (j12 j13 j14 j23 j24 j34) = n * base:")
    base = (2, 2, 2, 2, 2, 2)
    for n in (4, 8, 16, 24):
        js = tuple(n * b for b in base)
        exact = float(wigner_6j(js[0], js[1], js[3], js[5], js[4], js[2]))
        print(f"  n={n:3d}: exact {exact:+.6e}   PR {ponzano_regge(js):+.6e}")


if __name__ == "__main__":
    main()
