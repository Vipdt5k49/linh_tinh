import pandas as pd

def tach(all,out):
    return list(set(all).difference(out))



ALL = []

df1 = pd.read_excel(r'C:\Users\Admin\Desktop\PYTHON\wsms\goi_cuoc.xlsx')
a =list(df1['Goi'])
for i in a:
	b=i.split(',')
	ALL+=b
ALL=list(dict.fromkeys(ALL))

dt = {}
lst_cc = list(dict.fromkeys(list(df1['Nuoc'])))
for i in lst_cc:
    df2 = df1[df1['Nuoc']==i]
    df2 = df2.drop(columns=['Nuoc'])
    dt[i] = df2



def run(df):
    data = {}
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
    return out

out_data = {}

for i,j in dt.items():
	out_data[i]=run(j)

df1 = pd.read_excel(r'C:\Users\Admin\Desktop\PYTHON\wsms\nhom_goi.xlsx')
dt = {}
lst_cc = list(dict.fromkeys(list(df1['Nhom'])))
for i in lst_cc:
    df2 = df1[df1['Nhom']==i]
    df2 = df2.drop(columns=['Nhom'])
    dt[i] = list(df2['Goi'])


for a,b in out_data.items():
    for c,d in b.items():
        for e,f in d.items():
            d1={}
            d1[e]={}
            g=f.split(',')
            for h in g:
                for i,j in dt.items():
                    if h in j:
                        #print(a,c,e,h,i)
                        try:d1[e][i]+=f',{h}'
                        except:d1[e][i]=h
                        continue
            d.update(d1)

df=pd.DataFrame(columns=['Nuoc','Mang','Goi','ND nhom goi','ND mang can vao','Goi cau hinh'])

for a,b in out_data.items():
    for c,d in b.items():
        for e,f in d.items():
            for g,h in f.items():
                i = h.split(',')
                j = tach(ALL,i)
                p = ','.join(j)
                df.loc[len(df)]=[a,c,h,g,e,p]

df.to_csv(r'C:\Users\Admin\Desktop\PYTHON\wsms\out.csv')
