#!/usr/bin/env python3
"""Exact certificate for lower bounds on the growth rates of distributive lattices.

Input: the automaton written by `src/bounded W file` (lattices all of whose rank layers have at
most W elements; state 0 is the empty frontier; a lattice with n elements is a closed walk at
state 0 whose entered states have total weight n - 1; it is vertically indecomposable iff the
walk does not pass through state 0 in between).

Claim checked, for a rational L = p/q:
  there is a set C of states, strongly connected, and a vector U of positive integers on C with
      sum_{t in C} #(s -> t) * (q/p)^weight(t) * U[t]  >=  U[s]      for all s in C.      (*)
By the Collatz-Wielandt inequality the matrix M with entries #(s->t) (q/p)^weight(t) on C has
spectral radius >= 1; as M is irreducible, the generating function of the closed walks at a
state of C diverges at q/p.  Hence the number of these walks of weight n has exponential growth
rate at least p/q.
  mode "all": C is the strong component of state 0; closed walks at 0 are lattices, so
              lim d(n)^(1/n) >= p/q.
  mode "vi" : C is a strong component of the automaton without state 0 that is reachable from 0
              and from which 0 is reachable; so limsup d_vi(n)^(1/n) >= p/q.
The vector U is found in floating point and then (*) and the connectivity are verified with
integer arithmetic only.

usage: bounded_certificate.py automaton.txt vi|all L      e.g.  ... vi 1.7265363
"""
import sys
from fractions import Fraction
import numpy as np
sys.path.insert(0, __import__('os').path.dirname(__file__))
from bounded_growth import read, spectral
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import connected_components

path, mode, L = sys.argv[1], sys.argv[2], Fraction(sys.argv[3])
n, wt, rows, cols = read(path)
A = csr_matrix((np.ones(len(rows)), (rows, cols)), shape=(n, n))
_, lab = connected_components(A, directed=True, connection='strong')
rec = lab == lab[0]
if mode == 'all':
    keep = rec
else:
    nz = np.ones(n, bool); nz[0] = False
    sel = nz[rows] & nz[cols] & rec[rows] & rec[cols]
    B = csr_matrix((np.ones(sel.sum()), (rows[sel], cols[sel])), shape=(n, n))
    _, lab2 = connected_components(B, directed=True, connection='strong')
    big = np.argmax(np.bincount(lab2[rec & nz])); keep = (lab2 == big) & rec & nz
x = float(1 / L)
lam, u = spectral(n, wt, rows, cols, x, keep)
print(f'floating point: spectral radius at x = 1/L is {lam:.12f} (must exceed 1)')
# ---- exact part ----
C = [i for i in range(n) if keep[i]]; inC = set(C)
succ = {s: [] for s in C}; pred = {s: [] for s in C}; out0 = False; in0 = False
for s, t in zip(rows.tolist(), cols.tolist()):
    if s in inC and t in inC: succ[s].append(t); pred[t].append(s)
    if s == 0 and t in inC: in0 = True
    if t == 0 and s in inC: out0 = True
def reach(start, nb):
    seen = {start}; st = [start]
    while st:
        v = st.pop()
        for w in nb[v]:
            if w not in seen: seen.add(w); st.append(w)
    return seen
s0 = C[0]
assert reach(s0, succ) == inC and reach(s0, pred) == inC, 'C is not strongly connected'
if mode == 'vi': assert 0 not in inC and in0 and out0, 'C must avoid state 0 and be linked to it'
else: assert 0 in inC
# period: gcd of the weights of the closed walks in C (weight of a walk = sum of weights of entered states).
# With potentials d from a search tree, it is the gcd of d[s] + weight(t) - d[t] over all edges s -> t.
from math import gcd
d = {s0: 0}; st = [s0]
while st:
    v = st.pop()
    for w2 in succ[v]:
        if w2 not in d: d[w2] = d[v] + int(wt[w2]); st.append(w2)
per = 0
for s in C:
    for t in succ[s]: per = gcd(per, abs(d[s] + int(wt[t]) - d[t]))
print(f'period of C: {per}' + (' (aperiodic: closed walks of every large weight exist, so the bound holds as Omega(L1^n) for every L1 < L)' if per == 1 else ''))
# integer vector: scale the floats, round down, keep at least 1
scale = 2 ** 200 / float(u[keep].min())
U = {s: max(1, int(Fraction(float(u[s])) * Fraction(scale))) for s in C}
p, q = L.numerator, L.denominator; W = int(wt.max())
coef = [q ** w * p ** (W - w) for w in range(W + 1)]      # (q/p)^w * p^W
worst = None
for s in C:
    lhs = 0
    for t in succ[s]: lhs += coef[int(wt[t])] * U[t]
    rhs = p ** W * U[s]
    assert lhs >= rhs, f'inequality fails at state {s}'
    r = Fraction(lhs, rhs); worst = r if worst is None or r < worst else worst
print(f'exact check passed on {len(C)} states: (M U)_s >= U_s for all s in C (smallest ratio {float(worst):.12f})')
print(f'certified: growth rate of the {"vertically indecomposable " if mode == "vi" else ""}lattices with all layers <= {W} is at least {L} = {float(L)}')
