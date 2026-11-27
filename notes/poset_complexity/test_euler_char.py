import sys
exec(open('test_threshold_and_cubes.py').read().split("# test 1")[0])
from collections import Counter
bad=0; tot=0; vals=Counter()
for n in range(1,6):
    for rel in L[n]:
        ds=downsets(n,rel); mx={I:len(maxel(n,rel,I)) for I in ds}
        w=max(mx.values())
        for k in range(1,w+1):
            V=sorted([I for I in ds if mx[I]>=k], key=lambda I: bin(I).count('1'))
            g={}
            for I in V:
                g[I]=1-sum(g[J] for J in g if J&I==J and J!=I)
            chi=sum(g.values()); tot+=1; vals[chi]+=1
            if chi!=1:
                bad+=1
                if bad<=6: print("chi!=1",n,k,w,sorted(rel),chi)
print("cases",tot,"bad",bad,dict(vals))
