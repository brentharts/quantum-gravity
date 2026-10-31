#!/usr/bin/env python3
"""G8. Strong-coupling character coefficients of lattice Lorentz gauge theory (Euclidean SO(4)) and SU(2).

Normalisation of 4Y-M: weight exp(N beta Re Tr_N U_p), beta_W = N^2 beta.
  * SU(2), N = 2:  weight exp(beta_W cos theta),  U ~ diag(e^{i theta}, e^{-i theta}).
  * SO(4) = (SU(2) x SU(2)) / Z2 acting on the tetrad index, N = 4:  Tr_4 U = chi_{1/2}(A) chi_{1/2}(B)
    = 4 cos t1 cos t2, so the weight is exp(beta_W cos t1 cos t2).
The fundamental character coefficient a_F(beta_W) = <Tr_N U>_1 / N under the one-plaquette measure governs the
strong-coupling expansion: the leading term of a Wilson loop of area A is a_F^A, so sigma_F = -log a_F is the
leading-order string tension. -1 lies in the centre of SO(4) and acts as -1 on the vector representation, so
vector charges carry a nontrivial centre charge and are confined at strong coupling (area law; Osterwalder-Seiler).

For lattice gravity in first-order form this is the frozen-tetrad Lorentz sector, whose plaquette action generates
R_{mu nu} R^{mu nu} (Zubkov; Mannion-Taylor), i.e. the curvature-squared sector of quadratic gravity.  The 4Y-M
theorems (reflection positivity, uniqueness, transfer-matrix gap for beta_W < 4/29) apply to it as stated.

Leading orders (checked below): SU(2) a_F = I_2(beta_W)/I_1(beta_W) = beta_W/4 + O(beta_W^3);
SO(4) a_F = beta_W/16 + O(beta_W^3).

Not claimed: a rigorous area-law constant (that needs the cluster expansion with explicit bounds; see docs).
Run: python3 python/qg/lorentz_strong.py
"""
from __future__ import annotations

import math

from scipy import integrate, special


def su2_aF(bw):
    return special.iv(2, bw) / special.iv(1, bw)


def _haar(t):
    return (2 / math.pi) * math.sin(t) ** 2


def su2_aF_numeric(bw):
    num = integrate.quad(lambda t: _haar(t) * 2 * math.cos(t) * math.exp(bw * math.cos(t)), 0, math.pi)[0]
    den = integrate.quad(lambda t: _haar(t) * math.exp(bw * math.cos(t)), 0, math.pi)[0]
    return num / den / 2


def so4_aF(bw):
    f = lambda t2, t1: _haar(t1) * _haar(t2) * math.exp(bw * math.cos(t1) * math.cos(t2))
    g = lambda t2, t1: f(t2, t1) * 4 * math.cos(t1) * math.cos(t2)
    num = integrate.dblquad(g, 0, math.pi, 0, math.pi, epsabs=1e-13)[0]
    den = integrate.dblquad(f, 0, math.pi, 0, math.pi, epsabs=1e-13)[0]
    return num / den / 4


def main():
    print(" beta_W     SU(2) a_F   (Bessel)    sigma=-log a   |  SO(4) a_F    sigma=-log a   a_F / (beta_W/16)")
    for bw in (0.01, 0.05, 0.1, 4 / 29, 0.3):
        a2, a2n = su2_aF(bw), su2_aF_numeric(bw)
        a4 = so4_aF(bw)
        print(f" {bw:<9.5f}  {a2n:<11.6g} ({a2:<9.6g})  {-math.log(a2):<13.5f}  |  {a4:<11.6g}  {-math.log(a4):<13.5f}  {a4 / (bw / 16):.6f}")
    print("at the 4Y-M edge beta_W = 4/29 the leading-order SO(4) string tension is",
          f"{-math.log(so4_aF(4 / 29)):.4f} (lattice units)")


if __name__ == "__main__":
    main()
