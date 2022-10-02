# -*- coding: utf-8 -*-
"""

This is a PSF test.


"""


from pyexpat import model
from signal import Sigmasks
import statistics
import sys
import numpy as np
from astropy.modeling import models, fitting
from astropy.io import fits
import matplotlib.pyplot as plt
import math

import itertools
import FitsFileManaging
import BackgroundDetection
import ObjectDetection
import Calculations
import XMLFileHandling



def FWHM(j : int, i : int, j_dist : int, i_dist : int, min_j : int, min_i : int, background : int, header : dict, data : np.ndarray, size : np.ndarray):

    #gain = header["Gain"]
    #exp_time = header["Exptime"]
    
    obj_slice=data[min_j:min_j+2*(j_dist+2), min_i:min_i+2*(i_dist+2)]

    y = 0
    max_val = 0
    yp,xp = obj_slice.shape
    gaussian_x_list = []
    gaussian_y_list = []
    for row in obj_slice:
        x = 0
        for element in row:
            if element > max_val:
                max_val = element
                max_loc_y = y 
                max_loc_x = x
            x+=1
        y+=1
    max_loc = [[y,x]]
    
    mixed_guas = []



    """
    for x in range(-i_dist,i_dist):

        if obj_slice[j_dist+4][4+x] > background*1.08:
            
            #flux_above_sky = (obj_slice[j_dist+4][i_dist+4+x] - background)* gain/exp_time
            gaussian_x_list.append(obj_slice[j_dist+4][4+x])
    """
    
    center_val = obj_slice[j_dist+4][i_dist+4]
    
    
    for y in range(yp):
    
        #if obj_slice[4+y][i_dist+4] > background*1.08:
            
            #flux_above_sky = (obj_slice[j_dist+4+y][i_dist+4] - background)* gain/exp_time
        gaussian_y_list.append(obj_slice[y][i_dist+4])

    for x in range(xp):

        gaussian_x_list.append(obj_slice[j_dist+4][x])

    

    for row in obj_slice:
        for element in row:
            if element <= background*1.08:
                element = 0

    
    obj_slice_copy = obj_slice[obj_slice != 0]
    obj_slice_copy.flatten()
    #for x in range(len(obj_slice)):
    #    obj_slice[x] = (obj_slice[x]-1200)*gain/exp_time
    
    
    object_list = obj_slice_copy.tolist()
    #print(my_array)
    #star = [2563,3213,4134,6578,8302,9852,11202,12065,11849,11146,9810,8137,6527,4998,3845,2979]

    #mu = statistics.mean(my_array)
    #sigma = statistics.stdev(my_array)


    """
    mu_x = statistics.mean(gaussian_x_list)
    sigma_x = statistics.stdev(gaussian_x_list)
    """

    mu_y, sigma_y, variance_y, fwhm_y = stats_calc(gaussian_y_list)
    mu_x, sigma_x, variance_x, fwhm_x = stats_calc(gaussian_x_list)

    #sigma_y = statistics.pstdev(gaussian_y_list, mu=mu_y)
    #sigma_x = statistics.pstdev(gaussian_x_list, mu=mu_x)
    print("mu_y: %d, sigma_y: %d, FWHM_y: %d\n" % (mu_y,sigma_y, fwhm_y))
    print("mu_x: %d, sigma_x: %d, FWHM_x: %d\n" % (mu_x,sigma_x, fwhm_x))
    
    print("Value at center: %d\n" % center_val)
    print("j:%d, i:%d\n" % (j,i))
    #gaussian_list = list(itertools.chain.from_iterable(zip(gaussian_x_list,gaussian_y_list)))
    
    #variance = sigma**2
    #print(2.35*sigma)  THIS IS WHAT I NEED FOR FWHM
    #x = np.linspace(mu - 3*sigma, mu + 3*sigma, 100)
   
    figure, axis = plt.subplots(3,1)
    print(gaussian_y_list)
    axis[0].plot(gaussian_y_list, color="b", label="x")
    axis[1].plot(gaussian_x_list, color="b", label="x")
    axis[2].plot(object_list, color="g", label="y")
    plt.legend()
    plt.show()

def stats_calc(gaussian):

    mu = statistics.mean(gaussian)

    for x in range(len(gaussian)):
        
        temp =+ (gaussian[x] - mu)**2
    
    sigma = math.sqrt(temp/len(gaussian))

    variance = sigma**2

    #fwhm_const = 2*math.sqrt(2*math.ln(2))*sigma
    fwhm_const = 10
    return mu, sigma, variance, fwhm_const




def object_psf(j : int, i : int, j_dist : int, i_dist : int, min_j : int, min_i : int, background : int, header : dict, data : np.ndarray, size : np.ndarray):  
    
    obj_slice=data[min_j:min_j+2*(j_dist+2), min_i:min_i+2*(i_dist+2)]

    for row in obj_slice:
        for element in row:
            if element <= background:
                element = 0

    yp,xp = obj_slice.shape

    

    y, x, = np.mgrid[:yp, :xp]
    
    PSF_func = models.Gaussian2D()
    
    PSF_fit = fitting.LevMarLSQFitter()

    f = PSF_fit(PSF_func, x, y, obj_slice)

    



    

    """
    needs work


    plt.figure(figsize=(8, 2.5))
    plt.subplot(1, 3, 1)
    plt.imshow(obj_slice)
    plt.title("Data")
    plt.subplot(1, 3, 2)
    plt.imshow(f(x, y))
    plt.title("Model")
    plt.subplot(1, 3, 3)
    plt.imshow(obj_slice - f(x, y))
    plt.title("Residual")
    plt.show()

    """


def sigma_from_ADU():

    #take center or peak value of object and solve for sigma from PSF equation.
    #doesnt have to be peak value exactly but its possible sigma could be closer
    #to its real value especially for simulated data. 
    pass