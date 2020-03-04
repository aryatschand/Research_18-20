from flask import Flask
from flask import request
import FullRNN
import GetIrrigation
import random
import base64
import AnalyzeImage
import GetCommand
import UpdateDrone
import GetRFIDLocation
from datetime import datetime

app = Flask(__name__)

@app.route("/")

def home():

    args = request.args
    if len(args) >= 1:
        if args["usage"] == "irrigate":
            plant_num = args["number"]
            return str(GetIrrigation.getIrrigation(plant_num))
        elif args["usage"] == "newpoint":
            temp = int(args["temp"])
            light = int(args["light"])
            img_data = str(args["image"])
            img_data = img_data.replace(" ", "+")
            if img_data[0] == 'b':
                img_data = img_data[2:len(img_data)-1]
            now = datetime.now()
            with open("Images/" + str(now) + ".png", "wb") as fh:
                fh.write(base64.decodebytes(img_data.encode()))
            color = int(AnalyzeImage.color(str(now)))
            color = 20
            plant_num = args["number"]
            FullRNN.getWater(plant_num, temp, light, color, str(now))
            UpdateDrone.updateDrone(0, plant_num)
            return "success"
        elif args["usage"] == "demo":
            img_data = str(args["image"])
            img_data = img_data.replace(" ", "+")
            if img_data[0] == 'b':
                img_data = img_data[2:len(img_data)-1]
            with open("Images/LiveFeed.png", "wb") as fh:
                fh.write(base64.decodebytes(img_data.encode()))
            demo, location = GetCommand.getCommands()
            UpdateDrone.updateDrone(0, str(location))
            if str(demo) == "0":
                return "No Demo"
            else:
                return "Demo"
        elif args["usage"] == "giveDemo":
            UpdateDrone.updateDrone(1, '1-12')
            return "done"
        elif args["usage"] == "rfid":
            tag = args["tag"]
            plant_num, xLoc, yLoc = GetRFIDLocation.getLocation(str(tag))
            return str(plant_num) + "," + str(xLoc) + "," + str(yLoc)
    else:
        return "return" + str(GetIrrigation.getIrrigation('1'))
    


if __name__ == "__main__":
    app.run(debug=False, host='192.168.86.32', port=5000)