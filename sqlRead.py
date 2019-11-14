#!/usr/bin/python3

import pymysql
import timeit

# Open database connection
start = timeit.default_timer()
db = pymysql.connect("localhost","root","arya123","pythonTest" )

# prepare a cursor object using cursor() method
cursor = db.cursor()

# Prepare SQL query to INSERT a record into the database.
sql = "SELECT * FROM potluck"
try:
   # Execute the SQL command
   cursor.execute(sql)
   # Fetch all the rows in a list of lists.
   results = cursor.fetchall()
   for x in range(0,len(results)):
      print("id={}, name={}, food={}, confirm={}, data={}".format(results[x][0], results[x][1], results[x][2], results[x][3], results[x][4]))
except:
   print ("Error: unable to fetch data")

# disconnect from server
db.close()
stop = timeit.default_timer()
print('Time: ', stop - start)  