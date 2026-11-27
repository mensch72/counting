# objects: pairs (I',I) of down-sets, S=I\I', or convex sets S; several constraints/sizes/orders
import sys
from lib import *
from collections import Counter
def upset(P,S):
    n,up,dn=P; r=S
    for x in bits(S): r|=up[x]
    return r
def dnset(P,S):
    n,up,dn=P; r=S
    for x in bits(S): r|=dn[x]
    return r
def height(P,S):
    h=0
    while S: S&=~maxset(P,S); h+=1
    return h
def c_chain(h): return lambda P,S: all(is_chain(P,c) and pc(c)<=h for c in components(P,S))
def c_height(h): return lambda P,S: height(P,S)<=h
def c_comp(c): return lambda P,S: all(pc(x)<=c for x in components(P,S))
def c_tree(h):  # every element has a chain above it inside S (down-branching forest), height<=h
    def f(P,S):
        n,up,dn=P
        return height(P,S)<=h and all(is_chain(P,up[x]&S) for x in bits(S))
    return f
def c_chain_distinct(h):
    # chains of length<=h whose tops have pairwise different strict down-sets in P\S... (private lower part)
    def f(P,S):
        n,up,dn=P
        cs=components(P,S)
        if not all(is_chain(P,c) and pc(c)<=h for c in cs): return False
        ds=[dnset(P,c)&~c for c in cs]
        return all(not(pc(cs[i])>1 and pc(cs[j])>1 and ds[i]&ds[j]) for i in range(len(cs)) for j in range(i))
    return f
s_points=lambda P,S: pc(S)
s_comps=lambda P,S: len(components(P,S))
def run(name,constraint,size,mode,N,posets=None,show=1):
    tot=bad=0; ex=[]; vals=Counter()
    for n in range(1,N+1):
        for P in (posets(n) if posets else natural_posets(n)):
            ds=downsets(P)
            if mode=='pairs':   # all pairs (I',I), componentwise order
                V=[(I1,I) for I in ds for I1 in ds if I1&I==I1 and I1!=I and constraint(P,I&~I1)]
                sz={p:size(P,p[1]&~p[0]) for p in V}
                key=lambda p:pc(p[0])+pc(p[1]); leq=lambda a,b:a[0]&b[0]==a[0] and a[1]&b[1]==a[1]
            elif mode=='EM':    # convex sets S=(downset,upset), Egli-Milner order
                Ss=set(I&~I1 for I in ds for I1 in ds if I1&I==I1 and I1!=I and constraint(P,I&~I1))
                V=[(dnset(P,S),upset(P,S),S) for S in Ss]
                sz={p:size(P,p[2]) for p in V}
                key=lambda p:pc(p[0])-pc(p[1]); leq=lambda a,b:a[0]&b[0]==a[0] and a[1]&b[1]==b[1]
            elif mode=='canon': # convex sets S as canonical pair (dn(S)\S, dn(S)), componentwise
                Ss=set(I&~I1 for I in ds for I1 in ds if I1&I==I1 and I1!=I and constraint(P,I&~I1))
                V=[(dnset(P,S)&~S,dnset(P,S),S) for S in Ss]
                sz={p:size(P,p[2]) for p in V}
                key=lambda p:pc(p[0])+pc(p[1]); leq=lambda a,b:a[0]&b[0]==a[0] and a[1]&b[1]==a[1]
            elif mode=='top':   # pairs with S an up-set of I given... order by I only on pairs (I',I) with I' maximal? -> use S=(I\I') ordered by (I subset, then I' superset)
                V=[(I1,I) for I in ds for I1 in ds if I1&I==I1 and I1!=I and constraint(P,I&~I1)]
                sz={p:size(P,p[1]&~p[0]) for p in V}
                key=lambda p:pc(p[1])*100-pc(p[0]); leq=lambda a,b:a[1]&b[1]==a[1] and a[0]&b[0]==b[0]
            if not V: continue
            for k in range(1,max(sz.values())+1):
                W=sorted([p for p in V if sz[p]>=k],key=key)
                chi=euler(W,leq); tot+=1; vals[chi]+=1
                if chi!=1:
                    bad+=1
                    if len(ex)<show: ex.append((n,k,covers(P),chi,[tuple(bits(z) for z in p) for p in W][:8]))
    print(f"{name:32s} mode={mode:6s} N={N} cases={tot} bad={bad} chi-values={dict(sorted(vals.items()))}")
    for e in ex: print("     smallest failure:",e)
    return bad
if __name__=="__main__":
    N=int(sys.argv[1]) if len(sys.argv)>1 else 5
    for mode in ['pairs','canon','EM','top']:
        run("antichain/points",c_chain(1),s_points,mode,N)
        for h in [2,3,9]:
            run(f"chains<={h}/points",c_chain(h),s_points,mode,N)
        run("chains<=9/components",c_chain(9),s_comps,mode,N)
        run("chains<=2/components",c_chain(2),s_comps,mode,N)
        for h in [2,3]:
            run(f"slab height<={h}/points",c_height(h),s_points,mode,N)
            run(f"forest height<={h}/points",c_tree(h),s_points,mode,N)
        for c in [2,3]:
            run(f"components size<={c}/points",c_comp(c),s_points,mode,N)
        run("private chains<=3/points",c_chain_distinct(3),s_points,mode,N)
