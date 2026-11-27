from math import log2
def s(al):
    best=9
    for i in range(1,4999):
        t=i/10000
        v=al*log2(1/t)+al*al*log2(1+t*t/(1-2*t))
        best=min(best,v)
    return best
lo,hi=0.05,0.3
for _ in range(50):
    m=(lo+hi)/2
    if s(m)<(1-m)**2/4: lo=m
    else: hi=m
print("crossing alpha",lo,"exponent",s(lo))
