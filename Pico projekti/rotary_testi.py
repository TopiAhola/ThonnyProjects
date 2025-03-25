from machine import UART, Pin, I2C, Timer, ADC
from ssd1306 import SSD1306_I2C
from fifo import Fifo
import time, random
import micropython
micropython.alloc_emergency_exception_buf(200)


#Tactile switches
sw2 = Pin(7, Pin.IN, Pin.PULL_UP)
sw1 = Pin(8, Pin.IN, Pin.PULL_UP)
sw0 = Pin(9, Pin.IN, Pin.PULL_UP)
#reset = Pin(30, Pin.IN, Pin.PULL_UP) 
#Rotary encoder
rot_push = Pin(12, Pin.IN, Pin.PULL_UP)
rota = Pin(10, Pin.IN, Pin.PULL_UP) #clock signal
rotb = Pin(11, Pin.IN, Pin.PULL_UP) #clockwise rot =
#LED
d1 = Pin(22, Pin.OUT)
d2 = Pin(21, Pin.OUT)
d3 = Pin(20, Pin.OUT)

#I2C pinni näyttöä varten
i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)


#PWM luokalla voi säätää LEDien kirkkautta välillä 0-65536
# d1.duty_u16(1000) asettaa kohtalaisen kirkkauden
# d2.duty_u16(0) sammuttaa LEDin

#LEDit pitää määritellä näin:
#d1 = PWM(Pin(22), freq = 1000, duty_u16 = 0)   
#d2 = PWM(Pin(21), freq = 1000, duty_u16 = 0)
#d3 = PWM(Pin(20), freq = 1000, duty_u16 = 0)
class Encoder:
    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.fifo = Fifo(30, typecode = 'i')
        self.a.irq(handler = self.handler, trigger = Pin.IRQ_RISING, hard = True)

    def handler(self, pin):
        print("handler called")
        if self.b():
            self.fifo.put(-1)
        else:
            self.fifo.put(1)

enc1 = Encoder(rota, rotb)



#testi

while True:
    time.sleep(0.05)
    if enc1.fifo.has_data():
        enc1_input = enc1.fifo.get()
        print(enc1_input)
    

