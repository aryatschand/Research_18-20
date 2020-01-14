import pymysql

def collectData():

    db = pymysql.connect("localhost","root","parWONE123","plant_data_1920" )

    # prepare a cursor object using cursor() method
    cursor = db.cursor()

    # Prepare SQL query to INSERT a record into the database.
    sql = "SELECT * FROM irrigation_data"
    returnArray = [[]]
    for x in range(0,3):
        returnArray.append([])
    try:
    # Execute the SQL command
        cursor.execute(sql)
    # Fetch all the rows in a list of lists.
        results = cursor.fetchall()
        for x in range(0,len(results)):
            returnArray[0].append(results[x][1]) #water
            returnArray[1].append(results[x][2]) #color
            returnArray[2].append(results[x][3]) #temp
            returnArray[3].append(results[x][4]) #light
    # disconnect from server
    except:
        print("error")
    db.close()
    print(returnArray)
    return returnArray

if __name__ == "__main__":
    collectData()