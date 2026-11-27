# Triple-enhanced upper bound (Shearer over triples of chains with exact T3 on a window W).
# h(alpha) <= (at^2/2) * V_K(1/at),  at = alpha + 1/K,
# V_K(l) = sup { Lambda(mu) : mu prob. on {0..K}, mean l },  Lambda(mu) = E F(X,Y) - mu(W) E eta(X),
# and the sup is attained on <=3-point distributions (convexity argument).  eta: any function on W with
# eta(a)+eta(b)+eta(c) <= s(a,b,c) = F(a,b)+F(a,c)+F(b,c)-log2 T3(a,b,c) for all a,b,c in W.
import sys, numpy as np
from math import comb, log2, lgamma, log, floor
from scipy.optimize import linprog
def P(a,b): return comb(a+b,a)*comb(a+b+1,a)//(a+1)
def load_table(fn='t3_table.raw'):
    parts={}
    for line in open(fn):
        a,b,c,M,r,tot,nab=line.split()
        key=(int(a),int(b),int(c)); parts.setdefault(key,{})[int(r)]=(int(M),int(tot))
    T={}
    for k,v in parts.items():
        M=next(iter(v.values()))[0]
        if len(v)==M: T[k]=sum(x[1] for x in v.values())
    return T
def log2int(x):
    # accurate log2 of big int
    sh=max(0,x.bit_length()-60); return log2(x>>sh)+sh
def savings(T,W):
    s={}
    for a in W:
        for b in W:
            for c in W:
                k=tuple(sorted((a,b,c)))
                s[(a,b,c)]=log2int(P(a,b))+log2int(P(a,c))+log2int(P(b,c))-log2int(T[k])
    return s
def Fmat(K):
    x=np.arange(K+1)
    lg=np.array([lgamma(i+1) for i in range(2*K+3)])
    psi=lg[x]+lg[x+1]
    S=x[:,None]+x[None,:]
    return (lg[S]+lg[S+1]-psi[:,None]-psi[None,:])/log(2)
class Bound:
    def __init__(self,K,W,s):
        self.K=K; self.W=sorted(W); self.s=s; self.F=Fmat(K)
        self.inW=np.zeros(K+1); self.inW[self.W]=1
    def Mmat(self,eta):
        e=np.zeros(self.K+1)
        for a,v in zip(self.W,eta): e[a]=v
        return self.F-0.5*(e[:,None]*self.inW[None,:]+self.inW[:,None]*e[None,:])
    def sup(self,l,eta):
        """max of Lambda over <=3-point distributions on {0..K} with mean l; returns (value, support, weights)"""
        K=self.K; M=self.Mmat(eta); best=(-1,None,None)
        xs=range(0,min(K,int(floor(l)))+1)
        for x in xs:
            if x==l:
                v=M[x,x]
                if v>best[0]: best=(v,(x,),(1.0,))
            for y in range(x+1,K+1):
                # two-point x,y (needs y>=l)
                if y>=l:
                    py=(l-x)/(y-x); px=1-py
                    v=px*px*M[x,x]+2*px*py*M[x,y]+py*py*M[y,y]
                    if v>best[0]: best=(v,(x,y),(px,py))
                z=np.arange(y+1,K+1)
                z=z[z>l]
                if len(z)==0: continue
                # p(t): pz=t, py=(l-x-(z-x)t)/(y-x), px=1-t-py
                thi=(l-x)/(z-x)
                tlo=np.zeros(len(z)) if y>=l else (l-y)/(z-y)
                def val(t):
                    py=(l-x-(z-x)*t)/(y-x); px=1-t-py
                    return (px*px*M[x,x]+py*py*M[y,y]+t*t*M[z,z]+2*px*py*M[x,y]+2*px*t*M[x,z]+2*py*t*M[y,z])
                tm=(tlo+thi)/2
                v0=val(tlo); v1=val(tm); v2=val(thi)
                # quadratic through three points on [tlo,thi]; u in [0,1]
                A=2*(v0-2*v1+v2); B=-3*v0+4*v1-v2
                with np.errstate(divide='ignore',invalid='ignore'):
                    u=np.where(A<0,-B/(2*A),0.0)
                u=np.clip(u,0,1)
                vi=A*u*u+B*u+v0
                i=int(np.argmax(vi))
                if vi[i]>best[0]+1e-12:
                    t=tlo[i]+u[i]*(thi[i]-tlo[i]) if not np.isscalar(tlo) else u[i]*thi[i]
                    zz=int(z[i]); py=(l-x-(zz-x)*t)/(y-x)
                    best=(float(vi[i]),(x,y,zz),(1-t-py,py,t))
        return best
    def lam_coeffs(self,supp,wts):
        """Lambda(mu) = EF - sum_a coef_a eta_a ; returns (EF, coef over W)"""
        EF=sum(wi*wj*self.F[i,j] for i,wi in zip(supp,wts) for j,wj in zip(supp,wts))
        mW=sum(wi for i,wi in zip(supp,wts) if self.inW[i])
        coef=[mW*sum(wi for i,wi in zip(supp,wts) if i==a) for a in self.W]
        return EF,coef
    def optimise(self,l,iters=30,verbose=False):
        """cutting-plane: choose eta (feasible for the savings constraints) minimising sup Lambda."""
        W=self.W; nW=len(W)
        A_s=[];b_s=[]
        seen=set()
        for (a,b,c),sv in self.s.items():
            k=tuple(sorted((a,b,c)))
            if k in seen: continue
            seen.add(k)
            row=[0.0]*(nW+1)
            for u in k: row[W.index(u)]+=1
            A_s.append(row); b_s.append(sv)
        cands=[]
        eta=[0.0]*nW
        bestval=None
        for it in range(iters):
            v,supp,wts=self.sup(l,eta)
            if verbose: print("  iter",it,"sup=%.6f"%v,supp,[round(x,4) for x in wts])
            if bestval is None or v<bestval[0]: bestval=(v,list(eta),supp,wts)
            cands.append(self.lam_coeffs(supp,wts))
            A=list(A_s); b=list(b_s)
            for EF,coef in cands:
                A.append([-c for c in coef]+[-1.0]); b.append(-EF)
            res=linprog([0.0]*nW+[1.0],A_ub=A,b_ub=b,bounds=[(0,None)]*nW+[(None,None)])
            if not res.success: break
            neweta=list(res.x[:nW])
            if bestval[0]-res.x[nW]<1e-7: break
            eta=neweta
        return bestval
if __name__=="__main__":
    T=load_table()
    Wmax=int(sys.argv[1]) if len(sys.argv)>1 else 8
    Wmin=int(sys.argv[2]) if len(sys.argv)>2 else 1
    K=int(sys.argv[3]) if len(sys.argv)>3 else 300
    W=list(range(Wmin,Wmax+1))
    s=savings(T,W)
    for a in W: print("l=%d  F=%.4f  log2T3/3=%.4f  s(a,a,a)/3=%.4f  ratio=%.4f"%(a,log2(P(a,a)),log2int(T[(a,a,a)])/3,s[(a,a,a)]/3,log2int(T[(a,a,a)])/3/log2(P(a,a))))
    B=Bound(K,W,s)
    wide=lambda al:(1-al)**2/4
    def h3(al,verbose=False):
        at=al+1/K
        v,eta,supp,wts=B.optimise(1/at,verbose=verbose)
        return at*at/2*v,(v,eta,supp,wts)
    for al in [float(x) for x in sys.argv[4:]] or [0.10,0.11,0.12,0.125,0.13,0.135,0.14,1/7,0.15]:
        h,info=h3(al)
        print("alpha=%.4f h3<=%.5f wide=%.5f  maximiser supp=%s wts=%s eta=%s"%(al,h,wide(al),info[2],[round(x,4) for x in info[3]],[round(x,3) for x in info[1]]),flush=True)
