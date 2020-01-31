from flask import Flask
from flask import request
import fullRNN
import getIrrigation
import random
import base64
import imgAnalyze
import getCommands
import updateDrone
from datetime import datetime

app = Flask(__name__)

@app.route("/")

def home():

    args = request.args
    if len(args) >= 1:
        if args["usage"] == "irrigate":
            plant_num = args["number"]
            return str(getIrrigation.getIrrigation(plant_num))
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
            color = int(imgAnalyze.color(str(now)))
            color = 20
            plant_num = args["number"]
            fullRNN.getWater(plant_num, temp, light, color, str(now))
            updateDrone.updateDrone(0, plant_num)
            return "success"
        elif args["usage"] == "demo":
            img_data = str(args["image"])
            img_data = img_data.replace(" ", "+")
            if img_data[0] == 'b':
                img_data = img_data[2:len(img_data)-1]
            with open("Images/LiveFeed.png", "wb") as fh:
                fh.write(base64.decodebytes(img_data.encode()))
            demo, location = getCommands.getCommands()
            updateDrone.updateDrone(0, str(location))
            if str(demo) == "0":
                return "No Demo"
            else:
                return "Demo"
        elif args["usage"] == "giveDemo":
            updateDrone.updateDrone(1, '1-12')
            return "done"

    else:
        return "return" + str(getIrrigation.getIrrigation('1'))
    


if __name__ == "__main__":
    app.run(debug=False, host='192.168.86.27', port=5000)