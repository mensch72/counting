// Bounded-width automaton for distributive lattices.
//
// Same states and transitions as frontier.cpp, but instead of a bound on the total number of
// elements there is a bound W on the size of every rank layer.  A state is kept only if all
// layers that are already forced (the down-sets of Lambda of each size > rho) have at most W
// elements.  If the exploration terminates, the lattices all of whose layers have at most W
// elements are the walks of a finite automaton, and their number has a computable exponential
// growth rate, which is a lower bound for the growth rate of all (vertically indecomposable)
// distributive lattices.
//
// usage: bounded W out.txt     writes: number of states, then per state "id weight ntrans targets..."
//                              (state 0 is the empty frontier; a target repeated k times means k transitions)
#include <bits/stdc++.h>
#define MAXN 64
#include <nauty/nauty.h>
#include <nauty/nautinv.h>
using namespace std;
typedef uint32_t u32; typedef uint64_t u64; typedef unsigned __int128 u128;
static const int L = 32;
static int N; static int W;
static inline int pc(u32 x){ return __builtin_popcount(x); }
typedef array<uint8_t, L> Perm;

struct Trans { int w; int tgt; };
struct State {
  int l, rho; u32 dn[L];
  vector<Perm> G;            // group elements (always contains identity); empty means trivial
  int wt = 0;                // layer weight = number of rho-ideals
  int fut = 0;               // number of ideals of Lambda of size > rho (lower bound on remaining weight)
  bool expanded = false;
  vector<Trans> tr;
};
static vector<State> states;
static unordered_map<string,int> idx;
static const int EMPTY = 0;

static string to_s(u128 x){ if(!x) return "0"; string s; while(x){ s+=char('0'+(int)(x%10)); x/=10;} reverse(s.begin(),s.end()); return s; }

// canonical labelling of a poset given by dn[] on l elements; returns newpos[v]
static void canon_label(int l, const u32* dn, const u32* up, int* newpos){
  static DEFAULTOPTIONS_DIGRAPH(options); static statsblk stats;
  if(l==0) return;
  if(l==1){ newpos[0]=0; return; }
  graph g[L], cg[L]; int lab[L], ptn[L], orbits[L];
  for(int i=0;i<l;i++){ g[i]=0; u32 m=up[i]; while(m){ int j=__builtin_ctz(m); m&=m-1; ADDELEMENT(&g[i],j);} }
  int key[L]; for(int i=0;i<l;i++) key[i]=pc(dn[i])*64+pc(up[i]);
  int id[L]; for(int i=0;i<l;i++) id[i]=i;
  sort(id,id+l,[&](int a,int b){ return key[a]<key[b] || (key[a]==key[b] && a<b); });
  for(int i=0;i<l;i++){ lab[i]=id[i]; ptn[i]=(i+1<l && key[id[i]]==key[id[i+1]])?1:0; }
  options.getcanon=TRUE; options.defaultptn=FALSE;
  densenauty(g,lab,ptn,orbits,&options,&stats,1,l,cg);
  for(int i=0;i<l;i++) newpos[lab[i]]=i;
}

// enumerate all ideals of poset (dn on l elements); elements need not be topologically sorted
static void all_ideals(int l, const u32* dn, vector<u32>& out){
  int ord[L]; int no=0; u32 done=0;
  while(no<l) for(int x=0;x<l;x++) if(!(done>>x&1) && (dn[x]&~done)==0){ ord[no++]=x; done|=1u<<x; }
  out.clear(); out.push_back(0);
  for(int q=0;q<l;q++){ int x=ord[q]; size_t sz=out.size();
    for(size_t i=0;i<sz;i++) if((out[i]&dn[x])==dn[x]) out.push_back(out[i]|1u<<x); }
}

static u64 n_states_group=0;

// register state given by labelled data; returns id
static int intern(int l, int rho, const u32* dn_in, vector<Perm>& G, int fut){
  u32 up_in[L]; for(int i=0;i<l;i++) up_in[i]=0;
  for(int i=0;i<l;i++){ u32 m=dn_in[i]; while(m){ int j=__builtin_ctz(m); m&=m-1; up_in[j]|=1u<<i; } }
  int np[L]; canon_label(l,dn_in,up_in,np);
  State s; s.l=l; s.rho=rho; s.fut=fut;
  for(int i=0;i<l;i++){ u32 m=dn_in[i], r=0; while(m){ int j=__builtin_ctz(m); m&=m-1; r|=1u<<np[j]; } s.dn[np[i]]=r; }
  if(G.size()>1){
    for(auto& p: G){ Perm q; q.fill(0); for(int i=0;i<l;i++) q[np[i]]=np[p[i]]; s.G.push_back(q); }
    sort(s.G.begin(),s.G.end()); s.G.erase(unique(s.G.begin(),s.G.end()),s.G.end());
    if(s.G.size()==1) s.G.clear();
  }
  string key; key.reserve(2+4*l+s.G.size()*l);
  key.push_back((char)l); key.push_back((char)rho);
  key.append((const char*)s.dn, 4*l);
  for(auto& p: s.G) key.append((const char*)p.data(), l);
  auto it=idx.find(key); if(it!=idx.end()) return it->second;
  int id=states.size(); idx.emplace(move(key),id); if(!s.G.empty()) n_states_group++;
  states.push_back(move(s)); return id;
}

static u64 n_trans=0;

static void expand(int sid, int B){
  // B: budget = N - acc.  A transition with next-layer weight w' to a state with
  // lower bound fut' is kept iff w' + fut' <= B.
  State S = states[sid];   // copy (states may reallocate)
  int l=S.l, rho=S.rho;
  vector<u32> ids; all_ideals(l,S.dn,ids);
  vector<u32> Jl, J1, Jhi; // size rho, rho+1, >= rho+2
  for(u32 K: ids){ int c=pc(K); if(c==rho) Jl.push_back(K); else if(c==rho+1) J1.push_back(K); else if(c>rho+1) Jhi.push_back(K); }
  sort(Jl.begin(),Jl.end());
  int w=Jl.size(), w0=J1.size(); states[sid].wt=w;
  if(w>64){ fprintf(stderr,"layer too wide\n"); exit(1); }
  // containment masks
  vector<u64> c1(J1.size()), chi(Jhi.size());
  for(size_t a=0;a<J1.size();a++){ u64 m=0; for(int j=0;j<w;j++) if((Jl[j]&J1[a])==Jl[j]) m|=1ull<<j; c1[a]=m; }
  for(size_t a=0;a<Jhi.size();a++){ u64 m=0; for(int j=0;j<w;j++) if((Jl[j]&Jhi[a])==Jl[j]) m|=1ull<<j; chi[a]=m; }
  // group action on Jl
  int ng=S.G.size(); vector<vector<int>> gact(ng, vector<int>(w));
  for(int g=0;g<ng;g++) for(int j=0;j<w;j++){ u32 K=Jl[j], im=0; while(K){ int x=__builtin_ctz(K); K&=K-1; im|=1u<<S.G[g][x]; }
    int p=lower_bound(Jl.begin(),Jl.end(),im)-Jl.begin(); if(p>=w||Jl[p]!=im){ fprintf(stderr,"group action error\n"); exit(1);} gact[g][j]=p; }
  vector<int> m(w,0);
  vector<Trans> out;
  // cost of a (partial) birth vector: next weight + future bound
  // every rank layer above the current one that is already forced must have at most W elements
  auto layersOK=[&]()->bool{
    long long L[80]; for(int i=0;i<80;i++) L[i]=0;
    auto add=[&](int d,int b)->bool{ if(b>W) return false; long long c=1; for(int i=0;i<=b;i++){ if(d+i>=80) return false; if(d+i>=0) L[d+i]+=c; if(d+i>=0 && L[d+i]>W) return false; c=c*(b-i)/(i+1); } return true; };
    for(int j=0;j<w;j++){ if(m[j]>W) return false; long long c=m[j]; for(int i=1;i<=m[j];i++){ L[i-1]+=c; if(L[i-1]>W) return false; c=c*(m[j]-i)/(i+1); } }
    for(size_t a=0;a<J1.size();a++){ int b=0; u64 mm=c1[a]; while(mm){ int j=__builtin_ctzll(mm); mm&=mm-1; b+=m[j]; } if(!add(0,b)) return false; }
    for(size_t a=0;a<Jhi.size();a++){ int b=0; u64 mm=chi[a]; while(mm){ int j=__builtin_ctzll(mm); mm&=mm-1; b+=m[j]; } if(!add(pc(Jhi[a])-rho-1,b)) return false; }
    return true; };
  auto cost=[&](long long limit)->long long{
    long long t=0, f=0; for(int j=0;j<w;j++){ t+=m[j]; if(m[j]>=2){ if(m[j]>40) return limit+1; f+=(1ll<<m[j])-1-m[j]; } }
    if(w0+t+f>limit) return limit+1;
    for(size_t a=0;a<J1.size();a++){ int b=0; u64 mm=c1[a]; while(mm){ int j=__builtin_ctzll(mm); mm&=mm-1; b+=m[j]; } if(b>40) return limit+1; f+=(1ll<<b)-1; if(w0+t+f>limit) return limit+1; }
    for(size_t a=0;a<Jhi.size();a++){ int b=0; u64 mm=chi[a]; while(mm){ int j=__builtin_ctzll(mm); mm&=mm-1; b+=m[j]; } if(b>40) return limit+1; f+=(1ll<<b); if(w0+t+f>limit) return limit+1; }
    return w0+t+f;
  };
  function<void(int)> rec=[&](int j){
    if(j==w){
      // canonical under Gamma?
      vector<int> stab;
      if(ng>1){ for(int g=0;g<ng;g++){ int cmp=0; for(int q=0;q<w && !cmp;q++){ int a=m[gact[g][q]], b=m[q]; if(a<b) cmp=-1; else if(a>b) cmp=1; }
          // image vector m'(q)=m[gact(q)]; reject if some image is lexicographically smaller
          if(cmp<0) return; if(cmp==0) stab.push_back(g); } }
      int t=0; for(int q=0;q<w;q++) t+=m[q];
      int wn=w0+t; int futn=0;
      if(wn==0) return;           // cannot happen for nonempty Lambda; for Lambda empty means "stop"
      n_trans++;
      if(wn==1){ out.push_back({1,EMPTY}); return; }
      int ln=l+t; if(ln>L){ fprintf(stderr,"too many live elements\n"); exit(1); }
      u32 dn[L]; for(int i=0;i<l;i++) dn[i]=S.dn[i];
      int born[L]; // index j of ideal for each new element
      { int c2=l; for(int q=0;q<w;q++) for(int i=0;i<m[q];i++){ dn[c2]=Jl[q]; born[c2]=q; c2++; } }
      u32 dead=(ln==32?0xffffffffu:((1u<<ln)-1));
      for(u32 K: J1) dead&=K;
      for(int c2=l;c2<ln;c2++) dead&=(Jl[born[c2]]|1u<<c2);
      u32 full=(ln==32?0xffffffffu:((1u<<ln)-1)); u32 live=full&~dead;
      int nl=pc(live); int rn=rho+1-pc(dead);
      int pos[L]; { int c2=0; for(int i=0;i<ln;i++) if(live>>i&1) pos[i]=c2++; else pos[i]=-1; }
      u32 dn2[L];
      for(int i=0;i<ln;i++) if(live>>i&1){ u32 mm=dn[i]&live, r=0; while(mm){ int x=__builtin_ctz(mm); mm&=mm-1; r|=1u<<pos[x]; } dn2[pos[i]]=r; }
      // group on new frontier
      vector<Perm> G2;
      bool twins=false; for(int q=0;q<w;q++) if(m[q]>=2) twins=true;
      if(stab.size()>1 || twins){
        // first index of newborn block for ideal q
        vector<int> first(w); { int c2=l; for(int q=0;q<w;q++){ first[q]=c2; c2+=m[q]; } }
        vector<int> stabs = stab; if(ng<=1) stabs.assign(1,-1);
        // twin permutations: iterate over product of permutations of each block
        vector<vector<int>> bp(w); for(int q=0;q<w;q++){ bp[q].resize(m[q]); iota(bp[q].begin(),bp[q].end(),0); }
        std::set<Perm> seen;
        while(true){
          for(int g: stabs){
            Perm p; p.fill(0);
            // image of each element of ln
            int img[L];
            for(int i=0;i<l;i++) img[i]= (g<0)? i : S.G[g][i];
            for(int q=0;q<w;q++){ int tq=(g<0)?q:gact[g][q]; for(int i=0;i<m[q];i++) img[first[q]+i]=first[tq]+bp[q][i]; }
            for(int i=0;i<ln;i++) if(live>>i&1) p[pos[i]]=pos[img[i]];
            seen.insert(p);
          }
          // next combination of block permutations
          int q=0; for(;q<w;q++){ if(m[q]>=2 && next_permutation(bp[q].begin(),bp[q].end())) break; }
          if(q==w) break;
        }
        G2.assign(seen.begin(),seen.end());
      }
      int tid=intern(nl,rn,dn2,G2,futn);
      out.push_back({wn,tid});
      return;
    }
    for(int v=0;;v++){
      m[j]=v;
      if(!layersOK()){ break; }
      rec(j+1);
    }
    m[j]=0;
  };
  rec(0);
  states[sid].tr=move(out); states[sid].expanded=true;
}

int main(int argc,char**argv){
  W=atoi(argv[1]); N=1000000; const char* outf=argv[2];
  { State e; e.l=0; e.rho=0; states.push_back(e); string key; key.push_back(0); key.push_back(0); idx[key]=0; }
  for(size_t sid=0; sid<states.size(); sid++){ expand(sid,0);
    if(states.size()>20000000){ fprintf(stderr,"too many states\n"); return 1; }
    if(sid%200000==0 && sid) fprintf(stderr,"expanded %zu of %zu states\n",sid,states.size()); }
  states[EMPTY].wt=1;
  FILE* f=fopen(outf,"w"); fprintf(f,"%zu\n",states.size()); unsigned long long ntr=0; int maxl=0;
  for(size_t sid=0; sid<states.size(); sid++){ const State& S=states[sid]; maxl=max(maxl,S.l); fprintf(f,"%zu %d %zu",sid,S.wt,S.tr.size()); for(auto& t: S.tr) fprintf(f," %d",t.tgt); fprintf(f,"\n"); ntr+=S.tr.size(); }
  fclose(f);
  fprintf(stderr,"W=%d states=%zu transitions=%llu max live elements=%d\n",W,states.size(),ntr,maxl);
}
