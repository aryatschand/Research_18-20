#!/usr/bin/python3
import timeit
import pymysql
import random

start = timeit.default_timer()
# Open database connection
db = pymysql.connect("localhost","root","arya123","plant_data_1920" )

# prepare a cursor object using cursor() method
cursor = db.cursor()

for x in range (0, 100):
   waterRand = random.randint(10, 20)
   colorRand = random.randint(40, 60)
   heatRand = random.randint(10, 30)
   lightRand = random.randint(20, 30)
   # Prepare SQL query to INSERT a record into the database.
   sql = "INSERT INTO `irrigation_data` (`id`,`water`,`color`,`temperature`, `light`) VALUES (NULL, '{}', '{}', '{}', '{}');" .format(waterRand, colorRand, heatRand, colorRand)
   try:
   # Execute the SQL command
      cursor.execute(sql)
   # Commit your changes in the database
      db.commit()
   except:
   # Rollback in case there is any error
      db.rollback()

   # disconnect from server
db.close()
stop = timeit.default_timer()
print('Time: ', stop - start)  
