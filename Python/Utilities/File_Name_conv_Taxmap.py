import os

path = r'\\pdoclsde1\\Images\\survey\\Taxmaps_test\\'

for file in os.listdir(path):
    pdfsplit = file.split('.', 1)
    os.rename( path + file, path + pdfsplit[0].upper().ljust(12, '0') + '.' + pdfsplit[1])

then = os.listdir(path)
print(then)
