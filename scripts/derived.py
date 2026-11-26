#!/usr/bin/env python3
"""OEIS sequences that are functions of the sequences extended here.

A072407  canonically 2-indecomposable posets with n antichains (Erne, Heitzig, Reinhold 2002,
         Corollary 7):  v_0 = 1, w_1 = v_1 = 0,  v_k = sum_{j=0}^{k-1} w_{k-j} v_j  (k > 1),
         where v_k = A072361(k) (with v_1 = 0 as in the OEIS entry).
A186808  numbers n such that A006982(n) is prime.

Writes data/b072407.txt and data/b186808.txt and checks the known OEIS terms.
Primality is proved with PARI/GP (isprime) if `gp` is available, else only tested.
"""
import os, subprocess, shutil
here = os.path.dirname(os.path.abspath(__file__)); D = os.path.join(here, '..', 'data')
def rb(name):
    d = {}
    for l in open(os.path.join(D, name)):
        if l.strip() and l[0] != '#':
            a, b = l.split(); d[int(a)] = int(b)
    return d
d, v = rb('b006982.txt'), rb('b072361.txt'); N = max(v)
v = dict(v); v[0] = 1; v[1] = 0
w = {1: 0}
for k in range(2, N + 1):
    w[k] = v[k] - sum(w[k - j] * v[j] for j in range(1, k))
    assert w[k] >= 0
known_w = [int(x) for x in "0,1,0,0,0,0,0,2,1,1,0,7,5,16,14,40,41,120,131,321,402,901,1210,2590,3621,7371,10841,21178,32222,61273,95408,177384,282405,515174,833295,1500030,2455337,4372535,7229231,12761691,21260746,37286778,62483221,109014426,183542099,318906720,538889399,933361886,1581666042".split(',')]
bad = [k for k in range(1, 50) if w[k] != known_w[k - 1]]
print('A072407: 49 known terms, mismatches:', bad); assert not bad
open(os.path.join(D, 'b072407.txt'), 'w').write(''.join(f'{k} {w[k]}\n' for k in range(1, N + 1)))
print(f'A072407 extended to n = {N}; a(50) = {w[50]}, a({N}) = {w[N]}')

def is_prime(n):
    if n < 2: return False
    if shutil.which('gp'):
        out = subprocess.run(['gp', '-q', '-f'], input=f'print(isprime({n}))\n', capture_output=True, text=True).stdout.strip()
        return out == '1'
    # fallback: Miller-Rabin with fixed bases (a test, not a proof, for large n)
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % p == 0: return n == p
    r, s = n - 1, 0
    while r % 2 == 0: r //= 2; s += 1
    for a in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71):
        x = pow(a, r, n)
        if x in (1, n - 1): continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1: break
        else: return False
    return True
primes = [n for n in sorted(d) if is_prime(d[n])]
known_p = [4, 5, 6, 10, 12, 13, 18, 21, 23, 26]
assert primes[:10] == known_p, primes[:12]
open(os.path.join(D, 'b186808.txt'), 'w').write(''.join(f'{i + 1} {n}\n' for i, n in enumerate(primes)))
print(f'A186808: n <= {max(d)} with A006982(n) prime ({"proved with PARI" if shutil.which("gp") else "Miller-Rabin test only"}):', primes)
