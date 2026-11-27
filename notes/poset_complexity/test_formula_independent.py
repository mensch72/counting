import sys
from math import comb, factorial
from fractions import Fraction
from itertools import product
def posets(n):
    # list of rel as tuple below[x] bitmask (strictly below), transitive
    res=[[]]
    for m in range(n):
        new=[]
        for below in res:
            above_of=[0]*m
            for x in range(m):
                for y in range(m):
                    if below[x]>>y&1: above_of[y]|=1<<x
            for D in range(1<<m):
                if any(D>>x&1 and (below[x]&~D) for x in range(m)): continue
                for U in range(1<<m):
                    if D&U: continue
                    if any(U>>x&1 and (above_of[x]&~U) for x in range(m)): continue
                    if any(D>>d&1 and (U&~above_of[d]) for d in range(m)): continue
                    nb=[below[x]|((1<<m)|D if U>>x&1 else 0) for x in range(m)]+[D]
                    new.append(nb)
        res=new
    return res
def pc(x): return bin(x).count('1')
def info(n,below):
    lt=lambda a,b: below[b]>>a&1
    ac=[S for S in range(1<<n) if all(not(below[x]&S) for x in range(n) if S>>x&1)]
    ds=[S for S in range(1<<n) if all((below[x]&~S)==0 for x in range(n) if S>>x&1)]
    return ac,ds
def down(n,below,S):
    D=S
    for x in range(n):
        if S>>x&1: D|=below[x]
    return D
def flagsum(n,below,k):
    ac,_=info(n,below)
    big=[(down(n,below,S),S) for S in ac if pc(S)>=k]
    big.sort(key=lambda t:pc(t[0]))
    # sum over nonempty chains of (-1)^(len-1)
    val={}
    tot=0
    for D,S in big:
        v=1-sum(val[D2] for D2 in val if D2!=D and D2&~D==0)
        val[D]=v; tot+=v
    return tot, (max(pc(S) for S in ac))
def G_total(q,below,j,k,n):
    ac,ds=info(q,below)
    above=[0]*q
    for x in range(q):
        for y in range(q):
            if below[x]>>y&1: above[y]|=1<<x
    us=[S for S in range(1<<q) if all((above[x]&~S)==0 for x in range(q) if S>>x&1)]
    total=0
    for A in ds:
        ty=[(D,U) for D in ds if D&~A==0 for U in us if U&A==0 and all((U&~above[d])==0 for d in range(q) if D>>d&1)]
        mxA=[x for x in range(q) if A>>x&1 and not(above[x]&A)]
        els=[x for x in range(q) if A>>x&1]
        for r in range(0,n):
            ivs=[None]+[(s,t) for s in range(r) for t in range(s,r)]
            for choice in product(ivs,repeat=len(els)):
                E=[0]*(r+1)
                for e,iv in zip(els,choice):
                    if iv:
                        for i in range(iv[0],iv[1]+1): E[i]|=1<<e
                if any(E[i] not in acset for i in range(r)) if False else any(any(below[x]&E[i] for x in range(q) if E[i]>>x&1) for i in range(r)): continue
                if any(pc(E[i])+j<k for i in range(r)): continue  # B empty
                C=set((a,r) for a in mxA)
                for i in range(r):
                    for e in range(q):
                        if E[i]>>e&1 and not any(E[i+1]>>f&1 and (e==f or below[f]>>e&1) for f in range(q)): C.add((e,i+1))
                C=sorted(C)
                res=0
                for zm in range(1<<len(C)):
                    Z=[C[t] for t in range(len(C)) if zm>>t&1]
                    c=[]
                    for beta in range(r+1):
                        forb=0
                        for i in range(beta,r): forb|=E[i]
                        for (e,t) in Z:
                            if beta<=t: forb|=1<<e
                        c.append(sum(1 for (D,U) in ty if not D&forb))
                    ways={0:Fraction(1)}
                    for b in range(r+1):
                        new={}
                        for t,v in ways.items():
                            for nb in range(j-t+1):
                                if b>=1 and E[b-1]==E[b] and nb==0: continue
                                if pc(E[b])+t+nb<k: continue
                                new[t+nb]=new.get(t+nb,0)+v*Fraction(c[b]**nb,factorial(nb))
                        ways=new
                    res+=(-1)**pc(zm)*ways.get(j,0)*factorial(j)
                total+=(-1)**r*res
    return total
N=int(sys.argv[1])
P={m:posets(m) for m in range(N+1)}
print([len(P[m]) for m in P])
for n in range(1,N+1):
    W={}
    for k in range(1,n+1): W[k]=0
    for b in P[n]:
        for k in range(1,n+2):
            s,w=flagsum(n,b,k)
            assert s==(1 if w>=k else 0),(n,b,k,s,w)
            if k<=n and w>=k: W[k]+=1
    print("euler ok",n,W); sys.stdout.flush()
    for k in range(n,0,-1):
        form=sum(comb(n,j)*sum(G_total(n-j,b,j,k,n) for b in P[n-j]) for j in range(k,n+1))
        print(n,k,W[k],form,"OK" if form==W[k] else "MISMATCH"); sys.stdout.flush()
