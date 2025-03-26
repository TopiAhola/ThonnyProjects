from machine import UART, Pin, I2C, Timer, ADC
from ssd1306 import SSD1306_I2C
import time

sw2 = Pin(7, Pin.IN, Pin.PULL_UP)
sw0 = Pin(9, Pin.IN, Pin.PULL_UP)
i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)

oled_width = 128
oled_height = 64
display = SSD1306_I2C(oled_width, oled_height, i2c)

display.fill(0)
display.text("UFO start", 30, 30, 1)
display.show()
time.sleep(1)
#place ufo at bottom center
ufo_x = 54
ufo_y = 56

while True:
    #frame time
    time.sleep(0.03)
    #input processing
    #left
    if sw2.value()==0:
        print("left input", ufo_x)
        ufo_x = ufo_x -1
        if ufo_x < 0:
            ufo_x = 0
    #right
    elif sw0.value()==0:
        print("right input",ufo_x)
        ufo_x = ufo_x +1
        if ufo_x > 105:
            ufo_x = 105 #105px limits ufo to screen
    #none
    else:
        print("no input", ufo_x)   
    #rendering
    display.fill(0)
    display.text("<=>", ufo_x, ufo_y, 1)
    display.show()



