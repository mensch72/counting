import sys
sys.argv=['tri.py','0','0','0']
src=open('tri.py').read().split("m=int(sys.argv[1])")[0]
exec(src)
from math import log2, comb
import random
def best_over_seeds(m,l,iters,seeds):
    b=None
    for s in seeds:
        e,H=search(m,l,iters,s)
        if b is None or e>b[0]: b=(e,H)
    return b
for (m,l,iters) in [(3,5,60000),(3,6,60000),(4,4,40000),(4,5,40000)]:
    e,H=best_over_seeds(m,l,iters,[1,2,3])
    P=comb(2*l,l)*comb(2*l+1,l)//(l+1)
    print(f"m={m} l={l}: {e/(m*(m-1)/2):.3f} bits per pair (pair count {log2(P):.3f})"); sys.stdout.flush()
