// Brute-force check for the bounded-width automaton: read Hasse diagrams of posets (digraph6 from
// nauty's genposetg); for the series-indecomposable ones tabulate (number of down-sets n, number
// of points k, largest number of down-sets of equal size) -> count.
#include <bits/stdc++.h>
using namespace std; typedef uint32_t u32;
int main(int argc,char**argv){ int NMAX=atoi(argv[1]); string line; map<array<int,3>,unsigned long long> T;
  while(getline(cin,line)){ if(line.empty()||line[0]!='&') continue; int n=line[1]-63; u32 up[32]={0};
    int bit=0; for(int i=0;i<n;i++) for(int j=0;j<n;j++,bit++){ int c=line[2+bit/6]-63; if(c>>(5-bit%6)&1) up[i]|=1u<<j; }
    for(int k=0;k<n;k++) for(int i=0;i<n;i++) if(up[i]>>k&1) up[i]|=up[k];
    u32 dn[32]={0}; for(int i=0;i<n;i++) for(int j=0;j<n;j++) if(up[i]>>j&1) dn[j]|=1u<<i;
    u32 full=(1u<<n)-1, comp=1, fr=1; while(fr){ int x=__builtin_ctz(fr); fr&=fr-1; u32 nb=full&~(up[x]|dn[x]|1u<<x)&~comp; comp|=nb; fr|=nb; }
    if(comp!=full && n>1) continue;
    vector<int> ord; u32 done=0; while((int)ord.size()<n) for(int x=0;x<n;x++) if(!(done>>x&1)&&(dn[x]&~done)==0){ord.push_back(x);done|=1u<<x;}
    vector<u32> id{0}; bool over=false; for(int x:ord){ size_t sz=id.size(); for(size_t i=0;i<sz;i++) if((id[i]&dn[x])==dn[x]){ id.push_back(id[i]|1u<<x); if((int)id.size()>NMAX){over=true;break;} } if(over)break; }
    if(over) continue; int lay[33]={0}, mx=0; for(u32 I: id){ int c=__builtin_popcount(I); mx=max(mx,++lay[c]); }
    T[{(int)id.size(),n,mx}]++; }
  for(auto&kv:T) printf("%d %d %d %llu\n",kv.first[0],kv.first[1],kv.first[2],kv.second); }
