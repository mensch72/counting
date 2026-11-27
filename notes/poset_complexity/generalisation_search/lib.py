# common helpers: posets as (n, up, dn) with bitmask strict up-sets/down-sets
import itertools, random
from functools import lru_cache
def natural_posets(n):
    """all posets on {0..n-1} with x<y => x<y numerically (every iso class occurs)"""
    res=[[]]  # list of dn-lists
    for m in range(n):
        new=[]
        for dn in res:
            # choose down-set of new maximal element m: a down-set of current poset
            for D in range(1<<m):
                if all((D>>x&1)==0 or (dn[x]&~D)==0 for x in range(m)):
                    new.append(dn+[D])
        res=new
    out=[]
    for dn in res:
        up=[0]*n
        for y in range(n):
            for x in range(n):
                if dn[y]>>x&1: up[x]|=1<<y
        out.append((n,tuple(up),tuple(dn)))
    return out
def labelled_posets(n):
    pairs=[(i,j) for i in range(n) for j in range(i+1,n)]
    out=[]
    for st in itertools.product((0,1,2),repeat=len(pairs)):
        up=[0]*n; dn=[0]*n
        for (i,j),s in zip(pairs,st):
            if s==1: up[i]|=1<<j; dn[j]|=1<<i
            elif s==2: up[j]|=1<<i; dn[i]|=1<<j
        if all((up[y]&~up[x])==0 for x in range(n) for y in range(n) if up[x]>>y&1):
            out.append((n,tuple(up),tuple(dn)))
    return out
def downsets(P):
    n,up,dn=P
    return [I for I in range(1<<n) if all((I>>x&1)==0 or (dn[x]&~I)==0 for x in range(n))]
def bits(S):
    r=[];i=0
    while S:
        if S&1: r.append(i)
        S>>=1;i+=1
    return r
def pc(x): return bin(x).count('1')
def is_chain(P,S):
    n,up,dn=P
    return all((S&~(up[x]|dn[x]|1<<x))==0 for x in bits(S))
def maxset(P,I):
    n,up,dn=P; m=0
    for x in bits(I):
        if up[x]&I==0: m|=1<<x
    return m
def minset(P,I):
    n,up,dn=P; m=0
    for x in bits(I):
        if dn[x]&I==0: m|=1<<x
    return m
def components(P,S):
    n,up,dn=P; comps=[]; rest=S
    while rest:
        x=rest&-rest; c=x; fr=x
        while fr:
            y=fr.bit_length()-1; fr&=~(1<<y)
            nb=(up[y]|dn[y])&S&~c
            c|=nb; fr|=nb
        comps.append(c); rest&=~c
    return comps
def rels(P):
    n,up,dn=P
    return [(x,y) for x in range(n) for y in bits(up[x])]
def covers(P):
    n,up,dn=P
    return [(x,y) for x in range(n) for y in bits(up[x]) if up[x]&dn[y]==0]
def euler(V,leq):
    """Euler char of order complex of finite poset: V list sorted s.t. leq(a,b) => a before b"""
    g=[]
    for i,p in enumerate(V):
        g.append(1-sum(g[j] for j in range(i) if leq(V[j],p)))
    return sum(g)
def band(w,l,a,rng):
    """random band poset: points (i,t)->i*l+t-1"""
    def rd():
        d=[0]*(l+1); prev=0
        for t in range(1,l+1):
            lo=max(0,t-2*a,prev); hi=max(0,t-a)
            d[t]=rng.randint(lo,hi); prev=d[t]
        return d
    n=w*l; up=[0]*n; dn=[0]*n
    idx=lambda i,t:i*l+t-1
    for i in range(w):
        for t in range(1,l+1):
            for s in range(1,t):
                dn[idx(i,t)]|=1<<idx(i,s)
    for i in range(w):
        for j in range(w):
            if i==j: continue
            d=rd()
            for t in range(1,l+1):
                for s in range(1,d[t]+1):
                    dn[idx(i,t)]|=1<<idx(j,s)
    for y in range(n):
        for x in bits(dn[y]): up[x]|=1<<y
    # sanity transitivity
    for y in range(n):
        for x in bits(dn[y]): assert dn[x]&~dn[y]==0
    return (n,tuple(up),tuple(dn))
def width(P):
    return max(pc(maxset(P,I)) for I in downsets(P))
