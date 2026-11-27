# brute force: labelled posets on [n] by width (n<=6 fast; n=7 slower), and two-chain poset counts
import sys
from math import comb
from itertools import product
def posets_by_width(n):
    # DFS adding points; poset stored as list of up-sets 'above[i]' bitmasks (strict), below[i]
    res={}
    def width(below,above,m):
        # max antichain via brute over subsets (m<=7)
        comp=[below[i]|above[i] for i in range(m)]
        best=0
        # iterate antichains by DFS
        def rec(i,cur,forb):
            nonlocal best
            if cur>best: best=cur
            for j in range(i,m):
                if not (forb>>j)&1:
                    rec(j+1,cur+1,forb|comp[j])
        rec(0,0,0)
        return best
    def rec(m,below,above):
        if m==n:
            w=width(below,above,n); res[w]=res.get(w,0)+1; return
        # add point m with down-set D and up-set U among 0..m-1
        for D in range(1<<m):
            # D must be a down-set
            ok=True
            for i in range(m):
                if (D>>i)&1 and (below[i]&~D): ok=False;break
            if not ok: continue
            for U in range(1<<m):
                if U&D: continue
                ok=True
                for i in range(m):
                    if (U>>i)&1 and (above[i]&~U): ok=False;break
                if not ok: continue
                # every d in D below every u in U
                for i in range(m):
                    if (D>>i)&1 and (U&~above[i]): ok=False;break
                if not ok: continue
                nb=[below[i]|((1<<m) if (U>>i)&1 else 0) for i in range(m)]+[D]
                na=[above[i]|((1<<m) if (D>>i)&1 else 0) for i in range(m)]+[U]
                rec(m+1,nb,na)
    rec(0,[],[])
    return res
def two_chain(a,b):
    # count partial orders on chain A (a pts) + chain B (b pts) extending both chains: brute force via thresholds
    # dA[t] = number of B elements below A_t (nondecr), dB[s] = number of A elements below B_s (nondecr)
    cnt=0
    def mono(k,m):
        # nondecreasing sequences length k values 0..m
        def r(i,lo):
            if i==k: yield (); return
            for v in range(lo,m+1):
                for rest in r(i+1,v): yield (v,)+rest
        return list(r(0,0))
    for dA in mono(a,b):
        for dB in mono(b,a):
            # relation: B_s < A_t iff s<=dA[t-1]; A_t < B_s iff t<=dB[s-1]
            n=a+b
            lt=[[False]*n for _ in range(n)]
            for i in range(a):
                for j in range(i+1,a): lt[i][j]=True
            for i in range(b):
                for j in range(i+1,b): lt[a+i][a+j]=True
            for t in range(a):
                for s in range(b):
                    if s+1<=dA[t]: lt[a+s][t]=True
                    if t+1<=dB[s]: lt[t][a+s]=True
            ok=True
            for x in range(n):
                if not ok: break
                for y in range(n):
                    if lt[x][y]:
                        if lt[y][x]: ok=False;break
                        for z in range(n):
                            if lt[y][z] and not lt[x][z]: ok=False;break
                        if not ok: break
            cnt+=ok
    return cnt
def P2(a,b): return comb(a+b,a)**2-comb(a+b,a-1)*comb(a+b,a+1)
if __name__=="__main__":
    for a in range(1,5):
        for b in range(a,5):
            if a+b<=7:
                print("two-chain",a,b,two_chain(a,b),P2(a,b), comb(a+b,a)*comb(a+b+2,a+1)//(a+b+2))
    N=int(sys.argv[1]) if len(sys.argv)>1 else 6
    for n in range(1,N+1):
        r=posets_by_width(n); print(n,sum(r.values()),dict(sorted(r.items())),flush=True)
