from flask import Flask
from flask import request
import formatData
import getIrrigation
import random
import base64
import AnalyzeImage
import GetCommand
import updateDrone
import getRFIDLocation
import modelRun
from datetime import datetime

app = Flask(__name__)

@app.route("/")

# Main function
def home():
    # Take parameters from request
    args = request.args
    if len(args) >= 1:
        # Request from micropiece, return irrigation volume
        if args["usage"] == "irrigate":
            plant_num = args["number"]
            return str(getIrrigation.getIrrigation(plant_num))
        
        # Request from drone containing data points as parameters
        elif args["usage"] == "newpoint":
            temp = int(args["temp"])
            light = int(args["light"])
            img_data = str(args["image"])
            img_data = img_data.replace(" ", "+")
            if img_data[0] == 'b':
                img_data = img_data[2:len(img_data)-1]
            now = datetime.now()

            # Decode Base64 image for analysis
            with open("Images/" + str(now) + ".png", "wb") as fh:
                fh.write(base64.decodebytes(img_data.encode()))
            #color = int(AnalyzeImage.color(str(now)))
            color = 20
            plant_num = args["number"]
            model = modelRun.build_model()
            model.test(formatData.getWater(plant_num, temp, light, color, str(now)))
            updateDrone.updateDrone(0, plant_num)
            return "success"

        # From drone asking if a demo is requested from user
        elif args["usage"] == "demo":
            img_data = str(args["image"])
            img_data = img_data.replace(" ", "+")
            if img_data[0] == 'b':
                img_data = img_data[2:len(img_data)-1]
            with open("Images/LiveFeed.png", "wb") as fh:
                fh.write(base64.decodebytes(img_data.encode()))
            demo, location = GetCommand.getCommands()
            updateDrone.updateDrone(0, str(location))
            if str(demo) == "0":
                return "No Demo"
            else:
                return "Demo"

        # From iOS app instructing drone to collect point and micropiece update
        elif args["usage"] == "giveDemo":
            updateDrone.updateDrone(1, '1-12')
            return "done"

        # From drone with RFID ASCII string as parameter, return relative locaiton
        elif args["usage"] == "rfid":
            tag = args["tag"]
            plant_num, xLoc, yLoc = getRFIDLocation.getLocation(str(tag))
            return str(plant_num) + "," + str(xLoc) + "," + str(yLoc)
    else:
        return "return" + str(getIrrigation.getIrrigation('1'))
    
# Run server on local IP address on port 5000
if __name__ == "__main__":
    app.run(debug=False, host='192.168.86.27', port=5000)