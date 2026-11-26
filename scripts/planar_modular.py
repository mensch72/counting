#!/usr/bin/env python3
"""Planar modular lattices (OEIS A368461) by a structure theorem and a lattice-path count.

Every planar modular lattice arises from a planar distributive lattice D by inserting "eyes"
(doubly irreducible elements) into covering squares of D (Graetzer and Quackenbush), and D and the
numbers of eyes are determined up to isomorphism.  A vertically indecomposable planar distributive
lattice with more than two elements is a region of the square grid between two monotone lattice
paths: its rank layers are intervals of sizes w_0 = 1, w_1, ..., w_h = 1 with w_r >= 2 in between,
w changing by +1, -1 (one way each) or 0 (two ways).  Such a lattice has exactly two such
embeddings, mirror images of each other, and a layer with w points contains the middles of w - 1
covering squares.  Hence, by Burnside's lemma for the mirror,

    PM_vi(n) = ( A(n) + S(n) ) / 2        (n >= 4),      PM_vi(2) = 1,

where A counts (region, eye assignment) pairs and S those invariant under the mirror:
  A:  a layer with w points has weight x^w / (1-x)^(w-1);
  S:  only steps +-1; a layer has weight x^w / ((1-x)^[w even] (1-x^2)^floor((w-1)/2)).
All planar modular lattices follow by vertical sums.

usage: planar_modular.py N [oeis_b368461.txt]     prints n, PM_vi(n), PM(n)
"""
import sys
from math import comb

def series_counts(N, layer):
    """sum over width sequences of prod layer(w)[.], as a list of coefficients up to x^N.
       layer(w) -> list c[d] (d = 0..N) of the weight series of a layer of width w, and the
       multiplicity of a step with width change 0."""
    lay, zero_mult = layer
    F = {2: [0] * (N + 1)}
    c2 = lay(2)
    for d in range(2, N): F[2][1 + d] = c2[d]
    res = [0] * (N + 2)
    cache = {2: c2}
    for n in range(3, N + 1):
        for w in sorted(F):
            f = F[w][n]
            if not f: continue
            for w2, mult in ((w - 1, 1), (w, zero_mult), (w + 1, 1)):
                if not mult: continue
                if w2 == 1:
                    if n + 1 <= N: res[n + 1] += f
                    continue
                if n + w2 > N - 1: continue          # the top still needs one element
                if w2 not in cache: cache[w2] = lay(w2)
                c = cache[w2]; G = F.setdefault(w2, [0] * (N + 1)); fm = f * mult
                for d in range(w2, N - n):
                    G[n + d] += fm * c[d]
    return res

def main():
    N = int(sys.argv[1])
    def lay_all(w):       # x^w / (1-x)^(w-1):  coefficient of x^d is C(d-2, w-2)
        return [comb(d - 2, w - 2) if d >= w else 0 for d in range(N + 1)]
    def lay_sym(w):       # x^w / ((1-x)^[w even] (1-x^2)^floor((w-1)/2))
        p = (w - 1) // 2; c = [0] * (N + 1)
        for j in range(0, N - w + 1):          # j eyes
            if w % 2 == 0:                     # sum over 2*i <= j of C(i+p-1, p-1) (i pairs-eyes), rest in the fixed square
                c[w + j] = sum(comb(i + p - 1, p - 1) if p else (1 if i == 0 else 0) for i in range(j // 2 + 1))
            else:
                c[w + j] = comb(j // 2 + p - 1, p - 1) if j % 2 == 0 else 0
        return c
    A = series_counts(N, (lay_all, 2)); S = series_counts(N, (lay_sym, 0))
    vi = [0] * (N + 1); vi[2] = 1
    for n in range(4, N + 1):
        assert (A[n] + S[n]) % 2 == 0
        vi[n] = (A[n] + S[n]) // 2
    f = [0] * (N + 1); f[1] = 1
    for n in range(2, N + 1): f[n] = sum(vi[k] * f[n - k + 1] for k in range(2, n + 1))
    if len(sys.argv) > 2:
        known = {}
        for l in open(sys.argv[2]):
            if l.strip() and l[0] != '#':
                a, b = l.split(); known[int(a)] = int(b)
        bad = [n for n in known if n <= N and known[n] != f[n]]
        print(f'# compared with {len([n for n in known if n <= N])} known terms of A368461: mismatches {bad}', file=sys.stderr)
        assert not bad
    for n in range(1, N + 1): print(n, vi[n], f[n])

if __name__ == '__main__': main()
