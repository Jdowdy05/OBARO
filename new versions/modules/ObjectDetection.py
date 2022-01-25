# -*- coding: utf-8 -*-
"""
Module: 
-that searches for objects
-tries to detect if the object detected is an error pixel
-tries to find the correct center of the object.

Functions
---------
findSignal(data, local_background, size): int
    Finds max value pixel with its location and then checks to see if ErrorCorrection() needs to be called
    by looking in either the positive or negative x direction. If ErrorCorrection does need to be called 
    it flattens and sorts data before calling the function. Returns an int our pixel location.


errorCorrection(j, i, flatdata, data, local_background, k): int
    This is a recursive function that finds the n'th biggest number and gives us the location.
    Makes sure that the n'th biggest number is not a error pixel and is an actual object. Returns an int of our new pixel location.


objectCenterCorrection(j, i, data, local_background, size): int
    This function tries to find the center of the object as sometimes the brightest pixel is not the center of a object.
    Also gives us the size of our object as it finds the edges in order to find the center. 
    Returns an int of our pixel location and size of the object.

objectRegionStartPix(j, i, jSub2, iSub2, data, size): int
    Does some simple math to give the starting pixel of the region to be drawn around the object.
    Returns int of starting pixel for region.



@author: Jordan Dowdy
@version: 1.1.0, 10/12/21



"""


import numpy as np
import math





def find_object(data : np.ndarray, local_background : float, size : np.ndarray, j : int, i : int) -> 'tuple[int, int, bool]':
    
    n=-2            
    signal = True



    j, i, jSub2, iSub2 = object_center_correction(j, i, data, local_background, size)

    if data[j][i] <= local_background*1.08:
        jSub2, iSub2 = 0, 0
        signal = False
        return j, i, jSub2, iSub2, signal

    try:    
        if data[j][i-4] <= local_background*1.08:
            flatData=data
            flatData=np.sort(flatData, axis=None)
            
            j, i, signal = error_correction(j, i, flatData, data, local_background, n, signal)

    except(IndexError):

        if data[j][i+4] <= local_background*1.08:
            flatData=data
            flatData=np.sort(flatData, axis=None)
            j, i, signal = error_correction(j, i, flatData, data, local_background, n, signal)
    
    if signal == False:
        jSub2, iSub2 = 0, 0 
        return j, i, jSub2, iSub2, signal


    
    
    return j, i, jSub2, iSub2, signal



def error_correction(j : int, i : int, flatdata : np.ndarray, data : np.ndarray, local_background : float, n : int, signal : bool) -> 'tuple[int, int, bool]':

    j, i = np.where(data == flatdata[n])
    j=int(j[0])
    i=int(i[0])

    if data[j][i] <= local_background*1.08:
        signal = False
        return j, i, signal

    if data[j][i-2] <=local_background*1.08:
        n=n-1
        j, i, signal = error_correction(j, i, flatdata, data, local_background, n, signal)
    
    return j, i, signal
        


def object_center_correction(j : int, i : int, data : np.ndarray, local_background : float, size : np.ndarray) -> 'tuple[int, int, int, int]':
    """

    needs to be changed but not enough time this is not very poggers.

    need to compress all these for loops and if statements.

    ------------
    11/24/21

    compressed it down a bit but could still be more intelligent unlike me sad gamer moment


    """

    iter = 3       # number of iterations for center correction.

    yPos = 0
    yNeg = 0
    xPos = 0
    xNeg = 0

    

    
    for u in range(iter):
        x_neg_bool = False
        x_pos_bool = False
        y_neg_bool = False
        y_pos_bool = False

        if u % 2 == 0:  #alternates which axis is checked first

            for y in range(size[0]-1):
            
                if j+y<(size[0]) and data[j+y][i] <= (local_background*1.1) and y_pos_bool == False:
                
                    yPos = y
                
                    y_pos_bool = True

                if j-y>=0 and data[j-y][i] <= (local_background*1.1) and y_neg_bool == False:
                
                    yNeg = y
                
                    y_neg_bool = True

                if y_neg_bool == True and y_pos_bool == True:
                    break
        


            for x in range(size[1]-1):

                if i-x >=0 and data[j][i-x] <= (local_background*1.1) and x_neg_bool == False:
                
                    xNeg = x
                    x_neg_bool = True

                if i+x<(size[1]) and data[j][i+x] <= (local_background*1.1) and x_pos_bool == False:

                    xPos = x
                    x_pos_bool = True
        
                if x_neg_bool == True and x_pos_bool == True:
                    break
        
        else:

            for x in range(size[1]-1):
                if i-x >=0 and data[j][i-x] <= (local_background*1.1) and x_neg_bool == False:
                
                    xNeg = x
                    x_neg_bool = True

                if i+x<(size[1]) and data[j][i+x] <= (local_background*1.1) and x_pos_bool == False:

                    xPos = x
                    x_pos_bool = True
        
                if x_neg_bool == True and x_pos_bool == True:
                    break


            for y in range(size[0]-1):
            
                if j+y<(size[0]) and data[j+y][i] <= (local_background*1.1) and y_pos_bool == False:
                
                    yPos = y
                
                    y_pos_bool = True

                if j-y>=0 and data[j-y][i] <= (local_background*1.1) and y_neg_bool == False:
                
                    yNeg = y
                
                    y_neg_bool = True

                if y_neg_bool == True and y_pos_bool == True:
                    break
        

        jSub2=math.ceil((yNeg+yPos)/2)
        iSub2=math.ceil((xNeg+xPos)/2)
        if yPos>yNeg:
            j=j+(jSub2-yNeg)
        if yNeg>yPos:
            j=j-(jSub2-yPos)
        if j>=size[0]:
            j=(size[0]-1)
        if xPos>xNeg:
            i=i+(iSub2-xNeg)
        if xNeg>xPos:
            i=i-(iSub2-yPos)
        if i>=size[1]:
            i=(size[1]-1)



    return j, i, jSub2, iSub2

def object_region_start_pix(j : int, i : int, jSub2 : int, iSub2 : int, data : np.ndarray, size : np.ndarray, astr_object_pixel_loc : np.ndarray) -> 'tuple[int, int]':

    

    jSub3=j-(jSub2+4)
    if jSub3 <=0:
        jSub3=0
    if jSub3 >=size[0]:         #this isnt really needed but added just in case i add something new that would allow this to happen.
        jSub3=(size[0]-1)

    iSub3=i-(iSub2+4)
    if iSub3 <=0:
        iSub3=0
    if iSub3 >=size[1]:        #^
        iSub3=(size[1]-1)
    
    jSub4=j+(jSub2+4)
    if jSub4 <=0:              #^
        jSub4=0
    if jSub4 >=size[0]:
        jSub4=(size[0]-1)

    iSub4=i+(iSub2+4)
    if iSub4 <=0:              #^
        iSub4=0
    if iSub4 >=size[1]:
        iSub4=(size[1]-1)

    astr_object_pixel_loc = np.append(astr_object_pixel_loc, np.array([[jSub3, iSub3,jSub4,iSub4]]), axis=0)
    #print('my region:',jSub3, iSub3,jSub4,iSub4)
    return jSub3, iSub3, astr_object_pixel_loc
    
