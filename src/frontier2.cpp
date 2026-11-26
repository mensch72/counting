// Production version of the frontier DP (see frontier.cpp for the reference
// implementation and the description of the method).  Same algorithm, compact
// memory layout, 160-bit counters, cheap canonical forms.
//
// usage: frontier2 N        prints "n vi(n)" for n = 1..N, where vi(n) is the
//                           number of vertically indecomposable distributive
//                           lattices with n elements (A072361).
//        frontier2 N t      only lattices with exactly t atoms; prints
//                           "n b count" = number of v.i. distributive lattices
//                           with n elements, t atoms and b coatoms (duality check).
#include <bits/stdc++.h>
#define MAXN 64
#include <nauty/nauty.h>
#include <nauty/nautinv.h>
using namespace std;
typedef uint8_t u8; typedef uint16_t u16; typedef uint32_t u32; typedef uint64_t u64; typedef unsigned __int128 u128;
static const int L = 32;
static int N;
static inline int pc(u32 x){ return __builtin_popcount(x); }
typedef array<u8, L> Perm;

struct __attribute__((packed)) C160 { u64 a, b; u32 c; };
static inline void addc(C160& x, const C160& y){ u128 s=(u128)x.a+y.a; x.a=(u64)s; s=(s>>64)+x.b+y.b; x.b=(u64)s; u64 t=(u64)x.c+y.c+(u64)(s>>64); if(t>>32){ fprintf(stderr,"160-bit overflow\n"); exit(1);} x.c=(u32)t; }
static inline bool isz(const C160& x){ return !(x.a|x.b|x.c); }
static string to_s(C160 x){ // decimal
  u32 w[5]={ (u32)x.a,(u32)(x.a>>32),(u32)x.b,(u32)(x.b>>32),x.c }; string s;
  while(w[0]|w[1]|w[2]|w[3]|w[4]){ u64 r=0; for(int i=4;i>=0;i--){ u64 cur=(r<<32)|w[i]; w[i]=(u32)(cur/10); r=cur%10; } s+=char('0'+r); }
  if(s.empty()) s="0"; reverse(s.begin(),s.end()); return s; }

// ---------- arenas ----------
template<class T> struct Arena { vector<T*> chunks; size_t chunk, used; Arena(size_t c):chunk(c),used(c){}
  T* alloc(size_t n){ if(n>chunk){ T* p=(T*)calloc(n,sizeof(T)); if(!p){fprintf(stderr,"oom\n");exit(1);} chunks.push_back(p); used=chunk; return p; }
    if(used+n>chunk){ T* p=(T*)calloc(chunk,sizeof(T)); if(!p){fprintf(stderr,"oom\n");exit(1);} chunks.push_back(p); used=0; }
    T* r=chunks.back()+used; used+=n; return r; } };
static Arena<u8> recA(1<<24); static Arena<C160> cntA(1<<22); static Arena<u32> trA(1<<22);

// state record: [l][rho][ng lo][ng hi] dn[0..l) as u32, then ng perms of l bytes
static vector<u8*> rec; static vector<u32> recLen;
static vector<u8> aF, aL, wt; static vector<C160*> cnt; static vector<u32*> trP; static vector<int> trN;
static const int EMPTY=0;
// hash table
static vector<u32> ht; static u64 htMask; static size_t nStates=0;
static inline u64 hbytes(const u8* p, size_t n){ u64 h=1469598103934665603ull; size_t i=0; for(;i+8<=n;i+=8){ u64 v; memcpy(&v,p+i,8); h=(h^v)*0x9E3779B97F4A7C15ull; h^=h>>29; } for(;i<n;i++){ h=(h^p[i])*1099511628211ull; } h^=h>>32; h*=0xD6E8FEB86659FD93ull; h^=h>>32; return h; }
static void ht_grow(){ size_t cap=ht.size()*2; vector<u32> nh(cap,0xffffffffu); u64 m=cap-1; for(size_t i=0;i<nStates;i++){ u64 h=hbytes(rec[i],recLen[i])&m; while(nh[h]!=0xffffffffu) h=(h+1)&m; nh[h]=i; } ht.swap(nh); htMask=m; }
static u64 nGroupStates=0, nNauty=0, nTrans=0;

static int add_state(const u8* r, u32 len, int a_first, int a_last, int w){
  u64 h=hbytes(r,len)&htMask;
  while(ht[h]!=0xffffffffu){ u32 id=ht[h]; if(recLen[id]==len && !memcmp(rec[id],r,len)) return id; h=(h+1)&htMask; }
  u32 id=nStates++; ht[h]=id; u8* p=recA.alloc(len); memcpy(p,r,len); rec.push_back(p); recLen.push_back(len);
  aF.push_back(a_first); aL.push_back(a_last); wt.push_back(w); cnt.push_back(cntA.alloc(a_last-a_first+1)); trP.push_back(nullptr); trN.push_back(-1);
  if(r[2]|r[3]) nGroupStates++;
  if(nStates*2>ht.size()) ht_grow();
  return id;
}

// ---------- canonical labelling ----------
static inline u64 mix(u64 x){ x^=x>>31; x*=0x7fb5d329728ea185ull; x^=x>>27; x*=0x81dadef4bc2dd44dull; x^=x>>33; return x; }
static void canon_label(int l, const u32* dn, const u32* up, int* newpos){
  if(l==0) return; if(l==1){ newpos[0]=0; return; }
  u64 h[L], h2[L];
  for(int i=0;i<l;i++) h[i]=mix(pc(dn[i])*64+pc(up[i])+1);
  for(int round=0;round<2;round++){
    for(int i=0;i<l;i++){ u64 s1=0,s2=0; u32 m=dn[i]; while(m){ int j=__builtin_ctz(m); m&=m-1; s1+=mix(h[j]^0x1234567ull); } m=up[i]; while(m){ int j=__builtin_ctz(m); m&=m-1; s2+=mix(h[j]^0xabcdef01ull); }
      h2[i]=mix(h[i]*3+mix(s1)*5+mix(s2+77)*7); }
    memcpy(h,h2,sizeof(u64)*l);
  }
  int id[L]; for(int i=0;i<l;i++) id[i]=i;
  sort(id,id+l,[&](int a,int b){ return h[a]<h[b] || (h[a]==h[b] && a<b); });
  bool discrete=true; for(int i=0;i+1<l;i++) if(h[id[i]]==h[id[i+1]]){ discrete=false; break; }
  if(discrete){ for(int i=0;i<l;i++) newpos[id[i]]=i; return; }
  static DEFAULTOPTIONS_DIGRAPH(options); static statsblk stats; nNauty++;
  graph g[L], cg[L]; int lab[L], ptn[L], orbits[L];
  for(int i=0;i<l;i++){ g[i]=0; u32 m=up[i]; while(m){ int j=__builtin_ctz(m); m&=m-1; ADDELEMENT(&g[i],j);} }
  for(int i=0;i<l;i++){ lab[i]=id[i]; ptn[i]=(i+1<l && h[id[i]]==h[id[i+1]])?1:0; }
  options.getcanon=TRUE; options.defaultptn=FALSE;
  densenauty(g,lab,ptn,orbits,&options,&stats,1,l,cg);
  for(int i=0;i<l;i++) newpos[lab[i]]=i;
}

static void all_ideals(int l, const u32* dn, vector<u32>& out){
  int ord[L]; int no=0; u32 done=0;
  while(no<l) for(int x=0;x<l;x++) if(!(done>>x&1) && (dn[x]&~done)==0){ ord[no++]=x; done|=1u<<x; }
  out.clear(); out.push_back(0);
  for(int q=0;q<no;q++){ int x=ord[q]; size_t sz=out.size();
    for(size_t i=0;i<sz;i++) if((out[i]&dn[x])==dn[x]) out.push_back(out[i]|1u<<x); }
}

// canonicalise and register a state; returns id
static int intern(int l, int rho, const u32* dn_in, vector<Perm>& G, int a_first, int a_last, int w){
  u32 up_in[L]; for(int i=0;i<l;i++) up_in[i]=0;
  for(int i=0;i<l;i++){ u32 m=dn_in[i]; while(m){ int j=__builtin_ctz(m); m&=m-1; up_in[j]|=1u<<i; } }
  int np[L]; canon_label(l,dn_in,up_in,np);
  u32 dnc[L];
  for(int i=0;i<l;i++){ u32 m=dn_in[i], r=0; while(m){ int j=__builtin_ctz(m); m&=m-1; r|=1u<<np[j]; } dnc[np[i]]=r; }
  vector<Perm> G2;
  if(G.size()>1){
    for(auto& p: G){ Perm q; q.fill(0); for(int i=0;i<l;i++) q[np[i]]=np[p[i]]; G2.push_back(q); }
    sort(G2.begin(),G2.end()); G2.erase(unique(G2.begin(),G2.end()),G2.end());
    if(G2.size()==1) G2.clear();
  }
  if(G2.size()>65535){ fprintf(stderr,"group too large\n"); exit(1); }
  static vector<u8> buf; buf.resize(4+4*l+G2.size()*l);
  buf[0]=l; buf[1]=rho; buf[2]=G2.size()&255; buf[3]=G2.size()>>8;
  memcpy(&buf[4],dnc,4*l);
  for(size_t g=0;g<G2.size();g++) memcpy(&buf[4+4*l+g*l],G2[g].data(),l);
  return add_state(buf.data(),buf.size(),a_first,a_last,w);
}

static void expand(int sid, int a){
  int B=N-a;   // budget: next layer weight + forced future weight must be <= B
  int l=rec[sid][0], rho=rec[sid][1], ng=rec[sid][2]|(rec[sid][3]<<8);
  u32 Sdn[L]; memcpy(Sdn,rec[sid]+4,4*l);
  vector<Perm> SG(ng); for(int g=0;g<ng;g++){ SG[g].fill(0); memcpy(SG[g].data(),rec[sid]+4+4*l+g*l,l); }
  static vector<u32> ids; all_ideals(l,Sdn,ids);
  vector<u32> Jl, J1, Jhi;
  for(u32 K: ids){ int c=pc(K); if(c==rho) Jl.push_back(K); else if(c==rho+1) J1.push_back(K); else if(c>rho+1) Jhi.push_back(K); }
  sort(Jl.begin(),Jl.end());
  int w=Jl.size(), w0=J1.size();
  if(w>64){ fprintf(stderr,"layer wider than 64\n"); exit(1); }
  if(sid!=EMPTY && w!=wt[sid]){ fprintf(stderr,"weight mismatch\n"); exit(1); }
  vector<u64> c1(J1.size()), chi(Jhi.size());
  for(size_t i=0;i<J1.size();i++){ u64 m=0; for(int j=0;j<w;j++) if((Jl[j]&J1[i])==Jl[j]) m|=1ull<<j; c1[i]=m; }
  for(size_t i=0;i<Jhi.size();i++){ u64 m=0; for(int j=0;j<w;j++) if((Jl[j]&Jhi[i])==Jl[j]) m|=1ull<<j; chi[i]=m; }
  vector<vector<int>> gact(ng, vector<int>(w));
  for(int g=0;g<ng;g++) for(int j=0;j<w;j++){ u32 K=Jl[j], im=0; while(K){ int x=__builtin_ctz(K); K&=K-1; im|=1u<<SG[g][x]; }
    int p=lower_bound(Jl.begin(),Jl.end(),im)-Jl.begin(); if(p>=w||Jl[p]!=im){ fprintf(stderr,"group action error\n"); exit(1);} gact[g][j]=p; }
  int m[64]; for(int j=0;j<w;j++) m[j]=0;
  vector<u32> out;
  auto cost=[&](long long limit)->long long{
    long long t=0, f=0; for(int j=0;j<w;j++){ t+=m[j]; if(m[j]>=2){ if(m[j]>40) return limit+1; f+=(1ll<<m[j])-1-m[j]; } }
    if(w0+t+f>limit) return limit+1;
    for(size_t i=0;i<c1.size();i++){ int b=0; u64 mm=c1[i]; while(mm){ int j=__builtin_ctzll(mm); mm&=mm-1; b+=m[j]; } if(b>40) return limit+1; f+=(1ll<<b)-1; if(w0+t+f>limit) return limit+1; }
    for(size_t i=0;i<chi.size();i++){ int b=0; u64 mm=chi[i]; while(mm){ int j=__builtin_ctzll(mm); mm&=mm-1; b+=m[j]; } if(b>40) return limit+1; f+=(1ll<<b); if(w0+t+f>limit) return limit+1; }
    return w0+t+f;
  };
  function<void(int)> rec_=[&](int j){
    if(j==w){
      vector<int> stab;
      if(ng>1){ for(int g=0;g<ng;g++){ int cmp=0; for(int q=0;q<w && !cmp;q++){ int x=m[gact[g][q]], y=m[q]; if(x<y) cmp=-1; else if(x>y) cmp=1; }
          if(cmp<0) return; if(cmp==0) stab.push_back(g); } }
      int t=0; for(int q=0;q<w;q++) t+=m[q];
      long long c=cost(B); int wn=w0+t; int futn=(int)(c-wn);
      if(wn==0) return;
      nTrans++;
      if(wn==1){ out.push_back(EMPTY); return; }
      int ln=l+t; if(ln>L){ fprintf(stderr,"more than %d live elements\n",L); exit(1); }
      u32 dn[L]; for(int i=0;i<l;i++) dn[i]=Sdn[i];
      int born[L]; { int c2=l; for(int q=0;q<w;q++) for(int i=0;i<m[q];i++){ dn[c2]=Jl[q]; born[c2]=q; c2++; } }
      u32 full=(ln==32?0xffffffffu:((1u<<ln)-1)); u32 dead=full;
      for(u32 K: J1) dead&=K;
      for(int c2=l;c2<ln;c2++) dead&=(Jl[born[c2]]|1u<<c2);
      u32 live=full&~dead; int nl=pc(live); int rn=rho+1-pc(dead);
      int pos[L]; { int c2=0; for(int i=0;i<ln;i++) if(live>>i&1) pos[i]=c2++; else pos[i]=-1; }
      u32 dn2[L];
      for(int i=0;i<ln;i++) if(live>>i&1){ u32 mm=dn[i]&live, r=0; while(mm){ int x=__builtin_ctz(mm); mm&=mm-1; r|=1u<<pos[x]; } dn2[pos[i]]=r; }
      vector<Perm> G2;
      bool twins=false; for(int q=0;q<w;q++) if(m[q]>=2) twins=true;
      if(stab.size()>1 || twins){
        vector<int> first(w); { int c2=l; for(int q=0;q<w;q++){ first[q]=c2; c2+=m[q]; } }
        vector<int> stabs=stab; if(ng<=1) stabs.assign(1,-1);
        vector<vector<int>> bp(w); for(int q=0;q<w;q++){ bp[q].resize(m[q]); iota(bp[q].begin(),bp[q].end(),0); }
        std::set<Perm> seen;
        while(true){
          for(int g: stabs){
            Perm p; p.fill(0); int img[L];
            for(int i=0;i<l;i++) img[i]=(g<0)? i : SG[g][i];
            for(int q=0;q<w;q++){ int tq=(g<0)?q:gact[g][q]; for(int i=0;i<m[q];i++) img[first[q]+i]=first[tq]+bp[q][i]; }
            for(int i=0;i<ln;i++) if(live>>i&1) p[pos[i]]=pos[img[i]];
            seen.insert(p);
          }
          int q=0; for(;q<w;q++){ if(m[q]>=2 && next_permutation(bp[q].begin(),bp[q].end())) break; }
          if(q==w) break;
        }
        G2.assign(seen.begin(),seen.end());
      }
      int tid=intern(nl,rn,dn2,G2,a+wn,N-futn,wn);
      if(wt[tid]!=wn || aL[tid]!=N-futn){ fprintf(stderr,"state invariant mismatch\n"); exit(1); }
      out.push_back(tid);
      return;
    }
    for(int v=0;;v++){ m[j]=v; if(cost(B)>B) break; rec_(j+1); }
    m[j]=0;
  };
  rec_(0);
  u32* p=trA.alloc(out.size()?out.size():1); memcpy(p,out.data(),4*out.size()); trP[sid]=p; trN[sid]=out.size();
}

int main(int argc,char**argv){
  N=atoi(argv[1]); if(N>250){ fprintf(stderr,"N too large\n"); return 1; }
  int atoms=argc>2?atoi(argv[2]):0;
  vector<C160> vib; if(atoms){ vib.resize((size_t)(N+3)*65); memset(vib.data(),0,sizeof(C160)*vib.size()); }
  ht.assign(1<<16,0xffffffffu); htMask=ht.size()-1;
  { u8 r[4]={0,0,0,0}; add_state(r,4,1,N,1); }
  vector<C160> vi(N+3); memset(vi.data(),0,sizeof(C160)*(N+3));
  C160 one; one.a=1; one.b=0; one.c=0;
  expand(EMPTY,1);
  for(int i=0;i<trN[EMPTY];i++){ u32 t=trP[EMPTY][i];
    if(t==EMPTY){ if(atoms<=1){ addc(vi[2],one); if(atoms) addc(vib[2*65+1],one); } }
    else if((!atoms || wt[t]==atoms) && 1+wt[t]<=aL[t]) addc(cnt[t][1+wt[t]-aF[t]],one); }
  time_t t0=time(0);
  for(int a=2;a<=N;a++){
    size_t nst=nStates;
    for(size_t id=1;id<nst;id++){ if(aF[id]>a || aL[id]<a) continue; C160 c=cnt[id][a-aF[id]]; if(isz(c)) continue;
      if(trN[id]<0) expand(id,a);
      const u32* tp=trP[id]; int tn=trN[id];
      for(int i=0;i<tn;i++){ u32 t=tp[i]; if(t==EMPTY){ addc(vi[a+1],c); if(atoms) addc(vib[(size_t)(a+1)*65+wt[id]],c); } else { int a2=a+wt[t]; if(a2<=aL[t]) addc(cnt[t][a2-aF[t]],c); } }
    }
    if(a%10==0 || a==N) fprintf(stderr,"acc=%d states=%zu (group %llu) trans=%llu nauty=%llu  %lds\n",a,nStates,(unsigned long long)nGroupStates,(unsigned long long)nTrans,(unsigned long long)nNauty,(long)(time(0)-t0));
  }
  if(atoms){ for(int n=1;n<=N;n++) for(int b=1;b<65;b++) if(!isz(vib[(size_t)n*65+b])) printf("%d %d %s\n",n,b,to_s(vib[(size_t)n*65+b]).c_str()); }
  else for(int n=1;n<=N;n++) printf("%d %s\n",n,to_s(vi[n]).c_str());
}
