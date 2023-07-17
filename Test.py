import pandas as pd

def tach(all,out):
    return list(set(all).difference(out))

ALL = []

df1 = pd.read_excel(r'/storage/emulated/0/Download/python/goi_cuoc.xlsx')
a =list(df1['Goi'])
for i in a:
	b=i.split(',')
	ALL+=b
ALL=list(dict.fromkeys(ALL))
#print(len(ALL))

dt = {}
lst_cc = list(dict.fromkeys(list(df1['Nuoc'])))
for i in lst_cc:
    df2 = df1[df1['Nuoc']==i]
    df2 = df2.drop(columns=['Nuoc'])
    dt[i] = df2
#print(dt)
#print(ALL)


def run(df):
    data = {}
    for index, row in df.iterrows():    
        data[row['Mang']]=row['Goi'].split(',')
    all_cc=[]
    for i,j in data.items():
        all_cc = all_cc+j
    all_cc = list(data.fromkeys(all_cc))
    #print(all_cc)

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
    #print(out)
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
#ALL=[]
for i,j in dt.items():
	out_data[i]=run(j)
	#ALL=ALL.extend(j)
	#print(i)
df=pd.DataFrame(columns=['Nuoc','Mang','Goi','Noi dung','Goi cau hinh'])
#print(ALL)
	
for i,j in out_data.items():
	for m,n in j.items():
		for a,b in n.items():
			c=b.split(',')
			d=tach(ALL,c)
			e=','.join(d)

			df.loc[len(df)]=[i,m,b,a,e]
df.to_csv('out.csv')



