import re
import time
lst = ['abc']*10000000
s=time.time()
for i in lst:
    t=re.search('b',i)
print(time.time()-s)
