# symmetry obstruction: X = convex sets S whose components are chains with <=h points, |S|>=k.
# If Aut(P) acts transitively on X and |X|>=2, every Aut-invariant partial order on X is an antichain => chi=|X|!=1.
import itertools,sys
from lib import *
from t2 import c_chain,c_comp,c_tree
def auts(P):
    n,up,dn=P; R=set(rels(P)); out=[]
    for p in itertools.permutations(range(n)):
        if all((p[x],p[y]) in R for x,y in R): out.append(p)
    return out
def img(p,S): 
    r=0
    for x in bits(S): r|=1<<p[x]
    return r
def run(name,constraint,N):
    tot=obs=0; ex=None
    for n in range(1,N+1):
        for P in natural_posets(n):
            ds=downsets(P)
            Ss=set(I&~I1 for I in ds for I1 in ds if I1&I==I1 and I1!=I and constraint(P,I&~I1))
            A=auts(P)
            for k in range(1,max(map(pc,Ss))+1):
                X=[S for S in Ss if pc(S)>=k]; tot+=1
                if len(X)>=2 and len(set(img(p,X[0]) for p in A))==len(X):
                    obs+=1
                    if ex is None: ex=(covers(P),k,[bits(S) for S in X])
    print(f"{name:28s} N<={N}: (poset,k) cases={tot}, transitive-orbit obstructions={obs}; first:",ex)
N=int(sys.argv[1]) if len(sys.argv)>1 else 6
for h in [2,3,9]: run(f"chains<={h}",c_chain(h),N)
for c in [2,3,4]: run(f"components size<={c}",c_comp(c),N)
for h in [2,3]: run(f"down-forests height<={h}",c_tree(h),N)
