# -*- coding: utf-8 -*-
"""
Module to find a accurate background value.

Functions
---------
def dynamic_background(j : int, i : int, fits : np.ndarray, size : np.ndarray, bin_list : list) -> 'tuple[int, float]':
    This calculates the background of an area around a the pixel that has been passed through. It start by slicing
    the fits numpy array into a more localized chunk. This does give more weight in the positive direction for an axis.

def backgroundRegionStartPix(j, i, jSub2, iSub2, size): int
    Does some simple math to get the starting pixel of the background region to be drawn.
    Also tries to make sure we wont get an IndexError when drawing the region. The background
    region is 3 time larger than the object region. This returns our the pixel location as an int.

def background_partitioning(j : int, i : int, fits : np.ndarray, size : np.ndarray, dim : bool) -> int:
    This is to help find the background for larger objects and finds the background around this object. Uses similar methods as 
    the dynamic_background function. This returns an int of the localized background for the object. 


@author: Jordan Dowdy
@version: 1.1, 10/12/21
"""
import numpy as np
import math


def dynamic_background(j : int, i : int, fits : np.ndarray, size : np.ndarray, bin_list : list) -> 'tuple[int, float]':

    multiplier = 1.1
    
    j_slice_start = j-5
    j_slice_end = j+9
    
    i_slice_start = i-130
    i_slice_end = i+180


    if j_slice_start < 0:
        #j_slice_end+=abs(j_slice_start)
        j_slice_start = 0


    if j_slice_end > 2009:
        #j_slice_start=j_slice_start-(j_slice_end-2009)
        j_slice_end = 2009


    if i_slice_start < 0:
        i_slice_end+=abs(i_slice_start)
        i_slice_start = 0


    if i_slice_end > 509:
        i_slice_start=i_slice_start-(i_slice_end-509)
        i_slice_end = 509

    sliced_fits = fits[j_slice_start:j_slice_end, i_slice_start:i_slice_end ]

    hist, bins = np.histogram(sliced_fits, bins = bin_list)
    
    n = 0
    peak = 0 

    for element in hist:

        if element > peak:

            peak = element
            peak_location = n
        n+=1
    
    '''

    multiplier code needs work.


    idea for the multiplier is that if the histogram peak is not a steep drop to the next bin then the next bin value
    is most likely background and thefore the multiplier needs to be larger to let the next bin be within tolerance.

    if the next bin from the peak is steep drop off then we know we are most likely at a value that has all the background within it. 

    '''

    '''

    print(multiplier)
    print('n-1:', hist[n-1],' n:',hist[n],)
    try:
        print('n+1:',hist[n+1])

    except:
        print('no n+1')
    
    if hist[n] <= hist math.ceil(1.1*hist[n+1]):
        multiplier = 1.1

    else: 
        multiplier = 1.03

    '''
    
    dif = int(hist[peak_location+1]) - hist[peak_location+2]



    
    

    background_value = bins[peak_location+1]
    
    #print('background:',background_value)

    return background_value, multiplier


def background_region_start_pix(j : int, i : int , jSub2 : int, iSub2 : int, size : np.ndarray, s : int) -> 'tuple[int, int]':
    jSub2=j-(s*(jSub2))
    if jSub2 <=0:
        jSub2=0
    if jSub2 >=size[0]:
        jSub2=size[0]

    iSub2=i-(s*(iSub2))
    if iSub2 <=0:
        iSub2=0
    if iSub2 >=size[1]:
        iSub2=size[1]
    
    return jSub2, iSub2

def background_partitioning(j : int, i : int, fits : np.ndarray, size : np.ndarray, dim : bool ) -> int:
    
    """
    This is used to help find the background from object to object instead of pixel to pixel like dynamic background.

    """
    x_slice = False

    if size[1] < size[0]:
        x_slice = True
        
    if dim == False:
        slice_start = math.floor(j-(size[1]/2))
        slice_end = math.floor(j+(size[1]/2))

    if dim == True:
        slice_start = math.floor(j-80)
        slice_end = math.floor(j+120)

    if slice_start < 0:
        slice_end+=abs(slice_start)
        slice_start = 0


    if slice_end > 2009:
        slice_start=slice_start-(slice_end-2009)
        slice_end = 2009

    sliced_fits = fits[slice_start:slice_end, : ]

    bin_list = []
    bin_size = 50  #this value can be changed to more accurately find dimmer objects.
    x=600
    while x <= 6000:
        
        bin_list.append(x)
        x+=bin_size

    hist, bins = np.histogram(sliced_fits, bins = bin_list)
    
    n = 0
    
    peak = 0 

    for element in hist:

        if element > peak:
            peak = element
            peak_location = n
        n+=1

    local_background_value = bins[peak_location+1]

    #print('local background:', local_background_value)
    
    return local_background_value

    
