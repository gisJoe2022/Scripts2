# Python program to explain filecmp.cmpfiles() method

# importing filecmp module
import filecmp

# Path of first directory
dir1 = "C:\Users\josephh\Documents\btbooks"

# Path of second directory
dir2 = "C:\Users\josephh\Documents\btbooksdev"

# Common files
common = []

# Shallow compare the files
# common in both directories
match, mismatch, errors = filecmp.cmpfiles(dir1, dir2, common)

# Print the result of
# shallow comparison
print("Shallow comparison:")
print("Match :", match)
print("Mismatch :", mismatch)
print("Errors :", errors, "\n")


# Compare the
# contents of both files
# (i.e deep comparison)
match, mismatch, errors = filecmp.cmpfiles(dir1, dir2, common,
											shallow = False)

# Print the result of
# deep comparison
print("Deep comparison:")
print("Match :", match)
print("Mismatch :", mismatch)
print("Errors :", errors)
