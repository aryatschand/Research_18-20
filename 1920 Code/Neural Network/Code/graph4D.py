
from mpl_toolkits.mplot3d import Axes3D
import pymysql
import timeit
import numpy as np
import matplotlib.pyplot as plt  # To visualize
import pandas as pd  # To read data
import math

# Open database connection
start = timeit.default_timer()
db = pymysql.connect("localhost","root","parWONE123","plant_data_1920" )

# prepare a cursor object using cursor() method
cursor = db.cursor()

# Prepare SQL query to INSERT a record into the database.
sql = "SELECT * FROM irrigation_data"
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
      waterVals.append(results[x][2])
      
      colorVals.append(results[x][3])
      heatVals.append(results[x][4])
      lightVals.append(results[x][5])
except:
   print ("Error: unable to fetch data")

# disconnect from server
db.close()

print(waterVals)
print(colorVals)
print(heatVals)
print(lightVals)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

img = ax.scatter(waterVals, colorVals, heatVals, c=lightVals, cmap=plt.hot())
fig.colorbar(img)

plt.show()

stop = timeit.default_timer()
print('Time: ', stop - start)  