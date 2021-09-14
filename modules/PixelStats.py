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
    total = 0
    numPixelsCounted = 0
    
    for row in imageData:
        for element in row:
            if element < 6000: #the logic here needs to be a lot smarter
                total += element
                numPixelsCounted += 1
    
    avgBackground = total / numPixelsCounted
    
    return avgBackground

#Next function here.