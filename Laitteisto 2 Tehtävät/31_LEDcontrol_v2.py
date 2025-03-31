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
            
def button_handler(jotain):
    global button_input
    button_input = True

rot_push = Pin(12, Pin.IN, Pin.PULL_UP)
rota = Pin(10, Pin.IN, Pin.PULL_UP)
rotb = Pin(11, Pin.IN, Pin.PULL_UP)

led = PWM(Pin(22), freq = 1000, duty_u16 = 0)
enc1 = Encoder(rota, rotb)
rot_push.irq(handler = button_handler, trigger = Pin.IRQ_RISING)


led_on = False
led_brightness = 0
button_input = False

while True:
    time.sleep(0.050)
    enc1_input = 0
    while not enc1.fifo.empty():
        try:
            enc1_input = enc1_input + enc1.fifo.get()
        except:
            print("Fifo is empty..")
        print(enc1_input)

    if button_input:
        if led_on:
            led_on = False
            button_input = False
        elif not led_on:
            led_on = True
            button_input= False
        else:
            print("error")
            
    if led_on:          
        led_brightness = led_brightness + enc1_input*50
        if led_brightness > 65535:
            led_brightness = 65535
        if led_brightness < 0:
            led_brightness = 0
        led.duty_u16(led_brightness)
        print(led_brightness)
        
    else:
        led.duty_u16(0)
    
