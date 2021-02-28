import pymysql

# Get irrigation volume for micropiece adjustment
def getIrrigation(plant_num):

    # Open authenticated database connection
    db = pymysql.connect("localhost","root","parWONE123","plant_data_1920" )
    cursor = db.cursor()
    plant_num = str(plant_num)

    # SQL query to read information from database
    sql = "SELECT * FROM micropiece_commands where plant_num=" + plant_num
    
    try:
        # Execute the SQL command
        cursor.execute(sql)

        # Fetch and return desired row in a list of lists
        results = cursor.fetchall()
        return results[-1][2]
    except:
        print("error")
    db.close()

    # Return notification if there is any error
    return "error"

if __name__ == "__main__":
    print(getIrrigation('1'))