#!/usr/bin/python3
import timeit
import pymysql

start = timeit.default_timer()
# Open database connection
db = pymysql.connect("localhost","root","arya123","pythonTest" )

# prepare a cursor object using cursor() method
cursor = db.cursor()

# Prepare SQL query to INSERT a record into the database.
sql = """INSERT INTO `potluck` (`id`,`name`,`food`,`confirmed`,`signup_date`) VALUES (NULL, "Arjun", "Pasta","Y", '2012-02-12');"""
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
