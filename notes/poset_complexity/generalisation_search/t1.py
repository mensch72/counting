# size functions on down-sets, family {I: f(I)>=k} ordered by inclusion
import sys
from lib import *
from collections import Counter
def f_max(P,I,h): return maxset(P,I)
def f_forest(P,I,h):
    n,up,dn=P; S=0
    for x in bits(I):
        U=(up[x]&I)|1<<x
        if pc(U)<=h and is_chain(P,U): S|=1<<x
    return S
def f_trunk(P,I,h):
    n,up,dn=P; F=f_forest(P,I,h); S=0
    for m in bits(maxset(P,I)):
        c=m
        while True:
            S|=1<<c
            ch=[x for x in bits(dn[c]&F) if (up[x]&I&dn[c])==0]  # children in forest
            if len(ch)!=1: break
            c=ch[0]
    return S
def f_pathcomp(P,I,h):
    # components of forest that are chains, else only root
    F=f_forest(P,I,h); S=0
    for c in components(P,F):
        S|= c if is_chain(P,c) else maxset(P,c)
    return S
def f_levels(P,I,h):
    S=0;J=I
    for _ in range(h):
        m=maxset(P,J); S|=m; J&=~m
    return S
def f_strict(P,I,h):
    # x in I with up-set in I a chain of size<=h AND all elements of I below-or-incomparable... : chain c1>..>cj with each c_{i+1} the unique lower cover within I of c_i
    n,up,dn=P; S=0
    for m in bits(maxset(P,I)):
        c=m; j=0
        while j<h:
            S|=1<<c; j+=1
            lc=[x for x in bits(dn[c]) if up[x]&dn[c]==0]
            if len(lc)!=1: break
            x=lc[0]
            if pc(up[x]&I)!=j: break
            c=x
    return S
FUNS=dict(max=f_max,forest=f_forest,trunk=f_trunk,pathcomp=f_pathcomp,levels=f_levels,strict=f_strict)
def test(name,h,N,verbose=2):
    f=FUNS[name]; tot=bad=0; sub=0; ex=[]
    for n in range(1,N+1):
        for P in natural_posets(n):
            ds=downsets(P); sz={I:pc(f(P,I,h)) for I in ds}
            if not sub:
                for I1 in ds:
                    for I2 in ds:
                        if sz[I1|I2]+sz[I1&I2]<sz[I1]+sz[I2]: sub=(rels(P),I1,I2)
            for k in range(1,max(sz.values())+1):
                V=sorted([I for I in ds if sz[I]>=k],key=pc)
                chi=euler(V,lambda a,b:a&b==a); tot+=1
                if chi!=1:
                    bad+=1
                    if len(ex)<verbose: ex.append((n,k,covers(P),chi,[(bits(I),sz[I]) for I in V]))
    print(name,"h=",h,"N=",N,"cases",tot,"bad",bad,"submod-violation",sub)
    for e in ex: print("   ",e)
if __name__=="__main__":
    N=int(sys.argv[1]) if len(sys.argv)>1 else 5
    for name in FUNS:
        for h in ([1] if name=='max' else [2,3,9]):
            test(name,h,N)
