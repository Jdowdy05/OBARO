import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import scipy.stats

def regularization(xml_lst):
    obj_surf_bri = []
    back_surf_bri = []
    for x in range(len(xml_lst)):
        obj_surf_bri.append(xml_lst[x][4])
        back_surf_bri.append(xml_lst[x][5])

    bin_list = []
    bin_size = 1000  #this value can be changed to more accurately find dimmer objects.
    x=600
    while x <= 6000:
        
        bin_list.append(x)
        x+=bin_size

    hist, bins = np.histogram(obj_surf_bri, bins = bin_list)

    n = 0
    
    peak = 0 

    for element in hist:

        if element > peak:
            peak = element
            peak_location = n
        n+=1
    for x in range(len(hist)):
        if hist[peak_location+x] < 20:
            obj_cut = bins[peak_location+x]
            break
    for x in range(len(obj_surf_bri)):
        if obj_surf_bri[x] <= obj_cut:
            del obj_surf_bri[x]

    for x in range(len(back_surf_bri)):
        if back_surf_bri[x] <=0:
            del back_surf_bri[x]
    