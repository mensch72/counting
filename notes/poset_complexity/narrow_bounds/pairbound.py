# Pair (two-chain) upper bound: h(alpha) <= h2(alpha) = (alpha^2/2) * [ (1-th)^2 F(q,q) + 2 th (1-th) F(q,q+1) + th^2 F(q+1,q+1) ],
# 1/alpha = q+th, F(a,b)=log2 P(a,b), P(a,b)=C(a+b,a)C(a+b+1,a)/(a+1).
from math import comb, log2, floor
def P(a,b): return comb(a+b,a)*comb(a+b+1,a)//(a+1)
def F(a,b): return log2(P(a,b))
def h2(al):
    l=1/al; q=floor(l+1e-12); th=l-q
    return al*al/2*((1-th)**2*F(q,q)+2*th*(1-th)*F(q,q+1)+th*th*F(q+1,q+1))
def wide(al): return (1-al)**2/4
def cross(h,lo=0.05,hi=0.3):
    for _ in range(80):
        mid=(lo+hi)/2
        if h(mid)<wide(mid): lo=mid
        else: hi=mid
    return lo
if __name__=="__main__":
    # exhaustive check of the smoothing lemma on small profiles
    import itertools
    def Phi(p): return sum(F(p[i],p[j]) for i in range(len(p)) for j in range(i))
    for n in range(1,15):
        for w in range(2,6):
            best=max((Phi(p),p) for p in itertools.product(range(n+1),repeat=w) if sum(p)==n and list(p)==sorted(p))
            q,r=divmod(n,w); bal=tuple([q]*(w-r)+[q+1]*r)
            assert abs(best[0]-Phi(bal))<1e-9,(n,w,best,bal)
    print("smoothing lemma verified for n<=14, w<=5")
    for al in [0.08,0.09,0.1,0.11,0.12,0.125,0.13,0.14,1/7,0.15,1/6,0.18,0.2,0.25]:
        print(f"alpha={al:.4f} h2={h2(al):.5f} 2alpha={2*al:.4f} wide={wide(al):.5f}")
    a=cross(h2); print("pair-bound crossing alpha=%.5f c=%.5f"%(a,wide(a)))
