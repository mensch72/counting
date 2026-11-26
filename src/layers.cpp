// Frontier DP for unlabeled MODULAR lattices (OEIS A006981), experimental.
//
// A finite lattice is modular iff it is upper and lower semimodular; such
// lattices are graded.  Build the lattice layer by layer from the bottom.
// Let T = L_r be the current top layer and Y = { a ^ b : a, b in T } (pairwise
// meets, T itself included), as a poset, with the elements of rank r-1 marked.
// Call a, b in T adjacent if a ^ b has rank r-1.  The next layer is a family of
// subsets D_c of T (the lower covers of the new elements c) such that
//   (1,2) the D_c with |D_c| >= 2 partition the adjacent pairs into cliques,
//   (G)   every element of T lies in some D_c,
//   (3)   for all c != d the set { a ^ b : a in D_c, b in D_d } has a maximum
//         (this is c ^ d).
// These conditions and the next (Y', marks) only depend on (Y, marks), so the DP
// state is (Y, marks, Gamma), Gamma = image of the automorphism group of the
// lower part on T.  Gamma is stored as: twin classes of T (Gamma contains the
// full symmetric group on each class) plus the explicit list H of the elements
// that are monotone on every class.
//
// usage: layers N [dualfile|-] [mode]
//   mode = modular (default) | dist | usm | lsm | graded | geometric | cogeometric
//   usm/lsm: upper/lower semimodular lattices (rule (U) resp. (D) only); graded: neither rule;
//   geometric = usm + atomistic; cogeometric = lsm + coatomistic (the dual class).
//   The pruning rules that rest on modularity are switched off in these modes.
// (original usage line of modular.cpp:) modular N [dualfile] [dist]
//   with a third argument only distributive lattices are counted (no interval of length 2
//   with three atoms); the result must equal A072361/A006982, which checks this program
//   against the independent distributive DP.
//   prints n, vi(n), f(n); with dualfile also writes "n atoms coatoms count" for the
//   vertically indecomposable lattices (must be symmetric in atoms/coatoms: the class is self-dual)
#include <bits/stdc++.h>
#define MAXN 128
#include <nauty/nauty.h>
#include <nauty/nautinv.h>
using namespace std;
typedef uint8_t u8; typedef uint32_t u32; typedef uint64_t u64; typedef unsigned __int128 u128;
static int N; static bool verbose=false; static bool DIST=false;
// Class of graded lattices counted (see usage): U = upper semimodular rule, D = lower semimodular rule
static bool modeU=true, modeD=true, ATOM=false, COATOM=false;
static inline int pc(u64 x){ return __builtin_popcountll(x); }
static inline int ctz(u64 x){ return __builtin_ctzll(x); }
typedef vector<u8> Perm;
static string to_s(u128 x){ if(!x) return "0"; string s; while(x){ s+=char('0'+(int)(x%10)); x/=10;} reverse(s.begin(),s.end()); return s; }

struct State {
  int ny=0, nt=0;            // |Y|, |T|; T = elements 0..nt-1
  vector<u64> below;         // below[y] = mask of z <= y (reflexive)
  u64 lev1=0;                // elements of rank r-1
  vector<u8> cls;            // twin class id (= min member) of each T element
  vector<Perm> H;            // monotone transversal (always contains identity)
  int nat=0;                 // geometric mode only: number of atoms of the lower part (part of the state)
  int fut=0;                 // lower bound on the number of elements still to come
  bool expanded=false; vector<int> tr;
};
static vector<State> states; static unordered_map<string,int> idx;
static const int SINGLE=0;
// Duality bound.  In a modular lattice rank(a v b) - r = r - rank(a ^ b) = distance of a, b in the
// adjacency graph of layer r.  The part of the lattice above a layer is, upside down, a lower part
// of the dual lattice with the same distance matrix.  So a frontier can only be completed with w
// further elements if some lower part with the same distance profile has w elements below its top
// layer.  firstA[profile] = least such w seen (the DP runs in increasing weight, so the first is least).
static unordered_map<string,int> firstA;
static string dist_profile(int k, const vector<u64>& adj){
  vector<string> rows(k);
  for(int s0=0;s0<k;s0++){ string r; u64 seen=1ull<<s0, fr=seen; int d=0; while(true){ u64 nx=0,f=fr; while(f){ int x=__builtin_ctzll(f); f&=f-1; nx|=adj[x]; } nx&=~seen; if(!nx) break; d++; r.append(__builtin_popcountll(nx),(char)d); seen|=nx; fr=nx; } rows[s0]=r; }
  sort(rows.begin(),rows.end()); string out; for(auto& r: rows){ out+=r; out.push_back((char)255); } return out; }
static u64 nTrans=0, nFam=0, nNauty=0;
static const size_t SEENPART_CAP=4000000;

static inline u64 mix64(u64 x){ x^=x>>31; x*=0x7fb5d329728ea185ull; x^=x>>27; x*=0x81dadef4bc2dd44dull; x^=x>>33; return x; }
static void die(const char* s){ fprintf(stderr,"FATAL: %s\n",s); exit(1); }

// ---- canonical labelling of a vertex-coloured digraph on n <= 128 vertices ----
// col[v]: colour class index (cells ordered by colour); arcs given by rows of masks (2 words)
static void nauty_canon(int n, const vector<array<u64,2>>& arcs, const vector<int>& col, vector<int>& lab_out, string* canon_str){
  static DEFAULTOPTIONS_DIGRAPH(options); static statsblk stats; nNauty++;
  int m=SETWORDSNEEDED(n);
  static graph g[MAXN*2], cg[MAXN*2]; static int lab[MAXN], ptn[MAXN], orbits[MAXN];
  memset(g,0,sizeof(graph)*(size_t)m*n);
  for(int i=0;i<n;i++) for(int j=0;j<n;j++) if(arcs[i][j>>6]>>(j&63)&1) g[(size_t)i*m+SETWD(j)]|=bit[SETBT(j)];
  vector<int> id(n); iota(id.begin(),id.end(),0);
  stable_sort(id.begin(),id.end(),[&](int a,int b){ return col[a]<col[b]; });
  for(int i=0;i<n;i++){ lab[i]=id[i]; ptn[i]=(i+1<n && col[id[i]]==col[id[i+1]])?1:0; }
  options.getcanon=TRUE; options.defaultptn=FALSE;
  densenauty(g,lab,ptn,orbits,&options,&stats,m,n,cg);
  lab_out.assign(lab,lab+n);
  if(canon_str){ canon_str->assign((const char*)cg, sizeof(graph)*m*n); }
}

// make a permutation of T monotone on classes (classes given by cls ids)
static void monotone(Perm& p, const vector<u8>& cls, int nt){
  // group elements by class; image of a class is a class; map sorted -> sorted
  vector<vector<int>> mem(nt); for(int i=0;i<nt;i++) mem[cls[i]].push_back(i);
  Perm q(nt);
  for(int c=0;c<nt;c++) if(!mem[c].empty()){ vector<int> im; for(int x: mem[c]) im.push_back(p[x]); sort(im.begin(),im.end()); for(size_t i=0;i<mem[c].size();i++) q[mem[c][i]]=im[i]; }
  p=q;
}

static int diameter_bound(int nt, const vector<u64>& adj){
  // returns -1 if adjacency graph disconnected, else lower bound on remaining elements
  if(nt<=1) return 0;
  int diam=0;
  for(int s=0;s<nt;s++){ u64 seen=1ull<<s, fr=seen; int d=0; while(true){ u64 nx=0; u64 f=fr; while(f){ int x=ctz(f); f&=f-1; nx|=adj[x]; } nx&=~seen; if(!nx) break; seen|=nx; fr=nx; d++; }
    if(pc(seen)!=nt) return -1; diam=max(diam,d); }
  if(diam<=1) return 1;
  // every element of the next layer covers at most one element of an independent
  // set, and covers something; so the next layer has at least g elements, and its
  // own diameter is at least diam-1.
  u64 rem=(nt==64)?~0ull:((1ull<<nt)-1); int g=0;
  while(rem){ int best=-1, bd=1000; u64 m=rem; while(m){ int x=ctz(m); m&=m-1; int d=pc(adj[x]&rem); if(d<bd){ bd=d; best=x; } } g++; rem&=~(adj[best]|1ull<<best); }
  return max(2*(diam-1)+1, g+2*(diam-2)+1);
}

// Canonical form of a family of subsets of T under permutations of T inside the
// twin classes (and arbitrary reordering of the family), without nauty.
// Columns (members) are ordered by an invariant hash; this is canonical as soon
// as equal hashes only occur for equal sets.  Returns false if that fails.
static bool fam_fast(int nt, int k, const vector<u64>& D, const vector<u8>& cls, string& out){
  u64 row[64], col[64], r0[64], c0[64];
  for(int x=0;x<nt;x++) row[x]=r0[x]=mix64(cls[x]+11);
  for(int c=0;c<k;c++) col[c]=c0[c]=mix64(pc(D[c])*131+5);
  for(int round=0;round<3;round++){
    for(int c=0;c<k;c++){ u64 sm=0; u64 m=D[c]; while(m){ int x=ctz(m); m&=m-1; sm+=mix64(row[x]^0x55aa55aaull); } col[c]=mix64(c0[c]*3+mix64(sm)); }
    for(int x=0;x<nt;x++){ u64 sm=0; for(int c=0;c<k;c++) if(D[c]>>x&1) sm+=mix64(col[c]^0x77117711ull); row[x]=mix64(r0[x]*5+mix64(sm)); }
  }
  int id[64]; for(int c=0;c<k;c++) id[c]=c;
  sort(id,id+k,[&](int a,int b){ return col[a]<col[b] || (col[a]==col[b] && D[a]<D[b]); });
  for(int i=0;i+1<k;i++) if(col[id[i]]==col[id[i+1]] && D[id[i]]!=D[id[i+1]]) return false;
  // row signatures over canonical column positions
  vector<pair<int,u64>> sig(nt); for(int x=0;x<nt;x++){ u64 sg=0; for(int i=0;i<k;i++) if(D[id[i]]>>x&1) sg|=1ull<<i; sig[x]={cls[x],sg}; }
  sort(sig.begin(),sig.end());
  out.clear(); for(auto& p: sig){ out.push_back((char)p.first); out.append((const char*)&p.second,8); } out.push_back('F');
  return true;
}

// register a state from raw data (T = first nt elements); G: classes + H in raw labels
static int intern(State& S){
  int ny=S.ny, nt=S.nt;
  // canonical labelling: digraph y -> z for z < y, colours T / lev1 / deeper
  vector<array<u64,2>> arcs(ny); vector<int> col(ny);
  for(int y=0;y<ny;y++){ arcs[y]={S.below[y]&~(1ull<<y),0}; col[y]= y<nt?0:((S.lev1>>y&1)?1:2); }
  vector<int> np(ny);
  { // fast path: refine colours by hashing; if the partition is discrete it is a canonical order
    vector<u64> h(ny), h2(ny); vector<u64> above(ny,0);
    for(int y=0;y<ny;y++){ u64 m=S.below[y]&~(1ull<<y); while(m){ int z=ctz(m); m&=m-1; above[z]|=1ull<<y; } }
    for(int y=0;y<ny;y++) h[y]=mix64(col[y]*1000003ull+pc(S.below[y])*1009ull+pc(above[y])+7);
    for(int round=0;round<3;round++){ for(int y=0;y<ny;y++){ u64 s1=0,s2=0; u64 m=S.below[y]&~(1ull<<y); while(m){ int z=ctz(m); m&=m-1; s1+=mix64(h[z]^0x1234567ull); } m=above[y]; while(m){ int z=ctz(m); m&=m-1; s2+=mix64(h[z]^0xabcdef01ull); }
        h2[y]=mix64(h[y]*3+mix64(s1)*5+mix64(s2+77)*7); } h=h2; }
    vector<int> id(ny); iota(id.begin(),id.end(),0);
    sort(id.begin(),id.end(),[&](int a,int b){ return col[a]<col[b] || (col[a]==col[b] && h[a]<h[b]); });
    bool discrete=true; for(int i=0;i+1<ny;i++) if(col[id[i]]==col[id[i+1]] && h[id[i]]==h[id[i+1]]){ discrete=false; break; }
    if(discrete){ for(int i=0;i<ny;i++) np[id[i]]=i; }
    else { // nauty, with the refined colours as cells
      vector<int> col2(ny); { int c=0; for(int i=0;i<ny;i++){ if(i>0 && (col[id[i]]!=col[id[i-1]] || h[id[i]]!=h[id[i-1]])) c++; col2[id[i]]=c; } }
      vector<int> lab; nauty_canon(ny,arcs,col2,lab,nullptr); for(int i=0;i<ny;i++) np[lab[i]]=i; }
  }
  for(int y=0;y<nt;y++) if(np[y]>=nt) die("canonical labelling moved T");
  State C; C.ny=ny; C.nt=nt; C.below.assign(ny,0); C.fut=S.fut; C.nat=S.nat;
  for(int y=0;y<ny;y++){ u64 m=S.below[y], r=0; while(m){ int z=ctz(m); m&=m-1; r|=1ull<<np[z]; } C.below[np[y]]=r; if(S.lev1>>y&1) C.lev1|=1ull<<np[y]; }
  // classes
  C.cls.assign(nt,0); { vector<int> mn(nt,255); for(int x=0;x<nt;x++){ int c=S.cls[x]; mn[c]=min(mn[c],np[x]); } for(int x=0;x<nt;x++) C.cls[np[x]]=mn[S.cls[x]]; }
  for(auto& p: S.H){ Perm q(nt); for(int x=0;x<nt;x++) q[np[x]]=np[p[x]]; monotone(q,C.cls,nt); C.H.push_back(q); }
  sort(C.H.begin(),C.H.end()); C.H.erase(unique(C.H.begin(),C.H.end()),C.H.end());
  string key; key.push_back((char)ny); key.push_back((char)nt); key.push_back((char)C.nat);
  key.append((const char*)C.below.data(),8*ny); key.append((const char*)&C.lev1,8);
  key.append((const char*)C.cls.data(),nt);
  for(auto& p: C.H) key.append((const char*)p.data(),nt);
  auto it=idx.find(key); if(it!=idx.end()) return it->second;
  int id=states.size(); idx.emplace(move(key),id); states.push_back(move(C)); return id;
}

static void expand(int sid, int B){
  const State S=states[sid];
  int nt=S.nt, ny=S.ny;
  if(nt>63) die("layer wider than 63");
  // meets and adjacency
  vector<vector<int>> meet(nt, vector<int>(nt,-1));
  vector<u64> adj(nt,0);
  for(int a=0;a<nt;a++) for(int b=0;b<nt;b++){ if(a==b){ meet[a][b]=a; continue; }
    u64 m=S.below[a]&S.below[b]; int best=-1; u64 mm=m; while(mm){ int y=ctz(mm); mm&=mm-1; if((m&~S.below[y])==0){ best=y; break; } }
    if(best<0) die("meet missing in state"); meet[a][b]=best; if(S.lev1>>best&1) adj[a]|=1ull<<b; }
  const bool mod = modeU && modeD;
  const u64 fullT = (nt==64)? ~0ull : ((1ull<<nt)-1);
  // pairs that may lie in a common member (allowed) and pairs that must (required)
  vector<u64> allowed(nt), required(nt);
  bool allAdj=true;
  for(int x=0;x<nt;x++){ allowed[x]= modeD? adj[x] : (fullT&~(1ull<<x)); required[x]= modeU? adj[x] : 0; if(adj[x]!=(fullT&~(1ull<<x))) allAdj=false; }
  const bool pairOK = mod || (modeU && allAdj);
  bool trivialG = true; for(int x=0;x<nt;x++) if(S.cls[x]!=x) trivialG=false; if(S.H.size()>1) trivialG=false;
  bool trivialN = true; for(int x=0;x<nt;x++) if(S.cls[x]!=x) trivialN=false;
  int nH=S.H.size();
  vector<int> out; unordered_set<string> seenFam;
  vector<u64> cl; vector<u64> cov(nt,0); vector<int> msing(nt,0);
  vector<vector<int>> clmeet;          // meets of chosen cliques (indices into Y)
  vector<vector<int>> smeet(nt);       // smeet[a][i] = (single over a) ^ (clique i)
  int maxMembers = B;   // refined below

  // maximum of the meets of all pairs from two subsets of T, or -1
  auto setmeet=[&](u64 A,u64 Bm)->int{ u64 M=0; u64 dc=A; while(dc){ int x=ctz(dc); dc&=dc-1; u64 dd=Bm; while(dd){ int y=ctz(dd); dd&=dd-1; M|=1ull<<meet[x][y]; } }
    u64 mm=M; while(mm){ int y=ctz(mm); mm&=mm-1; if((M&~S.below[y])==0) return y; } return -1; };

  // members + lower bound on what must follow, for the current (cliques, msing); -1 if hopeless
  auto famcost=[&]()->int{
    int ncl=cl.size(); int k=ncl; bool twin=false; vector<int> pts;
    for(int a=0;a<nt;a++) if(msing[a]>0){ k+=msing[a]; pts.push_back(a); if(msing[a]>1) twin=true; }
    if(k<=1) return k;
    if(!mod) return k+1;
    int nv=ncl+pts.size(); if(nv>64) die("compressed layer too wide");
    vector<u64> g(nv,0);
    for(int i=0;i<ncl;i++) for(int j=0;j<ncl;j++) if(i!=j && clmeet[i][j]<nt) g[i]|=1ull<<j;
    for(size_t p=0;p<pts.size();p++) for(int i=0;i<ncl;i++) if(cl[i]>>pts[p]&1){ g[ncl+p]|=1ull<<i; g[i]|=1ull<<(ncl+p); }
    int diam=twin?1:0;
    for(int s0=0;s0<nv;s0++){ u64 seen=1ull<<s0, fr=seen; int d=0; while(true){ u64 nx=0,f=fr; while(f){ int x=ctz(f); f&=f-1; nx|=g[x]; } nx&=~seen; if(!nx) break; seen|=nx; fr=nx; d++; }
      if(pc(seen)!=nv) return -1; diam=max(diam,d); }
    if(diam<=1) return k+1;
    u64 rem=(nv==64)?~0ull:((1ull<<nv)-1); int gi=0;
    while(rem){ int best=-1, bd=1000; u64 m=rem; while(m){ int x=ctz(m); m&=m-1; int d=pc(g[x]&rem); if(d<bd){ bd=d; best=x; } } gi++; rem&=~(g[best]|1ull<<best); }
    return k+max(2*(diam-1)+1, gi+2*(diam-2)+1); };

  // canonical form of a family of subsets of T under Gamma = N.H
  auto famcanon=[&](const vector<u64>& D)->string{
    int k=D.size(); string best;
    for(int h=0;h<nH;h++){
      vector<u64> Dh(k); for(int c=0;c<k;c++){ u64 m=D[c], r=0; while(m){ int x=ctz(m); m&=m-1; r|=1ull<<S.H[h][x]; } Dh[c]=r; }
      string s;
      if(trivialN){ sort(Dh.begin(),Dh.end()); s.assign((const char*)Dh.data(),8*k); }
      else if(fam_fast(nt,k,Dh,S.cls,s)){ }
      else { int n=nt+k; if(n>MAXN) die("family graph too large"); vector<array<u64,2>> arcs(n,array<u64,2>{0,0}); vector<int> col(n);
        for(int x=0;x<nt;x++) col[x]=S.cls[x]; for(int c=0;c<k;c++) col[nt+c]=nt+pc(Dh[c]);
        for(int c=0;c<k;c++){ u64 m=Dh[c]; while(m){ int x=ctz(m); m&=m-1; int v=nt+c; arcs[x][v>>6]|=1ull<<(v&63); arcs[v][x>>6]|=1ull<<(x&63); } }
        vector<int> lab; nauty_canon(n,arcs,col,lab,nullptr);
        // compact canonical form: the members as sorted bit masks over the canonical positions of T
        // (the colour cells of T come first, so these positions are 0..nt-1 and respect the classes)
        int posT[64]; for(int i=0;i<nt;i++){ if(lab[i]>=nt) die("canonical labelling moved T (family)"); posT[lab[i]]=i; }
        vector<u64> cm(k); for(int c=0;c<k;c++){ u64 m=Dh[c], r=0; while(m){ int x=ctz(m); m&=m-1; r|=1ull<<posT[x]; } cm[c]=r; }
        sort(cm.begin(),cm.end()); s.assign((const char*)cm.data(),8*k); s.push_back('N'); }
      if(h==0 || s<best) best=s;
    }
    return best; };
  unordered_set<string> seenPart;

  // ---- process one complete family (all lattice conditions already hold) ----
  auto process=[&](){
    nFam++;
    int ncl=cl.size();
    vector<u64> D; vector<int> pt; for(u64 K: cl){ D.push_back(K); pt.push_back(-1); }
    for(int a=0;a<nt;a++) for(int i=0;i<msing[a];i++){ D.push_back(1ull<<a); pt.push_back(a); }
    int k=D.size(); if(k==0) return;
    if(k==1){ nTrans++; out.push_back(SINGLE); return; }
    vector<vector<int>> nm(k, vector<int>(k,-1)); u64 used=0;
    for(int c=0;c<k;c++) for(int d=c+1;d<k;d++){ int y;
        if(d<ncl) y=clmeet[c][d]; else if(c<ncl) y=((cl[c]>>pt[d])&1)? pt[d] : smeet[pt[d]][c]; else y=meet[pt[c]][pt[d]];
        if(y<0) die("unexpected missing meet");
        nm[c][d]=nm[d][c]=y; used|=1ull<<y; }
    if(k>63) die("new layer wider than 63");
    vector<u64> nadj(k,0); for(int c=0;c<k;c++) for(int d=0;d<k;d++) if(c!=d && nm[c][d]<nt) nadj[c]|=1ull<<d;
    int fb=1;
    if(mod){
      fb=diameter_bound(k,nadj); if(fb<0) return; if(k+fb>B) return;
      string prof=dist_profile(k,nadj); auto it=firstA.find(prof); int anow=N-B;
      int w = (it==firstA.end())? anow : it->second;
      if(w>fb) fb=w;
      if(k+fb>B) return;
      if(it==firstA.end()) firstA.emplace(move(prof),anow);
    } else {
      // lower semimodular: elements without a common lower cover have no common upper cover
      if(modeD){ u64 fk=(1ull<<k)-1; for(int c=0;c<k;c++) if(nadj[c]!=(fk&~(1ull<<c))){ fb=3; break; } }
      if(k+fb>B) return;
      if(ATOM && k<S.nat) return;   // Dowling-Wilson: every layer strictly between bottom and top has at least as many elements as there are atoms
      if(COATOM){ for(int x=0;x<nt;x++){ int cnt=0; for(int c=0;c<k;c++) if(D[c]>>x&1) cnt++; if(cnt<2) return; } }
    }
    // ---- orbit representative test: canonical form of the family under Gamma ----
    if(!trivialG){
      string best=famcanon(D);
      if(!seenFam.insert(best).second) return;
    }
    nTrans++;
    // ---- new group Gamma' ----
    vector<u64> E; vector<int> mu, firstMember; for(int c=0;c<k;c++){ if(c>0 && D[c]==D[c-1]) mu.back()++; else { E.push_back(D[c]); mu.push_back(1); firstMember.push_back(c); } }
    int q=E.size(); if(q>64) die("too many distinct sets");
    State NS; NS.nt=k;
    vector<int> setcls(q); iota(setcls.begin(),setcls.end(),0);
    vector<Perm> Hsets;
    if(trivialG){ Perm id(q); iota(id.begin(),id.end(),0); Hsets.push_back(id); }
    else {
      vector<vector<u64>> Eh(nH, vector<u64>(q));
      for(int h=0;h<nH;h++) for(int i=0;i<q;i++){ u64 m=E[i], r=0; while(m){ int x=ctz(m); m&=m-1; r|=1ull<<S.H[h][x]; } Eh[h][i]=r; }
      vector<pair<int,u64>> sigB(nt); for(int y=0;y<nt;y++){ u64 sg=0; for(int i=0;i<q;i++) if(E[i]>>y&1) sg|=1ull<<i; sigB[y]={S.cls[y],sg}; }
      auto oracle=[&](const vector<int>& sigma, u64 assigned)->bool{
        u64 img=0; { u64 m=assigned; while(m){ int i=ctz(m); m&=m-1; img|=1ull<<sigma[i]; } }
        vector<pair<int,u64>> B2(nt); for(int y=0;y<nt;y++) B2[y]={sigB[y].first, sigB[y].second&img}; sort(B2.begin(),B2.end());
        for(int h=0;h<nH;h++){ vector<pair<int,u64>> A(nt); for(int x=0;x<nt;x++){ u64 sg=0; u64 m=assigned; while(m){ int i=ctz(m); m&=m-1; if(Eh[h][i]>>x&1) sg|=1ull<<sigma[i]; } A[x]={S.cls[x],sg}; }
          sort(A.begin(),A.end()); if(A==B2) return true; }
        return false; };
      u64 allq = (q==64)? ~0ull : ((1ull<<q)-1);
      { vector<int> sigma(q); for(int i=0;i<q;i++) for(int j=i+1;j<q;j++){ if(mu[i]!=1||mu[j]!=1||pc(E[i])!=pc(E[j])) continue; if(setcls[j]!=j) continue; if(setcls[i]!=i) continue;
            iota(sigma.begin(),sigma.end(),0); sigma[i]=j; sigma[j]=i; if(oracle(sigma,allq)) setcls[j]=i; } }
      vector<int> sigma(q,-1); u64 usedImg=0; u64 assigned=0;
      function<void(int)> rs=[&](int i){
        if(i==q){ if(oracle(sigma,allq)){ Perm p(q); for(int t=0;t<q;t++) p[t]=sigma[t]; Hsets.push_back(p); } return; }
        int prev=-1; for(int t=i-1;t>=0;t--) if(setcls[t]==setcls[i]){ prev=t; break; }
        for(int j=0;j<q;j++){ if(usedImg>>j&1) continue; if(mu[j]!=mu[i]||pc(E[j])!=pc(E[i])) continue;
          if(prev>=0){ if(setcls[j]!=setcls[sigma[prev]] || j<sigma[prev]) continue; }
          else { bool ok=true; for(int t=0;t<j;t++) if(setcls[t]==setcls[j] && !(usedImg>>t&1)) { ok=false; break; } if(!ok) continue; }
          sigma[i]=j; usedImg|=1ull<<j; assigned|=1ull<<i;
          if(oracle(sigma,assigned)) rs(i+1);
          usedImg&=~(1ull<<j); assigned&=~(1ull<<i); sigma[i]=-1; }
      };
      rs(0);
      if(Hsets.empty()) die("identity not found in new group");
    }
    NS.cls.assign(k,0);
    for(int i=0;i<q;i++){ int rep = (mu[i]>1)? firstMember[i] : firstMember[setcls[i]]; for(int t=0;t<mu[i];t++) NS.cls[firstMember[i]+t]=rep; }
    for(auto& sg: Hsets){ Perm p(k); for(int i=0;i<q;i++) for(int t=0;t<mu[i];t++) p[firstMember[i]+t]=firstMember[sg[i]]+t; NS.H.push_back(p); }
    // ---- new Y ----
    vector<int> oldidx; { u64 m=used; while(m){ int y=ctz(m); m&=m-1; oldidx.push_back(y); } }
    int ny2=k+oldidx.size(); if(ny2>64) die("Y larger than 64");
    vector<int> pos(ny,-1); for(size_t i=0;i<oldidx.size();i++) pos[oldidx[i]]=k+i;
    NS.ny=ny2; NS.below.assign(ny2,0); NS.lev1=0;
    for(size_t i=0;i<oldidx.size();i++){ int y=oldidx[i]; u64 m=S.below[y]&used, r=0; while(m){ int z=ctz(m); m&=m-1; r|=1ull<<pos[z]; } NS.below[k+i]=r; if(y<nt) NS.lev1|=1ull<<(k+i); }
    for(int c=0;c<k;c++){ u64 r=1ull<<c; u64 dc=D[c]; while(dc){ int a=ctz(dc); dc&=dc-1; u64 m=S.below[a]&used; while(m){ int z=ctz(m); m&=m-1; r|=1ull<<pos[z]; } } NS.below[c]=r; }
    NS.fut=fb; NS.nat=S.nat;
    out.push_back(intern(NS));
  };

  // ---- singles ----
  vector<int> lo(nt,0), hiAllowed(nt,0);
  function<void(int)> rec_s=[&](int a){
    if(a==nt){ process(); return; }
    u64 memb=0; for(size_t i=0;i<cl.size();i++) if(cl[i]>>a&1) memb|=1ull<<i;
    int hi=hiAllowed[a];
    // non-increasing within current class (same twin class, same clique memberships)
    for(int p=a-1;p>=0;p--) if(S.cls[p]==S.cls[a]){ u64 mp=0; for(size_t i=0;i<cl.size();i++) if(cl[i]>>p&1) mp|=1ull<<i; if(mp==memb){ hi=min(hi,msing[p]); break; } }
    for(int v=lo[a];v<=hi;v++){ msing[a]=v; int c=famcost(); if(c<0 || c>B) break; rec_s(a+1); }
    msing[a]=lo[a];
  };
  // ---- cliques ----
  auto Free=[&](int x)->u64{ return allowed[x]&~cov[x]; };
  auto finish=[&](){
      if(cl.size()>60) die("too many cliques");
      for(int x=0;x<nt;x++){ bool ok=true; bool inCl=false; smeet[x].assign(cl.size(),-1);
        for(size_t i=0;i<cl.size();i++){ if(cl[i]>>x&1){ inCl=true; continue; } int y=setmeet(1ull<<x,cl[i]); if(y<0){ ok=false; break; } smeet[x][i]=y; }
        lo[x]=inCl?0:1; hiAllowed[x]=(ok && !ATOM)? maxMembers : 0; if((!ok || ATOM) && !inCl){ for(int z=0;z<nt;z++) msing[z]=0; return; } msing[x]=lo[x]; }
      { int c=famcost(); if(c<0 || c>B){ for(int x=0;x<nt;x++) msing[x]=0; return; } }
      rec_s(0); for(int x=0;x<nt;x++) msing[x]=0; };
  // add line K if it satisfies the lattice condition against the lines chosen so far; then call next
  auto with_line=[&](u64 K, const function<void()>& next){
        int ncl=cl.size(); vector<int> row(ncl+1,-1);
        for(int j=0;j<ncl;j++){ int y=setmeet(K,cl[j]); if(y<0) return; row[j]=y; }
        vector<u64> save=cov; u64 m=K; while(m){ int x=ctz(m); m&=m-1; cov[x]|=K&~(1ull<<x); }
        cl.push_back(K); for(int j=0;j<ncl;j++) clmeet[j].push_back(row[j]); clmeet.push_back(row);
        next();
        clmeet.pop_back(); for(int j=0;j<ncl;j++) clmeet[j].pop_back(); cl.pop_back(); cov=save; };
  // optional lines (no required pair): generated in increasing order of their two smallest points
  function<void(int,int)> rec_opt=[&](int pa,int pb){
    finish();
    if((int)cl.size()+1>maxMembers) return;
    for(int a=max(pa,0);a<nt;a++) for(int b=(a==pa? pb+1 : a+1); b<nt; b++){
      if(!(Free(a)>>b&1)) continue;
      u64 X=Free(a)&Free(b)&~((2ull<<b)-1);
      vector<int> xs; { u64 m=X; while(m){ xs.push_back(ctz(m)); m&=m-1; } }
      function<void(int,u64)> sub=[&](int i,u64 K){
        if(i==(int)xs.size()){ with_line(K,[&](){ rec_opt(a,b); }); return; }
        sub(i+1,K);
        int x=xs[i]; if((K&~Free(x))==0) sub(i+1,K|1ull<<x); };
      sub(0,(1ull<<a)|(1ull<<b));
    }
  };
  // Stanton-Kalbfleisch: a linear space on v points with a line of k < v points has at least
  // 1 + k^2 (v-k)/(v-1) lines.  Applies when all pairs of T are adjacent (then the members with
  // at least two elements form a linear space on T).
  vector<char> okSize(nt+1,1);
  auto setOkSize=[&](){ if(!(modeU && allAdj) || nt<3) return; for(int k2=2;k2<nt;k2++){ long long num=(long long)k2*k2*(nt-k2), den=nt-1; long long need=1+(num+den-1)/den; okSize[k2]= need<=maxMembers; } };
  function<void()> rec_c=[&](){
    int a=-1; for(int x=0;x<nt;x++) if(required[x]&~cov[x]){ a=x; break; }
    if(a<0){ if(mod) finish(); else rec_opt(0,0); return; }
    if((int)cl.size()+1>maxMembers) return;
    { int need=1; for(int x=0;x<nt;x++){ u64 u=required[x]&~cov[x]; if(!u) continue; for(u64 K: cl) if(!(K>>x&1)) need=max(need,pc(u&K)); }
      if((int)cl.size()+need>maxMembers) return; }
    if(pairOK){ // pair-counting bound: a future line avoids every saturated point z, and meets each line
      // through z at most once, so it has at most r_z points adjacent to z.
      int P=0, maxdeg=0; u64 unsat=0; for(int x=0;x<nt;x++){ int d=pc(adj[x]&~cov[x]); P+=d; maxdeg=max(maxdeg,d); if(d) unsat|=1ull<<x; } P/=2;
      int Lmax=maxdeg+1;
      for(int z=0;z<nt;z++) if(adj[z] && !(unsat>>z&1)){ int rz=0; for(u64 K: cl) if(K>>z&1) rz++; Lmax=min(Lmax, rz+pc(unsat&~adj[z])); }
      if(modeU && allAdj){ int mx=0; for(u64 K: cl) mx=max(mx,pc(K)); if(mx) Lmax=min(Lmax,nt-mx+1); while(Lmax>2 && !okSize[Lmax]) Lmax--; }
      if(Lmax<2) Lmax=2;
      if(modeU && allAdj && !cl.empty()){ // lines through x: at least rlb[x]; a line K meets 1 + sum_{x in K}(r_x - 1) lines
        int rlb[64]; for(int x=0;x<nt;x++){ int rz=0; for(u64 K: cl) if(K>>x&1) rz++; int u=pc(adj[x]&~cov[x]); rlb[x]=rz+(u+Lmax-2)/(Lmax-1); }
        int ncl=cl.size();
        for(int x=0;x<nt;x++){ int off=0; for(u64 K: cl) if(!(K>>x&1)) off++; if(rlb[x]+off>maxMembers) return; }
        for(u64 K: cl){ int tot=1; u64 m=K; while(m){ int x=ctz(m); m&=m-1; tot+=rlb[x]-1; } if(tot>maxMembers) return; }
        (void)ncl; }
      int per=Lmax*(Lmax-1)/2; int needL=(P+per-1)/per;
      if((int)cl.size()+needL>maxMembers) return; }
    // isomorph rejection of partial clique sets (equivalent partial sets have equivalent completions);
    // done after the cheap bounds because the canonical form is the expensive step
    if(!trivialG && !cl.empty()){
      // the table is only a cache: when it is full, new configurations are no longer recorded
      // (they are then explored again, and duplicates among complete families are still removed)
      if(seenPart.size()<SEENPART_CAP){ if(!seenPart.insert(famcanon(cl)).second) return; }
      else if(seenPart.count(famcanon(cl))) return; }
    u64 U_a=required[a]&~cov[a]; int b=ctz(U_a);
    u64 X=Free(a)&Free(b)&~(1ull<<b)&~(1ull<<a);
    vector<int> xs; { u64 m=X; while(m){ xs.push_back(ctz(m)); m&=m-1; } }
    // de Bruijn-Erdos: the lines meeting a set Q of pairwise adjacent points in >= 2 points
    // form a linear space on Q, so unless one line contains Q there are at least |Q| lines.
    u64 forced=0;
    { u64 Q=(1ull<<a)|(1ull<<b); u64 cand=adj[a]&adj[b];
      while(cand){ int best=-1, bd=-1; u64 m=cand; while(m){ int x=ctz(m); m&=m-1; int d=pc(adj[x]&cand)+((X>>x&1)?64:0); if(d>bd){ bd=d; best=x; } } Q|=1ull<<best; cand&=adj[best]; }
      if(pc(Q)>maxMembers){ if(Q&~(X|(1ull<<a)|(1ull<<b))) return; forced=Q; } }
    vector<u64> memb(nt,0); for(size_t i=0;i<cl.size();i++) for(int x=0;x<nt;x++) if(cl[i]>>x&1) memb[x]|=1ull<<i;
    function<void(int,u64)> sub=[&](int i,u64 K){
      if(i==(int)xs.size()){
        if(!okSize[pc(K)]) return;
        for(int x=0;x<nt;x++) if(!(K>>x&1)) for(int y=x+1;y<nt;y++) if((K>>y&1) && S.cls[y]==S.cls[x] && memb[y]==memb[x]) return;
        if(DIST){ // distributive: no three elements of a line with a common pairwise meet
          int e[64], ne=0; u64 mm=K; while(mm){ e[ne++]=ctz(mm); mm&=mm-1; }
          for(int p=0;p<ne;p++) for(int q2=p+1;q2<ne;q2++) for(int r2=q2+1;r2<ne;r2++) if(meet[e[p]][e[q2]]==meet[e[p]][e[r2]] && meet[e[p]][e[q2]]==meet[e[q2]][e[r2]]) return; }
        if(mod){ int ncl=cl.size();
          // Plane condition (a consequence of modularity, one layer ahead)
          for(int j=0;j<ncl;j++) if(pc(cl[j]&K)==1){ u64 un=cl[j]|K; int np=0; u64 Pi[64];
              for(int t=0;t<ncl;t++) if(pc(cl[t]&un)>=2) Pi[np++]=cl[t];
              for(int t=0;t<np;t++){ if(!(Pi[t]&K)) return; }
              for(int t=0;t<np;t++) for(int u=t+1;u<np;u++) if(!(Pi[t]&Pi[u])) return; }
          for(int j=0;j<ncl;j++) for(int t=j+1;t<ncl;t++) if(pc(cl[j]&cl[t])==1){ u64 un=cl[j]|cl[t]; if(pc(K&un)<2) continue;
              for(int u=0;u<ncl;u++) if(pc(cl[u]&un)>=2 && !(cl[u]&K)) return; } }
        with_line(K,[&](){ rec_c(); }); return; }
      int x=xs[i];
      if(!(forced>>x&1)) sub(i+1,K);
      if((K&~Free(x))==0) sub(i+1,K|1ull<<x);
    };
    sub(0,(1ull<<a)|(1ull<<b));
  };
  maxMembers = B-1; if(maxMembers<1) maxMembers=1;
  if(ATOM && S.nat>B-1){ // by Dowling-Wilson only the top can follow
    out.push_back(SINGLE); nTrans++; states[sid].tr=move(out); states[sid].expanded=true; return; }
  setOkSize();
  rec_c();
  states[sid].tr=move(out); states[sid].expanded=true;
}

int main(int argc,char**argv){
  N=atoi(argv[1]); const char* dualfile=argc>2?argv[2]:nullptr; verbose=true;
  string mode=argc>3?argv[3]:"modular";
  if(mode=="modular"){} else if(mode=="dist"){ DIST=true; }
  else if(mode=="usm"){ modeD=false; } else if(mode=="lsm"){ modeU=false; }
  else if(mode=="graded"){ modeU=modeD=false; }
  else if(mode=="geometric"){ modeD=false; ATOM=true; } else if(mode=="cogeometric"){ modeU=false; COATOM=true; }
  else { fprintf(stderr,"unknown mode\n"); return 1; }
  if(dualfile && !strcmp(dualfile,"-")) dualfile=nullptr;
  { State s; s.ny=1; s.nt=1; s.below={1}; s.lev1=0; s.cls={0}; s.H={Perm{0}}; s.fut=0; states.push_back(s); idx["__single__"]=0; }
  // counts are tagged by the number of atoms m (key = state id * 256 + m)
  vector<unordered_map<u64,u128>> by(N+2); vector<u128> vi(N+2,0); map<array<int,3>,u128> viAB;
  // from the single-element frontier: m >= 1 new elements all covering it
  // (m = 1 gives the 2-element chain)
  { for(int m=1;1+m+(m>1?1:0)<=N;m++){ if(m==1){ vi[2]+=1; viAB[{2,1,1}]+=1; continue; }
      if(m>255) die("too many atoms");
      State NS; NS.nt=m; NS.ny=m+1; NS.below.assign(m+1,0); for(int c=0;c<m;c++) NS.below[c]=(1ull<<c)|(1ull<<m); NS.below[m]=1ull<<m; NS.lev1=1ull<<m;
      NS.cls.assign(m,0); Perm id(m); iota(id.begin(),id.end(),0); NS.H={id}; NS.fut=1; if(ATOM) NS.nat=m;
      { vector<u64> full(m); for(int c=0;c<m;c++) full[c]=((1ull<<m)-1)&~(1ull<<c); firstA.emplace(dist_profile(m,full),1); }
      int t=intern(NS); by[1+m][((u64)t<<8)|m]+=1; } }
  time_t t0=time(0);
  for(int a=2;a<=N;a++){
    vector<pair<u64,u128>> items(by[a].begin(),by[a].end()); unordered_map<u64,u128>().swap(by[a]);
    sort(items.begin(),items.end(),[](const pair<u64,u128>&x,const pair<u64,u128>&y){return x.first<y.first;});
    for(auto& it: items){ int sid=it.first>>8; int m=it.first&255; u128 c=it.second;
      if(!states[sid].expanded) expand(sid,N-a);
      const vector<int> tr=states[sid].tr; int ntop=states[sid].nt;
      for(int t: tr){ if(t==SINGLE){ if(a+1<=N){ vi[a+1]+=c; viAB[{a+1,m,ntop}]+=c; } } else { int a2=a+states[t].nt; if(a2+states[t].fut<=N) by[a2][((u64)t<<8)|m]+=c; } }
    }
    if(verbose) fprintf(stderr,"acc=%d states=%zu families=%llu trans=%llu nauty=%llu %lds\n",a,states.size(),(unsigned long long)nFam,(unsigned long long)nTrans,(unsigned long long)nNauty,(long)(time(0)-t0));
  }
  if(dualfile){ FILE* fo=fopen(dualfile,"w"); for(auto& kv: viAB) fprintf(fo,"%d %d %d %s\n",kv.first[0],kv.first[1],kv.first[2],to_s(kv.second).c_str()); fclose(fo); }
  vector<u128> f(N+2,0); f[1]=1;
  for(int n=2;n<=N;n++){ u128 s=0; for(int k=2;k<=n;k++) s+=vi[k]*f[n-k+1]; f[n]=s; }
  for(int n=1;n<=N;n++) printf("%d %s %s\n",n,to_s(vi[n]).c_str(),to_s(f[n]).c_str());
  fprintf(stderr,"states=%zu families=%llu trans=%llu nauty=%llu\n",states.size(),(unsigned long long)nFam,(unsigned long long)nTrans,(unsigned long long)nNauty);
}
