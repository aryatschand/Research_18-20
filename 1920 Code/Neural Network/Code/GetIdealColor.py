import pymysql

# Get ideal color from 1819 data set
def idealColor():

    # Open authenticated database connection
    db = pymysql.connect("localhost","root","parWONE123","plant_data" )
    cursor = db.cursor()

    # SQL query to find average value in color column from database
    sql = "select avg(color) from plant_water_details where color > 0"
    
    try:
    # Execute the SQL command
        cursor.execute(sql)

    # Fetch and return desired rows in a list of lists
        results = cursor.fetchall()
        return results[0][0]
    except:
        print("error")
    db.close()

if __name__ == "__main__":
    print(idealColor())