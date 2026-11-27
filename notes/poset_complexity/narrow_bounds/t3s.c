// T3(a,b,k) for all k=1..c in one run (exact, unsigned __int128).
// Sum over two-chain posets Q on A u B (pairs d<=e) of the number of weakly increasing k-sequences of types.
// Order-duality halving: Q and its dual have the same multichain counts and (#(b<a),#(a<b)) swapped,
// so Q is taken with weight 2 / 1 / 0 according to #(b<a) > / = / < #(a<b).
// Work splitting: ./t3s a b c M r   handles depth-3 branches with index % M == r.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
typedef unsigned __int128 u128;
int a,b,c,M=1,R=0; int d[32],e[32]; long br=0;
u128 total[40]; unsigned long long nAB=0;
#define NN 14641
static u128 f[NN], g[NN]; static char valid[NN];
int A1,B1;
static inline int idx(int p,int P,int q,int Q){return ((p*A1+P)*B1+q)*B1+Q;}
void eval(int wt){
  nAB++;
  int p,P,q,Q;
  for(p=0;p<=a;p++)for(P=p;P<=a;P++)for(q=0;q<=b;q++)for(Q=q;Q<=b;Q++){
    int ok=1;
    if(p>0 && d[p]>q) ok=0;
    else if(p<a && e[p+1]<q) ok=0;
    else if(P<a && e[P+1]<Q) ok=0;
    else if(P>0 && d[P]>Q) ok=0;
    else if(p>0 && Q<b && e[p]>Q) ok=0;
    else if(q>0 && P<a && d[P+1]<q) ok=0;
    int i=idx(p,P,q,Q); valid[i]=ok; f[i]=ok;
  }
  for(int k=1;;k++){
    u128 s=0;
    for(p=0;p<=a;p++)for(P=p;P<=a;P++)for(q=0;q<=b;q++){ int i0=idx(p,P,q,0); for(Q=q;Q<=b;Q++) s+=f[i0+Q]; }
    total[k]+=s*wt;
    if(k==c) break;
    // 4D prefix sums over the region p<=P, q<=Q (cells outside the region are never written and stay 0)
    for(p=0;p<=a;p++)for(P=p;P<=a;P++)for(q=0;q<=b;q++){ int i0=idx(p,P,q,0); for(Q=q+1;Q<=b;Q++) f[i0+Q]+=f[i0+Q-1]; }
    for(p=0;p<=a;p++)for(P=p;P<=a;P++)for(q=1;q<=b;q++){ int i0=idx(p,P,q,0); for(Q=q;Q<=b;Q++) f[i0+Q]+=f[i0+Q-B1]; }
    for(p=0;p<=a;p++)for(P=p+1;P<=a;P++)for(q=0;q<=b;q++){ int i0=idx(p,P,q,0); for(Q=q;Q<=b;Q++) f[i0+Q]+=f[i0+Q-B1*B1]; }
    for(p=1;p<=a;p++)for(P=p;P<=a;P++)for(q=0;q<=b;q++){ int i0=idx(p,P,q,0); for(Q=q;Q<=b;Q++) f[i0+Q]+=f[i0+Q-B1*B1*A1]; }
    for(p=0;p<=a;p++)for(P=p;P<=a;P++)for(q=0;q<=b;q++){ int i0=idx(p,P,q,0); for(Q=q;Q<=b;Q++) if(!valid[i0+Q]) g[i0+Q]=f[i0+Q], f[i0+Q]=0; }
    // NOTE: prefix sums must be taken over the *unmasked* previous f; masking afterwards is what the recursion needs:
    // f_{k+1}(tau') = [tau' valid] * sum_{tau<=tau'} f_k(tau), and f_k is zero on invalid cells already.
  }
}
void rec(int t,int sd,int se){
  if(t>a){ int x=sd, y=a*b-se; if(x>y) eval(2); else if(x==y) eval(1); return; }
  if(t==4 || (a<4 && t==a)){ if((br++)%M!=R) return; }
  for(int dd=d[t-1];dd<=b;dd++){ d[t]=dd;
    int lo = e[t-1]>dd?e[t-1]:dd;
    for(int ee=lo;ee<=b;ee++){ e[t]=ee; rec(t+1,sd+dd,se+ee);} }
}
void pr(u128 x){ char s[64]; int i=63; s[i]=0; if(!x){printf("0");return;} while(x){s[--i]='0'+(int)(x%10); x/=10;} printf("%s",s+i);}
int main(int argc,char**argv){
  a=atoi(argv[1]);b=atoi(argv[2]);c=atoi(argv[3]); if(argc>5){M=atoi(argv[4]);R=atoi(argv[5]);}
  A1=a+1;B1=b+1; d[0]=0;e[0]=0; memset(f,0,sizeof f); rec(1,0,0);
  for(int k=1;k<=c;k++){ printf("%d %d %d %d %d ",a,b,k,M,R); pr(total[k]); printf(" %llu\n",nAB); }
  return 0;
}
