# -*- coding: utf-8 -*-
"""
Module that does the file handling for OBARO.

Functions
---------

def FitsLocator(fitsDir): list[str]
    Top Down directroy search that looks for relevant fits.
    Searches same directory as program if no directory was entered.
    Returns a list of file paths and a list of file names.

def loadFile(fileName): np.ndarray
    Opens fits file and gives fits file header data.
    Returns a np.ndarray that has all pixel data of fits image.


@author: Jordan Dowdy
@version: 1.1, 10/12/21

"""

import numpy as np
import os
from astropy.io import fits

def fits_locator(fitsDir : str) -> "list[str]":                             

    path_list=[]
    name_list=[]

    if  not fitsDir:
        fitsDir = "."

    for root, dirs, files in os.walk(fitsDir, topdown=True):
        for name in files:
            #if name.endswith(".gz") and name.startswith("lsst_a_"):
            if name.endswith(".fits") or name.endswith(".fits.gz"):
                path_list.append(os.path.join(root, name))
                name, fileType = name.split(".fits")
                name_list.append(name)
    return path_list, name_list

def load_file(fileName : str, i : int) -> np.ndarray:
    
    hdul = fits.open(fileName)
    info = hdul.info()
      
    data = hdul[i].data
    
    header=hdul[i].header
    imageSize=data.shape
    print(imageSize)
    hdul.close()
    return data, header, imageSize

def fileSegments(fileName : str):

    hdul = fits.open(fileName)
    segmnt_end = len(hdul)
    try:
        data = hdul[0].data
        imageSize = data.shape()
        segmnt_start = 0
    except:
        segmnt_start = 1
    hdul.close()
    return segmnt_start, segmnt_end