import pandas as pd

def tach(all,out):
    return list(set(all).difference(out))

ALL = ['DR5','TQ3','DX7','ASIA5','IR5','IR7','TQ7']
data = {}
df = pd.read_excel(r'C:\Users\Admin\Desktop\goi_cuoc.xlsx')
for index, row in df.iterrows():    
    data[row['Mang']]=row['Goi'].split(',')
all_cc=[]
for i,j in data.items():
    all_cc = all_cc+j
all_cc = list(data.fromkeys(all_cc))

out = {}
for i,j in data.items():
    
    out[i]={}
    temp = dict(data)
    del temp[i]
    p=[]
    for m,n in temp.items():
        p = p+n
    p=tach(p,j)
    t={}
    for m in p:
        t[m]=''
        for n,h in temp.items():
            if m in h:
                if t[m]=='':t[m]+=f'{n}'
                else:t[m]+=f',{n}'
        
    o = {}
    for m,n in t.items():
        try:
            o[n]=o[n]+f',{m}'
        except:
            o[n]=''
            o[n]=o[n]+f'{m}'

    out[i]=o
t={}
for m in all_cc:
    t[m]=''
    for n,h in data.items():
            if m in h:
                if t[m]=='':t[m]+=f'{n}'
                else:t[m]+=f',{n}'
o = {}
for m,n in t.items():
    try:
        o[n]=o[n]+f',{m}'
    except:
        o[n]=''
        o[n]=o[n]+f'{m}'
out['All']=o





