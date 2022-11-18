import os

path = r'\\pdoclsde1\\Images\\survey\\dev\\TaxMapPDF_Copy\\'

for file in os.listdir(path):
    #os.rename(path + file, path + file.upper())
    file.ljust(12, '0')

then = os.listdir(path)
print(then)





# Creating a string variable
#str = "Geeks for Geeks"

# Printing the output of ljust() method
#print(str.ljust(20, '0'))
