# lower bound: w chains of length l; for each ordered pair a threshold sequence d(t) (top element of chain j below x_t of chain i)
# with d nondecreasing and, whenever d(t)>0, a <= t-d(t) <= 2a.  Any choice gives a poset (transitivity: 2a >= offset).
from math import log2
def count(l,a):
    # states d in 0..l ; d(t) allowed: 0 if (t-2a<=0) [nothing below]... d(t)=0 allowed iff t-2a<=0 ; else t-2a<=d<=t-a
    ways={0:1}
    for t in range(1,l+1):
        allowed=[d for d in range(0,l+1) if (d==0 and t-2*a<=0) or (d>=1 and a<=t-d<=2*a)]
        new={}
        for d in allowed:
            s=sum(v for dd,v in ways.items() if dd<=d)
            if s: new[d]=s
        ways=new
    return sum(ways.values())
def h_lower(alpha):
    l=round(1/alpha); best=0
    for a in range(1,l):
        c=count(l,a)
        if c>0: best=max(best,log2(c))
    return best/l**2   # w(w-1) ordered pairs * bits / n^2, n=w*l
for l in range(3,13):
    al=1/l; hl=h_lower(al); print(f"l={l} alpha={al:.4f} lower h={hl:.4f} bits/(x,chain)={hl*l:.3f} upper 2alpha={2*al:.4f} wide cost={(1-al)**2/4:.4f}")
