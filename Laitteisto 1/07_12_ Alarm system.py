from machine import Pin
import time

#Outputs:
siren = Pin(20, Pin.OUT)
lamp = Pin(22, Pin.OUT)
#Inputs:
button = Pin(7, Pin.IN, Pin.PULL_UP)
alarm = Pin(9, Pin.IN, Pin.PULL_UP)

class ASM:     
    def __init__(self, name, clkprd):
        self.name = name
        self.state = self.off
        self.delay = clkprd        

    def run(self):
        self.state()
        time.sleep(self.delay)
        
    def off(self):        
        print("off")
        siren.value(0)
        lamp.value(0)        
        if alarm.value() == 0:
            print("alarm on")
            self.state = self.alarm0
        else:
            self.state = self.off
            
    def alarm0(self):        
        print("alarm0")
        siren.value(1)
        lamp.value(1)        
        if alarm.value()==0 and button.value()==1:
            self.state = self.alarm0
        elif alarm.value()==0 and button.value()==0:
            self.state = self.ack1
        else:
            self.state = self.alarm1
            
    def alarm1(self):        
        print("alarm1")
        siren.value(0)
        lamp.value(1)        
        if button.value()==0:           
            self.state = self.off
        else:
            self.state = self.alarm1
            
    def ack1(self):        
        print("ack1")
        siren.value(0)
        lamp.value(0)        
        if alarm.value()==0:            
            self.state = self.ack2
        else:
            self.state = self.off
            
    def ack2(self):        
        print("ack2")
        siren.value(0)
        lamp.value(1)    
        self.state = self.ack1
      
#Main program:
alarmsystem = ASM("Alarm system", 0.15)
while True:    
    alarmsystem.run()
