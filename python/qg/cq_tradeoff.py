#!/usr/bin/env python3
"""G11. Backreaction of a qubit on a classical degree of freedom: the decoherence-diffusion trade-off.

QGL (brentharts/Quantum_Gravity_Lab) couples a classical orbit to a quantum sensor without backreaction. If the
sensor is to push on the orbit (a force F sigma_z on a classical momentum p), the joint dynamics is classical-quantum
(CQ). Oppenheim et al. (Nat. Commun. 2023) prove that any completely positive, Markovian CQ dynamics with such a
force must both decohere the qubit and make p diffuse, with
    D2 >= D1^2 / (4 D0)       (here: decoherence rate Gamma = 2 D0 ... see below for the convention used)
and that continuous measurement plus feedback saturates it. This module builds the saturating unravelling and
measures both sides.

Model. Measure sigma_z continuously with strength k (stochastic master equation, efficiency 1):
    d rho = k (sigma_z rho sigma_z - rho) dt + sqrt(k) (sigma_z rho + rho sigma_z - 2 <sigma_z> rho) dW,
    record dy = 2 sqrt(k) <sigma_z> dt + dW,
and feed the record back as the force:  dp = (F / (2 sqrt(k))) dy = F <sigma_z> dt + (F / (2 sqrt(k))) dW.
Then
    coherence decays at rate Gamma = 2 k               (|rho_01(t)| = |rho_01(0)| e^(-2 k t) on average),
    p diffuses with  Var(dp | noise) = F^2 / (4 k) dt = 2 D2 dt,  so  D2 = F^2 / (8 k),
    and the product  Gamma * D2 = F^2 / 4  does not depend on k.
Weak measurement (small k) means little decoherence and large diffusion; strong measurement the reverse. The product
is the trade-off: with Gamma = 2 D0 it reads D0 D2 = F^2 / 8 for the drift D1 = F; check the normalisation of
Oppenheim et al. before quoting their constant. What is general (their theorem) is that the product cannot be made
arbitrarily small.

Not claimed: this is a toy CQ model of the trade-off, not a model of gravity.
Run: python3 python/qg/cq_tradeoff.py
"""
from __future__ import annotations

import math

import numpy as np


def simulate(k, F=1.0, T=2.0, dt=1e-4, n_traj=400, seed=0, z0=0.0):
    """Euler-Maruyama for the SME + feedback. Start in |+> (z0 = 0) to measure the decoherence rate, or in a
    sigma_z eigenstate (z0 = +-1, which the measurement leaves fixed) to measure the diffusion of p around its
    drift. Returns (mean coherence at T, Var(p_T) / T)."""
    rng = np.random.default_rng(seed)
    steps = int(round(T / dt))
    # Bloch vector: z = <sigma_z>, c = rho_01 (real for |+> start; stays real)
    z = np.full(n_traj, float(z0))
    c = np.full(n_traj, 0.5 * math.sqrt(max(0.0, 1 - z0 * z0)))
    p = np.zeros(n_traj)
    sk = math.sqrt(k)
    for _ in range(steps):
        dW = rng.normal(0.0, math.sqrt(dt), n_traj)
        # rho = [[(1+z)/2, c], [c, (1-z)/2]]
        # dz = sqrt(k) * 2 (1 - z^2) dW   (sigma_z measurement, no Hamiltonian)
        # dc = -2 k c dt - 2 sqrt(k) z c dW
        dy = 2 * sk * z * dt + dW
        p += (F / (2 * sk)) * dy
        z_new = z + 2 * sk * (1 - z * z) * dW
        c = c - 2 * k * c * dt - 2 * sk * z * c * dW
        z = np.clip(z_new, -1.0, 1.0)
    return float(np.mean(c)), float(np.var(p) / T)


def main():
    F, T = 1.0, 2.0
    print(" k      Gamma=2k   D2 (sim)   D2 = F^2/(8k)   Gamma*D2   coherence(T) sim / theory")
    for k in (0.05, 0.2, 0.8):
        coh, _ = simulate(k, F=F, T=T, z0=0.0)
        _, varp = simulate(k, F=F, T=T, z0=1.0, seed=int(100 * k) + 1, n_traj=8000)
        D2 = varp / 2
        print(f"{k:<6} {2 * k:<10.3f} {D2:<10.4f} {F * F / (8 * k):<15.4f} {2 * k * D2:<10.4f} "
              f"{coh:.4f} / {0.5 * math.exp(-2 * k * T):.4f}")
    print("Gamma * D2 = F^2/4 = 0.25 at every measurement strength: weaker decoherence costs more diffusion.")


if __name__ == "__main__":
    main()
