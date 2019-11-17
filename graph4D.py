
from mpl_toolkits.mplot3d import Axes3D
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
sql = "SELECT * FROM fourdimension"
waterVals = []
colorVals = []
heatVals = []
lightVals = []
try:
   # Execute the SQL command
   cursor.execute(sql)
   # Fetch all the rows in a list of lists.
   results = cursor.fetchall()
   for x in range(0,len(results)):
      waterVals.append(results[x][1])
      colorVals.append(results[x][2])
      heatVals.append(results[x][3])
      lightVals.append(results[x][4])
except:
   print ("Error: unable to fetch data")

# disconnect from server
db.close()

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

img = ax.scatter(waterVals, colorVals, heatVals, c=lightVals, cmap=plt.hot())
fig.colorbar(img)

plt.show()

stop = timeit.default_timer()
print('Time: ', stop - start)  