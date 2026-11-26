#!/usr/bin/env python3
"""Duality check: M[n][a][b] = number of v.i. distributive lattices with n
elements, a atoms and b coatoms must be symmetric in (a, b), and sum to vi(n).

usage: check_dual.py runs/vi_N.txt runs/dual_N_t*.txt
"""
import sys, re
vi = {int(l.split()[0]): int(l.split()[1]) for l in open(sys.argv[1])}
M = {}
for path in sys.argv[2:]:
    t = int(re.search(r'_t(\d+)\.txt$', path).group(1))
    for line in open(path):
        n, b, c = map(int, line.split()); M[(n, t, b)] = c
N = max(vi)
asym = [k for k, v in M.items() if M.get((k[0], k[2], k[1])) != v]
tot = {}
for (n, a, b), v in M.items(): tot[n] = tot.get(n, 0) + v
badsum = [n for n in range(2, N + 1) if tot.get(n, 0) != vi[n]]
print(f'cells: {len(M)}, off-diagonal: {sum(1 for k in M if k[1] != k[2])}, max atoms: {max(k[1] for k in M)}')
print('asymmetric cells:', asym[:10], ' | n with sum != vi(n):', badsum[:10])
assert not asym and not badsum
print('duality check passed for all n <=', N)
