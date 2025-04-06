'''Task 3.2 
Implement a program that uses the rotary encoder to select an item from a menu. The menu has three 
options: LED1, LED2, LED3. Encoder turns move the selection (arrow, highlight, etc.) and pressing the 
button activates the selection. Activation turns toggles the selected LED on/off. The state of the LED 
must be updated in the menu. 
Use an interrupt for both turn detection and encoder button. The turn and press event must be sent to 
the main program through a fifo. All of the menu logic must be in the main program. 
The encoder button does not have hardware filtering so switch bounce filtering must be performed.

Bounce filtering should be done in the interrupt handler with the help of time.ticks_XXX-functions. 
Filtering is done by taking a millisecond time stamp on each detected press and comparing that to the 
timestamp of previous press. The new press is ignored if it is too close, for example less than 50 ms 
away from the previous press.
'''
from machine import UART, Pin, I2C, Timer, ADC, PWM
from ssd1306 import SSD1306_I2C
from fifo import Fifo
import time, micropython

micropython.alloc_emergency_exception_buf(100)

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
            
class Button:
    def __init__(self, pin):
        self.previous_press =  Fifo(1, typecode = 'i')
        self.pressed = Fifo(1, typecode = 'i')
        self.pin.irq(handler = button_handler, trigger = Pin.IRQ_RISING)
        
    def button_handler(self):
        current_time = time.ticks_ms()
        try:
            previous_time = self.previous_press.get()
            if time.ticks_diff(current_time,previous_time) < 50:
                pass
            else:
                self.pressed.put(1)
        except:
            pass
        self.previous_press.put(current_time)


        
#Encoder 
rota = Pin(10, Pin.IN, Pin.PULL_UP)
rotb = Pin(11, Pin.IN, Pin.PULL_UP)
enc1 = Encoder(rota, rotb)
#Encoder push
rot_push_pin = Pin(12, Pin.IN, Pin.PULL_UP)
rot_push = Button(rot_push_pin)

#Outputs
class PWM_LED:
    def __init__(self, name, pin):
        self = PWM(Pin(pin), freq = 1000, duty_u16 = 0)
        self.name = name
        self.state = 0
        self.text = ""
        
    def toggle(self):
        if self.state == 0:
            self.state = 1
            self.duty_u16(1000)
            self.text = f"{self.name} - ON"
        if self.state == 1:
            self.state = 0
            self.duty_u16(0)
            self.text = f"{self.name} - ON"

led1 = PWM_LED("LED1",22)
led2 = PWM_LED("LED2",21)
led3 = PWM_LED("LED3",20)

# Display
i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
oled_width = 128
oled_height = 64
oled = SSD1306_I2C(oled_width, oled_height, i2c)

#Pääohjelma
cursor_pos = 0
led = [led1, led2, led3]
while True:
    time.sleep(0.050)
    
    #inputs   
    enc1_input = 0 
    while not enc1.fifo.empty():
        try:
            enc1_input = enc1_input + enc1.fifo.get()
        except:
            print("Fifo is empty..")
        print(enc1_input)
        
    rot_push_input = 0
    while not rot_push.pressed.empty():
        rot_push_input = rot_push.pressed.get()
        print(rot_push_input)

    curosr_pos = cursor_pos + enc1_input
    if curosr_pos < 0:
        curosr_pos = 0
    elif cursor_pos > 3:
        cursor_pos = 3
    else:
        pass

    #LED toggle
    if rot_push_input == 1:
        led[cursor_pos].toggle()

    #Menu render
    oled.fill(0)
    oled.text(led1.text,2,0,1)
    oled.text(led2.text,2,9,1)
    oled.text(led3.text,2,18,1)
    oled.text("[    ]",0,9*cursor_pos,1)
    oled.show()