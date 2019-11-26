 #!/usr/bin/python3

import pymysql
import timeit
import numpy as np
import matplotlib.pyplot as plt  # To visualize
import pandas as pd  # To read data
import math
import random
from sympy import *
import insertPoint
import collectData
import idealColor
import sys

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
    Linslope = ((count*totalMult)-(totalY*totalX))/((count*totalXSq)-(totalX*totalX))
    return Linslope

def intercept(xVals, yVals):
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
    yInt = ((totalY*totalXSq)-(totalX*totalMult))/((count*totalXSq)-(totalX*totalX))
    return yInt

def getMSE(predict, real):
    totalLoss = 0
    for x in range(0, len(real)):
        totalLoss += (real[x]-(predict[x]))**2
    return (1/len(real))*totalLoss

def findW(newTemp, newLight):
    dataArray = collectData.collectData()
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
    for x in range(0,3):
        w = random.randint(0,100)
        w = float(w)/10.0
        totalArr = []
        wArray.append(w)
        for x in range(int(len(colorVals))):
            total = correlations[0]*waterVals[x] + correlations[1]*tempVals[x] + correlations[2]*lightVals[x]
            totalArr.append(int(w*total))
        mseArray.append(round(getMSE(totalArr, colorVals)/10,2))

    x = Symbol('x')
    A, B, C = np.polyfit(wArray, mseArray,2)
    y = A*x**2 + B*x + C
    yprime = str(y.diff(x))
    arr = yprime.split(' + ')
    if len(arr) == 1:
        arr = yprime.split(' - ')
    predictedW = float(arr[1])/(float(arr[0][0:-2]))
    idealCol = idealColor.idealColor()
    temporary = float(idealCol)/predictedW
    temporary -= (correlations[1]*newTemp + correlations[2]*newLight)
    if temporary < 0:
        temporary*=-1
    theoreticalX = temporary/correlations[0]

    return theoreticalX