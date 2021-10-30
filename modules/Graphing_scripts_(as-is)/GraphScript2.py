# -*- coding: utf-8 -*-
"""
DON'T TRY TO INTEGRATE THIS WITH OTHER OBARO CODE IN CURRENT STATE
This is the script that I used to create the scatterplot for the KAS presentation.
I added it in case we want to adapt it and integrate into OBARO later.

Created on Sat Oct 30 15:08:54 2021
@author: Ethan
"""

from matplotlib import pyplot
import xml.etree.cElementTree as ET
#from xml.etree.ElementTree import XML, Element

tree = ET.parse("seed1000-01.xml")
root = tree.getroot()

dataFromXml = []

index = 0
for child in root:
    signal = int(child[4].attrib['value'])
    background = int(child[10].attrib['value'])
    
    dataFromXml.append((index, signal, background))
    
    index += 1

#NEXT FUNCTIONS ADAPTED FROM EARLIER GraphScript SCRIPT

def scatterPlotAll():
    index = []
    signal = []
    background = []
    
    for j in dataFromXml:
        index.append(j[0])
        signal.append(j[1])
        background.append(j[2])
    
    pyplot.figure(figsize=(8,6), dpi=100)
    
    pyplot.scatter(index, signal, s=3, label="Atronomical Object Brightness", c="blue")
    pyplot.scatter(index, background, s=3, label="Background Brightness", c="red")
    
    
    pyplot.title("Surface Brightness of All Astronomical Objects")
    pyplot.xlabel("Index of Astronomical Object (" + str(len(index)) + " objects)")
    pyplot.ylabel("Surface Brightness")
    pyplot.xlim(xmin=0)
    pyplot.ylim(0, 1800000)
    pyplot.yticks([0, 200000, 400000, 600000, 800000, 1000000, 1200000, 1400000, 1600000], [0, 200000, 400000, 600000, 800000, 1000000, 1200000, 1400000, 1600000])
    pyplot.legend()
    
    pyplot.savefig("scatter_all.png", dpi='figure')
    pyplot.show()