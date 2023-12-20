# coding=utf-8
# -------------------------------------------------------------------------------
"""
Name:           

Purpose:        

Author:         Jose Hayes

Created:        2022-09-26
"""
# -------------------------------------------------------------------------------
import glob
import shutil
import os
from PIL import Image, ImageSequence


# Step 1 - Copy tiff files to Survey Explorer directory
print ("Copy Process Started")
print("This will take ~10 minutes")
print (" ")
src_dir = r"\\pfilepsb\cart\taxmaps"
dst_dir = r"\\pdoclsde1\Images\survey\Taxmaps"
for tif in glob.iglob(os.path.join(src_dir, "*.tif")):
    shutil.copy(tif, dst_dir)
print (" ")
print ("Copy Process Complete")

# Step 2 - Convert tiff files to pdf



# STEP 3 - Format PDF file names
path = r"\\pdoclsde1\Images\survey\Taxmaps"

for file in os.listdir(path):
    pdfsplit = file.split('.', 1)
    os.rename( path + file, path + pdfsplit[0].upper().ljust(12, '0') + '.' + pdfsplit[1])

then = os.listdir(path)
print(" ")
print("File Renaming Complete")



