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


from cmath import cos, pi, sin
import numpy as np
import math

#from sqlalchemy import false





def find_object(data : np.ndarray, local_background : float, size : np.ndarray, j : int, i : int) -> 'tuple[int, int, bool]':
    
             
    signal = True



    j, i, jSub2, iSub2 = object_center_correction(j, i, data, local_background, size)
    
    #print("from find object", jSub2, iSub2)

    if data[j][i] <= local_background*1.08:
        jSub2, iSub2 = 0, 0
        signal = False
        return j, i, jSub2, iSub2, signal

    try:    
        if data[j][i+4] <= local_background*1.08:

            if data[j][i+1] <= local_background*1.08:
                
                cosmic = True

            signal = False

            #j, i, signal = error_correction(j, i, data, local_background, n, signal)

    except(IndexError):

        if data[j][size[1]-1] <= local_background*1.08:

            if data[j][i+1] <= local_background*1.08:

                cosmic = True

            signal = False

       
            #j, i, signal = error_correction(j, i, data, local_background, n, signal)
    
    signal = error_correction(j,i,signal)

    if signal == False:
        jSub2, iSub2 = 0, 0 
        return j, i, jSub2, iSub2, signal


    
    
    return j, i, jSub2, iSub2, signal



def error_correction(j : int, i : int, signal : bool) -> bool:
   
   
    #need logic here to determine small objects from bad background. Potentially do a PSF and overlay to make sure things looks alike. 

    #adding something to remove 1 pixel sized objects and cosmics (LA cosmic might have a good start for this)

    if j or i == 0:

        signal == False
    
    
    return signal
        


def object_center_correction(j : int, i : int, data : np.ndarray, local_background : float, size : np.ndarray) -> 'tuple[int, int, int, int]':
    """

    ------------
    11/24/21

    compressed it down a bit but could still be coded better lol 


    """

    iter = 4       # number of iterations for center correction.

    yPos = 0
    yNeg = 0
    xPos = 0
    xNeg = 0

    

    
    for u in range(iter):

        tol = 1     #helps to make sure we encompass all of the psf 

        x_neg_bool = False
        x_pos_bool = False
        y_neg_bool = False
        y_pos_bool = False

    
        for y in range(size[0]-1):
        
            if j+y<(size[0]) and data[j+y][i] <= (local_background*1.08) and y_pos_bool == False:

                if j+y+tol>(size[0]) or data[j+y+tol][i] <= (local_background*1.08):
            
                    yPos = y
            
                    y_pos_bool = True


            if j-y>=0 and data[j-y][i] <= (local_background*1.08) and y_neg_bool == False : 
            
                if j-y-tol<0 or data[j-y-tol][i] <= (local_background*1.08):

                    yNeg = y
                    y_neg_bool = True
                
        

            if y_neg_bool == True and y_pos_bool == True:
                break
    


        for x in range(size[1]-1):

            if i-x >=0 and data[j][i-x] <= (local_background*1.08) and x_neg_bool == False:
                
                if i-x-tol < 0 or data[j][i-x-tol] <= (local_background*1.08):
                    xNeg = x
                    x_neg_bool = True

            if i+x<(size[1]) and data[j][i+x] <= (local_background*1.08) and x_pos_bool == False:

                if i+x+tol>(size[1]) or data[j][i+x+tol] <= (local_background*1.08):
                    xPos = x
                    x_pos_bool = True
    
            if x_neg_bool == True and x_pos_bool == True:
                break
    
    
        

        jSub2=round((yNeg+yPos)/2)
        iSub2=round((xNeg+xPos)/2)
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
    if jSub3 >=size[0]:         #this isnt really needed but added just in case something added would allow this to happen.
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



def object_tilt_detection(j : int, i : int, jSub2 : int, iSub2 : int, data : np.ndarray, local_background : float, size : np.ndarray) -> 'tuple[int, int, int, bool]':
    
    tilt = False
    object_tilt = 0
    temp_iSub2 = iSub2
    temp_jSub2 = jSub2

    for y in range(3):
        y+=1
        temp_iSub2+=1
        temp_jSub2+=1

        for x in range(361):  
            x += 0.5
            angle = x

            iSub3 = temp_iSub2 * math.cos(angle * math.pi / 180)

            jSub3 =  temp_jSub2 * math.sin(angle * math.pi / 180)

            if data[round(j + jSub3)][round(i + iSub3)] > local_background:
                angle = object_tilt 
                y-=1
    
    if (temp_iSub2 - 2) != iSub2:
        tilt = True
        iSub2 = temp_iSub2

    if (temp_jSub2 - 2) != jSub2:
        tilt = True
        jSub2 = temp_jSub2


    return jSub2, iSub2, angle, tilt 
    
        
        
    
