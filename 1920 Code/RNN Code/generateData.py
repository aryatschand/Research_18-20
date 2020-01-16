#!/usr/bin/python3
import timeit
import pymysql
import random

start = timeit.default_timer()
# Open database connection
db = pymysql.connect("localhost","root","parWONE123","plant_data_1920" )

# prepare a cursor object using cursor() method
cursor = db.cursor()

for x in range (0, 852):
   waterRand = random.randint(550, 650)
   waterRand = float(waterRand * 1.0)
   waterRand = float(waterRand/100.0)
   colorRand = random.randint(18, 22)
   heatRand = random.randint(18, 25)
   lightRand = random.randint(20, 30)
   plant_num = x%12+1
   # Prepare SQL query to INSERT a record into the database.
   sql = "INSERT INTO `irrigation_data` (`id`, `plant_num`, `water`,`color`,`temperature`, `photoresistance`) VALUES (NULL, '{}', '{}', '{}', '{}', '{}');" .format(plant_num, waterRand, colorRand, heatRand, colorRand)
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
