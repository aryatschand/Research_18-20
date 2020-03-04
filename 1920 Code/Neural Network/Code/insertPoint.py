import pymysql
import random


# Function to insert new data point into SQL database
def insertPoint(plant_num, empirical, theoretical, color, heat, light, healthy, now):
   # Aggregate theoretical and empirical irrigation volumes
   water = round(min([theoretical, empirical]) * 0.67 + max([theoretical, empirical]) * 0.33,2)
   
   # Open authenticated database connection
   db = pymysql.connect("localhost","root","parWONE123","plant_data_1920" )
   cursor = db.cursor()

   # SQL query to insert new point into crop data database
   sql = "INSERT INTO `irrigation_data` (`id`, `plant_num`, `water`,`color`,`temperature`, `photoresistance`, `image`) VALUES (NULL, '{}', '{}', '{}', '{}', '{}', '{}');" .format(plant_num, water, color, heat, light, now)
   
   try:
   # Execute the SQL command
      cursor.execute(sql)

   # Commit changes in the database
      db.commit()

   except:
   # Rollback in case there is any error
      db.rollback()

   # SQL query to insert new point into micropiece commands database
   sql = ""
   if healthy == True:
      sql = "INSERT INTO `micropiece_commands` (`id`, `plant_num`, `water_volume`,`empirical`,`theoretical`, `notes`) VALUES (NULL, '{}', '{}', '{}', '{}', '{}');" .format(plant_num, water, round(empirical, 2), round(theoretical, 2), 'healthy')
   else:
      sql = "INSERT INTO `micropiece_commands` (`id`, `plant_num`, `water_volume`,`empirical`,`theoretical`, `notes`) VALUES (NULL, '{}', '{}', '{}', '{}', '{}');" .format(plant_num, water, round(empirical, 2), round(theoretical, 2), 'unhealthy')
   try:

   # Execute the SQL command
      cursor.execute(sql)

   # Commit your changes in the database
      db.commit()

   except:
   # Rollback in case there is any error
      print("error into micropiece")
      db.rollback()
   db.close()