# -*- coding: utf-8 -*-
"""
Created on Sat Oct 30 15:08:54 2021

@author: Ethan
"""

from matplotlib import pyplot
import xml.etree.cElementTree as ET
#from xml.etree.ElementTree import XML, Element

def pullFromXml(filePath):
    tree = ET.parse(filePath)
    root = tree.getroot()
    
    dataSet = []
    
    index = 0
    for child in root:
        signal = int(child[4].attrib['value'])
        background = int(child[10].attrib['value'])
        dataSet.append((index, signal, background))
        index += 1
    
    return dataSet

#NEXT FUNCTIONS ADAPTED FROM EARLIER GraphScript SCRIPT

def scatterPlot(dataSet1, version1, seedNum, dataSet2=None, version2=None):
    index1 = []
    signal1 = []
    background1 = []
    
    for j in dataSet1:
        index1.append(j[0])
        signal1.append(j[1])
        background1.append(j[2])
    
    pyplot.figure(figsize=(8,6), dpi=100)
    
    pyplot.scatter(index1, signal1, s=3, label=("Object Brightness (" + str(len(index1)) + " objects in PhoSim " + version1 + ")"), c="blue")
    pyplot.scatter(index1, background1, s=3, label=("Background Brightness (" + str(len(index1)) + " objects in PhoSim " + version1 + ")"), c="red")
    
    numObjects = len(index1)
    fileLabel = version1
    
    if dataSet2 is not None:
        index2 = []
        signal2 = []
        background2 = []
        
        for j in dataSet2:
            index2.append(j[0] + numObjects)
            signal2.append(j[1])
            background2.append(j[2])
        
        pyplot.scatter(index2, signal2, s=3, label=("Object Brightness (" + str(len(index2)) + " objects in PhoSim " + version2 + ")"), c="green")
        pyplot.scatter(index2, background2, s=3, label=("Background Brightness (" + str(len(index2)) + " objects in PhoSim " + version2 + ")"), c="fuchsia")
        
        numObjects += len(index2)
        fileLabel = "both"
    
    pyplot.title("Surface Brightness of Brightest Astronomical Object in Each FITS Image (seed " + seedNum + ")")
    pyplot.xlabel("Index of Astronomical Object (" + str(numObjects) + " objects)")
    pyplot.ylabel("Surface Brightness")
    pyplot.xlim(xmin=0)
    pyplot.ylim(0, 1800000)
    pyplot.yticks([0, 200000, 400000, 600000, 800000, 1000000, 1200000, 1400000, 1600000], [0, 200000, 400000, 600000, 800000, 1000000, 1200000, 1400000, 1600000])
    pyplot.legend()
    
    pyplot.savefig("plot_images\scatter_" + fileLabel + "_seed" + seedNum + ".png", dpi='figure')
    pyplot.show()

def plotSignalHist(dataSet, binSize, version, seedNum, includeBackground=False):
    
    signalValues = []
    backgroundValues = []
    for j in dataSet:
        signalValues.append(j[1])
    
    if includeBackground:
        for j in dataSet:
            backgroundValues.append(j[2])
    
    binList = []
    count = 0
    while count <= 1600000:
        binList.append(count)
        count += binSize
    
    pyplot.figure(figsize=(8,6), dpi=100)
    
    pyplot.hist(signalValues, bins = binList, label=("Object Surface Brightness (" + str(len(dataSet)) + " Objects)"))
    if includeBackground:
        pyplot.hist(backgroundValues, bins = binList, label="Background Surface Brightness (" + str(len(dataSet)) + " Objects)", alpha=0.5)
    
    pyplot.title("Distribution of Surface Brightness (PhoSim " + version + " - seed " + seedNum + ")")
    pyplot.xlabel("Surface Brightness of Brightest Astronomical Object in Each FITS Image")
    pyplot.ylabel("No. of Astronomical Objects / " + str(binSize) + " (SBU)")
    pyplot.xlim(0, 1600000)
    pyplot.ylim(ymin=0)
    pyplot.xticks([0, 200000, 400000, 600000, 800000, 1000000, 1200000, 1400000, 1600000], ["0", "2x10^5", "4x10^5", "6x10^5", "8x10^5", "1x10^6", "1.2x10^6", "1.4x10^6", "1.6x10^6"])
    pyplot.legend()
    
    if (includeBackground):
        pyplot.savefig("plot_images\histogram_" + version + "_seed" + seedNum + "_" + str(binSize) + "_both.png", dpi='figure')
    else:
        pyplot.savefig("plot_images\histogram_" + version + "_seed" + seedNum + "_" + str(binSize) + "_object.png", dpi='figure')
    pyplot.show()