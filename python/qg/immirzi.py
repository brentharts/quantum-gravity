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

import mpmath as mp

mp.mp.dps = 60


def _terms(gamma, weight, J):
    s = mp.mpf(0)
    for k in range(1, 2 * J + 1):  # j = k/2
        j = mp.mpf(k) / 2
        s += weight(j) * mp.e ** (-2 * mp.pi * gamma * mp.sqrt(j * (j + 1)))
    return s


def _tail_bound(gamma, weight_kind, J):
    """Upper bound on sum over j > J (j = k/2, k > 2J) of w(j) e^(-2 pi gamma j)."""
    q = mp.e ** (-mp.pi * gamma)  # e^(-2 pi gamma (k/2)) = q^k
    k0 = 2 * J + 1
    if weight_kind == "two":
        return 2 * q ** k0 / (1 - q)
    # weight 2j + 1 = k + 1: sum_{k >= k0} (k + 1) q^k
    return q ** k0 * (k0 + 1 - k0 * q) / (1 - q) ** 2


def f_bounds(gamma, weight_kind, J=400):
    w = (lambda j: 2) if weight_kind == "two" else (lambda j: 2 * j + 1)
    s = _terms(gamma, w, J)
    return s - 1, s - 1 + _tail_bound(gamma, weight_kind, J)


def solve(weight_kind, lo=0.05, hi=0.5, digits=40):
    lo, hi = mp.mpf(lo), mp.mpf(hi)
    for _ in range(200):
        mid = (lo + hi) / 2
        fl, fu = f_bounds(mid, weight_kind)
        if fl > 0:
            lo = mid
        elif fu < 0:
            hi = mid
        else:
            break
        if hi - lo < mp.mpf(10) ** (-digits):
            break
    # certify: f(lo) > 0 > f(hi) including the tail
    assert f_bounds(lo, weight_kind)[0] > 0 and f_bounds(hi, weight_kind)[1] < 0
    return lo, hi


def spin_half():
    return mp.log(2) / (mp.pi * mp.sqrt(3))


def main():
    print(f"(a) spin-1/2 only:            gamma = ln2/(pi sqrt3) = {mp.nstr(spin_half(), 20)}")
    lo, hi = solve("two")
    print(f"(b) all spins, 2 states:      gamma in [{mp.nstr(lo, 25)}, {mp.nstr(hi, 25)}]")
    lo2, hi2 = solve("dim")
    print(f"(c) all spins, 2j+1 states:   gamma in [{mp.nstr(lo2, 25)}, {mp.nstr(hi2, 25)}]")
    print("Spin-1/2 counting with the bound from (b): each puncture of spin j contributes area sqrt(j(j+1)) and")
    print("at most 2 states; allowing larger spins can only raise gamma, since more states fit in a given area.")


if __name__ == "__main__":
    main()
