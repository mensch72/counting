// T3(a,b,c): number of partial orders on the disjoint union of three chains A,B,C (lengths a,b,c)
// in which each chain keeps its order. Sum over two-chain posets (d<=e) of the number of weakly increasing
// c-sequences of "types" (p,P,q,Q). Exact arithmetic in unsigned __int128.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
typedef unsigned __int128 u128;
int a,b,c; int d[32],e[32];
u128 total=0; unsigned long long nAB=0;
static u128 f[20*20*20*20], g[20*20*20*20]; static char valid[20*20*20*20];
static inline int idx(int p,int P,int q,int Q){return ((p*(a+1)+P)*(b+1)+q)*(b+1)+Q;}
void eval(void){
  nAB++;
  int p,P,q,Q;
  for(p=0;p<=a;p++)for(P=0;P<=a;P++)for(q=0;q<=b;q++)for(Q=0;Q<=b;Q++){
    int ok = p<=P && q<=Q;
    if(ok && p>0 && d[p]>q) ok=0;
    if(ok && p<a && e[p+1]<q) ok=0;
    if(ok && P<a && e[P+1]<Q) ok=0;
    if(ok && P>0 && d[P]>Q) ok=0;
    if(ok && p>0 && Q<b && e[p]>Q) ok=0;
    if(ok && q>0 && P<a && d[P+1]<q) ok=0;
    valid[idx(p,P,q,Q)]=ok; f[idx(p,P,q,Q)]=ok;
  }
  for(int k=1;k<c;k++){
    // g = 4D prefix sum of f, then mask
    memcpy(g,f,sizeof(u128)*(a+1)*(a+1)*(b+1)*(b+1));
    for(p=0;p<=a;p++)for(P=0;P<=a;P++)for(q=0;q<=b;q++)for(Q=1;Q<=b;Q++) g[idx(p,P,q,Q)]+=g[idx(p,P,q,Q-1)];
    for(p=0;p<=a;p++)for(P=0;P<=a;P++)for(q=1;q<=b;q++)for(Q=0;Q<=b;Q++) g[idx(p,P,q,Q)]+=g[idx(p,P,q-1,Q)];
    for(p=0;p<=a;p++)for(P=1;P<=a;P++)for(q=0;q<=b;q++)for(Q=0;Q<=b;Q++) g[idx(p,P,q,Q)]+=g[idx(p,P-1,q,Q)];
    for(p=1;p<=a;p++)for(P=0;P<=a;P++)for(q=0;q<=b;q++)for(Q=0;Q<=b;Q++) g[idx(p,P,q,Q)]+=g[idx(p-1,P,q,Q)];
    int n=(a+1)*(a+1)*(b+1)*(b+1);
    for(int i=0;i<n;i++) f[i]=valid[i]?g[i]:0;
  }
  int n=(a+1)*(a+1)*(b+1)*(b+1); u128 s=0;
  if(c==0) s=1; else for(int i=0;i<n;i++) s+=f[i];
  total+=s;
}
void rec(int t){
  if(t>a){eval();return;}
  for(int dd=d[t-1];dd<=b;dd++){ d[t]=dd;
    int lo = e[t-1]>dd?e[t-1]:dd;
    for(int ee=lo;ee<=b;ee++){ e[t]=ee; rec(t+1);} }
}
void pr(u128 x){ char s[64]; int i=63; s[i]=0; if(!x){puts("0");return;} while(x){s[--i]='0'+(int)(x%10); x/=10;} printf("%s",s+i);}
int main(int argc,char**argv){
  a=atoi(argv[1]);b=atoi(argv[2]);c=atoi(argv[3]);
  d[0]=0;e[0]=0; rec(1);
  printf("T3(%d,%d,%d) = ",a,b,c); pr(total);
  long double lg=logl((long double)total)/logl(2.0L);
  printf("  log2=%.6Lf  nAB=%llu\n",lg,nAB);
  return 0;
}
