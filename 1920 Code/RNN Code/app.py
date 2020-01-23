from flask import Flask
from flask import request
import fullRNN
import getIrrigation
import random
import base64
import imgAnalyze

app = Flask(__name__)

@app.route("/")

def home():
    args = request.args
    if len(args) > 1:
        if args["usage"] == "irrigate":
            plant_num = args["number"]
            return str(getIrrigation.getIrrigation(plant_num))
        elif args["usage"] == "newpoint":
            temp = int(args["temp"])
            light = int(args["light"])
            img_data = str(args["image"])
            img_data = img_data.replace(" ", "+")
            img_data = img_data[2:len(img_data)-1]
            with open("imageToSave.png", "wb") as fh:
                fh.write(base64.decodebytes(img_data.encode()))
            color = int(imgAnalyze.color())
            plant_num = args["number"]
            print(plant_num, temp, light, color)
            fullRNN.getWater(plant_num, temp, light, color)
            return "success"
    else:
        return "return" + str(getIrrigation.getIrrigation('1'))
    


if __name__ == "__main__":
    app.run(debug=False, host='192.168.86.41', port=5000)