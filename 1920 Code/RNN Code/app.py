from flask import Flask
from flask import request
import fullRNN
app = Flask(__name__)

@app.route("/")

def home():
    args = request.args
    print(args)
    temp = int(args["temp"])
    light = int(args["light"])
    color = int(args["color"])
    value = fullRNN.getWater(temp, light, color)
    return str(value)

if __name__ == "__main__":
    app.run(debug=False, host='192.168.86.34', port=5000)