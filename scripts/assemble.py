#!/usr/bin/env python3
"""Turn the DP output (n, vi(n)) into b-files for A072361 and A006982 and check
them against the previously known OEIS terms.

usage: assemble.py runs/vi_N.txt
"""
import sys, os
here = os.path.dirname(os.path.abspath(__file__))
vi = {}
for line in open(sys.argv[1]):
    n, v = line.split(); vi[int(n)] = int(v)
N = max(vi)
# every lattice is a unique vertical sum of v.i. lattices (>= 2 elements each):
# f(n) = sum_{k=2..n} vi(k) f(n-k+1), f(1) = 1.
f = {0: 1, 1: 1}
for n in range(2, N + 1):
    f[n] = sum(vi[k] * f[n - k + 1] for k in range(2, n + 1))

def read_b(path):
    d = {}
    for line in open(path):
        if line.startswith('#') or not line.strip(): continue
        a, b = line.split(); d[int(a)] = int(b)
    return d
k1 = read_b(os.path.join(here, '..', 'data', 'oeis_b006982_n60.txt'))
k2 = read_b(os.path.join(here, '..', 'data', 'oeis_b072361_n49.txt'))
bad1 = [n for n in k1 if n <= N and f[n] != k1[n]]
bad2 = [n for n in k2 if n <= N and vi[n] != k2[n]]
print(f'A006982: {len(k1)} known terms (n=0..{max(k1)}), mismatches: {bad1}')
print(f'A072361: {len(k2)} known terms (n=1..{max(k2)}), mismatches: {bad2}')
k3 = read_b(os.path.join(here, '..', 'data', 'kohonen2021_table2_dvi_50_60.txt'))
bad3 = [n for n in k3 if n <= N and vi[n] != k3[n]]
print(f'A072361: values for n=50..60 printed in Kohonen (2021), Table 2, mismatches: {bad3}')
assert not bad1 and not bad2 and not bad3
with open(os.path.join(here, '..', 'data', 'b006982.txt'), 'w') as o:
    for n in range(0, N + 1): o.write(f'{n} {f[n]}\n')
with open(os.path.join(here, '..', 'data', 'b072361.txt'), 'w') as o:
    for n in range(1, N + 1): o.write(f'{n} {vi[n]}\n')
print(f'wrote b-files up to n={N};  A006982({N}) = {f[N]}')
print('ratio f(N)/f(N-1) =', f[N] / f[N - 1], '  vi(N)/vi(N-1) =', vi[N] / vi[N - 1])
