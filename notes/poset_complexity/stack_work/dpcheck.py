# (1) check the "dead element" lemma for the rank-ordered build of a poset:
#     X_r = {x : |down(x)| < r}, b = |X_r|, z in X_r is dead if |up(z) ∩ X_r| >= b - r + 2;
#     claim: a dead z lies below every element outside X_r.
# (2) check the state bound: live z and any x in X_r satisfy |up_X(z)| + |down(x)| <= b.
import sys
from lib import posets
bad=0; tot=0
for n in range(2,int(sys.argv[1])+1):
    for up in posets(n):
        dn=[0]*n
        for i in range(n):
            for j in range(n):
                if up[i]>>j&1: dn[j]|=1<<i
        ds=[bin(dn[x]).count('1')+1 for x in range(n)]
        for r in range(1,n+2):
            X=[x for x in range(n) if ds[x]<r]; b=len(X); Xm=sum(1<<x for x in X)
            for z in X:
                u=bin(up[z]&Xm).count('1')+1
                tot+=1
                if u>=b-r+2:
                    if any(not (up[z]>>y&1) for y in range(n) if y not in X): bad+=1
                else:
                    if any(u+ds[x]>b for x in X): bad+=1
    print(n,"checks",tot,"violations",bad); sys.stdout.flush()
