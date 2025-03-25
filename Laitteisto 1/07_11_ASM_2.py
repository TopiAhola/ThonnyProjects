from machine import Pin
import time

lamp = Pin(20, Pin.OUT)
btn = Pin(7, Pin.IN, Pin.PULL_UP)

class ASM:     
    def __init__(self, name, clkprd):
        self.name = name
        self.state = self.off
        self.delay = clkprd
        print(f"{self.name}, delay: {self.delay}s")

    def run(self):
        self.state()
        time.sleep(self.delay)
        
    def off(self):        
        print("off")
        lamp.value(0)
        if btn.value() == 0:
            print("nappula off")
            lamp.value(1)
            self.state = self.onw        
            
    def onw(self):        
        print("onw")
        lamp.value(1)
        if btn.value() == 0:
            print("nappula onw")
            self.state = self.onw
        else:
            self.state = self.on     
        
    def on(self):        
        print("on")
        lamp.value(1)
        if btn.value() == 0:
            print("nappula on")
            self.state = self.offw        
        
    def offw(self):        
        print("offw")
        lamp.value(0)
        if btn.value() == 0:
            print("nappula offw")
            self.state = self.offw
        else:
            self.state = self.off
        
#Main program:

light_machine = ASM("light_machine", 0.05)
while True:
    
    light_machine.run()
