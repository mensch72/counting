# independent check of T3(a,b,c) for a+b+c<=6: enumerate all labelled posets on [n], count those in which
# the three prescribed blocks are chains in the prescribed order.
import subprocess
def all_posets(n):
    out=[]
    def rec(m,below,above):
        if m==n: out.append(tuple(below)); return
        for D in range(1<<m):
            if any((D>>i)&1 and (below[i]&~D) for i in range(m)): continue
            for U in range(1<<m):
                if U&D: continue
                if any((U>>i)&1 and (above[i]&~U) for i in range(m)): continue
                if any((D>>i)&1 and (U&~above[i]) for i in range(m)): continue
                nb=[below[i]|((1<<m) if (U>>i)&1 else 0) for i in range(m)]+[D]
                na=[above[i]|((1<<m) if (D>>i)&1 else 0) for i in range(m)]+[U]
                rec(m+1,nb,na)
    rec(0,[],[])
    return out
cache={}
for (a,b,c) in [(1,1,1),(2,1,1),(2,2,1),(2,2,2),(3,2,1),(4,1,1),(3,3,0),(2,2,0),(3,1,1),(1,2,3)]:
    n=a+b+c
    if n not in cache: cache[n]=all_posets(n)
    blocks=[list(range(0,a)),list(range(a,a+b)),list(range(a+b,n))]
    need=[(blk[i],blk[i+1]) for blk in blocks for i in range(len(blk)-1)]
    cnt=sum(all((below[y]>>x)&1 for x,y in need) for below in cache[n])
    if min(a,b,c)>0:
        r=subprocess.run(['./t3',str(a),str(b),str(c)],capture_output=True,text=True).stdout.split()[2]
    else: r='(pair formula)'
    print((a,b,c),cnt,r)
