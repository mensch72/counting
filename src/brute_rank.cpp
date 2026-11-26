// Brute-force check: read Hasse diagrams of all k-point posets (digraph6, from
// nauty's genposetg) and tabulate, for series-indecomposable posets (i.e. those
// whose ideal lattice is vertically indecomposable), the number with n ideals.
#include <bits/stdc++.h>
using namespace std; typedef uint32_t u32;
int main(int argc,char**argv){ int NMAX=atoi(argv[1]); string line; map<pair<int,int>,unsigned long long> T; unsigned long long tot=0;
  while(getline(cin,line)){ if(line.empty()||line[0]!='&') continue; int n=line[1]-63; u32 up[32]={0};
    int bit=0; for(int i=0;i<n;i++) for(int j=0;j<n;j++,bit++){ int c=line[2+bit/6]-63; if(c>>(5-bit%6)&1) up[i]|=1u<<j; }
    for(int k=0;k<n;k++) for(int i=0;i<n;i++) if(up[i]>>k&1) up[i]|=up[k];   // transitive closure
    u32 dn[32]={0}; for(int i=0;i<n;i++) for(int j=0;j<n;j++) if(up[i]>>j&1) dn[j]|=1u<<i;
    tot++;
    // incomparability graph connected?
    u32 full=(1u<<n)-1, comp=1, fr=1; while(fr){ int x=__builtin_ctz(fr); fr&=fr-1; u32 nb=full&~(up[x]|dn[x]|1u<<x)&~comp; comp|=nb; fr|=nb; }
    if(comp!=full && n>1) continue;
    // count ideals (cap)
    vector<int> ord; u32 done=0; while((int)ord.size()<n) for(int x=0;x<n;x++) if(!(done>>x&1)&&(dn[x]&~done)==0){ord.push_back(x);done|=1u<<x;}
    vector<u32> id{0}; bool over=false; for(int x:ord){ size_t sz=id.size(); for(size_t i=0;i<sz;i++) if((id[i]&dn[x])==dn[x]){ id.push_back(id[i]|1u<<x); if((int)id.size()>NMAX){over=true;break;} } if(over)break; }
    if(!over) T[{(int)id.size(),n}]++;
  }
  for(auto&kv:T) printf("%d %d %llu\n",kv.first.first,kv.first.second,kv.second); fprintf(stderr,"posets read: %llu\n",tot);
}
