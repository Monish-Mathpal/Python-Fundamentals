#This code helps to use advance print function and 
#range operator with *operator in Phthon2
from __future__ import print_function
print(*range(1, input() + 1), sep="") 

#The above code written in python3
print(*range(1, int(input()) + 1), sep="")  
#Evaluating a list of commands
ntime = int(input())
olist = []
for looper in range(1,ntime+1):
	cmnd  = input()
	cmnd = cmnd.split(' ')
	if cmnd[0] != 'print':
    	eval("olist." + cmnd[0] + "(" + ",".join(cmnd[1:]) + ")")
   	 
	else:
    	print (olist)

