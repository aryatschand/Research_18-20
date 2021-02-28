import pymysql
import random

# Function to update drone command in database
def updateDrone(demo, location):
   # Open authenticated database connection
   db = pymysql.connect("localhost","root","parWONE123","plant_data_1920" )
   cursor = db.cursor()

   # SQL query to insert new point into drone database
   sql = "insert into `drone`(`id`, `demo`, `nextLocation`) Values (NULL, {}, '{}');" .format(demo, location)
   
   try:
   # Execute the SQL command
      cursor.execute(sql)

   # Commit your  in the database
      db.commit()
   except:
   # Rollback in case there is any error
      db.rollback()
   db.close()
