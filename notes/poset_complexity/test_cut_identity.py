import itertools,sys
from itertools import permutations, combinations
def posets(n):
    pairs=[(i,j) for i in range(n) for j in range(i+1,n)]
    seen=set()
    for bits in range(1<<len(pairs)):
        R=[[False]*n for _ in range(n)]
        for b,(i,j) in enumerate(pairs):
            if bits>>b&1: R[i][j]=True
        if not all(not(R[i][j] and R[j][k]) or R[i][k] for i in range(n) for j in range(i+1,n) for k in range(j+1,n)): continue
        rel=frozenset((i,j) for i in range(n) for j in range(n) if R[i][j])
        key=min(tuple(sorted((p[i],p[j]) for (i,j) in rel)) for p in permutations(range(n)))
        if key in seen: continue
        seen.add(key); yield rel
def sign(perm_on):  # perm_on: dict
    seen=set(); s=1
    for x in perm_on:
        if x in seen: continue
        l=0; y=x
        while y not in seen: seen.add(y); y=perm_on[y]; l+=1
        if l%2==0: s=-s
    return s
for n in range(1,7):
    ok=True; cnt=0
    for rel in posets(n):
        cnt+=1
        aut=[p for p in permutations(range(n)) if frozenset((p[i],p[j]) for (i,j) in rel)==rel]
        ds=[I for I in range(1<<n) if all(not(I>>j&1) or (I>>i&1) for (i,j) in rel)]
        for m in range(1,n+1):
            lab=0; cells=[]
            for I in ds:
                mx=[x for x in range(n) if I>>x&1 and not any((x,y) in rel and I>>y&1 for y in range(n))]
                sz=bin(I).count('1')
                for s in range(1,len(mx)+1):
                    if sz-s<m<=sz:
                        for S in combinations(mx,s):
                            lab+=(-1)**(s-1); cells.append((I,frozenset(S)))
            # unlabelled: orbits of cells, epsilon
            cs=set(cells); unl=0
            while cs:
                I,S=next(iter(cs)); orb=set(); eps=1
                for p in aut:
                    I2=sum(1<<p[x] for x in range(n) if I>>x&1); S2=frozenset(p[x] for x in S)
                    orb.add((I2,S2))
                    if I2==I and S2==S and sign({x:p[x] for x in S})<0: eps=0
                cs-=orb; unl+=eps*(-1)**(len(S)-1)
            if lab!=1 or unl!=1: ok=False; print("FAIL",n,m,sorted(rel),lab,unl)
    print(n,cnt,"all levels ok" if ok else "FAILED")
