import time
import pandas as pd
f = open(r'C:\Users\Admin\Desktop\PYTHON\test.txt','r')
data = f.read()

lst = data.split('PSX:V12.02.04R000:IGHL02PSX01')[1:-1]
lst_label = []
labels = [x for x in lst[0].split('\n') if ':' in x][:-1]
for label in labels:
    a = label.split(':')[0].strip()
    lst_label.append(a)

df = pd.DataFrame(columns=lst_label)


i=1
for a in lst:
    print(i)
    lst1 = [x for x in a.split('\n') if ':' in x][:-1]
    c = []
    for b in lst1:
        c.append(b.split(':')[1])
    
    df.loc[len(df)]=c
    i=i+1

print(df)
