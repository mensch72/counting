# Generalised band lower bound.  hi: [L]->{0..L-1} nondecreasing, hi(t)<t.  lo = hi o hi.
# c_m(hi) = #{nondecreasing d:[m]->Z, lo(t)<=d(t)<=hi(t)}.  Posets: chains of lengths in {L-1,L}.
import sys
from math import log2
def search(L):
    best={}  # pareto list of (c_{L-1}, c_L, hi)
    res=[]
    hi=[0]*(L+1)
    def rec(t,ways,cprev):
        # ways: dict d->count for d(t-1)
        if t>L:
            res.append((cprev,sum(ways.values()),tuple(hi[1:])));return
        for h in range(hi[t-1],t):
            hi[t]=h; lo=hi[h]
            new={}
            acc=0
            keys=sorted(ways)
            ki=0
            for d in range(0,h+1):
                while ki<len(keys) and keys[ki]<=d: acc+=ways[keys[ki]]; ki+=1
                if d>=lo and acc: new[d]=acc
            if new: rec(t+1,new,sum(ways.values()))
    rec(1,{0:1},1)
    # pareto
    res.sort(key=lambda r:(-r[0],-r[1]))
    par=[];bm=-1
    for r in res:
        if r[1]>bm: par.append(r); bm=r[1]
    return par
if __name__=="__main__":
    Lmax=int(sys.argv[1]) if len(sys.argv)>1 else 11
    import pickle
    out={}
    for L in range(2,Lmax+1):
        par=search(L); out[L]=par
        b=max(par,key=lambda r:r[1])
        print(L, "best c_L=",b[1],"bits=%.4f"%log2(b[1]),"h=%.5f"%(log2(b[1])/L**2),"a(1-a)=%.5f"%((L-1)/L**2),"hi=",b[2],"pareto size",len(par),flush=True)
    pickle.dump(out,open('lower_pareto.pkl','wb'))
