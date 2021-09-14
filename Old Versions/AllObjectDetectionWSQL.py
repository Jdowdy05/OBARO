from astropy.io import fits
import numpy as np
from array import *
import math
from openpyxl import Workbook
import os
from progress.bar import IncrementalBar
import mysql.connector
from mysql.connector import Error
#arcseconds=0.199922672
arcseconds=0.19990024
arcs=arcseconds**2
nameList=[]
pathList=[]
signalList=[[]]*2010
count=0
QQ=0
O=2
idN=0

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
    
def sqlStartUp():
    global connection
    
    def create_connection(host_name, user_name, user_password, db_name):
        connection = None
        try:
            connection = mysql.connector.connect(
                host=host_name,
                user=user_name,
                passwd=user_password,
                database=db_name
            )
            print("Connection to MySQL DB successful")
        except Error as e:
            print(f"The error '{e}' occurred")

        return connection

    connection = create_connection("localhost", "root", "BO3beast","OBARO_data")

    

    

def findSignal(QQ):  # locates pixel of heighest brightness value and returns pixel cords  // also detects error and if it is looks for next non error pixel // needs work

    global O
    global P
    global C
    global R
    j = -1
    C = 0
    R = 0
    def execute_query(connection, query):
        cursor = connection.cursor()
        try:
            cursor.execute(query)
            connection.commit()
            print("Query executed successfully")
        except Error as e:
            print(f"The error '{e}' occurred")

    create_users_table = """
                        CREATE TABLE IF NOT EXISTS files (
                        name CHAR(39), 
                        version TEXT, 
                        seed INT, 
                        PRIMARY KEY (name)
                        )   ENGINE = InnoDB
                        """
    execute_query(connection, create_users_table)
    cursor = connection.cursor()
    add_file = "INSERT INTO files ( name, version, seed) VALUES ( %s, %s, %s)"
    data_file = [nameList[QQ], ver, seed]
    cursor.execute(add_file, data_file)

    
    for row in data:
        i = -1
        j += 1
        for element in row:
            i += 1

            if element > avgBack*1.30:
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
                        objN+=1
                        backgroundN+=1
                        idN+=1
                        if SArea <=1:
                            continue
                        surf_bri()
                        surf_err()
                        mean()
                        create_users_table == """
                        CREATE TABLE IF NOT EXISTS objects (
                        objectNum INT,
                        name CHAR(39), 
                        oSum DOUBLE, 
                        oNpix INT, 
                        oArea DOUBLE, 
                        CONSTRAINT FK_name FOREIGN KEY (name) REFERENCES files(name),
                        PRIMARY KEY (objectNum)
                        )   ENGINE = InnoDB
                        """
                        execute_query(connection, create_users_table)
                        add_objects = "INSERT INTO objects ( objectNum, name, oSum, oNpix, oArea) VALUES ( %s, %s, %s, %s, %s)"
                        object_data = [objN, nameList[QQ], Ssum, Spix, SArea]
                        cursor = connection.cursor()
                        cursor.execute(add_objects, object_data)

                        create_users_table =="""
                        CREATE TABLE IF NOT EXISTS background (
                        backgroundNum INT,
                        name CHAR(39), 
                        bAvg DOUBLE,
                        bSum DOUBLE, 
                        bNpix INT, 
                        bArea DOUBLE, 
                        FOREIGN KEY fk_name (name) REFERENCES files(name),
                        PRIMARY KEY (backgroundNum)
                        )   ENGINE = InnoDB
                        """
                        execute_query(connection, create_users_table)
                        add_background = "INSERT INTO background ( backgroundNum, name, bAvg, bSum, bNpix, bArea) VALUES ( %s, %s, %s, %s, %s, %s)"
                        background_data = [backgroundN, nameList[QQ], avgBack, Bsum, Bpix, BArea]
                        cursor = connection.cursor()
                        cursor.execute(add_background, background_data)

                        create_users_table == """
                        CREATE TABLE IF NOT EXISTS mainData (
                        objectNum INT,
                        backgroundNum INT,
                        name CHAR(39),
                        objectMeanPixelValue DOUBLE,
                        objectTotalPixelValue DOUBLE,
                        objectRegionArea DOUBLE,
                        objectSurfaceBrightness DOUBLE,
                        objectSurfaceBrightnessError DOUBLE,
                        backgroundMeanPixelValue DOUBLE,
                        backgroundTotalPixelValueError DOUBLE,
                        backgroundRegionArea DOUBLE,
                        backgroundRegionBrightness DOUBLE,
                        backgroundRegionBrightnessError DOUBLE,
                        FOREIGN KEY fk_name (name) REFERENCES files(name),
                        FOREIGN KEY fk_objectNum (objectNum) REFERENCES objects(objectNum),
                        PRIMARY KEY (objectNum)
                        )   ENGINE = InnoDB
                        """
                        execute_query(connection, create_users_table)
                        add_mainData =  "INSERT INTO mainData ( objectNum, backgroundNum, name, objectMeanPixelValue, objectTotalPixelValue, objectRegionArea, objectSurfaceBrightness, objectSurfaceBrightnessError, backgroundMeanPixelValue, backgroundTotalPixelValueError, backgroundRegionArea, backgroundRegionBrightness, backgroundRegionBrightnessError) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                        main_data = [objN, backgroundN, nameList[QQ],  Smean, Serror, SArea, Signal_Surf_bri, SSR, Bmean, Berror, BArea, Background_Surf_bri, BSR]
                        cursor = connection.cursor()
                        cursor.execute(add_mainData, main_data)

                        
                    except:
                        continue
                
                    
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
        if C>509:
            C=509

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

    tempL = L*4

    tempW = W*4


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
    BSR=Berror/SArea
    #print('Signal Surface Error',SSR)
    #print('Background Surface Error',BSR)


def mean():
    global Ssum
    global Bsum
    global Spix
    global Bpix
    global Smean
    global Bmean
    Smean=0
    Bmean=0
    Smean=Ssum/Spix
    Bmean=Bsum/Bpix
    #print('Signal mean',Smean)
    #print('Background mean',Bmean)
QQ=0
P=0
objN=0
backgroundN=0
ver = input("Enter Phosim version: ")
seed = input("Enter seed number: ")
fileSpec()
sqlStartUp()
#bar = IncrementalBar('Processing', max=count)


for QQ in range(count):
    loadFile(QQ)
    avgBackground()
    findSignal(QQ)
    data_file = [nameList[QQ], ver, seed, objN]
    objN=0
    backgroundN=0
    del signalList
    signalList=[[]]*2010
    
    if P>=16:
        P=0
    P+=1
    
    
