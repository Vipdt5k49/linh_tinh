import requests
import pandas as pd
import re
import os
import pathlib
from datetime import datetime, timedelta
PATH = pathlib.Path(__file__).parent.resolve()

def check_updated_vesaf():
    def get_url():
        r=requests.get('https://wm.vinacapital.com/information-disclosure/')
        token = re.search(r'field_csrf_ft" value="[a-z0-9]{10}',r.text).group()[-10:]
        data = {'action': 'filterdiscl','data': f'txtfund=vesaf&txtcat=regular&txtnextp=1&field_csrf_ft={token}&_wp_http_referer=%2Finformation-disclosure%2F&txtkeywords=&mmyyyy='}
        response = requests.post('https://wm.vinacapital.com/wp-admin/admin-ajax.php',  data=data)
        url=re.search(r'http.{0,}_VESAF_FMS.*Thang_.{0,}xlsx',response.text).group()
        file_new=re.search(r'.{8}_VESAF_FMS.*Thang_.{0,}xlsx',url).group()
        return url, file_new
    
    vesaf_is_updated = False

    for x in os.listdir(PATH):
        if 'VESAF' in x and '~' not in x:
            now = datetime.now()
            now_str = now.strftime("%Y%m")
            file_time_str =x[:6]
            
            if int(now_str) - int(file_time_str)+1 < 2:
                vesaf_is_updated = True
                print(x)
                break
            else:
                k = get_url()
                url = k[0]
                file_new = k[1]
                if x == file_new:
                    vesaf_is_updated = True
                    print(file_new)
                    break
                else:
                    os.remove(f'{PATH}/{x}')
                    response = requests.get(url)
                    open(f'{PATH}/{file_new}', "wb").write(response.content)
                    vesaf_is_updated = True
                    print(file_new)
                    break
            
    if vesaf_is_updated == False:
        t = get_url()
        url = t[0]
        file_new = t[1]
        response = requests.get(url)
        open(f'{PATH}/{file_new}', "wb").write(response.content)
        print(file_new)


def check_updated_dcds():
    dcds_is_updated = False
    def get_url1():
        r = requests.get('https://dragoncapital.com.vn/bieu-mau-tai-lieu-quy/tai-lieu-quy/')
        file_new = f"{re.search(r'DCDS_BC_Thang_.{6}',r.text).group()}.xlsx"
        datetime_str  = file_new[14:20]
        datetime_object = datetime.strptime(datetime_str, '%m%Y')
        datetime_object = datetime_object + timedelta(days=31)
        datetime_str = datetime_object.strftime('%Y/%m')
        url = f'https://vfmcomvnaz.azureedge.net/dcvfmcomvn/uploads/vfm_files/report/{datetime_str}/{file_new}'
        return url, file_new


    for x in os.listdir(PATH):
        if 'DCDS' in x and '~' not in x:
            now = datetime.now()
            now_str = now.strftime("%Y%m")
            file_time_str = f'{x[-9:-5]}{x[-11:-9]}'
            if int(now_str) - int(file_time_str) < 2:
                dcds_is_updated = True
                print(x)
                break
            else:
                k = get_url1()
                url = k[0]
                file_new = k[1]
                if x == file_new:
                    dcds_is_updated = True
                    print(file_new)
                    break
                else:
                    os.remove(f'{PATH}/{x}')
                    response = requests.get(url)
                    open(f'{PATH}/{file_new}', "wb").write(response.content)
                    dcds_is_updated = True
                    print(file_new)
                    break

    if dcds_is_updated == False:
        t = get_url1()
        url = t[0]
        file_new = t[1]
        response = requests.get(url)
        open(f'{PATH}/{file_new}', "wb").write(response.content)
        print(file_new)

check_updated_vesaf()
check_updated_dcds()


dfDCDS=pd.DataFrame()
dfVESAF=pd.DataFrame()
def get_symbol(file_name):
    xls= pd.ExcelFile(rf'{PATH}/{file_name}')
    df=xls.sheet_names
    k=[i for i in df if i.startswith('BCDanhMuc')][0]
    df=pd.read_excel(xls,sheet_name=k,usecols='b,d,g',names=['symbol','quantity','total'])
    start=df[df['symbol'].str.contains("SHARES LIST")==True].index[0]
    end=df[df['symbol'].str.contains("SHARES UNLIST")==True].index[0]
    df=df.iloc[start+1:end+1].reset_index(drop=True)
    total=df[df['symbol'].str.contains("TOTAL")==True].index[0]
    total_per=df.iloc[total]['total']
    df=df.dropna().drop(columns='total').reset_index(drop=True)
    return df,total_per

for x in os.listdir(PATH):
    if 'DCDS' in x and '~' not in x:
        temp=get_symbol(x)
        percentDCDS = temp[1]
        dfDCDS = dfDCDS.append(temp[0])
    if 'VESAF' in x and '~' not in x:
        temp=get_symbol(x)
        percentVESAF = temp[1]
        dfVESAF = dfVESAF.append(temp[0])

def dfFinal(dfData):
    dfFinal=dfData.merge(dfAll,how='left',on='symbol')
    dfFinal['referenceSum']=dfFinal['quantity']*dfFinal['referencePrice']
    dfFinal['currentSum']=dfFinal['quantity']*dfFinal['currentPrice']
    dfFinal['change']=(dfFinal['currentPrice']-dfFinal['referencePrice'])/dfFinal['referencePrice']*100
    return dfFinal


def get_price(san):
    data = {
        'type': san,
        'typeTab': 'M',
        'sort': 'SortName-up',
        'stockStr': '',
    }
    response = requests.post('https://prs.tvsi.com.vn/get-detail-stock-by', data=data)
    return response.json()['arrDetailStock']

while True:
    lst = []
    for i in ['HSX','HNX','UPCOM']:
        lst.extend(get_price(i))


    dfAll = pd.DataFrame(columns=['symbol','referencePrice','currentPrice'])

    for i in lst:
        temp = re.search('.{5}last_price\*([^\*]*)',i).group()
        if temp[0] != '|':continue
        temp=temp[1:]
        lst = temp.split('_last_price*')
        s = lst[0]
        if lst[1] == '':
            temp = re.search('ref_price\*([^\*]*)',i).group()
            p1 = p2 = temp.split('*')[1]
        else:
            temp = re.search('ref_price\*([^\*]*)',i).group()
            p1 = temp.split('*')[1].replace(',','')
            p2 = lst[1].replace(',','')
        dfAll.loc[len(dfAll.index)] = [s, float(p1), float(p2)]



    dfDCDSFinal=dfFinal(dfDCDS)

    ref_tong=dfDCDSFinal['referenceSum'].sum()
    cur_tong=dfDCDSFinal['currentSum'].sum()
    change=(cur_tong-ref_tong)/ref_tong*100
    print('DCDS','|','{0:.2f}'.format(ref_tong),'|','{0:.2f}'.format(cur_tong),'|','{0:.2f}'.format(change),'%','|','{0:.2f}'.format(change*percentDCDS),'%')
    dfVESAFFinal=dfFinal(dfVESAF)
    ref_tong=dfVESAFFinal['referenceSum'].sum()
    cur_tong=dfVESAFFinal['currentSum'].sum()
    change=(cur_tong-ref_tong)/ref_tong*100
    print('VESAF','|','{0:.2f}'.format(ref_tong),'|','{0:.2f}'.format(cur_tong),'|','{0:.2f}'.format(change),'%','|','{0:.2f}'.format(change*percentVESAF),'%')
    print('\n')