# verify the generalised band construction: every choice gives a strict partial order (and distinct choices differ)
import itertools, random
def seqs(hi,m):
    L=len(hi); H=[0]+list(hi); lo=[H[H[t]] for t in range(L+1)]
    out=[]
    def rec(t,prev,cur):
        if t>m: out.append(tuple(cur)); return
        for d in range(max(prev,lo[t]),H[t]+1): rec(t+1,d,cur+[d])
    rec(1,0,[]); return out
def is_poset(lens,d):
    pts=[(i,t) for i,l in enumerate(lens) for t in range(1,l+1)]
    def lt(x,y):
        (j,s),(i,t)=x,y
        return s<t if i==j else s<=d[(i,j)][t-1]
    for x in pts:
        if lt(x,x): return False
        for y in pts:
            if lt(x,y):
                for z in pts:
                    if lt(y,z) and not lt(x,z): return False
    return True
random.seed(0)
for hi,lens in [((0,1,1,3,3),(5,5)),((0,1,1,3,3,5),(5,6)),((0,1,1,3),(4,4,4)),((0,1,1,3,3),(5,5,5)),((0,1,1,3,3,5),(6,5,6)),((0,1,1,3,3,5,5,7),(8,7,8))]:
    S={l:seqs(hi,l) for l in set(lens)}
    pairs=[(i,j) for i in range(len(lens)) for j in range(len(lens)) if i!=j]
    total=1
    for (i,j) in pairs: total*=len(S[lens[i]])
    if total<=3000: choices=itertools.product(*[S[lens[i]] for (i,j) in pairs])
    else: choices=(tuple(random.choice(S[lens[i]]) for (i,j) in pairs) for _ in range(1500))
    ok=all(is_poset(lens,dict(zip(pairs,ch))) for ch in choices)
    print(hi,lens,"counts per chain length:",{l:len(S[l]) for l in S},"choices",total,"all posets:",ok)
