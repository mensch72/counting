import itertools, sys
from math import comb
from itertools import combinations, product
def labelled(n):
    pairs=[(i,j) for i in range(n) for j in range(i+1,n)]
    out=[]
    for st in product((0,1,2),repeat=len(pairs)):
        rel=set()
        for (i,j),s in zip(pairs,st):
            if s==1: rel.add((i,j))
            elif s==2: rel.add((j,i))
        if all((a,d) in rel for (a,b) in rel for (c,d) in rel if b==c): out.append(frozenset(rel))
    return out
def downsets(n,rel): return [I for I in range(1<<n) if all(not(I>>j&1) or (I>>i&1) for (i,j) in rel)]
def maxel(n,rel,I): return [x for x in range(n) if I>>x&1 and not any((x,y) in rel and I>>y&1 for y in range(n))]
L={n:labelled(n) for n in range(0,6)}
print({n:len(L[n]) for n in L})
# test 1: threshold identity for |min P|>=k via product formula
for n in range(1,6):
    for k in range(1,n+1):
        brute=sum(1 for rel in L[n] if sum(1 for x in range(n) if not any(b==x for (a,b) in rel))>=k)
        form=0
        for j in range(k,n+1):
            s=sum(len(downsets(n-j,rel))**j for rel in L[n-j])  # up-sets count = down-sets count
            form+=(-1)**(j-k)*comb(j-1,k-1)*comb(n,j)*s
        if brute!=form: print("T1 FAIL",n,k,brute,form)
print("test1 done")
# test 2: chi of X_k (cubes [I\S,I] with all vertices having >=k maximal elements)
bad=0; tot=0
for n in range(1,6):
    for rel in L[n]:
        ds=downsets(n,rel); mx={I:maxel(n,rel,I) for I in ds}
        w=max(len(v) for v in mx.values())
        for k in range(1,w+1):
            chi=0
            for I in ds:
                M=mx[I]
                if len(M)<k: continue
                for s in range(0,len(M)+1):
                    for S in combinations(M,s):
                        ok=True
                        for r in range(1,s+1):
                            for R in combinations(S,r):
                                J=I
                                for x in R: J&=~(1<<x)
                                if len(mx[J])<k: ok=False;break
                            if not ok:break
                        if ok: chi+=(-1)**s
            tot+=1
            if chi!=1:
                bad+=1
                if bad<=5: print("chi!=1",n,k,sorted(rel),chi)
print("test2: cases",tot,"bad",bad)
