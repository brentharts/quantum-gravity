#!/usr/bin/env python3
"""G13. The Immirzi parameter from counting punctures, rederived (not quoted).

Area spectrum of loop quantum gravity: a puncture of spin j contributes a_j = 8 pi gamma sqrt(j(j+1)) l_P^2.
Black-hole entropy S = ln(number of spin-network states on a horizon of area A) = A/4 (l_P = 1) fixes gamma.

  * spin-1/2 punctures only:  N punctures, 2^N states (each puncture carries a 2-dim space, gauge constraint ignored at
    leading order), area 4 sqrt(3) pi gamma N, so S = N ln 2 = A/4  =>  gamma = ln 2 / (pi sqrt 3) = 0.12738.
  * all spins j = 1/2, 1, 3/2, ... with degeneracy 2j+1 per puncture: the exponential growth rate of the number of
    states at fixed area is lambda, the root of     sum_j (2j+1) exp(-lambda a_j / (8 pi gamma)... ) = 1.
    Writing the area as A = 8 pi gamma sum_i sqrt(j_i(j_i+1)) the count is a renewal problem; the number of states of
    area <= A grows as exp(lambda A / (8 pi gamma)) with lambda the root of  sum_j (2j+1) exp(-lambda sqrt(j(j+1))) = 1.
    S = A/4 then needs  lambda/(8 pi gamma) = 1/4,  i.e.  gamma = lambda/(2 pi).   (value 0.2741, Ghosh-Mitra,
    gr-qc/0411035 eq. (7)).  Counting only the projections m = +-j (degeneracy 2 instead of 2j+1) gives the Domagala-Lewandowski
    value 0.2375, and the spin-1/2 only count gives 0.1274.  The conventions differ in what is counted, not in the area spectrum.

The renewal root is computed here to 15 digits, and the exponential growth rate is checked against a direct count of
sequences of punctures with total area <= A.

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
