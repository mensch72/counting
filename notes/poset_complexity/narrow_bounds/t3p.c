// Same as t3.c, faster: u64 inner arithmetic (per-AB counts are < P(a,c)P(b,c) < 2^63 for sizes used),
// u128 total, and work splitting: ./t3p a b c M r  handles depth-2 branches with index % M == r.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
typedef unsigned __int128 u128; typedef unsigned long long u64;
int a,b,c,M=1,R=0; int d[32],e[32]; long br=0;
u128 total=0; u64 nAB=0;
static u64 f[14641], g[14641]; static char valid[14641];
static inline int idx(int p,int P,int q,int Q){return ((p*(a+1)+P)*(b+1)+q)*(b+1)+Q;}
void eval(void){
  nAB++;
  int p,P,q,Q; int n=(a+1)*(a+1)*(b+1)*(b+1);
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
  int B1=b+1, s1=1, s2=B1, s3=B1*B1, s4=B1*B1*(a+1);
  for(int k=1;k<c;k++){
    memcpy(g,f,sizeof(u64)*n);
    for(int i=0;i<n;i+=B1) for(int j=1;j<B1;j++) g[i+j]+=g[i+j-1];
    for(int i=0;i<n;i+=s3) for(int j=s2;j<s3;j++) g[i+j]+=g[i+j-s2];
    for(int i=0;i<n;i+=s4) for(int j=s3;j<s4;j++) g[i+j]+=g[i+j-s3];
    for(int i=s4;i<n;i++) g[i]+=g[i-s4];
    for(int i=0;i<n;i++) f[i]=valid[i]?g[i]:0;
  }
  u64 s=0; for(int i=0;i<n;i++) s+=f[i];
  total+=s;
}
void rec(int t){
  if(t>a){eval();return;}
  if(t==3 || (a<3 && t==a)){ if((br++)%M!=R) return; }
  for(int dd=d[t-1];dd<=b;dd++){ d[t]=dd;
    int lo = e[t-1]>dd?e[t-1]:dd;
    for(int ee=lo;ee<=b;ee++){ e[t]=ee; rec(t+1);} }
}
void pr(u128 x){ char s[64]; int i=63; s[i]=0; if(!x){printf("0");return;} while(x){s[--i]='0'+(int)(x%10); x/=10;} printf("%s",s+i);}
int main(int argc,char**argv){
  a=atoi(argv[1]);b=atoi(argv[2]);c=atoi(argv[3]); if(argc>5){M=atoi(argv[4]);R=atoi(argv[5]);}
  d[0]=0;e[0]=0; rec(1);
  printf("%d %d %d %d %d ",a,b,c,M,R); pr(total); printf(" %llu\n",nAB);
  return 0;
}
