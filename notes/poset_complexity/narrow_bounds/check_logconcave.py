# Test, on all computed values, the two inequalities that would make balanced profiles extremal for the triple bound:
# (1') T3(a+1,b,c)*T3(a-1,b,c) <= T3(a,b,c)^2  (a>=1; T3(0,b,c)=P(b,c))
# (2') T3(a-1,b+1,c) >= T3(a,b,c) for a>b
from triplebound2 import load_tables, P
T=load_tables()
def t3(a,b,c):
    k=tuple(sorted((a,b,c)))
    if k[0]==0: return P(k[1],k[2])
    return T.get(k)
n1=n2=0; bad=[]
R=range(0,17)
for a in R:
    for b in R:
        for c in R:
            x,y,z=t3(a+1,b,c),t3(a,b,c),(t3(a-1,b,c) if a>=1 else None)
            if a>=1 and None not in (x,y,z):
                n1+=1
                if x*z>y*y: bad.append(('1',a,b,c))
            if a>b:
                u,v=t3(a-1,b+1,c),t3(a,b,c)
                if None not in (u,v):
                    n2+=1
                    if u<v: bad.append(('2',a,b,c))
print("checked (1'):",n1,"cases; (2'):",n2,"cases; violations:",bad[:10],len(bad))
