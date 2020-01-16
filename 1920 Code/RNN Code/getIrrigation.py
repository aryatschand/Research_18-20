import pymysql

def getIrrigation(plant_num):

    db = pymysql.connect("localhost","root","parWONE123","plant_data_1920" )

    # prepare a cursor object using cursor() method
    cursor = db.cursor()
    plant_num = str(plant_num)

    # Prepare SQL query to INSERT a record into the database.
    sql = "SELECT * FROM micropiece_commands where plant_num=" + plant_num
    try:
    # Execute the SQL command
        cursor.execute(sql)
    # Fetch all the rows in a list of lists.
        results = cursor.fetchall()
        return results[-1][2]
    # disconnect from server
    except:
        print("error")
    db.close()
    return "error"

if __name__ == "__main__":
    print(getIrrigation('1'))