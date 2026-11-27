# heuristic floor for the stack method: generalised band posets (levels 1..L, w rows)
# entropy log2(c)/L^2 ; level-stack fraction m/L with m = longest t_1<...<t_m, t_j <= hi(hi(t_{j+1}))
from math import log2
import itertools, sys
def cnt(hi,L):
    H=lambda t: 0 if t==0 else hi[t-1]
    ways={0:1}
    for t in range(1,L+1):
        new={}
        for d in range(H(H(t)),H(t)+1):
            new[d]=sum(v for dd,v in ways.items() if dd<=d)
        ways=new
    return sum(ways.values())
def stack(hi,L):
    H=lambda t: 0 if t==0 else hi[t-1]
    best=[0]*(L+1)
    for t in range(1,L+1):
        lo=H(H(t)); best[t]=1+max([best[s] for s in range(1,lo+1)],default=0)
    return max(best)
def his(L):
    def rec(t,prev):
        if t>L: yield (); return
        for v in range(prev,t):
            for rest in rec(t+1,v): yield (v,)+rest
    return rec(1,0)
pts=[]
for L in range(2,int(sys.argv[1])+1):
    for hi in his(L):
        c=cnt(hi,L)
        if c>1: pts.append((stack(hi,L)/L, 1/L, log2(c)/L**2, L, hi))
import bisect
def best_under(kappa):
    cand=[p for p in pts if p[0]<kappa]
    return max(cand,key=lambda p:p[2]) if cand else None
print("kappa  wide   best entropy among band families with level-stack fraction < kappa")
res=[]
for k100 in range(12,52,2):
    k=k100/100; b=best_under(k); w=(1-k)**2/4
    print(f"{k:.2f} {w:.4f}", (round(b[2],4),b[3],b[4],round(b[0],3)) if b else None)
    if b: res.append((max(w,b[2]),k))
print("heuristic floor:",min(res))
