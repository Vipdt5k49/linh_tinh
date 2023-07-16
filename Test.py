lst1 =[1,2,3,5,7]
lst2=[7,2,8,9,0,45,653]
lst3=[1,3,7,986,111,44,22]

lst=lst1+lst2+lst3
lst=list(dict.fromkeys(lst))
#print(lst)
dt={}
for i in lst:dt[i]=''
lst_dict={'lst1':lst1,'lst2':lst2,'lst3':lst3}
#print(lst_dict)
for i in lst:
	for key, value in lst_dict.items():
		if i in value:
			dt[i]+=f',{key}'

names = set(dt.values())
d = {}
for n in names:
    d[n] = [k for k in dt.keys() if dt[k] == n]
for x,y in d.items():
	x=x[1:]
	print(x,y)

			