#!/usr/bin/python3

import pymysql
import timeit
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math

# Open authenticated database connection
start = timeit.default_timer()
db = pymysql.connect("localhost","root","parWONE123","plant_data_1920" )
cursor = db.cursor()

# SQL query to read information from database
sql = "SELECT * FROM irrigation_data"
waterVals = []
colorVals = []

try:
   # Execute the SQL command
   cursor.execute(sql)

   # Fetch and save all the rows in a list of lists
   results = cursor.fetchall()
   for x in range(0,len(results)):
      waterVals.append(results[x][1])
      colorVals.append(results[x][2])
except:
   print ("Error: unable to fetch data")

db.close()

# Initialize empty variables
totalWater = 0
totalWaterSq = 0
totalColor = 0
totalMult = 0
count = len(waterVals)

# Find linear slope by running through each element of data and plugging into formula
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

# Find logarithmic slope by running through each element of data and plugging into formula
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
count = len(waterVals)

# Find linear y-intercept by running through each element of data and plugging into formula
for x in range(0, len(waterVals)):
   totalXSq+=(waterVals[x]*waterVals[x])
   totalX+=waterVals[x]
   totalY+=colorVals[x]
   totalMult+=(colorVals[x]*waterVals[x])
yInt = ((totalY*totalXSq)-(totalX*totalMult))/((count*totalXSq)-(totalX*totalX))

# Prepare scatter plot and linear function graph
plt.scatter(waterVals, colorVals)
x = np.array(range(10, 40))  
y = yInt+x*Linslope
plt.plot(x, y)  
plt.title('Graph')
plt.xlabel('x')
plt.ylabel('y')

# Show graph
plt.show()

stop = timeit.default_timer()
print('Time: ', stop - start)  