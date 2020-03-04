import pymysql

# Get relative location from drone from RFID ASCII string
def getLocation(num):

    # Open authenticated database connection
    db = pymysql.connect("localhost","root","parWONE123","plant_data_1920" )
    cursor = db.cursor()

    # SQL query to read information from database
    sql = "SELECT * FROM rfid_location where rfid_num = '" + str(num) + "';"
    plant = 0
    xLoc = 0
    yLoc = 0

    try:
    # Execute the SQL command
        cursor.execute(sql)

    # Fetch and save all the rows in a list of lists
        results = cursor.fetchall()
        for x in range(0,len(results)):
            plant = results[x][2]
            xLoc = results[x][3]
            yLoc = results[x][4]
    except:
        print("error")
    db.close()

    # Return plant number and XY location
    return plant, xLoc, yLoc

# Test known tag
if __name__ == "__main__":
    print(getLocation(1001742768328))