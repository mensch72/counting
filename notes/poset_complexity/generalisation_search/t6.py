# (1) naive chain families with componentwise order at n=6;  (2) c(l,a) exponents;  (3) a=1 bands: best chain-union vs width
import random
from math import log2
from functools import lru_cache
from lib import *
from t2 import run,c_chain,c_comp,s_points
from t5 import maxC
run("chains<=2/points",c_chain(2),s_points,'pairs',6)
run("components size<=2/points",c_comp(2),s_points,'canon',6)
def c(l,a):
    @lru_cache(None)
    def f(t,prev):
        if t>l: return 1
        return sum(f(t+1,d) for d in range(max(0,t-2*a,prev),max(0,t-a)+1))
    return f(1,0)
for a in (1,2,3):
    print("a=%d: log2 c(l,a)/l^2 :"%a," ".join("l=%d:%.3f"%(l,log2(c(l,a))/l**2) for l in (3,4,5,6,8,10,12,16)))
rng=random.Random(3)
for w in (3,4,5):
    v=[]
    for _ in range(6):
        P=band(w,3,1,rng); v.append(maxC(P,c_chain(99),downsets(P)))
    print("a=1,l=3,w=%d: max convex chain-union size over 6 random bands:"%w,v)
