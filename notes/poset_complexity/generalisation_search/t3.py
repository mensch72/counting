# R-lattice family: pairs (I',I) of down-sets, I' subset I, no forbidden pair (x<y) in R(P) inside S=I\I',
# |S|>=k, componentwise order.  R(P) may depend on the labels.
import sys, random
import numpy as np
from lib import *
from collections import Counter
def heights(P):
    n,up,dn=P; h=[0]*n
    for x in sorted(range(n),key=lambda x:pc(dn[x])):
        h[x]=1+max([h[z] for z in bits(dn[x])],default=0)
    return h
def allpairs(P): return set(rels(P))
def R_all(P): return allpairs(P)
def R_none(P): return set()
def R_slab(h):
    def f(P):
        n,up,dn=P; R=set()
        # longest chain from x to y has > h elements
        L={}
        for x in range(n):
            for y in sorted(bits(up[x]),key=lambda y:pc(dn[y])):
                L[(x,y)]=1+max([L[(x,z)] for z in bits(up[x]&dn[y])],default=1)
                if L[(x,y)]>h: R.add((x,y))
        return R
    return f
def R_random(p,seed=1):
    rng=random.Random(seed)
    return lambda P: set(r for r in rels(P) if rng.random()<p)
def blocks_to_R(P,E,h=99):
    """E: set of cover edges forming disjoint paths; allowed pairs = pairs joined by an E-path of <=h points"""
    n,up,dn=P; nxt={x:y for x,y in E}
    allowed=set()
    for x in range(n):
        y=x; c=1
        while y in nxt and c<h:
            y=nxt[y]; c+=1; allowed.add((x,y))
    return allpairs(P)-allowed
def E_mutual_label(P):
    n,up,dn=P; cov=covers(P)
    pd={y:min(x for x,yy in cov if yy==y) for y in set(y for x,y in cov)}
    pu={x:min(y for xx,y in cov if xx==x) for x in set(x for x,y in cov)}
    return set((x,y) for x,y in cov if pd[y]==x and pu[x]==y)
def E_tight(P):
    """tight covers (height(y)=height(x)+1); x = min-label tight lower cover of y and y = min-label tight upper cover of x"""
    n,up,dn=P; h=heights(P); cov=[(x,y) for x,y in covers(P) if h[y]==h[x]+1]
    pd={y:min(x for x,yy in cov if yy==y) for y in set(y for x,y in cov)}
    pu={x:min(y for xx,y in cov if xx==x) for x in set(x for x,y in cov)}
    return set((x,y) for x,y in cov if pd[y]==x and pu[x]==y)
def E_firstfit(P):
    """first-fit chain partition, elements processed by (height,label)"""
    n,up,dn=P; h=heights(P); tops=[]; E=set()
    for x in sorted(range(n),key=lambda x:(h[x],x)):
        for i,t in enumerate(tops):
            if dn[x]>>t&1 and (up[t]&dn[x])==0:   # only extend along covers so that blocks are convex chains
                E.add((t,x)); tops[i]=x; break
        else: tops.append(x)
    return E
def R_chain(Efun,h=99): return lambda P: blocks_to_R(P,Efun(P),h)
def family(P,R):
    ds=downsets(P); n,up,dn=P
    bad=[(1<<x,1<<y) for x,y in R]
    V=[]
    for I in ds:
        for I1 in ds:
            if I1&I!=I1 or I1==I: continue
            if any((I&by) and not (I1&bx) for bx,by in bad): continue
            V.append((I1,I))
    return V
def chi_thresholds(V):
    """returns dict k->chi for family V of pairs with size |I|-|I'|"""
    V=sorted(V,key=lambda p:pc(p[0])+pc(p[1]))
    A=np.array([p[0] for p in V],dtype=np.int64); B=np.array([p[1] for p in V],dtype=np.int64)
    s=np.array([pc(p[1])-pc(p[0]) for p in V])
    M=((A[:,None]&A[None,:])==A[:,None])&((B[:,None]&B[None,:])==B[:,None])
    res={}
    for k in range(1,int(s.max())+1):
        idx=np.nonzero(s>=k)[0]; Mk=M[np.ix_(idx,idx)]
        g=np.zeros(len(idx),dtype=np.int64)
        for i in range(len(idx)):
            g[i]=1-int(Mk[:i,i]@g[:i])
        res[k]=int(g.sum())
    return res
def run(name,Rfun,posets,check_chain=False):
    tot=bad=0; ex=None; np_=0
    for P in posets:
        R=Rfun(P); V=family(P,R); np_+=1
        if not V: continue
        if check_chain:
            assert all(all(is_chain(P,c) for c in components(P,p[1]&~p[0])) for p in V)
        for k,chi in chi_thresholds(V).items():
            tot+=1
            if chi!=1:
                bad+=1
                if ex is None: ex=(covers(P),k,chi)
    print(f"{name:34s} posets={np_} (poset,k) cases={tot} failures={bad}",ex if ex else "")
if __name__=="__main__":
    lab=[P for n in range(1,6) for P in labelled_posets(n)]
    print("labelled posets with <=5 points:",len(lab))
    nat6=natural_posets(6)
    rules=[("R=all (antichains)",R_all,False),("R=slab h=2",R_slab(2),False),("R=slab h=3",R_slab(3),False),
           ("R=random p=.5",R_random(.5),False),("R=random p=.2",R_random(.2),False),
           ("chains: mutual min-label covers",R_chain(E_mutual_label),True),
           ("chains<=2: mutual min-label",R_chain(E_mutual_label,2),True),
           ("chains: tight mutual covers",R_chain(E_tight),True),
           ("chains<=3: tight mutual covers",R_chain(E_tight,3),True),
           ("chains: first-fit by height",R_chain(E_firstfit),True)]
    for name,R,cc in rules: run(name+" [lab<=5]",R,lab,cc)
    for name,R,cc in rules[1:]: run(name+" [nat 6]",R,nat6,cc)
