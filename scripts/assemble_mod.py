#!/usr/bin/env python3
"""Check and assemble the modular-lattice results.

usage: assemble_mod.py runs/mod_N1.txt [runs/mod_N2.txt ...]
Each file has lines "n vi(n) f(n)"; mod_dual_N.txt next to it has "n atoms coatoms count".
Checks: known terms of A006981 and A342132, agreement between runs with different N on their
common range, and symmetry of the (atoms, coatoms) table.  Writes b-files from the largest run.
"""
import sys, os, re
here = os.path.dirname(os.path.abspath(__file__))
def read_b(path):
    d = {}
    for line in open(path):
        if line.startswith('#') or not line.strip(): continue
        a, b = line.split(); d[int(a)] = int(b)
    return d
known_f = read_b(os.path.join(here, '..', 'data', 'oeis_b006981_n35.txt'))
known_vi = read_b(os.path.join(here, '..', 'data', 'oeis_b342132_n35.txt'))
runs = {}
for path in sys.argv[1:]:
    N = int(re.search(r'mod_(\d+)\.txt$', path).group(1))
    vi, f = {}, {}
    for line in open(path):
        n, v, t = line.split(); vi[int(n)] = int(v); f[int(n)] = int(t)
    assert max(vi) == N, 'incomplete run ' + path
    # recompute f from vi as a check of the vertical-sum recursion
    g = {1: 1}
    for n in range(2, N + 1): g[n] = sum(vi[k] * g[n - k + 1] for k in range(2, n + 1))
    assert g == f
    bad_f = [n for n in known_f if 1 <= n <= N and f[n] != known_f[n]]
    bad_vi = [n for n in known_vi if 2 <= n <= N and vi[n] != known_vi[n]]
    print(f'N={N}: mismatches with A006981 (n<=35): {bad_f}; with A342132 (2<=n<=35): {bad_vi}')
    assert not bad_f and not bad_vi
    k23 = [tuple(map(int, l.split())) for l in open(os.path.join(here, '..', 'data', 'kohonen2023_table1_36_40.txt')) if l.strip() and l[0] != '#']
    bad23 = [n for (n, a, b) in k23 if n <= N and (vi[n], f[n]) != (a, b)]
    print(f'      mismatches with Kohonen (2023), Table 1, for 36 <= n <= min(N, 40): {bad23}')
    assert not bad23
    dual = path.replace('mod_', 'mod_dual_')
    M = {}
    for line in open(dual):
        n, a, b, c = map(int, line.split()); M[(n, a, b)] = c
    asym = [k for k, v in M.items() if M.get((k[0], k[2], k[1])) != v]
    tot = {}
    for (n, a, b), v in M.items(): tot[n] = tot.get(n, 0) + v
    badsum = [n for n in range(2, N + 1) if tot.get(n, 0) != vi[n]]
    print(f'      duality table: {len(M)} cells, {sum(1 for k in M if k[1] != k[2])} off-diagonal, asymmetric: {asym[:5]}, bad sums: {badsum[:5]}')
    assert not asym and not badsum
    runs[N] = (vi, f)
Ns = sorted(runs)
for i in range(len(Ns) - 1):
    a, b = Ns[i], Ns[i + 1]
    same = all(runs[a][0][n] == runs[b][0][n] for n in range(1, a + 1))
    print(f'runs N={a} and N={b} agree for n<={a}: {same}')
    assert same
N = Ns[-1]; vi, f = runs[N]
with open(os.path.join(here, '..', 'data', 'b006981.txt'), 'w') as o:
    o.write('0 1\n')
    for n in range(1, N + 1): o.write(f'{n} {f[n]}\n')
with open(os.path.join(here, '..', 'data', 'b342132.txt'), 'w') as o:
    o.write(f'1 {known_vi[1]}\n')
    for n in range(2, N + 1): o.write(f'{n} {vi[n]}\n')
for n in range(36, N + 1): print(f'A006981({n}) = {f[n]}   A342132({n}) = {vi[n]}   (in Kohonen 2023 for n <= 40)')
