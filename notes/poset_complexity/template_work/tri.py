# Templates on m chains of length l: for each ordered pair (i,j) an upper envelope hi_ij:[1..l]->[0..l] (monotone);
# lower envelope lo_ik(t) = max over j of hi_jk(hi_ij(t));  admissible d: monotone, lo<=d<=hi.
# Validity: hi_ji(hi_ij(t)) < t (no cycles), lo<=hi.  Entropy = sum over ordered pairs log2 #admissible.
# Heuristic search for the max entropy per unordered pair, compared with the uniform band value and the pair count.
import random, sys
from math import log2, comb
def count(lo,hi,l):
    ways={0:1}
    for t in range(1,l+1):
        if lo[t]>hi[t]: return 0
        new={}
        for d in range(lo[t],hi[t]+1):
            s=sum(v for dd,v in ways.items() if dd<=d)
            if s: new[d]=s
        if not new: return 0
        ways=new
    return sum(ways.values())
def entropy(H,m,l):
    tot=0.0
    for i in range(m):
        for k in range(m):
            if i==k: continue
            hik=H[i][k]
            # cycle condition
            hki=H[k][i]
            for t in range(1,l+1):
                if hki[hik[t]]>=t: return None
            lo=[0]*(l+1)
            for j in range(m):
                if j==i or j==k: continue
                for t in range(1,l+1):
                    v=H[j][k][H[i][j][t]]
                    if v>lo[t]: lo[t]=v
            c=count(lo,hik,l)
            if c==0: return None
            tot+=log2(c)
    return tot
def rand_hi(l):
    h=[0]; cur=0
    for t in range(1,l+1):
        cur=random.randint(cur,t-1); h.append(cur)
    return h
def search(m,l,iters,seed):
    random.seed(seed)
    best=None; bestH=None
    for restart in range(iters//2000+1):
        while True:
            H=[[rand_hi(l) if i!=j else None for j in range(m)] for i in range(m)]
            e=entropy(H,m,l)
            if e is not None: break
        T=1.0
        for it in range(2000):
            i,j=random.sample(range(m),2); t=random.randint(1,l); old=H[i][j][:]
            new=old[:]; new[t]=max(0,min(l,old[t]+random.choice((-1,1))))
            # keep monotone
            for s in range(t+1,l+1): new[s]=max(new[s],new[t])
            for s in range(1,t): new[s]=min(new[s],new[t])
            H[i][j]=new
            e2=entropy(H,m,l)
            if e2 is None or (e2<e and random.random()>2**((e2-e)/T)): H[i][j]=old
            else: e=e2
            T=max(0.02,T*0.998)
            if best is None or e>best: best=e; bestH=[[h[:] if h else None for h in row] for row in H]
    return best,bestH
m=int(sys.argv[1])
for l in range(2,int(sys.argv[2])+1):
    b,H=search(m,l,int(sys.argv[3]),1)
    pairs=m*(m-1)/2
    P=comb(2*l,l)*comb(2*l+1,l)//(l+1)
    print(f"m={m} l={l}: best template entropy per unordered pair {b/pairs:.3f} bits; pair count log2 P(l,l)={log2(P):.3f}")
    print("   ",[[h[1:] if h else None for h in row] for row in H]); sys.stdout.flush()
