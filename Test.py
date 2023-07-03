import re
import time
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Process

def find(string):
	x=re.search(r'\d+',string).group()
	return x

def run1(list):
	for i in list:
		print(find(i))

def mt(lst):
	process =[]
	for i in lst:
		process.append(Process(target=run1,args=(i,)))
	for p in process:
		p.start()
	for p in process:
		p.join()

s='abc'*1000000
list= [f'{s}{x}{s}' for x in range(1,101)]
list1= [f'{s}{x}{s}' for x in range(1,21)]
list2= [f'{s}{x}{s}' for x in range(21,41)]
list3= [f'{s}{x}{s}' for x in range(41,61)]
list4= [f'{s}{x}{s}' for x in range(61,81)]
list5= [f'{s}{x}{s}' for x in range(81,101)]	

if __name__ == '__main__':
    start=time.time()
    mt([list1,list2,list3,list4,list5])
    #for i in list:print(find(i))
    print(time.time()-start)
