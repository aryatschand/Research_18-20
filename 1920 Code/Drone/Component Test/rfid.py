import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import time

reader = SimpleMFRC522()
id = ""
while (id == ""):
    try:
        id, text = reader.read()
        id = str(id)
        print(id)
    finally:
        GPIO.cleanup()
    time.sleep(0.2)
id = ""

