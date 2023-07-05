import pandas as pd
import re
xls= pd.ExcelFile(rf'/storage/emulated/0/Download/DCDS_BC_Thang_052023.xlsx')
#df=pd.read_excel(xls,sheet_name='BCDanhMucDauTu_06029')
df=xls.sheet_names
k=[i for i in df if i.startswith('BCDanhMuc')][0]
df=pd.read_excel(xls,sheet_name=k,usecols='a,b,d',names=['id','stock','quanity'])
index_start=df[df.id.find('II')].index[0]
index_end=df[df.id=='III'].index[1]
df=df.iloc[index_start:index_end]
print(df)
print(index_start)
#for i in df['id']:print(i)
#print(df[df.id=='II'].index[0])
