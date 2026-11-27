from t1 import *
import sys
N=int(sys.argv[1])
for name in ['trunk','pathcomp','strict','levels']:
    test(name,2,N)
