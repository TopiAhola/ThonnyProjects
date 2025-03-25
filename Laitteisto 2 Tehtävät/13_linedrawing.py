from machine import UART, Pin, I2C, Timer, ADC
from ssd1306 import SSD1306_I2C
import time
import framebuf


sw2 = Pin(7, Pin.IN, Pin.PULL_UP) #up
sw1 = Pin(8, Pin.IN, Pin.PULL_UP) #reset
sw0 = Pin(9, Pin.IN, Pin.PULL_UP) #down
i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
oled_width = 128
oled_height = 64
oled = SSD1306_I2C(oled_width, oled_height, i2c)

oled.fill(0)
oled.text("Line drawing", 25, 30, 1)
oled.show()
time.sleep(1)
oled.fill(0)
x=0
y=31

while True:
    time.sleep(0.03)
    
    if sw0.value()==0:
        y=y+1
        if y>63:
            y=63
    elif sw2.value()==0:
        y=y-1
        if y<0:
            y=0
    elif sw1.value()==0:
        oled.fill(0)
        x=0
        y=32
        print("reset")
    else:
        print("no input")
    #render 1 px
    oled.pixel(x,y,1)
    oled.show()
    x=x+1
    if x > 127:
        x = 0
    
        