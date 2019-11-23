#!/usr/bin/python3
import timeit
import pymysql
import random

start = timeit.default_timer()
# Open database connection
db = pymysql.connect("localhost","root","arya123","plant_data_1920" )

# prepare a cursor object using cursor() method
cursor = db.cursor()

sql = "CREATE TABLE irrigation_data (id int not null auto_increment, water int, color int, temperature int, light int, primary key(id));"
try:
# Execute the SQL command
   cursor.execute(sql)
# Commit your changes in the database
   db.commit()
except:
# Rollback in case there is any error
   db.rollback()
db.close()
stop = timeit.default_timer()
print('Time: ', stop - start)  