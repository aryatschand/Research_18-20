 #!/usr/bin/python3

import pymysql
import timeit
import numpy as np
import matplotlib.pyplot as plt  # To visualize
import pandas as pd  # To read data
import math
import random
from sympy import *

# Open database connection
db = pymysql.connect("localhost","root","arya123","plant_data_1920" )

# prepare a cursor object using cursor() method
cursor = db.cursor()

# Prepare SQL query to INSERT a record into the database.
sql = "SELECT * FROM irrigation_data"
waterVals = []
colorVals = []
tempVals = []
lightVals = []
try:
   # Execute the SQL command
   cursor.execute(sql)
   # Fetch all the rows in a list of lists.
   results = cursor.fetchall()
   for x in range(0,len(results)):
      waterVals.append(results[x][1])
      colorVals.append(results[x][2])
      tempVals.append(results[x][3])
      lightVals.append(results[x][4])
except:
   print ("Error: unable to fetch data")

# disconnect from server
db.close()

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
answer = float(arr[1])/(float(arr[0][0:-2]))

print(answer)
