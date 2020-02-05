import sys
import Adafruit_DHT
import time

sensor = Adafruit_DHT.DHT11
DHT11_pin = 18

humidity, temperature = Adafruit_DHT.read_retry(sensor, DHT11_pin)
if humidity is not None:
    print(temperature, humidity)
else:
    print("nope")
