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
from cmath import log
from itertools import count
import numpy as np
import math

import BackgroundDetection


arcseconds=0.19990024       #this can be changed from seed to seed and is recommended for more accuracy 
arcs=arcseconds**2







def object_sum_calc(j : int, i : int, jSub2 : int, iSub2 : int, jSub3 : int, iSub3 : int,
    avgB : float, data : np.ndarray, size : np.ndarray)-> 'tuple[int, int]':

    """
    need to add tolerance here. isn't too important as wont change sum drastically.
    """
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

def background_sum_calc(j : int, i : int, jSub2 : int, iSub2 : int, jSub5 : int, iSub5 : int, background : int, data : np.ndarray,
    size : np.ndarray, object_pix, s : int) -> 'tuple[int, int]':
    background_pix=1
    background_sum=0
    i_dif=abs(iSub2-iSub5)
    j_dif=abs(jSub2-jSub5)
    for y in range((2*((j_dif)))):
        x = 0
        for x in range((2*((i_dif)))):
            if (jSub5+y)>=size[0] or (iSub5+x)>=size[1] or (jSub5+y)<0 or (iSub5+x)<0  :
                continue
            if data[jSub5+y][iSub5+x] <= background*1.08:
                background_pix += 1
                background_sum += data[jSub5+y][iSub5+x]
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

def magnitude(data, header, size, obj_sum, object_pixel_count, local_background):
    OAS = False
    gain = header["Gain"]
    exp_time = header["Exptime"]
    try: 
        mag_zp = header["ZERO-PT"]

    except:
        mag_zp = - 2.5*log(gain*1/exp_time) #the magnitude of a star with a count of 1

    if OAS == True:

        sig_above_back = obj_sum - (object_pixel_count * local_background)
        total_flux = (gain*sig_above_back)/exp_time # gain * ADU
        mag = mag_zp + - 2.5*log(gain*sig_above_back/exp_time)
        return sig_above_back, total_flux, mag_zp, mag
    #mag = mag_zero_point - 2.5*log(flux) //still needs work...zero point mag may be hard to calculate as we have no reference star
    #inst_mag = - 2.5*log(sig_above_back/exp_time)
    if OAS == False:
        sig_above_back = obj_sum - (object_pixel_count * local_background)
        total_flux = (gain*obj_sum)/exp_time # ADU/exp_time or total number of photons over exposuretime 
        mag = mag_zp + - 2.5*log(gain*obj_sum/exp_time)
        
        return total_flux, mag