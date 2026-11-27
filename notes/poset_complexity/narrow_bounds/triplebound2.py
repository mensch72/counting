# Triple-enhanced upper bound with core W0 and satellites W1 (see report for the theorem).
#   Lambda(mu) = E F(X,Y) - sigma*(E[eta;W0]+E[zeta;W1]) + zstar*sigma*(beta-sigma)^+ ,
#   sigma=mu(W0), beta=mu(W1);   constraints on (eta,zeta):
#   (i)  eta(a)+eta(b)+eta(c) <= s(a,b,c)           a,b,c in W0
#   (ii) (eta(a)+eta(b))/2 + zeta(z) <= s(a,b,z)     a,b in W0, z in W1,   0<=zeta<=zstar
#   h(alpha) <= (at^2/2) * sup_{mu on {0..K}, mean 1/at} Lambda(mu),  at = alpha+1/K; sup attained on <=3 points.
import sys, numpy as np
from math import comb, log2, lgamma, log, floor
from scipy.optimize import linprog
def P(a,b): return comb(a+b,a)*comb(a+b+1,a)//(a+1)
def log2int(x):
    sh=max(0,x.bit_length()-60); return log2(x>>sh)+sh
def load_tables(files=('t3_table.raw','t3_sat.raw')):
    T={}
    for fn in files:
        parts={}
        try: lines=open(fn).read().split('\n')
        except FileNotFoundError: continue
        for line in lines:
            if not line.strip(): continue
            a,b,c,M,r,tot,nab=line.split()
            parts.setdefault((int(a),int(b),int(c)),{})[int(r)]=(int(M),int(tot))
        for k,v in parts.items():
            M=next(iter(v.values()))[0]
            if len(v)!=M: continue
            val=sum(x[1] for x in v.values()); ks=tuple(sorted(k))
            if ks in T: assert T[ks]==val,(ks,T[ks],val)
            T[ks]=val
    return T
def sav(T,a,b,c):
    return log2int(P(a,b))+log2int(P(a,c))+log2int(P(b,c))-log2int(T[tuple(sorted((a,b,c)))])
def Fmat(K):
    x=np.arange(K+1)
    lg=np.array([lgamma(i+1) for i in range(2*K+3)])
    psi=lg[x]+lg[x+1]
    S=x[:,None]+x[None,:]
    return (lg[S]+lg[S+1]-psi[:,None]-psi[None,:])/log(2)
class Bound:
    def __init__(self,K,W0,W1,T):
        self.K=K; self.W0=sorted(W0); self.W1=sorted(W1); self.T=T; self.F=Fmat(K)
        self.i0=np.zeros(K+1); self.i0[self.W0]=1
        self.i1=np.zeros(K+1); self.i1[self.W1]=1
        self.vars=[('e',a) for a in self.W0]+[('z',z) for z in self.W1]+['zstar','t']
        nv=len(self.vars); self.A=[]; self.b=[]
        ix={v:i for i,v in enumerate(self.vars)}; self.ix=ix
        W0=self.W0
        for i,a in enumerate(W0):
            for b in W0[i:]:
                for c in W0[W0.index(b):]:
                    row=[0.0]*nv
                    for u in (a,b,c): row[ix[('e',u)]]+=1
                    self.A.append(row); self.b.append(sav(T,a,b,c))
                for z in self.W1:
                    row=[0.0]*nv; row[ix[('e',a)]]+=0.5; row[ix[('e',b)]]+=0.5; row[ix[('z',z)]]+=1
                    self.A.append(row); self.b.append(sav(T,a,b,z))
        for z in self.W1:
            row=[0.0]*nv; row[ix[('z',z)]]=1; row[ix['zstar']]=-1; self.A.append(row); self.b.append(0.0)
    def mats(self,x):
        ix=self.ix; K=self.K
        bar=np.zeros(K+1)
        for a in self.W0: bar[a]=x[ix[('e',a)]]
        for z in self.W1: bar[z]=x[ix[('z',z)]]
        M1=self.F-0.5*(self.i0[:,None]*bar[None,:]+bar[:,None]*self.i0[None,:])
        dd=self.i1-self.i0
        M2=M1+x[ix['zstar']]*0.5*(self.i0[:,None]*dd[None,:]+dd[:,None]*self.i0[None,:])
        return M1,M2
    def sup(self,l,x):
        K=self.K; best=(-1,None,None,None)
        for form,M in enumerate(self.mats(x)):
            for xx in range(0,min(K,int(floor(l)))+1):
                if xx==l and M[xx,xx]>best[0]: best=(M[xx,xx],(xx,),(1.0,),form)
                for y in range(xx+1,K+1):
                    if y>=l:
                        py=(l-xx)/(y-xx); px=1-py
                        v=px*px*M[xx,xx]+2*px*py*M[xx,y]+py*py*M[y,y]
                        if v>best[0]: best=(v,(xx,y),(px,py),form)
                    z=np.arange(max(y+1,int(floor(l))+1),K+1)
                    if len(z)==0: continue
                    thi=(l-xx)/(z-xx)
                    tlo=np.zeros(len(z)) if y>=l else (l-y)/(z-y)
                    def val(t):
                        py=(l-xx-(z-xx)*t)/(y-xx); px=1-t-py
                        return (px*px*M[xx,xx]+py*py*M[y,y]+t*t*M[z,z]+2*px*py*M[xx,y]+2*px*t*M[xx,z]+2*py*t*M[y,z])
                    v0=val(tlo); v1=val((tlo+thi)/2); v2=val(thi)
                    A=2*(v0-2*v1+v2); B=-3*v0+4*v1-v2
                    with np.errstate(divide='ignore',invalid='ignore'):
                        u=np.where(A<0,-B/(2*A),0.0)
                    u=np.clip(u,0,1)
                    vi=A*u*u+B*u+v0
                    i=int(np.argmax(vi))
                    if vi[i]>best[0]+1e-12:
                        t=tlo[i]+u[i]*(thi[i]-tlo[i]); zz=int(z[i]); py=(l-xx-(zz-xx)*t)/(y-xx)
                        best=(float(vi[i]),(xx,y,zz),(float(1-t-py),float(py),float(t)),form)
        return best
    def cut(self,supp,wts,form):
        """Lambda_form(mu) as affine function of the LP variables: returns row,rhs for  Lambda <= t"""
        ix=self.ix; nv=len(self.vars)
        EF=sum(wi*wj*self.F[i,j] for i,wi in zip(supp,wts) for j,wj in zip(supp,wts))
        sg=sum(wi for i,wi in zip(supp,wts) if self.i0[i]); be=sum(wi for i,wi in zip(supp,wts) if self.i1[i])
        row=[0.0]*nv
        for i,wi in zip(supp,wts):
            if self.i0[i]: row[ix[('e',i)]]-=sg*wi
            if self.i1[i]: row[ix[('z',i)]]-=sg*wi
        if form==1: row[ix['zstar']]+=sg*(be-sg)
        row[ix['t']]=-1.0
        return row,-EF
    def optimise(self,l,iters=60,verbose=False):
        nv=len(self.vars)
        x=np.zeros(nv); cuts=[]; best=None
        for it in range(iters):
            v,supp,wts,form=self.sup(l,x)
            if verbose: print("  iter",it,"sup=%.6f"%v,supp,[round(w,4) for w in wts],form,flush=True)
            if best is None or v<best[0]: best=(v,x.copy(),supp,wts,form)
            cuts.append(self.cut(supp,wts,form))
            A=self.A+[c[0] for c in cuts]; b=self.b+[c[1] for c in cuts]
            cost=[0.0]*nv; cost[-1]=1.0
            res=linprog(cost,A_ub=A,b_ub=b,bounds=[(0,None)]*(nv-1)+[(None,None)])
            if not res.success: print("LP fail",res.message); break
            if best[0]-res.x[-1]<1e-6: break
            x=res.x.copy()
        return best
wide=lambda al:(1-al)**2/4
if __name__=="__main__":
    T=load_tables()
    K=int(sys.argv[1]); c0,c1=int(sys.argv[2]),int(sys.argv[3]); Z=int(sys.argv[4])
    W0=list(range(c0,c1+1)); W1=[z for z in range(1,Z+1) if z not in W0]
    B=Bound(K,W0,W1,T)
    def h3(al,verbose=False):
        at=al+1/K
        r=B.optimise(1/at,verbose=verbose)
        return at*at/2*r[0],r
    args=[float(x) for x in sys.argv[5:]]
    if args:
        for al in args:
            h,r=h3(al,verbose=False)
            x=r[1]
            print("alpha=%.5f  h3<=%.5f  wide=%.5f  sup Lambda=%.5f  maximiser %s %s form%d"%(al,h,wide(al),r[0],r[2],[round(w,4) for w in r[3]],r[4]))
            print("    eta=",{a:round(float(x[B.ix[('e',a)]]),3) for a in W0}," zeta=",{z:round(float(x[B.ix[('z',z)]]),3) for z in W1},"zstar=%.3f"%x[B.ix['zstar']],flush=True)
    else:
        lo,hi=0.122,0.15
        for _ in range(14):
            m=(lo+hi)/2
            h,r=h3(m)
            if h<wide(m): lo=m
            else: hi=m
            print("  bisect alpha=%.5f h3=%.5f wide=%.5f"%(m,h,wide(m)),flush=True)
        print("crossing: alpha<=%.5f  c<=%.5f"%(lo,wide(lo)))
