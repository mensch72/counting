#!/usr/bin/env python3
"""Growth rates of distributive lattices all of whose rank layers have at most W elements.

Reads the automaton written by src/bounded (state 0 = empty frontier).  A lattice in the class is a
closed walk from state 0 to state 0; its number of elements is 1 + the sum of the weights of the
states entered.  It is vertically indecomposable iff the walk does not pass through state 0.

For a positive real x let M(x) be the matrix with entries  (#transitions s -> t) * x^weight(t).
  * all lattices of the class:  growth rate 1/x where the spectral radius of M(x) is 1;
  * vertically indecomposable:  the same for M(x) restricted to the states other than 0.

usage: bounded_growth.py automaton.txt [nmax]
"""
import sys
import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import connected_components

def read(path):
    f = open(path); n = int(f.readline()); wt = [0] * n; rows = []; cols = []
    for line in f:
        p = line.split(); s = int(p[0]); wt[s] = int(p[1])
        for t in p[3:]: rows.append(s); cols.append(int(t))
    return n, np.array(wt), np.array(rows), np.array(cols)

def spectral(n, wt, rows, cols, x, keep):
    """spectral radius of M(x) restricted to the index set keep (boolean), by power iteration"""
    sel = keep[rows] & keep[cols]
    A = csr_matrix((x ** wt[cols[sel]].astype(float), (rows[sel], cols[sel])), shape=(n, n))
    u = keep.astype(float); u /= u.sum(); lam = 0
    for it in range(200000):
        v = A @ u; s = v.sum()
        if s == 0: return 0.0, u
        v /= s
        if it % 50 == 0 and abs(s - lam) < 1e-15 * max(1, s): lam = s; u = v; break
        lam = s; u = v
    return lam, u

def growth(n, wt, rows, cols, keep):
    lo, hi = 0.3, 1.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if spectral(n, wt, rows, cols, mid, keep)[0] < 1: lo = mid
        else: hi = mid
    return 1 / lo, lo

if __name__ == '__main__':
    n, wt, rows, cols = read(sys.argv[1]); nmax = int(sys.argv[2]) if len(sys.argv) > 2 else 60
    # exact counts of v.i. lattices of the class for small n (walks 0 -> 0 avoiding 0)
    from collections import defaultdict
    adj = defaultdict(list)
    for s, t in zip(rows.tolist(), cols.tolist()): adj[s].append(t)
    cur = defaultdict(int); cnt = [0] * (nmax + 1)
    layer = [defaultdict(int) for _ in range(nmax + 2)]
    for t in adj[0]:
        a = 1 + int(wt[t])
        if a <= nmax: layer[a][t] += 1
    for a in range(2, nmax + 1):
        for s, c in layer[a].items():
            if s == 0: cnt[a] += c; continue
            for t in adj[s]:
                a2 = a + int(wt[t])
                if a2 <= nmax: layer[a2][t] += c
    print('v.i. lattices of the class, n=2..%d:' % min(nmax, 40), cnt[2:41])
    # states from which the empty frontier can be reached again (the others are dead ends)
    A = csr_matrix((np.ones(len(rows)), (rows, cols)), shape=(n, n))
    ncomp, lab = connected_components(A, directed=True, connection='strong')
    keep_all = lab == lab[0]
    nz = np.ones(n, bool); nz[0] = False
    # largest strongly connected set of non-empty states reachable from 0 and returning to 0
    sel = nz[rows] & nz[cols] & keep_all[rows] & keep_all[cols]
    B = csr_matrix((np.ones(sel.sum()), (rows[sel], cols[sel])), shape=(n, n))
    nc2, lab2 = connected_components(B, directed=True, connection='strong')
    sizes = np.bincount(lab2[keep_all & nz]) if (keep_all & nz).any() else np.array([0])
    big = np.argmax(sizes); keep_vi = (lab2 == big) & keep_all & nz
    print('states: %d, recurrent (in the component of the empty frontier): %d, largest non-empty strong component: %d' % (n, keep_all.sum(), keep_vi.sum()))
    g_all, x_all = growth(n, wt, rows, cols, keep_all)
    g_vi, x_vi = growth(n, wt, rows, cols, keep_vi)
    print('growth rate, all lattices of the class      : %.10f' % g_all)
    print('growth rate, vertically indecomposable ones : %.10f' % g_vi)
