import os
import base64
import requests
import RPi.GPIO as GPIO
import time
import sys
import Adafruit_DHT

temp=20
sensor = Adafruit_DHT.DHT11
DHT11_pin = 18

humidity, temperature = Adafruit_DHT.read_retry(sensor, DHT11_pin)
if humidity is not None:
    temp = int(temperature)

light=20
mpin=17
tpin=27
GPIO.setmode(GPIO.BCM)
cap=0.000001
adj=2.130620985
i=0
t=0
GPIO.setup(mpin, GPIO.OUT)
GPIO.setup(tpin, GPIO.OUT)
GPIO.output(mpin, False)
GPIO.output(tpin, False)
time.sleep(0.2)
GPIO.setup(mpin, GPIO.IN)
time.sleep(0.2)
GPIO.output(tpin, True)
starttime=time.time()
endtime=time.time()
measureresistance=endtime-starttime
    
res=(measureresistance/cap)*adj
i=i+1
t=t+res
if i==10:
    t=t/i
    light=int(t)
    i=0
    t=0
print(temp,light)

stream = os.popen('fswebcam /home/pi/test/Images/image.jpg')
output = stream.read()
mystring = ""

with open("/home/pi/test/Images/image.jpg", "rb") as img_file:
    my_string = base64.b64encode(img_file.read())
    
querystring = "http://192.168.86.34:5000/?usage=newpoint&image="
querystring+= str(my_string)
querystring+="&light="
querystring+=str(light)
querystring+="&temp="
querystring+=str(temp)
querystring+="&number=1"

response = requests.get(querystring)
print(response.text)



