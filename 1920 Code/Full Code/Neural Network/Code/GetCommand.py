import pymysql

# Get parameters of command to send to drone
def getCommands():

    # Open authenticated database connection
    db = pymysql.connect("localhost","root","parWONE123","plant_data_1920" )
    cursor = db.cursor()

    # SQL query to read information from database
    sql = "SELECT * FROM drone"
    returnArray = [[]]
    for x in range(0,2):
        returnArray.append([])

    try:
    # Execute the SQL command
        cursor.execute(sql)

    # Fetch and save all the rows in a list of lists
        results = cursor.fetchall()
        for x in range(0,len(results)):
            returnArray[0].append(results[x][1]) 
            returnArray[1].append(results[x][2])
    except:
        print("error")
    db.close()

    # Return commands to send over LAN
    return returnArray[0][-1], returnArray[1][-1]

if __name__ == "__main__":
    print(getCommands())