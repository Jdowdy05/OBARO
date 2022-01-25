# -*- coding: utf-8 -*-
"""
This module generates and writes to an XML document.

Functions
---------
def XMLStoreData(objects : Element,n : int, nameList : "list[str]", objectError : float, backgroundError : float, objectSurfaceBrightness : float,
                backgroundSurfaceBrightness : float, objectArea : float, backgroundArea : float, objectSurfaceError : float, backgroundSurfaceError : float,
                objectMean : float, backgroundMean : float, objectPixelCount : int, backgroundPixelCount : int): Element
                
    Makes main element "Object" and makes all sub elements for all values to be stored for a single object.
    This returns the the element "ObjectData".

def WriteXML(data : str): None
    Writes XML data and saves it as inputted by user. This returns None.

@author: Jordan Dowdy
@version: 1.1.0, 10/11/21

"""

from sys import path
from xml.etree.ElementTree import Element
import xml.etree.cElementTree as ET
import os
import numpy as np
def XML_generation() -> Element:
    
    objects_tree = ET.Element("ObjectData")
    
    
    
    return objects_tree

def XML_store_data(objects_tree : Element, n : int, name_list : "list[str]", object_error : float, background_error : float, object_surface_brightness : float,
    background_surface_brightness : float, object_area : float, background_area : float, object_surface_error : float, background_surface_error : float,
    object_mean : float, background_mean : float, object_pixel_count : int, background_pixel_count : int, object_number : int) -> Element:
    
    
        
    dataField=ET.Element("Object")
    objects_tree.append(dataField)
    ET.SubElement(dataField, 'File_Name', name = str(name_list[n])+":"+str(object_number)).text
    ET.SubElement(dataField, 'Object_Mean_Pixel_Value', value = str(object_mean)).text
    ET.SubElement(dataField, "Object_Total_Pixel_Value_Error", value = str(object_error)).text
    ET.SubElement(dataField, "Object_Region_Area", value = str(object_area)).text
    ET.SubElement(dataField, "Object_Surface_Brightness", value = str(object_surface_brightness)).text
    ET.SubElement(dataField, "Object_Surface_Brightness_Error", value = str(object_surface_error)).text
    ET.SubElement(dataField, "Object_Pixel_Count", value = str(object_pixel_count)).text
    ET.SubElement(dataField, "Background_Mean_Pixel_Value", value = str(background_mean)).text
    ET.SubElement(dataField, "Background_Total_Pixel_Value_Error", value = str(background_error)).text
    ET.SubElement(dataField, "Background_Region_Area", value = str(background_area)).text
    ET.SubElement(dataField, "Background_Surface_Brightness", value = str(background_surface_brightness)).text
    ET.SubElement(dataField, "Background_Surface_Brightness_Error", value = str(background_surface_error)).text
    ET.SubElement(dataField, "Background_Pixel_Count", value = str(background_pixel_count)).text

    
    

    return objects_tree


def write_XML(tree : Element, xml_name : str) -> None:
    
    tree_xml = ET.ElementTree(tree)

    #xml_name="seed1000-5327.xml"
    #directroy in the write function bellow needs to be changed for each pc.
    tree_xml.write("C:\\Users\\jorda\\Documents\\Python Scripts\\OBARO\\all objects\\"+xml_name+'.xml', encoding='utf-8', xml_declaration=True)
    


def parse_XML(XMLname : str) -> np.ndarray:
    object_mean = []
    background_mean = []
    
    tree = ET.parse(XMLname)

    root = tree.getroot()
    i=0
    for child in root:
        object_mean.append(int(root[i][4].attrib['value']))
        background_mean.append(int(root[i][10].attrib['value']))
        i=i+1
    

    object_mean = np.array(object_mean)
    background_mean = np.array(background_mean)
    return object_mean, background_mean