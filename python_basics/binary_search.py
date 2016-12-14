def binarysearc(list,value):
    n=bsearch(list,value,(len(list)-1),0)
    return n    
def bsearch(list,value,i,j):
    middle = j+(i-j)/2
    
    if i==j:return i
    #elif 
    elif value == list[middle]:return middle 
    elif value > list[middle]:return bsearch(list,value,i,middle+1) 
           
    return bsearch(list,value,middle-1,j)
