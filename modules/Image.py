# -*- coding: utf-8 -*-
"""
@author: Ethan Colbert
@version: 1.0
"""

import numpy as np
from astropy.io import fits

class Image:
    """
    Provides a representation of all needed data from FITS files.
    
    Methods
    -------
    __init__(filePath)
        Constructor. Opens file at location filePath, extracts all necessary
        data, then closes the file.
    
    """
    def __init__(self, filePath : str):
        """
        Parameters
        ----------
        filePath : str
            the location of the FITS file to be represented.

        Returns
        -------
        None.
        
        """
        
        hdul = fits.open(filePath)
        self._imageData = hdul[0].data
        
        #will also read necessary header data and and store it.
        hdul.close()
    
    @property
    def imageData(self) -> np.ndarray:
        return self._imageData
    