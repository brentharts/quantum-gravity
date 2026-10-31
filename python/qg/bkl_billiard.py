#!/usr/bin/env python3
"""G7 / G12. The BKL map as a continued-fraction (billiard) map, and its era statistics.

The Kasner exponents of a Mixmaster epoch are parametrised by u >= 1:
    p1 = -u / (1 + u + u^2),  p2 = (1 + u) / (1 + u + u^2),  p3 = u (1 + u) / (1 + u + u^2).
The BKL map (as in QGL's `qgl_bkl.bkl_u_map`) is
    u -> u - 1        if u >= 2   (next epoch of the same era),
    u -> 1 / (u - 1)  if 1 < u < 2 (start of a new era).
Writing u_0 = k_0 + x_0 at the start of an era, the era has k_0 epochs and the next era starts at 1/x_0: the era
lengths are the continued-fraction digits of u_0, and the fractional parts evolve by the Gauss map x -> {1/x}.
The Gauss map preserves the measure dx / ((1 + x) ln 2), so for almost every u_0 the era lengths have the
Gauss-Kuzmin law
    P(k) = -log2(1 - 1/(k + 1)^2).
Geometrically this is a billiard in the fundamental domain of PGL(2, Z), the Weyl group of the hyperbolic Kac-Moody
algebra AE3 (Damour-Henneaux-Nicolai); `QuantumGravity/Billiards.lean` checks the AE3 Cartan matrix.

Exact Kasner identities (sum p = sum p^2 = 1) and the epoch/era bookkeeping are checked in
`python/tests/test_bkl.py`.  Run: python3 python/qg/bkl_billiard.py
"""
from __future__ import annotations

import math
from fractions import Fraction

import mpmath


def kasner(u):
    d = 1 + u + u * u
    return (-u / d, (1 + u) / d, u * (1 + u) / d)


def bkl_u_map(u):
    return u - 1 if u >= 2 else 1 / (u - 1)


def era_lengths(u0, n_eras, dps=None):
    """Era lengths by iterating the BKL map itself (not the continued fraction), in high precision."""
    if dps is None:
        dps = max(50, 3 * n_eras)
    with mpmath.workdps(dps):
        u = mpmath.mpf(u0) if not isinstance(u0, mpmath.mpf) else u0
        out, k = [], 0
        while len(out) < n_eras:
            k += 1
            if u < 2:
                out.append(k)
                k = 0
            u = bkl_u_map(u)
        return out


def cf_digits(x, n, dps=None):
    if dps is None:
        dps = max(50, 3 * n)
    with mpmath.workdps(dps):
        x = mpmath.mpf(x)
        out = []
        for _ in range(n):
            a = int(mpmath.floor(x))
            out.append(a)
            x = 1 / (x - a)
        return out


def gauss_kuzmin(k):
    return -math.log2(1 - 1 / (k + 1) ** 2)


def main():
    p = kasner(Fraction(7, 3))
    print("Kasner u=7/3:", p, " sum p =", sum(p), " sum p^2 =", sum(q * q for q in p))
    with mpmath.workdps(4000):
        u0 = mpmath.pi + 1  # a generic (non-quadratic) starting value
        eras = era_lengths(u0, 1000, dps=4000)
        cf = cf_digits(u0, 1000, dps=4000)
    print("era lengths = continued-fraction digits of u0:", eras == cf, " first:", eras[:12])
    n = len(eras)
    print(" k  observed  Gauss-Kuzmin")
    for k in range(1, 7):
        print(f"{k:2d}  {eras.count(k) / n:.4f}    {gauss_kuzmin(k):.4f}")


if __name__ == "__main__":
    main()
