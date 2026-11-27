import sys
from lib import *
from collections import Counter
for n in range(2,int(sys.argv[1])+1):
    cache={}
    def sig(up):
        if up not in cache: cache[up]=sigma(up)
        return cache[up]
    bad=0; tot=0; worst=Counter(); dist=Counter()
    for up in posets(n):
        s=sig(up); tot+=1; dist[s]+=1
        ds=[sig(delete(up,y)) for y in range(n)]
        mn=min(ds)
        worst[mn-s]+=1
        if mn>s:
            bad+=1
            if bad<=3: print("  counterexample",n,up,s,ds)
    print(n,"posets",tot,"min_y sigma(P-y)-sigma(P):",dict(worst),"sigma dist",dict(sorted(dist.items()))); sys.stdout.flush()
