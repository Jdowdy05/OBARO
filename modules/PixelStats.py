# -*- coding: utf-8 -*-
"""
A module for performing any statistical calculations on the pixels of
the FITS images.

Functions
---------
imageBackground(imageData) : float
    Returns an average background of the image which we use as a basis to
    which we compare individual pixels.

@author: Ethan Colbert
@version: 1.0
"""

import numpy as np

def imageBackground(imageData : np.ndarray) -> float:
    """
    Parameters
    ----------
    imageData : numpy.ndarray
        A numpy array containing the pixel data that constitutes the image

    Returns
    -------
    avgBackground : float
        An estimate of the overall background of the image

    """
    #THIS CODE IS EXPERIMENTAL - NEEDS TEST TO ENSURE REPRESENTATIONAL ACCURACY
    total = 0
    numPixelsCounted = 0
    width = imageData.shape[0]
    height = imageData.shape[1]
    lowerDim = min(width, height)
    
    for count in range(0, lowerDim):
        total += imageData[count][count]
        total += imageData[lowerDim - count][count]
        total += imageData[count][lowerDim - count]
        total += imageData[lowerDim - count][lowerDim - count]
        numPixelsCounted += 4
    
    prelimAvg = total / numPixelsCounted
    #END OF EXPERIMENTAL CODE
    
    total = 0
    numPixelsCounted = 0
    
    for row in imageData:
        for element in row:
            if element < (1.25 * prelimAvg): #previously hard-coded as 6000
                total += element
                numPixelsCounted += 1
    
    avgBackground = total / numPixelsCounted
    
    return avgBackground

#Next function here.