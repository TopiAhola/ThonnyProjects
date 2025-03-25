from machine import Pin
import time

ledi3 = Pin(20, Pin.OUT)
nappula2 = Pin(7, Pin.IN, Pin.PULL_UP)

class ASM:     
    def __init__(self, name, clkprd):
        self.name = name
        self.state = self.off
        self.delay = clkprd
        print(f"{self.name}{self.delay} is in state {self.state}.")

    def run(self):
        self.state()        
        
    def off(self):
        time.sleep(self.delay)
        print("off")
        ledi3.value(0)
        if nappula2.value() == 0:
            print("nappula off")
            ledi3.value(1)
            self.state = self.onw
        
            
    def onw(self):
        time.sleep(self.delay)
        print("onw")
        ledi3.value(1)
        if nappula2.value() == 0:
            print("nappula onw")
            self.state = self.onw
        else:
            self.state = self.on
     
        
    def on(self):
        time.sleep(self.delay)
        print("on")
        ledi3.value(1)
        if nappula2.value() == 0:
            print("nappula on")
            self.state = self.offw
        time.sleep(self.delay)
        
    def offw(self):
        time.sleep(self.delay)
        print("offw")
        ledi3.value(0)
        if nappula2.value() == 0:
            print("nappula offw")
            self.state = self.offw
        else:
            self.state = self.off
        
#Main program:

light_machine = ASM("light_machine", 0.1)
while True:
    
    light_machine.run()
