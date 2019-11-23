#!/usr/bin/python3

import pymysql
import timeit
import numpy as np
import matplotlib.pyplot as plt  # To visualize
import pandas as pd  # To read data
import math

# Open database connection
start = timeit.default_timer()
db = pymysql.connect("localhost","root","arya123","pythonTest" )

# prepare a cursor object using cursor() method
cursor = db.cursor()

# Prepare SQL query to INSERT a record into the database.
sql = "SELECT * FROM irrigation"
waterVals = []
colorVals = []
try:
   # Execute the SQL command
   cursor.execute(sql)
   # Fetch all the rows in a list of lists.
   results = cursor.fetchall()
   for x in range(0,len(results)):
      waterVals.append(results[x][1])
      colorVals.append(results[x][2])
except:
   print ("Error: unable to fetch data")

# disconnect from server
db.close()

totalWater = 0
totalWaterSq = 0
totalColor = 0
totalMult = 0
count = len(waterVals)

for x in range(0, len(waterVals)):
   totalWaterSq+=(waterVals[x]*waterVals[x])
   totalWater+=waterVals[x]
   totalColor+=colorVals[x]
   totalMult+=(colorVals[x]*waterVals[x])
Linslope = ((count*totalMult)-(totalColor*totalWater))/((count*totalWaterSq)-(totalWater*totalWater))
print("Linear Slope = " + str(Linslope))
yLogx = 0
sumY = 0
sumLogx = 0
sumLogxSq = 0

for x in range(0, 3):
    yLogx += colorVals[x] * math.log(waterVals[x])
    sumY += colorVals[x]
    sumLogx += math.log(waterVals[x])
    sumLogxSq += (math.log(waterVals[x]) * math.log(waterVals[x]))

Logslope = ((3*yLogx)-(sumY*sumLogx))/((3*sumLogxSq)-(sumLogx*sumLogx))
print("Logarithmic Slope = " + str(Logslope))

totalX = 0
totalXSq = 0
totalY = 0
totalMult = 0
count = len(xVals)

for x in range(0, len(xVals)):
   totalXSq+=(waterVals[x]*waterVals[x])
   totalX+=waterVals[x]
   totalY+=colorVals[x]
   totalMult+=(colorVals[x]*waterVals[x])
yInt = ((totalY*totalXSq)-(totalX*totalMult))/((count*totalXSq)-(totalX*totalX))

plt.scatter(waterVals, colorVals)
x = np.array(range(10, 40))  
y = yInt+x*Linslope
plt.plot(x, y)  
plt.show()
plt.title('Graph')
plt.xlabel('x')
plt.ylabel('y')

plt.show()

stop = timeit.default_timer()
print('Time: ', stop - start)  