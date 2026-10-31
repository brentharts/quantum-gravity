#!/usr/bin/env python3
"""G10. Two-dimensional Yang-Mills on a Brownian disk and a Brownian sphere (gamma = sqrt(8/3) LQG).

Inputs, all theorems:
  * YM2 depends on a surface only through its area (Migdal; rigorous: Driver, Sengupta, Levy).
    On a disk of area A with boundary holonomy U:  Z(U, A) = sum_lam d_lam chi_lam(U) exp(-g^2 A C_lam / 2),
    normalised so that the Haar integral over U is 1.  On a sphere:  Z(S^2, A) = sum_lam d_lam^2 exp(-g^2 A C_lam / 2).
  * The free Brownian disk of perimeter L has area law with density (Bettinelli-Miermont 2017)
        f_L(A) = L^3 / sqrt(2 pi A^5) * exp(-L^2 / (2 A)),   A > 0,
    i.e. A ~ InverseGamma(shape 3/2, scale L^2/2).
  * The free Brownian sphere with cosmological constant mu has area weight A^(-7/2) e^(-mu A) (string
    susceptibility gamma_str = -1/2; Le Gall, Miermont).

Results (exact; checked below):
  (1) Laplace transform:  E_L[exp(-s A)] = (1 + L sqrt(2 s)) exp(-L sqrt(2 s)).
  (2) Wilson loop of the boundary, representation F, Haar-averaged boundary:  <W_F> = d_F exp(-g^2 A C_F / 2)
      (area law, string tension sigma_F = g^2 C_F / 2); averaged over the Brownian disk of perimeter L:
          <<W_F>>_L = d_F (1 + g L sqrt(C_F)) exp(-g L sqrt(C_F)),
      a perimeter law in the quantum boundary length with "dressed tension" g sqrt(C_F) = sqrt(2 sigma_F).
      The Haar integral of Z(U, A) over U is 1 for every A, so the YM weight does not reweight the disk
      geometry: quenched and annealed averages coincide.
  (3) Sphere, annealed: integral_0^inf A^(-7/2) e^(-mu A) Z(S^2, A) dA = Gamma(-5/2) sum_lam d_lam^2 (mu + g^2 C_lam/2)^(5/2)
      (each term; the sum needs a cutoff).  Representation lam shifts the cosmological constant by g^2 C_lam / 2;
      only the trivial representation is non-analytic at mu = 0, so the critical exponent (mu^(5/2), gamma_str = -1/2)
      is unchanged: YM2 coupled to pure 2D quantum gravity stays in the c = 0 universality class.

Not claimed: YM2 has no propagating gluons; this is a test of the coupling machinery, not 4D physics.
For SU(2), lam = spin j, d = 2j + 1, C = j (j + 1).

Run: python3 python/qg/ym2_brownian.py
"""
from __future__ import annotations

import math

import numpy as np
from scipy import integrate, special


def disk_area_density(A, L):
    return L ** 3 / np.sqrt(2 * np.pi * A ** 5) * np.exp(-L ** 2 / (2 * A))


def laplace_closed(s, L):
    z = L * math.sqrt(2 * s)
    return (1 + z) * math.exp(-z)


def laplace_numeric(s, L):
    val, _ = integrate.quad(lambda A: disk_area_density(A, L) * math.exp(-s * A), 0, np.inf, limit=400)
    return val


def su2_casimir(j):
    return j * (j + 1)


def wilson_disk_fixed_area(j, g, A):
    return (2 * j + 1) * math.exp(-g * g * A * su2_casimir(j) / 2)


def wilson_brownian_disk(j, g, L):
    c = math.sqrt(su2_casimir(j))
    return (2 * j + 1) * (1 + g * L * c) * math.exp(-g * L * c)


def wilson_brownian_disk_mc(j, g, L, n=400_000, seed=0):
    """Monte Carlo over the area law: A = (L^2/2) / Gamma(3/2, 1)."""
    rng = np.random.default_rng(seed)
    A = (L * L / 2) / rng.gamma(1.5, 1.0, size=n)
    w = (2 * j + 1) * np.exp(-g * g * A * su2_casimir(j) / 2)
    return w.mean(), w.std() / math.sqrt(n)


def sphere_term(mu, c):
    """integral_0^inf A^(-7/2) e^(-(mu + c) A) dA, analytically continued: Gamma(-5/2) (mu + c)^(5/2)."""
    return special.gamma(-2.5) * (mu + c) ** 2.5


def sphere_term_regularised_numeric(mu, c):
    """Check the continuation: subtract the first terms of the expansion at A = 0,
    integral A^(-7/2) [e^(-xA) - 1 + xA - x^2 A^2 / 2] dA = Gamma(-5/2) x^(5/2), x = mu + c."""
    x = mu + c
    f = lambda A: A ** -3.5 * (math.expm1(-x * A) + x * A - (x * A) ** 2 / 2)
    v1, _ = integrate.quad(f, 0, 1, limit=400)
    v2, _ = integrate.quad(f, 1, np.inf, limit=400)
    return v1 + v2


def main():
    L = 1.3
    print("Brownian disk area law: normalisation", round(integrate.quad(lambda A: disk_area_density(A, L), 0, np.inf)[0], 10))
    for s in (0.1, 1.0, 4.0):
        print(f"  Laplace s={s}: closed {laplace_closed(s, L):.10f}  numeric {laplace_numeric(s, L):.10f}")
    g = 1.0
    print("SU(2) boundary Wilson loop on a Brownian disk of perimeter L (g = 1):")
    for j in (0.5, 1.0, 1.5):
        for Lq in (0.5, 2.0):
            mc, err = wilson_brownian_disk_mc(j, g, Lq)
            print(f"  j={j} L={Lq}: closed {wilson_brownian_disk(j, g, Lq):.6f}  MC {mc:.6f} +- {err:.6f}")
    print("Sphere: each representation shifts mu by g^2 C/2 (continuation check):")
    for c in (0.0, 0.375, 1.0):
        print(f"  c={c}: Gamma(-5/2)(mu+c)^(5/2) = {sphere_term(0.7, c):.8f}  regularised integral {sphere_term_regularised_numeric(0.7, c):.8f}")


if __name__ == "__main__":
    main()
