#!/usr/bin/python3
import timeit
import pymysql
import random

start = timeit.default_timer()
# Open database connection
db = pymysql.connect("localhost","root","parWONE123","plant_data")

# prepare a cursor object using cursor() method
cursor = db.cursor()
plantcount = 0
datetimecount = ""

for x in range (0, 2760):
   if plantcount < 12:
      plantcount+=1
   else:
      plantcount=1

   waterRand = random.randint(550, 650)
   waterRand = float(waterRand * 1.0)
   waterRand = float(waterRand/100.0)
   print(waterRand)


   color = random.randint(0, 2)
   newcolor = 0
   if color == 0:
      newcolor = 0
   else:
      newcolor = random.randint(18, 25)

   # Prepare SQL query to INSERT a record into the database.
   sql = "INSERT INTO `plant_water_details` (`plant_number`,`water_volume`,`color`) VALUES ('{}', '{}', '{}');" .format(plantcount, waterRand, newcolor)
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
