import sys
from lib import *
from collections import Counter
for n in range(3,int(sys.argv[1])+1):
    cache={}
    def sig(up):
        if up not in cache: cache[up]=sigma(up)
        return cache[up]
    c=Counter(); ex={}
    for up in posets(n):
        s=sig(up)
        down=[0]*n
        for i in range(n):
            for j in range(n):
                if up[i]>>j&1: down[j]|=1<<i
        ok=[y for y in range(n) if sig(delete(up,y))<=s]
        mx=[y for y in range(n) if up[y]==0]; mn=[y for y in range(n) if down[y]==0]
        c['some max ok']+= any(y in ok for y in mx)
        c['all max ok']+= all(y in ok for y in mx)
        c['some min ok']+= any(y in ok for y in mn)
        c['some extremal ok']+= any(y in ok for y in mx+mn)
        if not any(y in ok for y in mx) and 'm' not in ex: ex['m']=(up,s,[sig(delete(up,y)) for y in range(n)])
        if not any(y in ok for y in mx+mn) and 'e' not in ex: ex['e']=(up,s,[sig(delete(up,y)) for y in range(n)])
        c['tot']+=1
    print(n,dict(c),ex); sys.stdout.flush()
