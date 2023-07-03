import re
import time
import requests 
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Process
s='abc'*1000000
list= [f'{s}{x}{s}' for x in range(1,101)]
list1= [f'{s}{x}{s}' for x in range(1,21)]
list2= [f'{s}{x}{s}' for x in range(21,41)]
list3= [f'{s}{x}{s}' for x in range(41,61)]
list4= [f'{s}{x}{s}' for x in range(61,81)]
list5= [f'{s}{x}{s}' for x in range(81,101)]
out=[]
f=open('o.txt','w')
def find(string):
	x=re.search(r'\d+',string).group()
	#f.write(x)
	return x

def run1(list):
	for i in list:
		f.write(find(i))

start=time.time()
def mt():
	process =[]
	for i in [list1,list2,list3,list4,list5]:
		process.append(Process(target=run1,args=(i,)))
	for p in process:
		p.start()
	for p in process:
		p.join()
	
		
#	p1=Process(target=run1,args=(list1,))
#	p1.start()
#	p2=Process(target=run1,args=(list2,))
#	p2.start()
#	p3=Process(target=run1,args=(list3,))
#	p3.start()
#	p4=Process(target=run1,args=(list4,))
#	p4.start()
#	p5=Process(target=run1,args=(list5,))
#	p5.start()
#	p1.join()
#	p2.join()
#	p3.join()
#	p4.join()
#	p5.join()
	
mt()
f.close ()
print(time.time()-start)

