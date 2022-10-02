# -*- coding: utf-8 -*-
"""
This is the main file for Object Brightness Analyzer for Rubin Observatory (OBARO). very epic very wow.
This version is for the brightest object in a fits file.

Class
--------
class FITS:
    Finds the brightest astronomical object in a FITS image and determines size, brightness, and 
    error for both object and its corresponding background the single brightest object in a fits image.


Functions
---------
def astr_main(self) -> 'tuple[int, Element]':
    used to call the other functions of the FITS class.

def load_fits(self) -> dict:
    loads a single fits file for analyzing and returns a dictionary of FITS image array(data) and size of FITS image(size).


def astr_object(self, data : np.ndarray, size : np.ndarray) -> dict:
    finds object and its size along with some background information and returns a dictionary

    "astr_object" : astr_objects_info, this stores object region size, center, and original pixel detection
    "fits" : fits, this is the np.ndarry of each pixel value
    "size" : size, size of image
    "object_count": object_count, number of objects detected in image

def math(self, astr_object_data : np.ndarray, data : np.ndarray, size : np.ndarray) -> np.ndarray:
    calls other functions in the Calculations module to do the maths. returns object data.

def data_storing(self, astr_object_data) -> Element:
    Stores all relevant data in the xml file and then returns the Element. All values are stored after a single
    fits has been analyzed.


Variables
---------
fits -> np.ndarray: holding all pixel values of the fits image loaded.
size -> np.ndarray: holds 2 numbers which are the size of the image in pixels in both y and x directions.
background -> int: highest binned value within a given area of current pixel location.
multiplier -> float: a multiplier for background which changes depending on how close other binned values 
              are to the background bin. Explained in more detail in BackgroundDetection.py
j -> int: j component to pixel that is considered objected value.
i -> int: i component to pixel that is considered objected value
jSub2 -> int: center of object in y direction.
iSub2 -> int: center of object in x direction.
jSub3 -> int: half the size of the object in pixels in the y direction.
iSub3 -> int: half the size of the object in pixels in the x direction.
jSub4 -> int: starting pixel in the y direction for region drawing around object.
iSub4 -> int: starting pixel in the x direction for region drawing around object.
jSub5 -> int: starting pixel in the y direction for region drawing around background.
iSub5 -> int: starting pixel in the x direction for region drawing around background.
objectSum -> int: sum of total pixel values of object
objectPixelCount -> int: total pixel count of object
backgroundSum -> int: sum of total pixel values of background


@author: Jordan Dowdy 
@version: 1.1.1, 10/11/21

$19 fortnite card

"""

import math
import time
from os import name, times
import sys
import time
sys.path.insert(0, 'C:\\Users\\jorda\\Documents\\Python Scripts\\OBARO\\all objects\\modules')

import numpy as np

import xml.etree.cElementTree as ET

from xml.etree.ElementTree import XML, Element


import FitsFileManaging
import BackgroundDetection
import ObjectDetection
import Calculations
import XMLFileHandling



class FITS:

    def __init__(self, path_list : list, name_list : list, root : Element, count : int) -> 'tuple[int, Element]':
        self.path_list = path_list
        self.name_list = name_list
        self.count = count
        self.root = root

    def astr_main(self) -> 'tuple[int, Element]':
        
        

        astr_object = FITS.astr_object(self, FITS.load_fits(self)["fits"], FITS.load_fits(self)["size"])
        if astr_object["object_count"] > 0:
            self.root = FITS.data_storing(self, FITS.math(self, astr_object["astr_object"], astr_object["fits"], astr_object["size"], astr_object["object_count"]), astr_object["object_count"])
            
            
        if self.count >= 0:
            self.count = self.count - 1
            
            return self.count, self.root
        else:
            
            
            return self.count, self.root
            
            


    def load_fits(self) -> dict: 

        fits, size = FitsFileManaging.load_file(self.path_list, self.count)
        
        return {
            "fits": fits, 
            "size" : size
            }
        
    

        
        
    def astr_object(self, fits : np.ndarray, size : np.ndarray) -> dict:
        
        object_count = 0
        s = 2
        astr_objects_info = np.empty((0, 9), int)
        astr_object_pixel_loc = np.empty((0, 4), int)

        

        bin_list=[]
        bin_size=50
        bin=600
        while bin <= 6000:
        
            bin_list.append(bin)
            bin+=bin_size
        



        j=0
        for row in fits:
            
            

            i=0
            for element in row:
                
                if i%20 == 0  or i == 0:   #increasing the int after the remainder operator will increase program speed but lower accuracy   
                    background, multiplier = BackgroundDetection.dynamic_background(j, i, fits, size, bin_list)
                    
                if element > background*multiplier: #change 
                    dim_object = False
                    twin_object = False #bool for if we are in a region of another/same object. 

                    if object_count >= 0:
                            
                            for x in range(object_count):
                        
                                if (j >= (astr_object_pixel_loc[x][0]) and j <= (astr_object_pixel_loc[x][2]) and i >= (astr_object_pixel_loc[x][1]) and
                                    i <= (astr_object_pixel_loc[x][3])):  
                                    '''
                                    instead of having a list or array of every object pixel cord we can just have the bounds of the object region and say
                                    if we are in this bound or region then do not run these other functions as we have already calculated this object.
                            
                            
                                    '''
                                    
                                    twin_object = True

                                    break

                    if twin_object == True:
                        
                        continue
                    
                    if element < background*3:
                        dim_object = True

                    local_background = BackgroundDetection.background_partitioning(j,i,fits,size,dim_object)

                    jSub2, iSub2, jSub3, iSub3, signal = ObjectDetection.find_object(fits, local_background, size, j, i)    
                    
                    for x in range(object_count):
                        
                                if (jSub2 >= (astr_object_pixel_loc[x][0]) and jSub2 <= (astr_object_pixel_loc[x][2]) and iSub2 >= (astr_object_pixel_loc[x][1]) and
                                    iSub2 <= (astr_object_pixel_loc[x][3])):  

                                    twin_object = True

                                    break
                    if twin_object == True:
                        
                        continue
                    #print('signal for object',object_count, 'is', signal)
                    if signal == False:         # 
                       
                        continue

                    object_count+=1

                    jSub4, iSub4, astr_object_pixel_loc = ObjectDetection.object_region_start_pix(jSub2,iSub2,jSub3,iSub3,fits,size,astr_object_pixel_loc)


                    jSub5, iSub5 = BackgroundDetection.background_region_start_pix(jSub2,iSub2,jSub3,iSub3,size, s)

                    
                    print(':',j, i, jSub2, iSub2, jSub3, iSub3, jSub4, iSub4, jSub5, iSub5, background, local_background ,object_count)
                    
                    
                    astr_objects_info = np.append(astr_objects_info, np.array([[jSub2, iSub2, jSub3, iSub3, jSub4, iSub4, jSub5, iSub5, background]]), axis=0)
                i+=1
            j+=1

        
        #print(astr_objects_info)
        return {
                "astr_object" : astr_objects_info,
                "fits" : fits, 
                "size" : size,
                "object_count": object_count
                }

    

    def math(self, astr_object : np.ndarray, fits : np.ndarray, size : np.ndarray, object_count : int) -> np.ndarray:
        s=3
        astr_object_data = np.empty((0, 14), float)
         
        for u in range(object_count):
            object_sum, object_pixel_count = Calculations.object_sum_calc(int(astr_object[u][0]), int(astr_object[u][1]), int(astr_object[u][2]), int(astr_object[u][3]),
                                            int(astr_object[u][4]), int(astr_object[u][5]), int(astr_object[u][8]), fits, size)
            
            background_sum, background_pixel_count = Calculations.background_sum_calc(int(astr_object[u][0]), int(astr_object[u][1]), int(astr_object[u][2]), int(astr_object[u][3]), int(astr_object[u][6]),
                                            int(astr_object[u][7]), int(astr_object[u][8]), fits, size, object_pixel_count, s)

            object_error, background_error = Calculations.error_sum_calc(object_sum, background_sum)
            
            object_surface_brightness, background_surface_brightness, object_area, background_area = Calculations.surface_brightness(object_sum, background_sum, 
                                                                                                    object_pixel_count, background_pixel_count)

            object_surface_error, background_surface_error = Calculations.surface_error(object_error, object_area, background_error, background_area)

            object_mean, background_mean = Calculations.mean(object_sum, background_sum, object_pixel_count, background_pixel_count)


            
        
        
            astr_object_data = np.append(astr_object_data, np.array([[object_error, background_error,
                object_surface_brightness, background_surface_brightness, object_area,  # used to more easily return data.
                background_area, object_surface_error, background_surface_error, object_mean, background_mean, object_sum,  
                background_sum, object_pixel_count, background_pixel_count]]), axis=0)   

            #print(astr_object_data[u])
        return astr_object_data


    def data_storing(self, astr_object_data, object_count) -> Element:

        for u in range(object_count):

            self.root = XMLFileHandling.XML_store_data(self.root, self.count, self.name_list, int(astr_object_data[u][0]), int(astr_object_data[u][1]), 
                        int(astr_object_data[u][2]), int(astr_object_data[u][3]), int(astr_object_data[u][4]), int(astr_object_data[u][5]), int(astr_object_data[u][6]),
                        int(astr_object_data[u][7]), int(astr_object_data[u][8]), int(astr_object_data[u][9]), int(astr_object_data[u][12]), int(astr_object_data[u][13]),u)
                        
                                        
         
        return self.root
    
    


def rec(root_tree : Element, count : int, F : classmethod, xml_name : str) -> Element:
    
    if count >=0:
        print(count)
        count, root_tree = F.astr_main()
        XMLFileHandling.write_XML(root_tree, xml_name)
        root_tree = rec(root_tree, count, F, xml_name)
    return root_tree

def main():

    dir_name = input("Enter path to fits directory:")
    root_tree = XMLFileHandling.XML_generation()    #starts xml tree
    xml_name = input("Save XML file as(seed-phosim ver):")
    path_list, name_list = FitsFileManaging.fits_locator(dir_name)  #gives paths of files and names of files
    path_list.reverse()
    name_list.reverse() #so we can start at fits file R01S01C00 and work up                                 
    time.sleep(3)
    
    count = len(name_list) - 1
    
    F = FITS(path_list, name_list, root_tree, count)
    root_tree = rec(root_tree, count, F, xml_name)
    

       
    XMLFileHandling.write_XML(root_tree, xml_name)
    



if __name__ == '__main__':
    sys.setrecursionlimit(4300)
    sys.exit(main())
