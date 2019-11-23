 #!/usr/bin/python3

import pymysql
import timeit
import numpy as np
import matplotlib.pyplot as plt  # To visualize
import pandas as pd  # To read data
import math

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

Linslope = regression(waterVals, colorVals)
yInt = intercept(waterVals, colorVals)

totalLoss = 0
for x in range(0, len(waterVals)):
    totalLoss += (colorVals[x]-(yInt+waterVals[x]*Linslope))**2

MSE = (1/len(waterVals))*totalLoss
print(MSE)

plt.scatter(waterVals, colorVals)
x = np.array(range(10, 40))  
y = yInt+x*Linslope
plt.plot(x, y)  
plt.title('Scatter')
plt.xlabel('x')
plt.ylabel('y')

plt.show()