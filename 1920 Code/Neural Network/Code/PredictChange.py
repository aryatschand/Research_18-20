import pymysql
import timeit
import numpy as np
import matplotlib.pyplot as plt  # To visualize
import pandas as pd  # To read data
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
    Linslope = ((count*totalMult)-(totalY*totalX))/((count*totalXSq)-(totalX*totalX))
    return Linslope

# Calculate empirical predicted irrigation volume based on significant changes
def changePredict(plant_num, collectedColor, idealColor):
    # Save the full data set to a 2D list
    dataArray = QueryData.collectData(plant_num)
    waterVals = dataArray[0]
    colorVals = dataArray[1]

    # Find the difference between the ideal and collected color
    difference = 1-(1.0*collectedColor/idealColor)
    newWater = waterVals[-1]

    # If the difference is significant in either direction, update based on correlation
    if difference > 0.05:
        slope = abs(regression(waterVals, colorVals))
        addAmt = slope * abs(collectedColor - idealColor)
        lastWater = waterVals[-1]
        newWater = lastWater + addAmt
    elif difference < -0.05:
        slope = abs(regression(waterVals, colorVals))
        addAmt = slope * abs(collectedColor - idealColor)
        lastWater = waterVals[-1]
        newWater = lastWater - addAmt
    healthy = True

    # Remove extreme irrigation volume changes
    if newWater > 30:
        while newWater > 7:
            newWater-=1.1837513
            healthy = False
    if newWater<2:
        while newWater < 5:
            newWater+=0.391
            healthy = False
    return newWater, healthy

if __name__ == "__main__":
    changePredict('1', 20, 21.49)