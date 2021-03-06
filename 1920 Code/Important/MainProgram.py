import os
import base64
import requests
import RPi.GPIO as GPIO
import Adafruit_CharLCD as LCD
from mfrc522 import SimpleMFRC522
import time
import sys
import Adafruit_DHT
import sys

# Get server IP as command line parameter
ip = sys.argv[1]

# Set GPIO pins of 16x2 LCD
lcd_rs = 16
lcd_en = 24
lcd_d4 = 23
lcd_d5 = 21
lcd_d6 = 20
lcd_d7 = 22
lcd_backlight = 2

lcd_columns = 16
lcd_rows = 2

# Initialize variables for RFID reader
rfid = ""
reader = SimpleMFRC522()

# Initialize LCD
lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows, lcd_backlight)

plant_num = ""
xLocation = ""
yLocation = ""

# Repeat on loop
while True:
    time.sleep(1.0)
    lcd.clear()
    lcd.message('Capturing\nImage')

    # Shell command to capture image from webcam and save to directory
    stream1 = os.popen('fswebcam /home/pi/test/Images/image.jpg')
    output1 = stream1.read()
    mystring1 = ""
    lcd.clear()
    lcd.message('Converting\nTo B64')
    
    # Open captured image and encode to base64
    with open("/home/pi/test/Images/image.jpg", "rb") as img_file1:
        my_string1 = base64.b64encode(img_file1.read())
    
    # Send base64 string to server as parameter
    response = requests.get("http://"+ ip + ":5000/?usage=demo&image=" + str(my_string1))
    time.sleep(1.0)
    lcd.clear()
    lcd.message('Response:\n' + response.text)
    
    # If the drone should run demo program
    if response.text == "Demo":
        lcd.clear()
        lcd.message('Finding\nRFID Tag')
        
        # Read for RFID tags until one is found
        while (rfid == ""):
            try:
                id, text = reader.read()
            finally:
                rfid = str(id)  
        time.sleep(0.2)

        # Send RFID number to server to get relative location
        querystring = "http://"+ ip + ":5000/?usage=rfid&tag="
        querystring+= str(rfid)

        # Parse response to extract plant number and relative location
        response = requests.get(querystring)
        response = response.text.split(",")
        plant_num = response[0]
        xLocation = response[1]
        yLocation = response[2]
        
        lcd.clear()
        lcd.message('Tag Number\n' + str(id))
        time.sleep(1.0)

        lcd.clear()
        lcd.message('X Coord: ' + str(xLocation) + '\nY Coord: ' + str(yLocation))
        time.sleep(1.0)

        lcd.clear()
        lcd.message('Measuring\nTemperature')
        
        # Set temperature sensor variables and GPIO pins
        temp=20
        sensor = Adafruit_DHT.DHT11
        DHT11_pin = 18

        # Read temperature and humidity from sensor
        humidity, temperature = Adafruit_DHT.read_retry(sensor, DHT11_pin)
        if humidity is not None:
            temp = int(temperature)
        lcd.clear()
        lcd.message('Measuring\nLight')
        
        # Set photoresistor variables and GPIO pins
        light=20
        mpin=17
        tpin=27
        GPIO.setmode(GPIO.BCM)
        cap=0.000001
        adj=2.130620985
        i=0
        t=0
        
        # Run until light value is collected
        while light == 20:
            # Set up sensor
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
            
            # Run until the sensor value is minimum
            while (GPIO.input(mpin) == GPIO.LOW):
                endtime=time.time()

            # The measured resistance is the time for function
            measureresistance=endtime-starttime
            
            # Format resistance
            res=(measureresistance/cap)*adj
            i=i+1
            t=t+res
            if i==10:
                t=t/i
                light = int(t)
                i=0
                t=0
        
        lcd.clear()
        lcd.message('Capturing\nImage')

        # Shell command to capture image from webcam and save to directory
        stream = os.popen('fswebcam /home/pi/test/Images/image.jpg')
        output = stream.read()
        mystring = ""

        # Open captured image and encode as base64
        with open("/home/pi/test/Images/image.jpg", "rb") as img_file:
            my_string = base64.b64encode(img_file.read())
        
        lcd.clear()
        lcd.message('Temp: ' + str(temp) + "\nLight: " + str(light))

        # Set request string to send to server
        querystring = "http://"+ ip + ":5000/?usage=newpoint&image="
        querystring+= str(my_string)
        querystring+="&light="
        querystring+=str(light)
        querystring+="&temp="
        querystring+=str(temp)
        querystring+="&number="
        querystring+=str(plant_num)

        # Collect and display response
        response = requests.get(querystring)
        time.sleep(3.0)
        lcd.clear()
        lcd.message("Response\n"+response.text)
        time.sleep(3.0)
        rfid = ""