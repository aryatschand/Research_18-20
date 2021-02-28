import pymysql
import timeit
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math

# Open authenticated database connection
db = pymysql.connect("localhost","root","parWONE123","plant_data_1920" )
cursor = db.cursor()

# SQL query to read information from database
sql = "SELECT * FROM irrigation_data"
waterVals = []
colorVals = []
tempVals = []
lightVals = []

try:
   # Execute the SQL command
   cursor.execute(sql)

   # Fetch all the rows in a list of lists
   results = cursor.fetchall()
   for x in range(0,len(results)):
      waterVals.append(results[x][1])
      colorVals.append(results[x][2])
      tempVals.append(results[x][3])
      lightVals.append(results[x][4])
except:
   print ("Error: unable to fetch data")

db.close()

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

# 2 variable linear regression, return y-intercept
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

# Execute regression functions
Linslope = regression(waterVals, colorVals)
yInt = intercept(waterVals, colorVals)

# Calculate loss using base error function
totalLoss = 0
for x in range(0, len(waterVals)):
    totalLoss += (colorVals[x]-(yInt+waterVals[x]*Linslope))**2

# MSE equals the average error in data set
MSE = (1/len(waterVals))*totalLoss

# Plot data and regression on 2D grid for visualization
plt.scatter(waterVals, colorVals)
x = np.array(range(10, 40))  
y = yInt+x*Linslope
plt.plot(x, y)  
plt.title('Scatter')
plt.xlabel('x')
plt.ylabel('y')
plt.show()