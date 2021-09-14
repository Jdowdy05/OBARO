from re import X
from astropy.io import fits
import numpy as np
from array import *
import math
from openpyxl import Workbook
import os
from progress.bar import IncrementalBar
arcseconds=0.199922672
#arcseconds=0.19990024
arcs=arcseconds**2
nameList=[]
pathList=[]
signalList=[[]]*2010
count=0
QQ=0
O=2
M=0

errorfiles=0
def fileSpec():                             #looks for fits files files
    global count
    for root, dirs, files in os.walk(".", topdown=True):
        for name in files:
            if name.endswith(".gz"):
                if name.startswith("lsst_a"):
                #print(os.path.join(root, name))
                    pathList.append(os.path.join(root, name))
                    nameList.append(name)
    count = len(nameList)
    #print(nameList)

def loadFile(i):  # loads file and gives image header data
    global fileName
    global CC
    global data
    global hdul
    global imageSize

    fileName = (pathList[i])
    fits_image_filename = fits.open(fileName)
    hdul = fits.open(fileName)
    #hdul.info()
    data = hdul[0].data
    imageSize=data.shape

def xcelStartup():                          #puts column names in excel sheet
    global workbook
    global sheet  
    workbook = Workbook()
    sheet = workbook.active
    sheet['A1']='File Name:'
    sheet['B1']='Signal Region (Mean)'
    sheet['C1']='Signal Region (Surface Brightness)'
    sheet['D1']='Signal Region (Surface Error)'
    sheet['E1']='Background (Mean)'
    sheet['F1']='Background (Surface Brightness)'
    workbook.save(filename='Phosim-5.1.7-All-Objects-'+str(M)+'.xlsx')
    
    
    

def findSignal(QQ):  # locates pixel of heighest brightness value and returns pixel cords  // also detects error and if it is looks for next non error pixel // needs work
    global O
    global P
    global C
    global R
    j = -1
    C = 0
    R = 0
    
    for row in data:
        i = -1
        j += 1
        for element in row:
            i += 1
            
            if element > backR*1.10:
                C=i
                R=j
                #print(signalList[j])
                if i not in signalList[j]: 
                    #print(element) 
                    signalSize()
                    signalRegionSize()
                    bgRegionSize()
                    minPix()
                    
                    try:
                        signalSumCalc()
                        backgroundSumCalc()
                        errorCalc()
                        ArcArea()
                        if SArea <=0.3:
                            #print(' Area:',SArea)
                            continue
                        
                        surf_bri()
                        surf_err()
                        mean()
                    except:
                        continue
                    sheet['B'+str(O)]=Smean
                    sheet['C'+str(O)]=Signal_Surf_bri
                    sheet['D'+str(O)]=SSR
                    sheet['E'+str(O)]=Bmean
                    sheet['F'+str(O)]=Background_Surf_bri
                    sheet['G'+str(O)]=Bpix
                    sheet['H'+str(O)]=Spix
                    workbook.save(filename='Phosim-5.1.7-All-Objects-'+str(M)+'.xlsx')
                    #print('Object Mean Pixel Value',Smean)
                    #print('Object Total Pixel Value Error',Serror)
                    #print('Object Region Area',SArea)
                    #print('Object Surface Brightness',Signal_Surf_bri)
                    #print('Object Surface Brightness Error',SSR)
                    #print('Background Mean Pixel Value',Bmean)
                    #print('Background Total Pixel Value Error',Berror)
                    #print('Background Region Area',BArea)
                    #print('Background Surface Brightness',Background_Surf_bri)
                    #print('Background Surface Brightness Error',BSR)
                    O+=1

    


def avgBackground():  # finds average background brightness for more accurate signal region detection 
    global avgBack
    totalBpix = 0
    totalB = 0

    for row in data:

        for element in row:

            if element < backR*1.10:
                totalBpix += 1
                totalB += element

    avgBack = totalB/totalBpix
    #print('Average Background value', avgBack)


def signalSize():                   #finds the size of box needed to fit all of the signal
    global imageSize
    global xl
    global xr
    global yu
    global yd
    global R
    global C
    
    yu = 0
    yd = 0
    xr = 0
    xl = 0
    a=0
    #print('this is R and C:',R,C,data[R][C])
    for x in range(imageSize[1]):
        if C-x >=0:
            if data[R][C-x] <= (avgBack*1.10):
                
                xl = x
                break
                
    for x in range(imageSize[1]):
        if C+x<imageSize[1]:
            if data[R][C+x] <= (avgBack*1.10):
                
                xr = x
                break
    
    for y in range(imageSize[0]):
        if R+y<imageSize[0]:
            if data[R+y][C] <= (avgBack*1.10):
                
                yu = y
                break
    for y in range(imageSize[0]):
        if R-y>=0:
            if data[R-y][C] <= (avgBack*1.10):
                
                yd = y
                break        

    if xr and xl == 1 or 2:
        for y in range(imageSize[0]):
            if R+y<imageSize[0]:
                if data[R+y][C] <= (avgBack*1.10):
                
                    yu = y
                    break
        for y in range(imageSize[0]):
            if R-y>=0:
                if data[R-y][C] <= (avgBack*1.10):
                
                    yd = y
                    break        

        j=math.ceil((yd+yu)/2)
        if yu>yd:
            R=R+(j-yd)
        if yd>yu:
            R=R-(j-yu)
        if R>2009:
            R=2009
            
        for x in range(imageSize[1]):
            if C-x >=0:
                if data[R][C-x] <= (avgBack*1.10):
                
                    xl = x
                    break
                
        for x in range(imageSize[1]):
            if C+x<imageSize[1]:
                if data[R][C+x] <= (avgBack*1.10):
                
                    xr = x
                    break

    if yu and yd == 1 or 2:

        for x in range(imageSize[1]):
            if C-x >=0:
                if data[R][C-x] <= (avgBack*1.10):
                
                    xl = x
                    break
                
        for x in range(imageSize[1]):
            if C+x<imageSize[1]:
                if data[R][C+x] <= (avgBack*1.10):
                
                    xr = x
                    break
        i=math.ceil((xr+xl)/2)
        if xr>xl:
            C=C+(i-xl)
        if xl>xr:
            C=C-(i-xl)
        #if C>509:
            #C=509

        for y in range(imageSize[0]):
            if R+y<imageSize[0]:
                if data[R+y][C] <= (avgBack*1.10):
                
                    yu = y
                    break
        for y in range(imageSize[0]):
            if R-y>=0:
                if data[R-y][C] <= (avgBack*1.10):
                
                    yd = y
                    break        
    
    #print(j,i)
    #print(' Center:',R,C)
def signalRegionSize():  # determines size of region around signal
    global L
    global W
    L=0
    W=0
    
    
    L = math.ceil((yd+yu)/2)
    W = math.ceil((xr+xl)/2)
   
    #print('W=',W)
    #print('L=',L)

def bgRegionSize():  # makes background region size 
    global tempL
    global tempW
    global L
    global Wb

    tempL = L*2

    tempW = W*2


def minPix():
    global minSypix
    global minSxpix
    global minBxpix
    global minBypix
    global tempL
    global tempW
    global L
    global W
    minSypix = R-L
    minSxpix = C-W
    minBxpix = C-tempW
    minBypix = R-tempL    

def backToObjectRatio():
    global backR
    i=0
    j=0
    h=0
    l=10000
    V=0

    for j in range(imageSize[0]):
        
        for i in range(imageSize[1]):

            if data[j][i] <=1710:
                V=V+1
                if V==20000:
                    l=1710
            
            if l>=data[j][i]:
                if data[j][i] <=1710:
                  continue  
                l=data[j][i]
    

    G=l*1.6
    #print(' ',G,' ',l)
    #rat=h/l
    backR=G
    #print(h/l)



def signalSumCalc():  # calculates signal sum and npix
    global signalList
    global Ssum
    global Spix
    Ssum = 0
    Spix = 0
    i = 0
    j = 0
    for i in range((2*L)):
        j = 0
        for j in range((2*L)):
            if (minSypix+i)>=imageSize[0] or (minSxpix+j)>=imageSize[1] or (minSypix+i)<0 or (minSxpix+j)<0  :
                continue 
            if minSxpix+j not in signalList[minSypix+i]:
                if data[minSypix+i][minSxpix+j] > avgBack*1.10:
                    oof=signalList[minSypix+i]
                    oof.append(minSxpix+j)
                    Spix += 1
                    Ssum = Ssum+data[minSypix+i][minSxpix+j]
    #print("Signal Sum", Ssum)

def backgroundSumCalc():  # calculates background sum // also calculates npix for the square region
    global Bsum
    global Bpix
    global imageSize
    Bsum = 0
    i = 0
    Bpix = 0

    for i in range((abs(tempL)*2)):
        j = 0
        for j in range((abs(tempW)*2)):
            if (minBypix+i)>=imageSize[0] or (minBxpix+j)>=imageSize[1] or (minBypix+i)<0 or (minBxpix+j)<0:
                continue
            if data[minBypix+i][minBxpix+j] <= avgBack*1.10:
                Bpix += 1
                Bsum = Bsum+data[minBypix+i][minBxpix+j]

    #print('Background Sum', Bsum)

def errorCalc():                    #calculates error
    global Serror
    global Berror
    Serror = math.sqrt(abs(Ssum))
    Berror = math.sqrt(abs(Bsum))
    #print('Signal Error', Serror)
    #print('Background Error', Berror)



def ArcArea():                      #area of signal and background
    global SArea
    global BArea
    SArea=Spix*arcs
    BArea=Bpix*arcs

    #print('Signal Area',SArea)
    #print('Background Area',BArea)

def surf_bri():
    global Signal_Surf_bri
    global Background_Surf_bri
    Signal_Surf_bri=Ssum/SArea
    Background_Surf_bri=(Bsum+Ssum)/(BArea+SArea)                #Bsum/BArea

    #print('Signal Surface Brightness',Signal_Surf_bri)
    #print('Background Surface Brightness',Background_Surf_bri)

def surf_err():
    global SSR
    global BSR
    SSR=Serror/SArea
    BSR=Berror/SArea
    #print('Signal Surface Error',SSR)
    #print('Background Surface Error',BSR)


def mean():
    global Smean
    global Bmean
    Smean=Ssum/Spix
    Bmean=Bsum/Bpix
    #print('Signal mean',Smean)
    #print('Background mean',Bmean)
QQ=0
P=1
M=0
fileSpec()
xcelStartup()
bar = IncrementalBar('Processing', max=count)

for QQ in range(count):
    loadFile(QQ)
    backToObjectRatio()
    avgBackground()
    sheet['A'+str(O)]=nameList[QQ]
    findSignal(QQ)
    
    del signalList
    signalList=[[]]*2010
    if P>144:
        O=2
        P=1
        M+=1
        workbook.close()
        xcelStartup()
        workbook.save(filename='Phosim-5.1.7-All-Objects-'+str(M)+'.xlsx')
        
    bar.next()
    P+=1
    workbook.save(filename='Phosim-5.1.7-All-Objects-'+str(M)+'.xlsx')
bar.finish()