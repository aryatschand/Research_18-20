# Add your Python code here. E.g.
from microbit import *
pin0.set_analog_period(20)

while True:
    if (button_a.is_pressed()):
        pin0.write_analog(150)
        display.scroll("A")
    elif (button_b.is_pressed()):
        pin0.write_analog(200)
        display.scroll("B")
    else:
        display.show(Image.HEART)


# Servo control: 
# 100 = 1 millisecond pulse all right 
# 200 = 2 millisecond pulse all left 
# 150 = 1.5 millisecond pulse center 