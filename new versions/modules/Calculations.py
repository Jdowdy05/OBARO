# -*- coding: utf-8 -*-
"""
This module does calculations for all values that end up storing.

Functions
---------
def objectSumCalc(j : int, i : int, jSub2 : int, iSub2 : int, jSub3 : int, iSub3 : int, avgB : float,
                data : np.ndarray, size : np.ndarray)-> 'tuple[int, int]':

    looks at all pixels in object region and adds pixels and pixel values that are considered object which returns a tuple containing object sum and object pixel count

def background_sum_calc(j : int, i : int, jSub2 : int, iSub2 : int, jSub4 : int, iSub4 : int, avgB : float,data : np.ndarray,
                        size : np.ndarray, object_pix, s : int) -> 'tuple[int, int]':
    
    looks at all pixels in background region and adds together all pixels and pixel values considered background. Makes sure it   which
    returns a tuple containing background sum and background pixel count

def error_sum_calc(object_sum : int, background_sum : int) -> 'tuple[float, float]':



@author: Jordan Dowdy
@version: 1.1.0, 10/11/21



"""
import numpy as np
import math
import BackgroundDetection


arcseconds=0.19990024       #this can be changed from seed to seed and is recommended for more accuracy 
arcs=arcseconds**2

def object_sum_calc(j : int, i : int, jSub2 : int, iSub2 : int, jSub3 : int, iSub3 : int,
    avgB : float, data : np.ndarray, size : np.ndarray)-> 'tuple[int, int]':

    object_pix=1
    object_sum=0
    for y in range((2*(jSub2+4))):
        x = 0
        for x in range((2*(iSub2+4))):
            if (jSub3+y)>=size[0] or (iSub3+x)>=size[1] or (jSub3+y)<0 or (iSub3+x)<0  :
                continue
            if data[jSub3+y][iSub3+x] > avgB*1.08:
                object_pix += 1
                object_sum = object_sum+data[jSub3+y][iSub3+x]

    return object_sum, object_pix

def background_sum_calc(j : int, i : int, jSub2 : int, iSub2 : int, jSub4 : int, iSub4 : int, background : int, data : np.ndarray,
    size : np.ndarray, object_pix, s : int) -> 'tuple[int, int]':
    background_pix=1
    background_sum=0
    i_dif=iSub2-iSub4
    j_dif=jSub2-jSub4
    for y in range((2*((j_dif)+1))):
        x = 0
        for x in range((2*((i_dif)+1))):
            if (jSub4+y)>=size[0] or (iSub4+x)>=size[1] or (jSub4+y)<0 or (iSub4+x)<0  :
                continue
            if data[jSub4+y][iSub4+x] < background*1.08:
                background_pix += 1
                background_sum = background_sum+data[jSub4+y][iSub4+x]
    """
    # for good background measurements we want at least twice as many background pixels as object pixels
    if background_pix <= 2*object_pix: 
        s=s+1
        jSub4, iSub4 = BackgroundDetection.background_region_start_pix(j, i, jSub2, iSub2, size, s)
        background_sum_calc(j, i, jSub2, iSub2, jSub4, iSub4, background, data, size, object_pix, s)
    
    """
    return background_sum, background_pix

def error_sum_calc(object_sum : int, background_sum : int) -> 'tuple[float, float]':       

    object_error = math.sqrt(abs(object_sum))
    background_error = math.sqrt(abs(background_sum))

    return object_error, background_error

def arc_area(object_pix : int, background_pix : int) -> 'tuple[float, float]':

    object_area=object_pix*arcs
    background_area=background_pix*arcs
    return object_area, background_area

def surface_brightness(object_sum : int, background_sum : int, object_pix : int,
                        background_pix : int) -> 'tuple[float, float, float, float]':

    object_area, background_area = arc_area(object_pix,background_pix)
    object_surface_brightness=object_sum/object_area
    background_surface_brightness=background_sum/background_area

    
    return object_surface_brightness, background_surface_brightness, object_area, background_area

def surface_error(object_error: float, object_area: float, background_error : float, background_area : float) -> 'tuple[float, float]':
    object_surface_error=object_error/object_area
    background_surface_error=background_error/background_area

    return object_surface_error, background_surface_error

def mean(object_sum : int, background_sum : int, object_pix : int, background_pix : int) -> 'tuple[float, float]':

    object_mean=object_sum/object_pix
    background_mean=background_sum/background_pix
    
    return object_mean, background_mean