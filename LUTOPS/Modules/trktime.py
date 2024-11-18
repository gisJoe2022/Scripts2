#-------------------------------------------------------------------------------
# Name:        timer.py
# Purpose:      Allows timing of portions of code.
#
# Author:      RebekahM
#
# Created:     29/09/2011
#-------------------------------------------------------------------------------
import os, sys
from time import clock


#cmd_folder = "\\\\emcgis\\nas\\LUTOPS\\GIS\\Production\\python\\CommonModules\\"
cmd_folder = "\\\\pwebgisapp1\\GIS_Process_Scripts\\PRODpyScriptShare\\LUTOPS\\Modules\\"
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)



class stopwatch:
    def __init__(self):

        self.StartTime = clock()

    def Stop(self):

        self.ElapsedTime = str(round((clock() - self.StartTime),4))
##        self.ElapsedTime = clock() -  self.StartTime
        return self.ElapsedTime

    def Reset(self):
        self.StartTime = clock()

    def Total(self):
        x = self.Stop()
        self.ProcessTime = "Total Processing Time: " + str(x)
        return self.ProcessTime
