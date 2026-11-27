# gain on band posets: maximum |S| for the various families, compared with the width
import random,sys,statistics
from lib import *
from t3 import *
from t2 import c_chain
def E_utight(P):
    """isomorphism-invariant: x<y tight cover, x the ONLY tight lower cover of y, y the ONLY tight upper cover of x"""
    n,up,dn=P; h=heights(P); cov=[(x,y) for x,y in covers(P) if h[y]==h[x]+1]
    from collections import Counter
    cd=Counter(y for x,y in cov); cu=Counter(x for x,y in cov)
    return set((x,y) for x,y in cov if cd[y]==1 and cu[x]==1)
def E_natural(l): return lambda P: set((x,x+1) for x in range(P[0]) if (x+1)%l!=0 and (P[1][x]&P[2][x+1])==0)
def relabel(P,perm):
    n,up,dn=P; nu=[0]*n; nd=[0]*n
    for x in range(n):
        for y in bits(up[x]): nu[perm[x]]|=1<<perm[y]; nd[perm[y]]|=1<<perm[x]
    return (n,tuple(nu),tuple(nd))
def maxR(P,R,ds):
    bad=[(1<<x,1<<y) for x,y in R]; best=0
    for I in ds:
        for I1 in ds:
            if I1&I!=I1: continue
            s=pc(I)-pc(I1)
            if s>best and not any((I&by) and not (I1&bx) for bx,by in bad): best=s
    return best
def maxC(P,constraint,ds):
    best=0
    for I in ds:
        for I1 in ds:
            if I1&I!=I1: continue
            s=pc(I)-pc(I1)
            if s>best and constraint(P,I&~I1): best=s
    return best
if __name__=="__main__":
    # sanity: invariant rule also satisfies the identity (it is an R-lattice)
    run("chains: unique tight covers [lab<=5]",R_chain(E_utight),[P for n in range(1,6) for P in labelled_posets(n)],True)
    run("chains: unique tight covers [nat 6]",R_chain(E_utight),natural_posets(6),True)
    rng=random.Random(7); T=int(sys.argv[1]) if len(sys.argv)>1 else 12
    print("columns: mean (min..max) over",T,"random band posets")
    for (w,l,a) in [(3,4,1),(3,4,2),(3,5,1),(3,5,2),(4,4,2),(4,4,1)]:
        cols={}
        for _ in range(T):
            P=band(w,l,a,rng); n=P[0]; ds=downsets(P)
            perm=list(range(n)); rng.shuffle(perm); Pr=relabel(P,perm); dsr=downsets(Pr)
            vals={
             'width':maxR(P,R_all(P),ds),
             'slab2':maxR(P,R_slab(2)(P),ds),'slab3':maxR(P,R_slab(3)(P),ds),
             'anychain':maxC(P,c_chain(99),ds),'anychain<=2':maxC(P,c_chain(2),ds),
             'natural':maxR(P,R_chain(E_natural(l))(P),ds),
             'utight':maxR(P,R_chain(E_utight)(P),ds),
             'tight+lab':maxR(Pr,R_chain(E_tight)(Pr),dsr),
             'mutlab':maxR(Pr,R_chain(E_mutual_label)(Pr),dsr),
             'firstfit':maxR(Pr,R_chain(E_firstfit)(Pr),dsr)}
            for k,v in vals.items(): cols.setdefault(k,[]).append(v)
        print(f"w={w} l={l} a={a} n={w*l}: "+"; ".join(f"{k} {statistics.mean(v):.1f} ({min(v)}..{max(v)})" for k,v in cols.items()))
