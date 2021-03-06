#!/usr/bin/python3
import timeit
import pymysql
import random

start = timeit.default_timer()
# Open database connection
db = pymysql.connect("localhost","root","parWONE123","plant_data_1920" )

# prepare a cursor object using cursor() method
cursor = db.cursor()

sql = "drop table irrigation_data;"
try:
# Execute the SQL command
   cursor.execute(sql)
# Commit your changes in the database
   db.commit()
except:
# Rollback in case there is any error
   db.rollback()
sql = "drop table micropiece_commands;"
try:
# Execute the SQL command
   cursor.execute(sql)
# Commit your changes in the database
   db.commit()
except:
# Rollback in case there is any error
   db.rollback()
sql = "CREATE TABLE irrigation_data (id int not null auto_increment, plant_num int, water double, color int, temperature int, photoresistance int, primary key(id));"
try:
# Execute the SQL command
   cursor.execute(sql)
# Commit your changes in the database
   db.commit()
except:
# Rollback in case there is any error
   db.rollback()
sql = "CREATE TABLE micropiece_commands (id int not null auto_increment, plant_num int, water_volume double, empirical double, theoretical double, notes varchar(255), primary key(id));"
try:
# Execute the SQL command
   cursor.execute(sql)
# Commit your changes in the database
   db.commit()
except:
# Rollback in case there is any error
   db.rollback()
for x in range (0, 852):
   waterRand = random.randint(550, 650)
   waterRand = float(waterRand * 1.0)
   waterRand = float(waterRand/100.0)
   colorRand = random.randint(3200, 4500)*1.0
   colorRand = waterRand * float((colorRand*1.0)/1000.0)
   heatRand = random.randint(3000, 3250)*1.0
   heatRand = waterRand * float((heatRand*1.0)/1000.0)
   lightRand = random.randint(10000, 11500)*1.0
   lightRand = waterRand * float((lightRand*1.0)/1000.0)
   plant_num = x%12+1
   # Prepare SQL query to INSERT a record into the database.
   sql = "INSERT INTO `irrigation_data` (`id`, `plant_num`, `water`,`color`,`temperature`, `photoresistance`) VALUES (NULL, '{}', '{}', '{}', '{}', '{}');" .format(plant_num, waterRand, colorRand, heatRand, lightRand)
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
