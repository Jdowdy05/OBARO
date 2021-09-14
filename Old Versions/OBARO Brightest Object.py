from astropy.io import fits
import numpy as np
from array import *
import math
from openpyxl import Workbook
import os
from progress.bar import IncrementalBar
#arcseconds=0.199922672
arcseconds=0.19990024
arcs=arcseconds**2
nameList=[]
pathList=[]
tempNum=[]
count=0


#put all .fits.gz files in the same folder as the script and run it. you'll get a excel file with all relavent collected data.



#arseconds in this script is just a averaged value of arcseconds from five different fits files.
#arcs is arcseconds squared which is needed for all calculations involving area.
#nameList is a python list of all fits files in the same folder as the script.
#count is the number of fits files so the script knows how many times to re run.







def fileSpec():                             #looks for fits files files
    global count
    for root, dirs, files in os.walk(".", topdown=True):
        for name in files:
            if name.endswith(".gz"):
                #print(os.path.join(root, name))
                pathList.append(os.path.join(root, name))
                nameList.append(name)
    count = len(nameList)
    #print(nameList)
def xcelStartup():                          #puts column names in excel sheet
    global workbook
    global sheet  
    workbook = Workbook()
    sheet = workbook.active
    sheet['A1']='File Name:'
    sheet['B1']='Object Mean Pixel Value'
    sheet['C1']='Object Mean Pixel Value Error '
    sheet['D1']='Object Region Area'
    sheet['E1']='Object Surface Brightness'
    sheet['F1']='Object Surface Brightness Error'
    sheet['G1']='Background Mean Pixel Value'
    sheet['H1']='Background Mean Pixel Value Error '
    sheet['I1']='Background Region Area'
    sheet['J1']='Background Surface Brightness'
    sheet['K1']='Background Surface Brightness Error'
    workbook.save(filename='Master Data sheet seed 1000 ver3.xlsx')

def loadFile(QQ):  # loads file and gives image header data
    
    global fileName
    global CC
    global data
    global hdul
    global imageSize

    fileName = (pathList[QQ])
    fits_image_filename = fits.open(fileName)
    hdul = fits.open(fileName)
    #hdul.info()
    data = hdul[0].data
    imageSize=data.shape


def findSignal():  # locates pixel of heighest brightness value and returns pixel cords  // also detects error and if it is looks for next non error pixel // needs work
    global avgBack
    global C
    global R
    h = 0
    j = -1
    C = 0
    R = 0
    e = 0
    for row in data:
        i = -1
        j += 1
        for element in row:
            i += 1
            if element >= h:
                h = element
                R = j
                C = i
                e = h

    if data[R][C-2] <= avgBack*1.05:
        h = 0
        j = -1
        x = 0
        y = 0
        e = 0
        tempR = 0
        tempC = 0
        for row in data:
            i = -1
            j += 1
            for element in row:
                i += 1
                if element >= h:
                    y = j
                    x = i
                    h = element
                    if y == R and x == C:
                        y = tempR
                        x = tempC
                        h = e
                    tempR = y
                    tempC = x
                    e = h
        R = y
        C = x
    

def avgLocalBackground():              # avg local background of signal to accurately calculate sums 
    global C
    global R
    global minBxpix
    global minBypix
    global LavgBack
    global tempL
    global tempW
    print(R,C)
    LtotalB=0
    LtotalBpix=0
    h=6000
    i=0
    for i in range((2*abs(tempL))):
        
        j = 0

        for j in range((2*abs(tempW))):
            
            if (minBypix+i)>=imageSize[0] or (minBxpix+j)>=imageSize[1] or (minBypix+i)<0 or (minBxpix+j)<0:
                
                continue
            
            if data[minBypix+i][minBxpix+j] <= h:

                h = data[minBypix+i][minBxpix+j]
    i=0
    for i in range((2*abs(tempL))):

        j = 0

        for j in range((2*abs(tempW))):

            if (minBypix+i)>=imageSize[0] or (minBxpix+j)>=imageSize[1] or (minBypix+i)<0 or (minBxpix+j)<0:
                
                continue

            if data[minBypix+i][minBxpix+j] <=h*1.05:     #change where h is to 6k and remove code above both for loops
                
                LtotalBpix += 1

                LtotalB += data[minBypix+i][minBxpix+j]          

    LavgBack=LtotalB/LtotalBpix


def avgBackground():  # finds average background brightness for more accurate signal region detection 
    global avgBack
    totalBpix = 0
    totalB = 0

    for row in data:

        for element in row:

            if element < 6000:
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
    yu = 0
    yd = 0
    xr = 0
    xl = 0

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
    #print(xl)

def signalRegionSize():  # determines size of region around signal
    global L
    global W
    global Wb
    L=0
    W=0
    Wb=0
    if yd >= yu:
        L = yd
    if yd <= yu:
        L = yu
    if xl >= xr:
        W = xl
    if xl <= xr:
        W = xr
    Wb = W
    #print('W=',W)
    #print('L=',L)

def bgRegionSize():  # makes background region size 
    global tempL
    global tempW
    global L
    global Wb

    tempL = L*4

    tempW = Wb*4

def minPix():
    global minSypix
    global minSxpix
    global minBxpix
    global minBypix
    global tempL
    global tempW
    global L
    minSypix = R-L
    minSxpix = C-L
    minBxpix = C-tempW
    minBypix = R-tempL    



    

def signalSumCalc():  # calculates signal sum and npix
    global Ssum
    global Spix
    global LavgBack
    Ssum = 0
    Spix = 0
    i = 0
    j = 0
    
    for i in range((2*L)):
        j = 0
        for j in range((2*L)):
            if (minSypix+i)>=imageSize[0] or (minSxpix+j)>=imageSize[1] or (minSypix+i)<0 or (minSxpix+j)<0  :
                continue
            if data[minSypix+i][minSxpix+j] > avgBack*1.10:
                Spix += 1
                Ssum = Ssum+data[minSypix+i][minSxpix+j]

    #print("Signal Sum", Ssum)


def backgroundSumCalc():  # calculates background sum // also calculates npix for the square region
    global Bsum
    global Bpix
    global LavgBack
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
    global Spix
    global Bpix
    SArea=Spix*arcs
    BArea=Bpix*arcs

    #print('Signal Area',SArea)
    #print('Background Area',BArea)

def surf_bri():
    global SArea
    global BArea
    global Ssum
    global Bsum
    global Signal_Surf_bri
    global Background_Surf_bri
    Signal_Surf_bri=Ssum/SArea
    Background_Surf_bri=(Bsum+Ssum)/(BArea+SArea)                #Bsum/BArea

    #print('Signal Surface Brightness',Signal_Surf_bri)
    #print('Background Surface Brightness',Background_Surf_bri)

def surf_err():
    global SArea
    global BArea
    global Serror
    global Berror
    global SSR
    global BSR
    SSR=Serror/SArea
    BSR=Berror/BArea

    #print('Signal Surface Error',SSR)
    #print('Background Surface Error',BSR)


def mean():
    global Ssum
    global Bsum
    global Spix
    global Bpix
    global Smean
    global Bmean
    Smean=Ssum/Spix
    Bmean=Bsum/Bpix
    #print('Signal mean',Smean)
    #print('Background mean',Bmean)

fileSpec()
xcelStartup()
QQ=0
errorfiles=0
bar = IncrementalBar('Processing', max=count)
for QQ in range(count):
    loadFile(QQ)
    avgBackground()
    findSignal()
    signalSize()
    signalRegionSize()
    bgRegionSize()
    minPix()
    #avgLocalBackground()               rework
    if L==0 or W==0 or tempL==0 or tempW==0:
        sheet['A'+str(QQ+2)]="error for file:"+nameList[QQ]
        errorfiles+=1
        bar.next
        continue
    signalSumCalc()
    backgroundSumCalc()
    errorCalc()
    ArcArea()
    surf_bri()
    surf_err()
    mean()
    
    sheet['A'+str(QQ+2)]=nameList[QQ]
    sheet['B'+str(QQ+2)]=Smean
    sheet['C'+str(QQ+2)]=Serror
    sheet['D'+str(QQ+2)]=SArea
    sheet['E'+str(QQ+2)]=Signal_Surf_bri
    sheet['F'+str(QQ+2)]=SSR
    sheet['G'+str(QQ+2)]=Bmean
    sheet['H'+str(QQ+2)]=Berror
    sheet['I'+str(QQ+2)]=BArea
    sheet['J'+str(QQ+2)]=Background_Surf_bri
    sheet['K'+str(QQ+2)]=BSR
    
    print('Object Mean Pixel Value',Smean)
    print('Object Total Pixel Value Error',Serror)
    print('Object Region Area',SArea)
    print('Object Surface Brightness',Signal_Surf_bri)
    print('Object Surface Brightness Error',SSR)
    print('Background Mean Pixel Value',Bmean)
    print('Background Total Pixel Value Error',Berror)
    print('Background Region Area',BArea)
    print('Background Surface Brightness',Background_Surf_bri)
    print('Background Surface Brightness Error',BSR)
    bar.next()
workbook.save(filename='Master Data sheet seed 1000 ver3.xlsx')
#bar.finish()
#print(errorfiles)