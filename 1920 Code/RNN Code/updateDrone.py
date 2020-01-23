#!/usr/bin/python3
import pymysql
import random

def updateDrone(demo, location):
   # Open database connection
   db = pymysql.connect("localhost","root","parWONE123","plant_data_1920" )

   # prepare a cursor object using cursor() method
   cursor = db.cursor()
   # Prepare SQL query to INSERT a record into the database.
   sql = "insert into `drone`(`id`, `demo`, `nextLocation`) Values (NULL, {}, '{}');" .format(demo, location)
   print(sql)
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
