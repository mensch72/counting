import pickle
from math import log2
par=pickle.load(open('lower_pareto.pkl','rb'))
def h_low_raw(al):
    # best mixed construction with chain lengths L-1, L where 1/al in [L-1, L]
    l=1/al; best=(0,None)
    for L,pl in par.items():
        if L-1<=l+1e-12<=L+1e-12:
            th=min(1.0,max(0.0,l-(L-1)))
            for c0,c1,hi in pl:
                v=((1-th)*log2(c0)+th*log2(c1))/l**2
                if v>best[0]: best=(v,(L,hi,th))
    return best
def h_low(al):   # monotone hull
    grid=[al]+[1/L for L in par if 1/L<=al]
    return max(h_low_raw(a) for a in grid)
wide=lambda al:(1-al)**2/4
if __name__=="__main__":
    for al in [0.085,0.09,0.1,0.11,0.12,0.125,0.13,0.14,1/7,0.15,1/6,0.18,0.19,0.2,0.22,0.25,0.3,1/3]:
        v,info=h_low(al); print("alpha=%.4f h_low=%.5f a(1-a)=%.5f wide=%.5f %s"%(al,v,al*(1-al),wide(al),info))
    lo,hi=0.1,0.3
    for _ in range(60):
        m=(lo+hi)/2
        if h_low(m)[0]<wide(m): lo=m
        else: hi=m
    print("floor: alpha=%.5f c>=%.5f"%(lo,wide(lo)), h_low(lo))
