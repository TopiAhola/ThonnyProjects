from machine import UART, Pin, I2C, Timer, ADC
from ssd1306 import SSD1306_I2C
import time

sw2 = Pin(7, Pin.IN, Pin.PULL_UP)
sw0 = Pin(9, Pin.IN, Pin.PULL_UP)
i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
oled_width = 128
oled_height = 64
oled = SSD1306_I2C(oled_width, oled_height, i2c)

oled.fill(0)
oled.text("Text list", 30, 30, 1)
oled.show()
time.sleep(1)

text_list = []
while True:    
    text_list.append(input("Input text: "))
    if len(text_list) >7: #display fits 7 lines of text with +1px spacing
        del text_list[0]
    
    oled.fill(0)
    line_px = 0
    for line in text_list:        
        oled.text(line, 0, line_px, 1)
        #oled.show()
        line_px = line_px + 9 #text is 8 px + 1px space for clarity
    oled.show()