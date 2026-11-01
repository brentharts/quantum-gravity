#!/usr/bin/env python3
"""G9. Quantum 6j symbols of SU(2)_k: the building blocks of Turaev-Viro (Euclidean 3D gravity with Lambda > 0).

Ponzano-Regge (sixj.py) is the q -> 1 limit; at a root of unity q = exp(2 pi i / (k + 2)) the state sum becomes the
finite Turaev-Viro invariant, whose spins are cut off at j <= k/2 and whose loop weight is the quantum dimension
[2] = 2 cos(pi/(k+2)), the Temperley-Lieb weight sqrt q_TL of Hartshorn's planar-map section (q_TL = 1, 2, 3, 4 at
k = 1, 2, 4, infinity).

Conventions: [n] = sin(pi n/(k+2)) / sin(pi/(k+2)) (real), [n]! = [1]...[n]; a triple (a, b, c) of spins is
k-admissible if it satisfies the triangle rule, a + b + c is an integer, and a + b + c <= k. The Racah-Wigner
q-6j symbol (Kirillov-Reshetikhin) is
  {j1 j2 j3; j4 j5 j6}_q = D(j1 j2 j3) D(j1 j5 j6) D(j4 j2 j6) D(j4 j5 j3)
      * sum_z (-1)^z [z+1]! / ([z - j1-j2-j3]! [z - j1-j5-j6]! [z - j4-j2-j6]! [z - j4-j5-j3]!
                               [j1+j2+j4+j5 - z]! [j2+j3+j5+j6 - z]! [j3+j1+j6+j4 - z]!),
  D(abc) = sqrt([a+b-c]! [a-b+c]! [-a+b+c]! / [a+b+c+1]!).
Checked: the q -> 1 limit against sympy's 6j; orthogonality sum_x [2x+1][2f+1] {a b x; c d f}{a b x; c d f'} = delta;
Biedenharn-Elliott; and the total quantum dimension D^2 = sum_j [2j+1]^2 = (k+2) / (2 sin^2(pi/(k+2))).
Run: python3 python/qg/quantum6j.py
"""
from __future__ import annotations

import math
from fractions import Fraction as Fr


class SU2k:
    def __init__(self, k):
        self.k = k
        self.r = k + 2

    def qn(self, n):
        return math.sin(math.pi * n / self.r) / math.sin(math.pi / self.r)

    def qfact(self, n):
        out = 1.0
        for m in range(1, int(n) + 1):
            out *= self.qn(m)
        return out

    def admissible(self, a, b, c):
        s = a + b + c
        return (abs(a - b) <= c <= a + b and s.denominator == 1 and s <= self.k)

    def delta(self, a, b, c):
        f = self.qfact
        return math.sqrt(f(a + b - c) * f(a - b + c) * f(-a + b + c) / f(a + b + c + 1))

    def sixj(self, j1, j2, j3, j4, j5, j6):
        """Standard q-6j symbol {j1 j2 j3; j4 j5 j6}: triangles (j1 j2 j3), (j1 j5 j6), (j4 j2 j6), (j4 j5 j3)."""
        j1, j2, j3, j4, j5, j6 = map(Fr, (j1, j2, j3, j4, j5, j6))
        tri = [(j1, j2, j3), (j1, j5, j6), (j4, j2, j6), (j4, j5, j3)]
        if not all(self.admissible(*t) for t in tri):
            return 0.0
        F = self.qfact
        a1, a2, a3, a4 = (sum(t) for t in tri)
        b1, b2, b3 = j1 + j2 + j4 + j5, j2 + j3 + j5 + j6, j3 + j1 + j6 + j4
        tot = 0.0
        for z in range(int(max(a1, a2, a3, a4)), int(min(b1, b2, b3)) + 1):
            tot += (-1) ** z * F(z + 1) / (F(z - a1) * F(z - a2) * F(z - a3) * F(z - a4)
                                           * F(b1 - z) * F(b2 - z) * F(b3 - z))
        return math.prod(self.delta(*t) for t in tri) * tot

    def spins(self):
        return [Fr(n, 2) for n in range(self.k + 1)]

    def orthogonality(self, a, b, c, d):
        a, b, c, d = map(Fr, (a, b, c, d))
        fs = [f for f in self.spins() if self.admissible(a, d, f) and self.admissible(c, b, f)]
        xs = [x for x in self.spins() if self.admissible(a, b, x) and self.admissible(c, d, x)]
        worst = 0.0
        for f in fs:
            for fp in fs:
                s = sum(self.qn(2 * x + 1) * self.qn(2 * f + 1) * self.sixj(a, b, x, c, d, f) * self.sixj(a, b, x, c, d, fp)
                        for x in xs)
                worst = max(worst, abs(s - (1.0 if f == fp else 0.0)))
        return worst, len(fs)

    def biedenharn_elliott(self, j1, j2, j3, j4, j5, j6, j7, j8, j9):
        js = list(map(Fr, (j1, j2, j3, j4, j5, j6, j7, j8, j9)))
        j1, j2, j3, j4, j5, j6, j7, j8, j9 = js
        S = sum(js)
        lhs = 0.0
        for x in self.spins():
            sg = (-1) ** int(S + x)
            lhs += sg * self.qn(2 * x + 1) * (self.sixj(j1, j2, x, j3, j4, j7) * self.sixj(j3, j4, x, j5, j6, j8)
                                              * self.sixj(j5, j6, x, j2, j1, j9))
        rhs = self.sixj(j7, j8, j9, j5, j1, j4) * self.sixj(j7, j8, j9, j6, j2, j3)
        return lhs - rhs, rhs

    def total_dimension_sq(self):
        return sum(self.qn(2 * j + 1) ** 2 for j in self.spins())


def classical_limit_check(k=4000):
    from sympy.physics.wigner import wigner_6j
    Q = SU2k(k)
    worst = 0.0
    for args in ((1, 1, 1, 1, 1, 1), (Fr(1, 2), Fr(1, 2), 1, Fr(1, 2), Fr(1, 2), 1), (2, 1, 2, 1, 2, 2), (3, 2, 2, 2, 3, 3)):
        worst = max(worst, abs(Q.sixj(*args) - float(wigner_6j(*args))))
    return worst


def main():
    print(f"q -> 1 (k = 4000) against sympy 6j: max difference {classical_limit_check():.2e}")
    for k in (3, 4, 5, 8):
        Q = SU2k(k)
        o = max(Q.orthogonality(*args)[0] for args in ((Fr(1, 2),) * 4, (1, 1, 1, 1), (Fr(1, 2), 1, Fr(1, 2), 1))
                if True)
        be, rhs = Q.biedenharn_elliott(1, 1, 1, 1, 1, 1, 1, 1, 1)
        D2 = Q.total_dimension_sq()
        print(f"k={k}: [2] = {Q.qn(2):.6f} (= 2cos(pi/{k + 2}) = {2 * math.cos(math.pi / (k + 2)):.6f}); orthogonality "
              f"err {o:.1e}; Biedenharn-Elliott err {abs(be):.1e} (rhs {rhs:+.5f}); D^2 = {D2:.6f} vs "
              f"{(k + 2) / (2 * math.sin(math.pi / (k + 2)) ** 2):.6f}")


if __name__ == "__main__":
    main()
