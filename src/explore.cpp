// Exploration: count prime posets by (elements, #ideals) up to NMAX ideals.
// Prime = no nontrivial module (equivalently: comparability graph is prime).
#include <bits/stdc++.h>
#define MAXN 64
#include <nauty/nauty.h>
#include <nauty/nautinv.h>
using namespace std;
typedef uint32_t u32; typedef uint64_t u64;
static int NMAX;
struct Poset { int k; u32 up[32], dn[32]; };
static inline int pc(u32 x){return __builtin_popcount(x);}

static string canon(const Poset&P){
  static DEFAULTOPTIONS_DIGRAPH(options); static statsblk stats;
  int n=P.k, m=1; graph g[32], cg[32]; int lab[32],ptn[32],orbits[32];
  for(int i=0;i<n;i++){ g[i]=0; for(int j=0;j<n;j++) if(P.up[i]>>j&1) ADDELEMENT(&g[i],j);}
  // colour by (|dn|,|up|)
  vector<int> idx(n); iota(idx.begin(),idx.end(),0);
  auto key=[&](int v){return pc(P.dn[v])*64+pc(P.up[v]);};
  sort(idx.begin(),idx.end(),[&](int a,int b){return key(a)<key(b);});
  for(int i=0;i<n;i++){lab[i]=idx[i]; ptn[i]=(i+1<n && key(idx[i])==key(idx[i+1]))?1:0;}
  options.getcanon=TRUE; options.defaultptn=FALSE;
  densenauty(g,lab,ptn,orbits,&options,&stats,m,n,cg);
  string s; s.resize(1+n*4); s[0]=(char)n;
  for(int i=0;i<n;i++){ u32 row=0; for(int j=0;j<n;j++) if(ISELEMENT(&cg[i],j)) row|=1u<<j; memcpy(&s[1+4*i],&row,4);} 
  return s;
}
static void ideals(const Poset&P, vector<u32>&out){
  // elements sorted so that dn[x] only has ... not guaranteed: use topological order
  int n=P.k; vector<int> ord; u32 done=0;
  while((int)ord.size()<n) for(int x=0;x<n;x++) if(!(done>>x&1) && (P.dn[x]&~done)==0){ord.push_back(x);done|=1u<<x;}
  out.clear(); out.push_back(0);
  for(int x:ord){ size_t sz=out.size(); for(size_t i=0;i<sz;i++) if((out[i]&P.dn[x])==P.dn[x] && !(out[i]>>x&1)) { out.push_back(out[i]|1u<<x); if((int)out.size()>NMAX) return; } }
}
int main(int argc,char**argv){
  NMAX=atoi(argv[1]);
  vector<Poset> cur; 
  { Poset N; N.k=4; // a=0<c=2, b=1<c=2, b=1<d=3
    u32 up[4]={4,12,0,0}, dn[4]={0,0,3,2}; for(int i=0;i<4;i++){N.up[i]=up[i];N.dn[i]=dn[i];} cur.push_back(N);}
  map<pair<int,int>,u64> cnt; vector<u64> byI(NMAX+1,0);
  { vector<u32> id; ideals(cur[0],id); byI[id.size()]++; }
  for(int k=4;k<31 && !cur.empty();k++){
    unordered_set<string> seen; vector<Poset> nxt;
    auto add=[&](const Poset&C,int ic){ string s=canon(C); if(seen.insert(s).second){ nxt.push_back(C); byI[ic]++; } };
    // critical posets of size k+1 = 2m
    if((k+1)%2==0 && k+1>=6){ int m=(k+1)/2; 
      { Poset H; H.k=2*m; for(int i=0;i<2*m;i++)H.up[i]=H.dn[i]=0; for(int i=0;i<m;i++)for(int j=i;j<m;j++){H.up[i]|=1u<<(m+j);H.dn[m+j]|=1u<<i;} vector<u32> id; ideals(H,id); if((int)id.size()<=NMAX) add(H,id.size()); }
      { Poset W; W.k=2*m; for(int i=0;i<2*m;i++)W.up[i]=W.dn[i]=0; // a_i = i, b_j = m+j ; a chain, b chain, b_j<a_i iff j<i
        for(int i=0;i<m;i++)for(int j=i+1;j<m;j++){W.up[i]|=1u<<j;W.dn[j]|=1u<<i; W.up[m+i]|=1u<<(m+j);W.dn[m+j]|=1u<<(m+i);} 
        for(int j=0;j<m;j++)for(int i=j+1;i<m;i++){W.up[m+j]|=1u<<i;W.dn[i]|=1u<<(m+j);} vector<u32> id; ideals(W,id); if((int)id.size()<=NMAX) add(W,id.size()); }
    }
    u64 cand=0;
    for(const Poset&P:cur){ vector<u32> id; ideals(P,id); int ni=id.size(); u32 full=(1u<<k)-1;
      vector<int> sup(ni),avo(ni); vector<u32> cu(ni);
      for(int a=0;a<ni;a++){ int c=0,d=0; u32 F=full&~id[a]; for(int b=0;b<ni;b++){ if((id[b]&id[a])==id[a])c++; if((id[b]&F)==0)d++; } sup[a]=c; avo[a]=d; u32 m=full; for(int x=0;x<k;x++) if(id[a]>>x&1) m&=P.up[x]; cu[a]=m; }
      for(int a=0;a<ni;a++){ u32 D=id[a]; if(D==full) continue; for(int b=0;b<ni;b++){ u32 U=full&~id[b]; if(U&~cu[a]) continue; if(D==0 && U==full) continue; if(D==0&&U==0) continue;
          int ic=sup[a]+avo[b]; if(ic>NMAX) continue;
          bool twin=false; for(int y=0;y<k&&!twin;y++) if((D&~(1u<<y))==P.dn[y] && (U&~(1u<<y))==P.up[y]) twin=true; if(twin) continue;
          Poset C=P; C.k=k+1; C.dn[k]=D; C.up[k]=U; for(int y=0;y<k;y++){ if(D>>y&1) C.up[y]|=1u<<k; if(U>>y&1) C.dn[y]|=1u<<k; }
          cand++; add(C,ic); } }
    }
    fprintf(stderr,"k=%d primes=%zu candidates=%llu\n",k+1,nxt.size(),(unsigned long long)cand);
    cur.swap(nxt);
  }
  u64 tot=0; for(int i=1;i<=NMAX;i++){ tot+=byI[i]; printf("%d %llu %llu\n",i,(unsigned long long)byI[i],(unsigned long long)tot);} 
}
