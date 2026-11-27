exec(open('test_threshold_and_cubes.py').read().split("# test 1")[0])
from collections import Counter
def is_ca(n,rel,S):
    el=[x for x in range(n) if S>>x&1]
    comp=lambda a,b: (a,b) in rel or (b,a) in rel
    for a in el:
        for b in el:
            for c in el:
                if len({a,b,c})==3 and comp(a,b) and comp(a,c) and not comp(b,c): return False
    return True
vals=Counter(); bad=[]
for n in range(1,6):
    for rel in L[n]:
        ds=downsets(n,rel)
        pairs=[(I1,I) for I in ds for I1 in ds if I1&I==I1 and I1!=I and is_ca(n,rel,I&~I1)]
        mx=max(bin(I&~I1).count('1') for I1,I in pairs)
        for k in range(1,mx+1):
            V=[p for p in pairs if bin(p[1]&~p[0]).count('1')>=k]
            V.sort(key=lambda p: bin(p[0]).count('1')+bin(p[1]).count('1'))
            g={}
            for p in V:
                g[p]=1-sum(v for q,v in g.items() if q!=p and q[0]&p[0]==q[0] and q[1]&p[1]==q[1])
            chi=sum(g.values()); vals[chi]+=1
            if chi!=1 and len(bad)<5: bad.append((n,k,sorted(rel),chi))
print(dict(vals)); print(bad)
