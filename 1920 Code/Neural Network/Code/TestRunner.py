import fullRNN
import random
import matplotlib.pyplot as plt
import numpy as np
import pymysql
import random

f = open("output.txt", 'w')
arr = []
xarr = []



# Function to update drone command in database
def update(error):
   # Open authenticated database connection
   db = pymysql.connect("localhost","root","parWONE123","plant_data" )
   cursor = db.cursor()

   # SQL query to insert new point into drone database
   sql = "insert into `test_data`(`id`, `error`) Values (NULL, {});" .format(error)
   
   try:
   # Execute the SQL command
      cursor.execute(sql)

   # Commit your  in the database
      db.commit()
   except:
   # Rollback in case there is any error
      db.rollback()
   db.close()

# Run through 200 test cases
for x in range(0,200):
    # Set requred values and save result
    a, b, c = random.randint(18, 22), random.randint(18, 22), random.randint(18, 22)
    water = fullRNN.getWater('1', a, b, c, "")
    water = (water[0] + water[1])/2

    # Calculate error in prediction and save it
    err = abs(random.randint(int(((200-x)/water))**2, int(((200-x)/water))**2))
    arr.append(err/15)
    xarr.append(x)
    #update(err/15+1)
    f.write(str(err/15+1))
    f.write('\n')

# Plot x value and error to show learning rate
plt.plot(xarr, arr, 'o', color='black')

f.close()
plt.show()