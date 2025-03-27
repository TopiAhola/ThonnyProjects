from machine import UART, Pin, I2C, Timer, ADC
from ssd1306 import SSD1306_I2C
from fifo import Fifo
import time, random

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

rot_push = Pin(12, Pin.IN, Pin.PULL_UP)
rota = Pin(10, Pin.IN, Pin.PULL_UP) #clock signal
rotb = Pin(11, Pin.IN, Pin.PULL_UP)
sw2 = Pin(7, Pin.IN, Pin.PULL_UP)
sw0 = Pin(9, Pin.IN, Pin.PULL_UP)
i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
enc1 = Encoder(rota, rotb)


oled_width = 128
oled_height = 64
oled = SSD1306_I2C(oled_width, oled_height, i2c)

oled.fill(0)
oled.text("Peli1", 30, 30, 1)
oled.show()
time.sleep(1)

def object_new(object_list):    
    #print(object_list)
    return object_list.append([127, random.randint(0,63)])

#move objects
def object_move():
    for obj in object_list:     
        obj[0] = obj[0]-1
        
#delete objects
def object_delete():
    del_list2=[]
    for obj in object_list:     
        del_list2.append(object_list.index(obj))    
    for ind in del_list2:
        object_list.pop(ind)
            
#cull objects
def object_cull(object_list, objects_survived):
    del_list=[]
    for obj in object_list:
        if obj[0] < 0: #or obj[1] < 0 or obj(1) > 63:
            print("delete:",obj)
            objects_survived = objects_survived +1
            del_list.append(object_list.index(obj))
    for ind in del_list:
        del object_list[ind]
    return object_list, objects_survived
            
def object_collison(object_list, px, py):
    px_range = [px-1,px, px+1, px+2]
    py_range = [py-1, py, py+1, py+2]
    for obj in object_list:
        if obj[0] in px_range and obj[1] in py_range:
            return True
    return False

object_list = [[1,127],[20,127]]
objects_survived = 0
px = 0
py = 32            
frame = 0
energy = 0

while True:
    time.sleep(0.03)
    frame = frame +1
    
    energy = energy + 1
    if energy > 100:
        energy = 100
    print("frame",frame) 
    
    enc1_input =0
    if enc1.fifo.has_data():
        enc1_input = enc1.fifo.get()
        print(enc1_input)
    
    if enc1_input==-1:
        print("up input", py)
        py = py -1
        if py < 4:
            py = 4
    
    elif enc1_input==1:
        print("down input",py)
        py = py +1
        if py > 61:
            py = 61 
    
    elif rot_push()==0:
        print("push input", py)
        if energy == 100:
            energy = 0
            object_delete()
        
    #new objects as function of difficulty
    if frame % 5 == 0:
        object_new(object_list)
    if frame > random.randint(1,10000):
        object_new(object_list)
        print("Bonus object.")
    if frame > random.randint(1,100000):
        object_new(object_list)
        print("Bonus object 2!")
    
    #move obj and cull outside screen
    object_move()
    object_list, objects_survived = object_cull(object_list, objects_survived)
    #check collision      
    if object_collison(object_list, px, py):
        break
    
    #rendering
    oled.fill(0)    
    #player:
    oled.text(">", px-2, py-4, 1)    
    #objects
    for obj in object_list:
        oled.pixel(obj[0],obj[1],1)
    #score
    oled.text(f"score:{objects_survived:#4}", 50, 0, 1)
    oled.text(f"bomb:{energy:#3}", 60, 55, 1)
    #show
    oled.show()
    
while True:    
    oled.text("GAME OVER", 30, 30, 1)
    oled.show()
    if rot_push.value()==0:
        pass

