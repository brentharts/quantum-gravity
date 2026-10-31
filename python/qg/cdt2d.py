#!/usr/bin/env python3
"""G3. The transfer matrix of (1+1)-dimensional causal dynamical triangulations.

The one-step propagator of 2D CDT with a marked entrance loop (Ambjorn-Loll 1998) is
    G(x, y; g) = g x y / ((1 - g x)(1 - g x - g y)),
whose coefficient of x^l1 y^l2 is
    M(l1, l2) = g^(l1 + l2 - 1) * binom(l1 + l2 - 1, l1 - 1)          (checked below by series expansion).
l2 * M(l1, l2) is symmetric in (l1, l2), so M is similar to the symmetric matrix
    S(l1, l2) = sqrt(l2 / l1) * M(l1, l2)            (see `symmetric_transfer`),
and the transfer matrix has real spectrum.  The critical point is g_c = 1/2; with g = (1/2) exp(-a^2 Lambda) and
physical lengths L = a l, T = a t the continuum Hamiltonian has an equally spaced spectrum (Ambjorn-Loll).
Numerically the truncated transfer matrix has an exactly geometric top spectrum at every g < 1/2,
    lambda_(n+1) / lambda_n = r(g) = (1 - s) / (1 + s),   s = sqrt(1 - 4 g^2),
so the lattice gap is Delta_lat = -log r = 2 artanh(s), and with g = (1/2) exp(-a^2 Lambda), s ~ a sqrt(2 Lambda):
    Delta_lat(a) / a -> 2 sqrt(2 Lambda),   E_n - E_0 = 2 sqrt(2 Lambda) n.
(Ambjorn-Loll write 2 sqrt(Lambda') (n + 1) with Lambda' = 2 Lambda in this normalisation of g.)  A gap that scales with
the spacing, the behaviour 4Y-M's no-go theorem demands of a theory with a continuum mass gap (Hypothesis R).
This module checks it numerically. The spectrum lambda_0 r^n is positive, as reflection positivity requires; the
truncated matrix only shows this up to roundoff for its smallest eigenvalues.

Run: python3 python/qg/cdt2d.py
"""
from __future__ import annotations

import math

import numpy as np
from scipy import linalg, special


def log_M(l1, l2, g):
    n = l1 + l2 - 1
    return (n * math.log(g) + special.gammaln(n + 1) - special.gammaln(l1) - special.gammaln(l2 + 1))


def symmetric_transfer(g, lmax):
    """S = D^(1/2) M D^(-1/2) with D = diag(l): S(l1, l2) = sqrt(l1 / l2) M(l1, l2)... chosen so that
    S is symmetric: l2 M(l1, l2) = l1 M(l2, l1)  =>  sqrt(l2/l1) M(l1, l2) is symmetric."""
    l = np.arange(1, lmax + 1, dtype=float)
    L1, L2 = np.meshgrid(l, l, indexing="ij")
    n = L1 + L2 - 1
    logS = (n * math.log(g) + special.gammaln(n + 1) - special.gammaln(L1) - special.gammaln(L2 + 1)
            + 0.5 * (np.log(L2) - np.log(L1)))
    return np.exp(logS)


def series_check(g=0.3, N=8):
    """Compare M with the Taylor coefficients of G(x, y; g)."""
    import sympy as sp
    x, y = sp.symbols("x y")
    G = g * x * y / ((1 - g * x) * (1 - g * x - g * y))
    ser = sp.series(sp.series(G, x, 0, N + 1).removeO(), y, 0, N + 1).removeO()
    poly = sp.Poly(sp.expand(ser), x, y)
    worst = 0.0
    for l1 in range(1, N):
        for l2 in range(1, N):
            c = float(poly.coeff_monomial(x ** l1 * y ** l2))
            worst = max(worst, abs(c - math.exp(log_M(l1, l2, g))))
    return worst


def spectrum(a, Lam=1.0, lmax=1500, k=4):
    g = 0.5 * math.exp(-a * a * Lam)
    S = symmetric_transfer(g, lmax)
    assert np.allclose(S, S.T, rtol=1e-10, atol=0)
    w = linalg.eigh(S, eigvals_only=True, subset_by_index=[lmax - k, lmax - 1])[::-1]
    return w


def main():
    print(f"series check of M(l1, l2): max error {series_check():.2e}")
    print("a      lambda_0      E_1-E_0 (=Delta_lat/a)   (E_2-E_0)/(E_1-E_0)  (E_3-E_0)/(E_1-E_0)   min eigenvalue > 0 ?")
    for a in (0.2, 0.1, 0.05, 0.035):
        lmax = int(40 / a)
        w = spectrum(a, lmax=lmax)
        E = -np.log(w / w[0]) / a
        g = 0.5 * math.exp(-a * a)
        S = symmetric_transfer(g, min(lmax, 400))
        mn = linalg.eigh(S, eigvals_only=True, subset_by_index=[0, 0])[0]
        print(f"{a:<6} {w[0]:<13.6g} {E[1]:<24.5f} {E[2] / E[1]:<20.5f} {E[3] / E[1]:<20.5f} {mn:.3e}")
    print("continuum: E_1 - E_0 = 2 sqrt(2 Lambda) = 2.828427, ratios 2 and 3")
    print("exact ratio r(g) = (1 - s)/(1 + s), s = sqrt(1 - 4 g^2):")
    for a in (0.3, 0.1):
        g = 0.5 * math.exp(-a * a)
        w = spectrum(a, lmax=int(40 / a), k=5)
        s = math.sqrt(1 - 4 * g * g)
        print(f"  a={a}: lambda_(n+1)/lambda_n = {np.round(w[1:] / w[:-1], 10)}, r = {(1 - s) / (1 + s):.10f}")
    print("(the smallest eigenvalues of the truncated matrix are at roundoff level, consistent with the positive"
          " geometric spectrum lambda_0 r^n)")


if __name__ == "__main__":
    main()
