#!/usr/bin/env python3
"""Independent check on thin lattices: planar (width <= 2) case.

A vertically indecomposable distributive lattice J(P) with P of width 2 is a
region of the square grid between two monotone lattice paths.  Its rank layers
are intervals of sizes w_0 = 1, w_1, ..., w_h = 1 with w_r >= 2 in between, and
w changes by +1, -1 (one way each) or 0 (two ways).  The two-chain partition of
P is unique up to swapping the chains, so each lattice arises from exactly two
regions (mirror images), or from one if the region is mirror-symmetric
(only +-1 steps).  Hence

    V(n) = (R(n) + S(n)) / 2     (n >= 4),   V(2) = 1,

with R, S counted by a trivial DP over (width, area).  Compare with the frontier
DP restricted to width <= 2:   frontier2 N 0 2

usage: planar_check.py N dp_output.txt
"""
import sys
N = int(sys.argv[1])
def count(zero_weight):
    # f[w][s] = number of prefixes ending at an interior layer of width w with area s (incl. bottom)
    res = [0] * (N + 1)
    cur = {(2, 3): 1}            # after bottom (1) and first layer (2)
    while cur:
        nxt = {}
        for (w, s), c in cur.items():
            for dw, mult in ((1, 1), (-1, 1), (0, zero_weight)):
                if not mult: continue
                w2 = w + dw; s2 = s + w2
                if s2 > N: continue
                if w2 == 1: res[s2] += c * mult
                else: nxt[(w2, s2)] = nxt.get((w2, s2), 0) + c * mult
        cur = nxt
    return res
R, S = count(2), count(0)
V = [0] * (N + 1); V[2] = 1
for n in range(4, N + 1):
    assert (R[n] + S[n]) % 2 == 0
    V[n] = (R[n] + S[n]) // 2
dp = {int(l.split()[0]): int(l.split()[1]) for l in open(sys.argv[2])}
bad = [n for n in range(1, N + 1) if dp.get(n, 0) != V[n]]
print('planar v.i. counts, n=2..16:', V[2:17])
print(f'n <= {N}: mismatches {bad[:10]};  V({N}) = {V[N]}')
assert not bad
print('planar check passed')
