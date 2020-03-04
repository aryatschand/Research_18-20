import pymysql
import timeit
import numpy as np
import matplotlib.pyplot as plt  # To visualize
import pandas as pd  # To read data
import math
import random
from sympy import *
import InsertPoint
import QueryData
import GetIdealColor
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

def changePredict(plant_num, collectedColor, idealColor):
    dataArray = QueryData.collectData(plant_num)
    waterVals = dataArray[0]
    colorVals = dataArray[1]
    difference = 1-(1.0*collectedColor/idealColor)
    newWater = waterVals[-1]
    print(newWater)
    if difference > 0.05:
        slope = abs(regression(waterVals, colorVals))
        addAmt = slope * abs(collectedColor - idealColor)
        print(addAmt)
        lastWater = waterVals[-1]
        newWater = lastWater + addAmt
    elif difference < -0.05:
        slope = abs(regression(waterVals, colorVals))
        addAmt = slope * abs(collectedColor - idealColor)
        lastWater = waterVals[-1]
        newWater = lastWater - addAmt
    healthy = True
    if newWater > 30:
        while newWater > 7:
            newWater-=1.1837513
            healthy = False
            print("change1")
    if newWater<2:
        while newWater < 5:
            newWater+=0.391
            healthy = False
            print("change2")
    return newWater, healthy

if __name__ == "__main__":
    changePredict('1', 20, 21.49)