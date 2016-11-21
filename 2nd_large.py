#finding second largest number in the list
n = int(input())
lis = sorted(list(set(list(map(int,input().split(' '))))))
i=len(lis)-1
while True:
	if lis[i] < max(lis):
    	break
	else:
    	i-=1
   	 
print (lis[i]) 
