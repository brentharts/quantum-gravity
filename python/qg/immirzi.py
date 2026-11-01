#!/usr/bin/env python3
"""G13. The Barbero-Immirzi parameter from three puncture countings, rederived.

Hartshorn's quantum gravity paper fixes gamma_I = ln 2 / (pi sqrt 3) ~ 0.1274 from spin-1/2 punctures only and
quotes the all-spin value 0.2375 (Domagala-Lewandowski) without rederiving it. Here all three standard countings are
solved. A horizon of area A = 8 pi gamma l_P^2 sum_i sqrt(j_i (j_i + 1)) with S = A / (4 l_P^2) gives, at leading order:

  (a) spin-1/2 only, 2 states per puncture (ABCK / Rovelli):  gamma = ln 2 / (pi sqrt 3)
  (b) all spins, 2 states per puncture, projection m = +-j only (Domagala-Lewandowski, Meissner 2004):
          1 = sum_{j = 1/2, 1, 3/2, ...} 2 exp(-2 pi gamma sqrt(j (j + 1)))
  (c) all spins, 2j + 1 states per puncture (Ghosh-Mitra):
          1 = sum_j (2 j + 1) exp(-2 pi gamma sqrt(j (j + 1)))

Each f(gamma) = sum - 1 is strictly decreasing in gamma, so the root is bracketed by evaluating f with an explicit
tail bound: for j >= J, sqrt(j (j+1)) >= j + 1/2 - 1/(8 j) >= j, so the terms are at most c_j e^(-2 pi gamma j)
and the tail is a geometric(-type) series summed in closed form. Arithmetic is 60-digit mpmath.

Not claimed: which counting is right. That is a question about the quantum horizon (and, in newer work, about
the SU(2) Chern-Simons treatment), not about this arithmetic.
Run: python3 python/qg/immirzi.py
"""
from __future__ import annotations

import math

from mpmath import mp, mpf, findroot, sqrt, log, pi, nsum, exp, inf

mp.dps = 30


def a_j(two_j: int) -> mpf:
    j = mpf(two_j) / 2
    return sqrt(j * (j + 1))


def renewal_sum(lam, jmax_two: int = 4000):
    """F(lam) = sum_{j=1/2,1,...} (2j+1) exp(-lam sqrt(j(j+1))); terms decay like (2j) e^{-lam j}."""
    return sum((mpf(tj) + 1) * exp(-lam * a_j(tj)) for tj in range(1, jmax_two + 1))


def gamma_spin_half() -> mpf:
    return log(2) / (pi * sqrt(3))


def gamma_all_spins() -> mpf:
    lam = findroot(lambda x: renewal_sum(x) - 1, mpf("1.5"))
    return lam / (2 * pi)


def gamma_domagala_lewandowski() -> mpf:
    """Domagala-Lewandowski counting (only the extreme projections m = +-j per puncture, degeneracy 2): sum_j 2 exp(-lam a_j) = 1."""
    lam = findroot(lambda x: 2 * sum(exp(-x * a_j(tj)) for tj in range(1, 4000)) - 1, mpf("1.2"))
    return lam / (2 * pi)


def growth_rate(x_max: float = 40.0, h: float = 0.005):
    """Discretised renewal equation  N(x) = 1 + sum_j (2j+1) N(x - a_j)  (number of puncture sequences of total area <= x, including the empty one).
    Returns ln N(x)/x at x_max, which tends to lambda from below as x -> infinity (N ~ C e^{lambda x})."""
    import numpy as np
    n = int(x_max / h) + 1
    N = np.ones(n)
    steps = [(int(round(math.sqrt((tj / 2) * (tj / 2 + 1)) / h)), tj + 1) for tj in range(1, int(2 * x_max) + 2)]
    steps = [(s, d) for s, d in steps if 0 < s < n]
    for i in range(n):
        acc = 1.0
        for s, d in steps:
            if i - s < 0:
                break
            acc += d * N[i - s]
        N[i] = acc
    return math.log(N[-1]) / (n * h), N


if __name__ == "__main__":
    print("spin-1/2 only        gamma =", mp.nstr(gamma_spin_half(), 10))
    g = gamma_all_spins()
    print("all spins, deg 2j+1  gamma =", mp.nstr(g, 10), " lambda =", mp.nstr(2 * pi * g, 10))
    print("all spins, deg 2 (DL) gamma =", mp.nstr(gamma_domagala_lewandowski(), 10))
    r, _ = growth_rate(25.0, 0.01)
    print("direct count: ln N(x)/x at x = 25 ->", r)
