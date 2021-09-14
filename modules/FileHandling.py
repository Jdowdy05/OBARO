# -*- coding: utf-8 -*-
"""
A module containing methods that handle the interactions between
OBARO and the FITS files.

Functions
---------
findFitsFiles(topDir) : list[str]
    Walks the directory tree rooted at topDir and returns a list
    of the paths to all relevant FITS files it finds.

loadFitsImage(filePath) : numpy.ndarray
    Opens the specified FITS image and returns the actual image data in a
    numpy array.

@author: Ethan Colbert
@version: 1.0
"""

#import typingmodule
import numpy as np
import os
from astropy.io import fits

def findFitsFiles(topDir : str) -> list[str]:
    """
    Parameters
    ----------
    topDir : str
        the root of the directory tree to be searched

    Returns
    -------
    fileList : list[str]
        a list of the paths to all lsst FITS files in the directory tree
        that was searched
    """
    fileList = []
    
    for (root, dirs, files) in os.walk(topDir, topdown=True):
        for fileName in files:
            if (fileName.endswith(".fits.gz") and fileName.startswith("lsst")):
                fileList.append(os.path.join(root, fileName))
    
    return fileList

"""
This method was moved to the Image class - delete once class is tested.
def loadFitsImage(filePath : str) -> np.ndarray:
    #triple quotes here
    Parameters
    ----------
    filePath : str
        the path to the FITS file to be opened

    Returns
    -------
    image : numpy.ndarray
        A numpy array containing the actual image data from the FITS image.

    #triple quotes here
    
    #hdul = fits.open(filePath)
    #image = hdul[0].data
    #hdul.close()
    image = fits.getdata(filePath)
    
    return image
"""

#Next function here.