import pymysql

def idealColor():

    db = pymysql.connect("localhost","root","parWONE123","plant_data" )

    # prepare a cursor object using cursor() method
    cursor = db.cursor()

    # Prepare SQL query to INSERT a record into the database.
    sql = "select avg(color) from plant_water_details where color > 0"
    try:
    # Execute the SQL command
        cursor.execute(sql)
    # Fetch all the rows in a list of lists.
        results = cursor.fetchall()
        return results[0][0]
    except:
        print("error")
    db.close()