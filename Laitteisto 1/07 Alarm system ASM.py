from machine import Pin
import time

#Outputs:
siren = Pin(20, Pin.OUT)
lamp = Pin(22, Pin.OUT)
#Inputs:
button = Pin(7, Pin.IN, Pin.PULL_UP)
alarm = Pin(9, Pin.IN, Pin.PULL_UP)
#States - outputs in state
#off - 
#alarm0 - lamp, siren
#alarm1 - light
#ack1 - 
#ack2 - lamp

class Button:
    

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
        ledi3.value(0)
        if nappula2.value() == 0:
            print("nappula off")
            ledi3.value(1)
            self.state = self.onw        
            
    def onw(self):        
        print("onw")
        ledi3.value(1)
        if nappula2.value() == 0:
            print("nappula onw")
            self.state = self.onw
        else:
            self.state = self.on     
        
    def on(self):        
        print("on")
        ledi3.value(1)
        if nappula2.value() == 0:
            print("nappula on")
            self.state = self.offw        
        
    def offw(self):        
        print("offw")
        ledi3.value(0)
        if nappula2.value() == 0:
            print("nappula offw")
            self.state = self.offw
        else:
            self.state = self.off
        
#Main program:

light_machine = ASM("light_machine", 0.05)
while True:
    
    light_machine.run()

