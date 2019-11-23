#!/usr/bin/python3
import pymysql
import random

def insertPoint(water, color, heat, light):
   # Open database connection
   db = pymysql.connect("localhost","root","arya123","plant_data_1920" )

   # prepare a cursor object using cursor() method
   cursor = db.cursor()

   for x in range (0, 100):
      # Prepare SQL query to INSERT a record into the database.
      sql = "INSERT INTO `irrigation_data` (`id`,`water`,`color`,`heat`, `light`) VALUES (NULL, '{}', '{}', '{}', '{}');" .format(water, color, heat, light)
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
