# value of the triple (Shearer) bound on BALANCED profiles only (not a proven bound: assumes balanced profiles are extremal)
from triplebound import *
from itertools import product
T=load_table(); W=list(range(1,9)); s=savings(T,W)
def hbal(al):
    l=1/al; q=floor(l+1e-12); th=l-q
    if th<1e-9: mu={q:1.0}
    elif q+1>8: return None
    else: mu={q:1-th,q+1:th}
    EF=sum(mu[x]*mu[y]*log2(P(x,y)) for x in mu for y in mu)
    Es=sum(mu[x]*mu[y]*mu[z]*s[(x,y,z)] for x in mu for y in mu for z in mu)
    return al*al/2*(EF-Es/3)
wide=lambda al:(1-al)**2/4
lo,hi=0.126,0.25
for _ in range(60):
    m=(lo+hi)/2
    if hbal(m)<wide(m): lo=m
    else: hi=m
print("balanced-profile triple value crossing: alpha=%.5f c=%.5f l=%.4f"%(lo,wide(lo),1/lo))
if __name__=="__main__":
    for al in [0.125,0.13,0.134682,0.135,0.14,1/7,0.15,1/6,0.2,0.25,1/3,0.5]:
        print("alpha=%.4f  balanced h3=%.5f  wide=%.5f"%(al,hbal(al),wide(al)))
