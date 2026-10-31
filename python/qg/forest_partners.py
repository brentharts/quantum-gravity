#!/usr/bin/env python3
"""G4. Dobrushin partner counts of gauge-fixing forests on lattices and polytopes.

For a 2-complex (links, plaquettes) and a set F of fixed links forming a forest, the partner count
of a free link e is

    P(e) = sum over plaquettes p containing e of (#free links of p) - 1,

and the single-link SU(2) Dobrushin argument of 4Y-M gives uniqueness and decay for
beta_W < 4 / max_e P(e) (row sum |beta| P(e), beta_W = 4 beta).  QuantumGravity/ForestRowSum.lean
records the counting identities; this module searches for good forests.

Complexes:
  * Z^d (d = 3, 4), as a periodic torus of side L, with "parent map" forests: each site x takes the
    link from x - e_{s(x)} (one incoming fixed link per site).  Such a set is always a forest in Z^d
    (following parents strictly decreases the coordinate sum).  The 4Y-M pattern (one *outgoing*
    link per site, `GaugeFix.lean`) is the mirror image and is included as `z4_4ym_pattern`.
  * the boundary of the 5-simplex (minimal triangulation of S^4) and the 600-cell (a regular
    triangulation of S^3 by 600 tetrahedra), with plaquettes = triangles; forests are acyclic sets
    of edges of the finite graph.

Run: python3 python/qg/forest_partners.py
"""
from __future__ import annotations

import itertools
import math
import random
from typing import Dict, List, Sequence, Tuple

# ----------------------------------------------------------------------------------------------
# generic counting


def partner_counts(plaqs: Sequence[Sequence[int]], fixed: set, nlinks: int) -> List[int]:
    """P(e) for every free link e (fixed links get -1)."""
    P = [0] * nlinks
    for p in plaqs:
        free = [f for f in p if f not in fixed]
        for e in free:
            P[e] += len(free) - 1
    for e in fixed:
        P[e] = -1
    return P


def threshold_su2(Pmax: int) -> float:
    return 4.0 / Pmax if Pmax > 0 else math.inf


# ----------------------------------------------------------------------------------------------
# Z^d tori


def zd_complex(d: int, L: int):
    sites = list(itertools.product(range(L), repeat=d))
    idx = {s: i for i, s in enumerate(sites)}

    def link(x, mu):
        return idx[x] * d + mu

    def shift(x, mu, k=1):
        y = list(x)
        y[mu] = (y[mu] + k) % L
        return tuple(y)

    plaqs = []
    for x in sites:
        for mu, nu in itertools.combinations(range(d), 2):
            plaqs.append([link(x, mu), link(shift(x, mu), nu), link(shift(x, nu), mu), link(x, nu)])
    return sites, idx, link, shift, plaqs


_ZD_CACHE: Dict[Tuple[int, int], tuple] = {}


def zd_parent_forest(d: int, L: int, s: Dict[Tuple[int, ...], int], period: int):
    """Fixed links: for each site x, the link from x - e_{s(x mod period)} to x.
    Returns (max partners, number of free links attaining it)."""
    if (d, L) not in _ZD_CACHE:
        sites, idx, link, shift, plaqs = zd_complex(d, L)
        parents = [[link(shift(x, mu, -1), mu) for mu in range(d)] for x in sites]
        _ZD_CACHE[(d, L)] = (sites, plaqs, parents)
    sites, plaqs, parents = _ZD_CACHE[(d, L)]
    fixed = {parents[i][s[tuple(c % period for c in x)]] for i, x in enumerate(sites)}
    P = partner_counts(plaqs, fixed, len(sites) * d)
    m = max(P)
    return m, P.count(m), fixed


def z4_4ym_pattern():
    """The pattern of 4Y-M GaugeFix.lean: at site x (parities), fix the forward link in direction
    table[x0 + 2 x1 + 4 x2 + 8 x3]."""
    table = [0, 0, 2, 3, 3, 1, 2, 1, 1, 2, 1, 3, 3, 2, 0, 0]
    d, L = 4, 4
    sites, idx, link, shift, plaqs = zd_complex(d, L)
    fixed = set()
    for x in sites:
        par = sum((x[m] % 2) << m for m in range(4))
        fixed.add(link(x, table[par]))
    P = partner_counts(plaqs, fixed, len(sites) * d)
    per_plaq = {sum(1 for f in p if f in fixed) for p in plaqs}
    return max(P), min(q for q in P if q >= 0), per_plaq


def zd_search(d: int, period: int, iters: int = 20000, seed: int = 1, exhaustive_limit: int = 10 ** 5,
              restarts: int = 4):
    """Best max-partner count over parent-map forests of the given period (exhaustive if small,
    otherwise annealing on (max, multiplicity of the max) with restarts). Returns (best, pattern, how)."""
    cells = list(itertools.product(range(period), repeat=d))
    L = period if period >= 3 else 4
    total = d ** len(cells)
    if total <= exhaustive_limit:
        best, best_s = None, None
        for ch in itertools.product(range(d), repeat=len(cells)):
            s = dict(zip(cells, ch))
            m, k, _ = zd_parent_forest(d, L, s, period)
            if best is None or (m, k) < best:
                best, best_s = (m, k), s
        return best[0], best_s, "exhaustive"
    best, best_s = None, None
    for r in range(restarts):
        rng = random.Random(seed + r)
        s = {c: rng.randrange(d) for c in cells}
        m, k, _ = zd_parent_forest(d, L, s, period)
        cur = (m, k)
        if best is None or cur < best:
            best, best_s = cur, dict(s)
        T = 3.0
        for _ in range(iters // restarts):
            c = rng.choice(cells)
            old = s[c]
            s[c] = rng.randrange(d)
            m, k, _ = zd_parent_forest(d, L, s, period)
            dl = (m - cur[0]) * 100 + (k - cur[1])
            if dl <= 0 or rng.random() < math.exp(-dl / T):
                cur = (m, k)
                if cur < best:
                    best, best_s = cur, dict(s)
            else:
                s[c] = old
            T = max(0.05, T * 0.9995)
    return best[0], best_s, "annealed"


# ----------------------------------------------------------------------------------------------
# finite simplicial complexes


def boundary_simplex(n: int):
    """Boundary of the n-simplex: vertices 0..n, all edges and triangles."""
    V = list(range(n + 1))
    edges = list(itertools.combinations(V, 2))
    tris = list(itertools.combinations(V, 3))
    return V, edges, tris


def cell600():
    """Vertices of the 600-cell (unit quaternions of the binary icosahedral group), its 720 edges and
    1200 triangles."""
    phi = (1 + 5 ** 0.5) / 2
    pts = set()
    for s in itertools.product((1, -1), repeat=4):
        pts.add(tuple(0.5 * x for x in s))
    for i in range(4):
        for s in (1, -1):
            v = [0.0] * 4
            v[i] = float(s)
            pts.add(tuple(v))
    base = (phi / 2, 0.5, 1 / (2 * phi), 0.0)
    even = [p for p in itertools.permutations(range(4)) if _parity(p) == 0]
    for p in even:
        for s in itertools.product((1, -1), repeat=3):
            v = [0.0] * 4
            vals = [base[0] * s[0], base[1] * s[1], base[2] * s[2], 0.0]
            for k in range(4):
                v[p[k]] = vals[k]
            pts.add(tuple(round(x, 12) + 0.0 for x in v))
    V = sorted(pts)
    assert len(V) == 120, len(V)
    target = phi / 2
    adj = {i: set() for i in range(120)}
    edges = []
    for i, j in itertools.combinations(range(120), 2):
        if abs(sum(a * b for a, b in zip(V[i], V[j])) - target) < 1e-9:
            edges.append((i, j))
            adj[i].add(j)
            adj[j].add(i)
    tris = [(i, j, k) for i, j in edges for k in adj[i] & adj[j] if k > j]
    assert len(edges) == 720 and len(tris) == 1200, (len(edges), len(tris))
    return V, edges, tris


def _parity(p):
    inv = sum(1 for i in range(len(p)) for j in range(i + 1, len(p)) if p[i] > p[j])
    return inv % 2


class DSU:
    def __init__(self, n):
        self.p = list(range(n))

    def find(self, x):
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]
            x = self.p[x]
        return x

    def union(self, a, b):
        a, b = self.find(a), self.find(b)
        if a == b:
            return False
        self.p[a] = b
        return True


def is_forest(nv, edges, F):
    d = DSU(nv)
    return all(d.union(*edges[e]) for e in F)


def greedy_cover_forest(V, edges, plaqs, seeds=40):
    """Grow a forest greedily, each step adding the edge (keeping acyclicity) that gives a fixed
    neighbour to the most free edges that have none yet; best of several random tie-breaks."""
    nbr = [set() for _ in edges]
    for p in plaqs:
        for e in p:
            nbr[e] |= set(p) - {e}
    best = None
    for seed in range(seeds):
        rng = random.Random(seed)
        d, F, cov = DSU(len(V)), set(), [0] * len(edges)
        while True:
            cands = [(sum(1 for f in nbr[e] if f not in F and cov[f] == 0), rng.random(), e)
                     for e in range(len(edges))
                     if e not in F and d.find(edges[e][0]) != d.find(edges[e][1])]
            if not cands:
                break
            _, _, e = max(cands)
            d.union(*edges[e])
            F.add(e)
            for f in nbr[e]:
                cov[f] += 1
        P = partner_counts(plaqs, F, len(edges))
        key = (max(P), P.count(max(P)))
        if best is None or key < best[0]:
            best = (key, set(F))
    return best


def triangle_lower_bound(nV, nE, k):
    """For a closed complex of triangles with every edge in exactly k triangles and two edges sharing
    at most one triangle: P(e) = 2k - (#fixed edges sharing a triangle with e), each fixed edge is a
    neighbour of 2k edges, and a forest has at most nV - 1 edges, so
        max_e P(e) >= 2k - floor(2k (nV - 1) / (nE - nV + 1))."""
    return 2 * k - (2 * k * (nV - 1)) // (nE - nV + 1)


def simplicial_search(V, edges, tris, iters=20000, seed=0):
    """Minimise max partners over forests F by annealing (add/remove/swap one edge)."""
    eidx = {e: i for i, e in enumerate(edges)}
    plaqs = [[eidx[(a, b)], eidx[(a, c)], eidx[(b, c)]] for a, b, c in tris]
    nE, nV = len(edges), len(V)
    rng = random.Random(seed)

    def score(F):
        P = partner_counts(plaqs, F, nE)
        m = max(P)
        return (m, sum(1 for q in P if q == m))

    # start: greedy spanning tree
    d = DSU(nV)
    F = set()
    order = list(range(nE))
    rng.shuffle(order)
    for e in order:
        if d.union(*edges[e]):
            F.add(e)
    cur = score(F)
    best, bestF = cur, set(F)
    T = 2.0
    for _ in range(iters):
        G = set(F)
        move = rng.random()
        if move < 0.4 and G:
            G.remove(rng.choice(sorted(G)))
        else:
            e = rng.randrange(nE)
            if e in G:
                continue
            G.add(e)
            if not is_forest(nV, edges, G):
                # swap: drop a random edge of the cycle-closing set
                G.remove(rng.choice(sorted(G - {e})))
                if not is_forest(nV, edges, G):
                    continue
        s = score(G)
        dlt = (s[0] - cur[0]) * 1000 + (s[1] - cur[1])
        if dlt <= 0 or rng.random() < math.exp(-dlt / max(T, 1e-3)):
            F, cur = G, s
            if s < best:
                best, bestF = s, set(G)
        T *= 0.9997
    no_fix = max(partner_counts(plaqs, set(), nE))
    (gm, gk), gF = greedy_cover_forest(V, edges, plaqs)
    if (gm, gk) < best:
        best, bestF = (gm, gk), gF
    return best[0], no_fix, len(bestF), bestF


# period-3 forest of Romanov's 3D paper (lean/ForestGauge3.lean, `pat3`; index x0*9 + x1*3 + x2)
PAT3_ROMANOV = [2, 1, 0, 1, 0, 2, 1, 2, 0, 1, 0, 2, 1, 2, 0, 2, 1, 0, 1, 2, 0, 2, 1, 0, 1, 0, 2]


def z3_romanov_pattern():
    cells = list(itertools.product(range(3), repeat=3))
    s = {c: PAT3_ROMANOV[c[0] * 9 + c[1] * 3 + c[2]] for c in cells}
    m, k, _ = zd_parent_forest(3, 3, s, 3)
    return m, k


def main():
    m, mn, per = z4_4ym_pattern()
    print(f"Z^4, 4Y-M straight-line forest: max partners {m} (min {mn}), fixed links per plaquette {per}, "
          f"SU(2) beta_W < {4}/{m} = {threshold_su2(m):.4f}")
    m, k = z3_romanov_pattern()
    print(f"Z^3, period-3 forest of the 3D paper: max partners {m} ({k} free links per 3^3 cell attain it), "
          f"beta_W < 4/{m} = {threshold_su2(m):.4f}")
    for d, per in ((3, 2), (3, 3)):
        b, s, how = zd_search(d, per)
        print(f"Z^{d}, parent-map forests of period {per} ({how}): best max partners {b}, "
              f"beta_W < 4/{b} = {threshold_su2(b):.4f}")
    for name, cx in (("boundary of 5-simplex (S^4)", boundary_simplex(5)),
                     ("boundary of 4-simplex (S^3)", boundary_simplex(4)),
                     ("600-cell (S^3)", cell600())):
        V, E, Tr = cx
        best, nofix, size, _ = simplicial_search(V, E, Tr, iters=6000 if len(E) > 100 else 4000)
        k = nofix // 2
        lb = triangle_lower_bound(len(V), len(E), k)
        print(f"{name}: {len(V)} vertices, {len(E)} edges, {len(Tr)} triangles, {k} triangles per edge; "
              f"max partners without fixing {nofix}, best forest found {best} ({size} fixed links), "
              f"counting lower bound {lb}{' (optimal)' if lb == best else ''}; beta_W < 4/{best} = {threshold_su2(best):.4f}")


if __name__ == "__main__":
    main()
