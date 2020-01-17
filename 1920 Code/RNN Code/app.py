from flask import Flask
from flask import request
import fullRNN
import getIrrigation
import random
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
            color = int(args["color"])
            plant_num = args["number"]
            fullRNN.getWater(plant_num, temp, light, color)
            return "success"
    else:
        return "return" + str(getIrrigation.getIrrigation('1'))
    


if __name__ == "__main__":
    app.run(debug=False, host='192.168.86.32', port=5000)