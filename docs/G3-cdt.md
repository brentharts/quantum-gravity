# G3. Causal dynamical triangulations through the transfer matrix

## 2D: a calibration case (`python/qg/cdt2d.py`)

The 2D CDT one-step propagator with a marked entrance loop is G(x, y; g) = gxy/((1 − gx)(1 − gx − gy)) (Ambjørn–Loll).
Its coefficients give the transfer matrix

  M(l₁, l₂) = g^{l₁+l₂−1} C(l₁+l₂−1, l₁−1),

which is checked against the series expansion. l₂M(l₁, l₂) is symmetric, so M is similar to a symmetric matrix.

**Found numerically (to 10 digits, at every g tested):** the top of the spectrum is exactly geometric,

  λ_{n+1}/λ_n = r(g) = (1 − s)/(1 + s),   s = √(1 − 4g²).

So the lattice gap is Δ_lat = 2 artanh s. With g = ½e^{−a²Λ}, Δ_lat(a)/a → 2√(2Λ) and E_n − E_0 = 2√(2Λ)·n.
This is the equally spaced Ambjørn–Loll spectrum. Their 2√Λ′ corresponds to Λ′ = 2Λ in this normalisation of g.

This is the behaviour 4Y-M's no-go theorem demands of a theory with a continuum gap: a lattice gap of order a. It is
the gravitational counterpart of Hypothesis R holding in a solvable model.

**To prove:** the geometric spectrum for the infinite matrix. The generating function iterates a Möbius map, so a
proof via its fixed points is expected.

## 3+1: what can be proved

In the region of large bare cosmological constant κ₄ (the analogue of strong coupling), the spatial-volume process
of CDT is dominated by small slices. A Dobrushin argument for the slice-volume chain (each slice conditioned on its
two neighbours) should give uniqueness and a gap there, with the transfer-matrix positivity of CDT providing the
spectral interpretation.
- Combined with `NoGraviton.lean`, this excludes the region from being gravitational.
- Status: open. The first step is a bound on the number of 4D CDT slabs between given 3-slices, which is
  exponential in the slice volumes (Ambjørn–Jurkiewicz–Loll), with explicit constants.
