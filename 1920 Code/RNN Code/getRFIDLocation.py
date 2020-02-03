import pymysql

def getLocation(num):

    db = pymysql.connect("localhost","root","parWONE123","plant_data_1920" )

    # prepare a cursor object using cursor() method
    cursor = db.cursor()

    # Prepare SQL query to INSERT a record into the database.
    sql = "SELECT * FROM rfid_location where rfid_num = '" + str(num) + "';"
    plant = 0
    xLoc = 0
    yLoc = 0
    try:
    # Execute the SQL command
        cursor.execute(sql)
    # Fetch all the rows in a list of lists.
        results = cursor.fetchall()
        for x in range(0,len(results)):
            plant = results[x][2]
            xLoc = results[x][3]
            yLoc = results[x][4]
    # disconnect from server
    except:
        print("error")
    db.close()
    return plant, xLoc, yLoc

if __name__ == "__main__":
    print(getLocation(1001742768328))