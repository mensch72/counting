# Test: #labelled posets of width>=k via flags of large antichains, top antichain inserted in product form
import sys
from math import comb, factorial
from itertools import combinations, product
exec(open('test_threshold_and_cubes.py').read().split("# test 1")[0])
def width(n,rel):
    best=0
    for S in range(1<<n):
        el=[x for x in range(n) if S>>x&1]
        if all((a,b) not in rel and (b,a) not in rel for a in el for b in el if a<b): best=max(best,len(el))
    return best
def antichains(n,rel):
    out=[]
    for S in range(1<<n):
        el=[x for x in range(n) if S>>x&1]
        if all((a,b) not in rel and (b,a) not in rel for a in el for b in el if a<b): out.append(S)
    return out
def types(n,rel):
    ds=downsets(n,rel)
    us=[U for U in range(1<<n) if all(not(U>>i&1) or (U>>j&1) for (i,j) in rel)]
    out=[]
    for D in ds:
        for U in us:
            if D&U: continue
            if all((d,u) in rel for d in range(n) if D>>d&1 for u in range(n) if U>>u&1): out.append((D,U))
    return out
def leq(rel,a,b): return a==b or (a,b) in rel
def core_sum(q,rel,j,k):
    """signed sum over r and core flags of number of valid (type,birth) assignments for j labelled inserted elements"""
    total=0
    for A in downsets(q,rel):
        total+=core_sum_A(q,rel,j,k,A)
    return total
def core_sum_A(q,rel,j,k,A):
    ac=[S for S in antichains(q,rel) if S&~A==0]; ty=[(D,U) for (D,U) in types(q,rel) if D&~A==0 and U&A==0]; total=0
    mxA=[x for x in range(q) if A>>x&1 and not any((x,y) in rel and A>>y&1 for y in range(q))]
    def count(E):  # E = [E_0..E_{r-1}]
        r=len(E)
        needy=[]
        for i in range(r):
            nxt=E[i+1] if i+1<r else 0
            for e in range(q):
                if E[i]>>e&1 and not any(nxt>>f&1 and leq(rel,e,f) for f in range(q)): needy.append((e,i))
        res=0
        allz=needy+[(e,10**6) for e in mxA]
        for zmask in range(1<<len(allz)):
            Z=[allz[t] for t in range(len(allz)) if zmask>>t&1]
            c=[]
            for beta in range(r+1):
                forb_all=0
                for i in range(beta,r): forb_all|=E[i]
                forbD=0
                for (e,i) in Z:
                    if beta<=i+1: forbD|=1<<e
                c.append(sum(1 for (D,U) in ty if not((D|U)&forb_all) and not(D&forbD)))
            # DP over births: ways[t]= sum over (n_0..n_i) with total t of prod c^n/n!
            ways={0:1.0}
            from fractions import Fraction
            ways={0:Fraction(1)}
            ok=True
            for i in range(r+1):
                new={}
                for t,v in ways.items():
                    for nb in range(0,j-t+1):
                        if i>=1:
                            Eprev=E[i-1]; Ecur=E[i] if i<r else 0
                            if Eprev==Ecur and nb==0: continue   # strictness N_{i-1}!=N_i
                        tt=t+nb
                        sizeE=bin(E[i]).count('1') if i<r else 0
                        if sizeE+tt<k: continue
                        new[tt]=new.get(tt,0)+v*Fraction(c[i]**nb,factorial(nb))
                ways=new
            res+=(-1)**len(Z)*ways.get(j,0)*factorial(j)
        return res
    def rec(E):
        nonlocal total
        total+=(-1)**len(E)*count(E)
        if len(E)>=q+j: return
        for S in ac:
            # prepend a lower antichain? build top-down: new lowest element E_0
            rec([S]+E)
    # build sequences by prepending; prune: lengths bounded by number of antichains of P <= limit
    def rec2(E,depth):
        nonlocal total
        v=count(E)
        total+=(-1)**len(E)*v
        if depth>=q+j+1: return
        later=0
        for X in E[1:]: later|=X
        first=E[0] if E else 0
        for S in ac:
            if bin(S).count('1')+j<k: continue
            if S & later & ~first: continue   # interval sequences only (Lemma 5)
            if E and S==first and j==0: continue
            rec2([S]+E,depth+1)
    rec2([],0)
    return total
for n in range(1,6):
    for k in range(1,n+1):
        brute=sum(1 for rel in L[n] if width(n,rel)>=k)
        form=0
        for j in range(k,n+1):
            q=n-j
            form+=comb(n,j)*sum(core_sum(q,rel,j,k) for rel in L[q])
        print(n,k,brute,form,"OK" if brute==form else "MISMATCH"); sys.stdout.flush()
