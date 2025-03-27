from machine import UART, Pin, I2C, Timer, ADC
from ssd1306 import SSD1306_I2C
import time, random


sw2 = Pin(7, Pin.IN, Pin.PULL_UP)
sw0 = Pin(9, Pin.IN, Pin.PULL_UP)
i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
oled_width = 128
oled_height = 64
oled = SSD1306_I2C(oled_width, oled_height, i2c)

oled.fill(0)
oled.text("Peli1", 30, 30, 1)
oled.show()
time.sleep(1)

px = 0
py = 32
#pelaajan hitbox on py +4 ja py+5, ja px +2, +3 suhteessa renderiin # pisteet: (4,2)(5,2)(4,3)(5,3)
# pelaajan hitboxin liikerata 4-61
#pelaajan hitbox suhteessa itseensä on (px,py)(px,py+1)

#objektit (x,y)
object_list = [[1,127],[20,127]]
objects_survived = 0

def object_new(object_list):    
    #print(object_list)
    return object_list.append([127, random.randint(0,63)])

#move objects
def object_move():
    for obj in object_list:     
        obj[0] = obj[0]-1
    
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
            
frame = 0
while True:
    time.sleep(0.01)
    frame = frame +1
    print("frame",frame)
    
    if sw2.value()==0:
        print("up input", py)
        py = py -1
        if py < 4:
            py = 4
    
    elif sw0.value()==0:
        print("down input",py)
        py = py +1
        if py > 61:
            py = 61 
    
    else:
        print("no input", py)
        
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
    oled.text(f"score: {objects_survived}", 45, 0, 1)    
    #show
    oled.show()
    
oled.text("GAME OVER", 30, 30, 1)
oled.show()
