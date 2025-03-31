from machine import UART, Pin, I2C, Timer, ADC, PWM
from ssd1306 import SSD1306_I2C
from fifo import Fifo
import time, random

'''
Task 3.1 
Implement a program that uses the rotary encoder to control LED brightness. The encoder button is 
used to toggle the LED on/off and turning the encoder adjusts the brightness if the LED is on-state. If the 
LED is off, then the encoder turns are ignored. The program must use interrupts for detecting encoder 
turns and a fifo to communicate turns to the main program. The interrupt handler may not contain any 
LED handling logic. Its purpose is to send turn events to the main program. 
The encoder button must be polled in the main program and filtered for switch bounce. 
'''



class Encoder:
    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.fifo = Fifo(30, typecode = 'i')
        self.a.irq(handler = self.handler, trigger = Pin.IRQ_RISING, hard = True)

    def handler(self, pin):
        #print("handler called")
        if self.b():
            self.fifo.put(-1)
        else:
            self.fifo.put(1)

rot_push = Pin(12, Pin.IN, Pin.PULL_UP)
rota = Pin(10, Pin.IN, Pin.PULL_UP) #clock signal
rotb = Pin(11, Pin.IN, Pin.PULL_UP)

led1 = PWM(Pin(22), freq = 1000, duty_u16 = 0)
enc1 = Encoder(rota, rotb)
led1_on = False
led1_brightness = 0

while True:
    time.sleep(0.130)
    
    enc1_input = 0
    while not enc1.fifo.empty():
        try:
            enc1_input =+  enc1.fifo.get()
        except:
            print("Fifo is empty..")
        print(enc1_input)

    if rot_push.value() == 0:
        time.sleep(0.050)
        if rot_push.value() == 0 and led1_on:
            print("Button")
            led1_on = False
        elif rot_push.value() == 0 and not led1_on:
            print("Button")
            led1_on = True
        else:
            pass

    if led1_on:
        led1_brightness = led1_brightness + enc1_input*50
        if led1_brightness > 65535:
            led1_brightness = 65535
        if led1_brightness < 0:
            led1_brightness = 0
        led1.duty_u16(led1_brightness)
        print(led1_brightness)
    else:
        led1.duty_u16(0)
    

