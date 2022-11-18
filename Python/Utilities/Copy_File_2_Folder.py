# coding=utf-8
# -------------------------------------------------------------------------------
"""
Name:           Update WashSDE Land Use Districts

Purpose:        Copy files from one folder to another.

Author:         https://stackoverflow.com/questions/11903037/copy-all-jpg-file-in-a-directory-to-another-directory-in-python

Created:        2021-10-20
"""
# -------------------------------------------------------------------------------
import glob
import shutil
import os

print ("Copy Process Started")
print (" ")

src_dir = "//emcgis/nas/GISDATA/Workgroups/GISPlanning/Transportation_Projects/TV_HWY/Data/Shaw_Photos_All"
dst_dir = "//emcgis/nas/GISDATA/Workgroups/GISPlanning/Transportation_Projects/TV_HWY/Data/Shaw_Photos_jpg"
for jpgfile in glob.iglob(os.path.join(src_dir, "*.jpg")):
    shutil.copy(jpgfile, dst_dir)
print (" ")
print ("Copy Process Complete")