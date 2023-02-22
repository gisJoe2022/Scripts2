# Python3 program to Find missing
# integers in list
		
def find_missing(lst):
	max = lst[0]
	for i in lst :
	if i > max :
		max= i
		
	min = lst [0]
	for i in lst :
	    if i < min:
		min = i
	missing = max+1
	list1=[]

	for _ in lst :
	
		max = max -1
		if max not in lst :
		    list1.append(max)
		
		
            return list1

# Driver code
lst = [1,5,4,6,8, 2,3, 7, 9, 10]
print(find_missing(lst))
