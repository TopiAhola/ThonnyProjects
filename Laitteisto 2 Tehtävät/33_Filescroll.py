'''
Task 3.3 
Implement a program that uses the rotary encoder to scroll data that is read from a file  
• Read 1000 values from a file to a list. 
o It is easiest to use filefifo to read the values. 
• Find minimum and maximum values from the list 
• Use rotary encoder to scroll a window of 128 values on the screen. 
o Program must prevent scrolling backwards past the first sample. 
o Program must prevent scrolling past the last sample that still fills the screen (last index 
128) 
• Use an interrupt and fifo to send turns to the main program. 
Note that your program needs an instance of both filefifo and fifo.'''

from machine import UART, Pin, I2C, Timer, ADC, PWM
from ssd1306 import SSD1306_I2C
from fifo import Fifo
from filefifo import Filefifo

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
                      
# Encoder 
rota = Pin(10, Pin.IN, Pin.PULL_UP)
rotb = Pin(11, Pin.IN, Pin.PULL_UP)
enc1 = Encoder(rota, rotb)


# Display
i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
oled_width = 128
oled_height = 64
oled = SSD1306_I2C(oled_width, oled_height, i2c)

#get data
sample_rate = 250
data_file = Filefifo(10, name="capture_250Hz_01.txt", repeat=False)
data = []
for datapoint in range(0,1000):
    try:
       data.append(data_file.get())
    except RuntimeError:
        print("Out of data")
        break
print("data", len(data), data)

# Scale data
max_value = max(data)
min_value = min(data)
scaled_data = []
for point in data:    
    scaled_data.append(int(63-(63*((point-min_value)/(max_value-min_value)))))
del data
print("scaled data", len(scaled_data), scaled_data)

x1 = 0
x1_max = len(scaled_data)-128
print(x1_max)
while __name__ == "__main__":
    # Inputs
    enc1_input = 0 
    while not enc1.fifo.empty():
        try:
            enc1_input = enc1_input + enc1.fifo.get()
        except:
            print("Fifo is empty..")
        print(enc1_input)
        
    x1 = x1 + 4*enc1_input
    if x1 < 0:
        x1 = 0
    if x1 > x1_max:
        x1 = x1_max
 
        
    # Render
    oled.fill(0)
    for x in range(0,128):
        oled.pixel(x,scaled_data[x1+x],1)
    oled.text(f"{x1},{scaled_data[x1]}",0,0,1)
    oled.show()







