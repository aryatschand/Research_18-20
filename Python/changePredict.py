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

def changePredict(collectedColor, idealColor):
    dataArray = collectData.collectData()
    waterVals = dataArray[0]
    colorVals = dataArray[1]

    difference = 1-(1.0*collectedColor/idealColor)
    newWater = 0

    if difference > 0.05:
        slope = regression(waterVals, colorVals)
        addAmt = slope * abs(collectedColor - idealColor)
        lastWater = colorVals[-1]
        newWater = lastWater + addAmt
    elif difference < -0.05:
        slope = regression(waterVals, colorVals)
        addAmt = slope * abs(collectedColor - idealColor)
        lastWater = colorVals[-1]
        newWater = lastWater - addAmt
    return newWater