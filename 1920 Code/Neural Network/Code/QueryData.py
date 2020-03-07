import pymysql

# Function to return full data set as 2D array
def collectData(plant_num):

    # Open authenticated database connection
    db = pymysql.connect("localhost","root","parWONE123","plant_data_1920" )
    cursor = db.cursor()
    plant_num = str(plant_num)

    # SQL query to read information from database
    sql = "SELECT * FROM irrigation_data where plant_num=" + plant_num
    returnArray = [[]]
    for x in range(0,3):
        returnArray.append([])

    try:
    # Execute the SQL command
        cursor.execute(sql)
        
    # Fetch and save all the rows in a list of lists
        results = cursor.fetchall()
        for x in range(0,len(results)):
            returnArray[0].append(results[x][2])
            returnArray[1].append(results[x][3])
            returnArray[2].append(results[x][4])
            returnArray[3].append(results[x][5])
    except:
        print("error")
    db.close()
    return returnArray

if __name__ == "__main__":
    print(collectData('1'))