import arcpy
from arcpy import metadata as md

# Delete existing metadata
mdFC = input("Enter Feature Class: ")
fcMD = mdFC
tgt_item_md = md.Metadata(fcMD)


# Collect input from user
mdTitle = input("Enter title: ")
mdTags = input("Enter tags; separated by commas: ")
mdSummary = input("Enter Summary, i.e. purpose: ")
mdDescription = input("Enter Description, i.e. abstract: ")
mdCredit = input("Enter Credit: ")
#mdAccessConstraints = input("Enter Use Limitations: ")

templatePath = r'\\emcgis\nas\GISDATA\Distro\Documentation\MetadataTools\WCmdNAP.xml'
tempMD = md.Metadata(templatePath)
if not tgt_item_md.isReadOnly:
    tgt_item_md.copy(tempMD)
    tgt_item_md.save()
    
new_md = md.Metadata()
new_md.title = mdTitle
new_md.tags = mdTags
new_md.summary = mdSummary
new_md.description = mdDescription
new_md.credits = mdCredit
#new_md.accessConstraints = mdAccessConstraints
new_md.accessConstraints = """The geographic data layers produced by the Government of Washington County, Oregon (“Washington County”), and any associated maps and applications, are provided as a public resource. While every reasonable effort is made to ensure the accuracy and completeness of the data, Washington County makes no warranties, expressed or implied, including but not limited to any warranties of merchantability and fitness for a particular purpose concerning the accuracy, completeness or suitability of its data, and this data  should not be construed or used as a legal description of any parcel of real property.  Washington County will not assume any liability for errors, omissions, or inaccuracies in the data.
Any determination of topography or contours, or any depiction of physical improvements, property lines or boundaries, parcel size or shape is for general information only and shall not be used for the design, modification, purchase, lease, development or construction of real property or improvements to real property, for flood plain or wetlands determination or as evidence in any legal proceeding.
Copyright by Washington County. Except as provided herein, all rights are reserved.  Authorization to reproduce material for internal or personal use by any user of this information is granted by Washington County, the copyright owner.
Please email GISAppSupport@co.washington.or.us to report any errors or issues or to get more information about Washington County’s geospatial data, maps or applications."""

if not tgt_item_md.isReadOnly:
    tgt_item_md.copy(new_md)
    tgt_item_md.save()

tgt_item_md.synchronize("SELECTIVE")

