# -*- coding: utf-8 -*-
"""
The script that runs a full analysis of a set of FITS images.

@author: Ethan
@version: 1.0
"""

import FileHandling
import PixelStats
import numpy as np

print("Enter path to directory:\n")
imageDir = input()

imageList = FileHandling.findFitsFiles(imageDir)

#imageData = None
#avgBackground = 0.0

#This is just a dummy that prints out the average background for now.
for imageFile in imageList:
    imageData = FileHandling.loadFitsImage(imageFile)
    avgBackground = PixelStats.imageBackground(imageData)
    print("The average background is: " + str(avgBackground))