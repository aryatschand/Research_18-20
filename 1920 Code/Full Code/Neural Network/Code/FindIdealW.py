import pymysql
import timeit
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math
import random
from sympy import *
import insertPoint
import QueryData
import GetIdealColor
import sys

# 2 variable linear regression, return linear slope
def regression(xVals, yVals):
    totalX = 0
    totalXSq = 0
    totalY = 0
    totalMult = 0
    count = len(xVals)

    for x in range(0, len(xVals)):
        totalXSq+=(xVals[x]*xVals[x])
        totalX+=xVals[x]
        totalY+=yVals[x]
        totalMult+=(yVals[x]*xVals[x])
    Linslope = 100.0*((count*totalMult)-(totalY*totalX))/((count*totalXSq)-(totalX*totalX)/2)
    return abs(Linslope)

# 2 variable linear regression, return y-intercept
def intercept(xVals, yVals):
    totalX = 0.0
    totalXSq = 0.0
    totalY = 0.0
    totalMult = 0.0
    count = len(xVals)

    for x in range(0, len(xVals)):
        totalXSq+=(xVals[x]*xVals[x])
        totalX+=xVals[x]
        totalY+=yVals[x]
        totalMult+=(yVals[x]*xVals[x])
    yInt = float(((totalY*totalXSq)-(totalX*totalMult))/((count*totalXSq)-(totalX*totalX)))
    return yInt

# Calculate MSE by average error calculated throughout data set
def getMSE(predict, real):
    totalLoss = 0
    for x in range(0, len(real)):
        totalLoss += (real[x]-(predict[x]))**2
    totalLoss = math.sqrt(totalLoss)/10
    return 1.0*(1.0/len(real))*totalLoss

# Find ideal weight values for data set
def findW(plant_num, newTemp, newLight):
    dataArray = QueryData.collectData(plant_num)
    waterVals = dataArray[0]
    colorVals = dataArray[1]
    tempVals = dataArray[2]
    lightVals = dataArray[3]
    correlations = []
    correlations.append(regression(waterVals, colorVals))
    correlations.append(regression(tempVals, colorVals))
    correlations.append(regression(lightVals, colorVals))
    mseArray = []
    wArray = []

    # Use correlations to find predicted value and calculate loss accordingly
    for x in range(0,len(waterVals)):
        w = random.randint(0,100)
        w = float(w)/10.0
        totalArr = []
        wArray.append(w)
        for x in range(int(len(colorVals))):
            total = correlations[0]*waterVals[x] + correlations[1]*tempVals[x] + correlations[2]*lightVals[x]
            totalArr.append(int(w*total))
        mseArray.append(round(getMSE(totalArr, colorVals)/10,2))

    # Utilize quadric regression to plot MSE values
    x = Symbol('x')
    A, B, C = np.polyfit(wArray, mseArray,2)
    y = A*x**2 + B*x + C
    yprime = str(y.diff(x))
    arr = yprime.split(' + ')
    if len(arr) == 1:
        arr = yprime.split(' - ')

    # Parse and convert output to find ideal weight based on loss calculation
    stra = str(arr[1])
    strb = str(arr[0][0:-2])
    converta = float(stra[0:10])
    convertb = float(strb[0:10])
    predictedW = float(converta)/(float(convertb))
    idealCol = GetIdealColor.idealColor()

    # Use weights to find theoretical predicted irrigation volume
    temporary = float(idealCol)/predictedW
    temporary -= (correlations[1]*newTemp + correlations[2]*newLight)
    theoreticalX = temporary/correlations[0]
    
    # Remove extreme irrigation volume changes
    if theoreticalX < 0:
        theoreticalX*=-1
    healthy = True
    if theoreticalX > 30:
        while theoreticalX > 7:
            theoreticalX-=1.1837513
            healthy = False
    if theoreticalX<2:
        while theoreticalX < 5:
            theoreticalX*=1.23754
            healthy = False  

    # Return theoretical irrigation volume and crop health status          
    return theoreticalX, healthy

if __name__ == "__main__":
    print(findW('1', 20, 20))