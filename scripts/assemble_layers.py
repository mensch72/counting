#!/usr/bin/env python3
"""Check and assemble results of src/layers.cpp for semimodular (usm) and geometric lattices.

usage: assemble_layers.py usm|geometric runs/lay_MODE_N1.txt [runs/lay_MODE_N2.txt ...]
Files have lines "n vi(n) f(n)".  For usm, f(n) is the number of semimodular lattices (A229202).
For geometric, vi(n) is the number of geometric lattices for n >= 2 (A281574); geometric lattices
with more than two elements are vertically indecomposable, so f is not used.
Checks the known OEIS terms and the agreement of runs with different N; writes a b-file.
"""
import sys, os, re
here = os.path.dirname(os.path.abspath(__file__)); D = os.path.join(here, '..', 'data')
def rb(p):
    d = {}
    for l in open(p):
        if l.strip() and l[0] != '#':
            a, b = l.split(); d[int(a)] = int(b)
    return d
mode = sys.argv[1]
known = rb(os.path.join(D, 'oeis_a229202_n25.txt' if mode == 'usm' else 'oeis_a281574_n37.txt'))
runs = {}
for path in sys.argv[2:]:
    N = int(re.search(r'_(\d+)\.txt$', path).group(1))
    vi, f = {}, {}
    for l in open(path):
        n, v, t = l.split(); vi[int(n)] = int(v); f[int(n)] = int(t)
    assert max(vi) == N, 'incomplete run ' + path
    seq = dict(f) if mode == 'usm' else {n: (1 if n == 1 else vi[n]) for n in vi}
    bad = [n for n in known if 1 <= n <= N and seq[n] != known[n]]
    print(f'{mode} N={N}: mismatches with known terms (n<={max(known)}): {bad}')
    assert not bad
    runs[N] = seq
Ns = sorted(runs)
for i in range(len(Ns) - 1):
    a, b = Ns[i], Ns[i + 1]
    same = all(runs[a][n] == runs[b][n] for n in range(1, a + 1))
    print(f'runs N={a} and N={b} agree for n<={a}: {same}'); assert same
N = Ns[-1]; seq = runs[N]
name = 'b229202.txt' if mode == 'usm' else 'b281574.txt'
with open(os.path.join(D, name), 'w') as o:
    if mode == 'usm': o.write('0 1\n')
    for n in range(1, N + 1): o.write(f'{n} {seq[n]}\n')
for n in range(max(known) + 1, N + 1): print(f'new: a({n}) = {seq[n]}')
