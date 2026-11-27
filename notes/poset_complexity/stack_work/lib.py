import subprocess, itertools
def posets(n):
    """unlabelled posets on n points as tuples lt[i] = bitmask of elements strictly above i"""
    out=subprocess.run(['nauty-genposetg',str(n),'t','q'],capture_output=True,text=True).stdout.split()
    res=[]
    for line in out:
        assert line[0]=='&'
        m=ord(line[1])-63; bits=[]
        for ch in line[2:]:
            v=ord(ch)-63
            bits+= [(v>>k)&1 for k in range(5,-1,-1)]
        up=[0]*m
        for i in range(m):
            for j in range(m):
                if bits[i*m+j]: up[i]|=1<<j
        # transitive closure
        ch=True
        while ch:
            ch=False
            for i in range(m):
                u=up[i]; nu=u
                for j in range(m):
                    if u>>j&1: nu|=up[j]
                if nu!=u: up[i]=nu; ch=True
        res.append(tuple(up))
    return res
def delete(up,y):
    n=len(up); idx=[i for i in range(n) if i!=y]
    new=[]
    for i in idx:
        u=0
        for k,j in enumerate(idx):
            if up[i]>>j&1: u|=1<<k
        new.append(u)
    return tuple(new)
def sigma(up, return_layers=False):
    n=len(up); full=(1<<n)-1
    down=[0]*n
    for i in range(n):
        for j in range(n):
            if up[i]>>j&1: down[j]|=1<<i
    ds=[I for I in range(1<<n) if all((not I>>j&1) or (down[j]&~I)==0 for j in range(n))]
    ds.sort(key=lambda I: bin(I).count('1'))
    def maxs(I): return [x for x in range(n) if I>>x&1 and not (up[x]&I)]
    def B(A):  # elements of A below everything outside A
        out=full&~A; b=0
        for x in range(n):
            if A>>x&1 and (up[x]&out)==out: b|=1<<x
        return b
    best={}; g={}
    bysize={}
    for I in ds: bysize.setdefault(bin(I).count('1'),[]).append(I)
    done=[]
    for s in sorted(bysize):
        for I in bysize[s]:
            M=maxs(I); b=0
            for r in range(1,len(M)+1):
                for S in itertools.combinations(M,r):
                    Ip=I
                    for x in S: Ip&=~(1<<x)
                    v=r+g[Ip]
                    if v>b: b=v
            best[I]=b
        for A in bysize[s]:
            bA=B(A); m=0
            for J in done+bysize[s]:
                if J&~bA==0 and best[J]>m: m=best[J]
            g[A]=m
        done+=bysize[s]
    return max(best.values()) if best else 0
