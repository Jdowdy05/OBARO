
from astropy.io import fits
import os
import numpy as np


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
    
    data = hdul[0].data
    
    header=hdul[0].header
    
    print(len(hdul))
    hdul.close()
    
    

    
path = []
name = []


#dir = input("DIR: ")
path, name =  fits_locator("/Users/jordan/Documents/VS Code/OBARO-main/Test FITS Data/lsst_1000_f1_R01_S00_E000")


load_file(path[0], 0)

for x in range(1,1):
    print(x)

