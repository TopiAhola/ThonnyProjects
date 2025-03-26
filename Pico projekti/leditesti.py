from machine import Pin, PWM
import time
from led import Led

#Led(self, pin, mode = Pin.OUT, brightness = 1, value = None)

ledi1 = Led(22)
ledi2 = Led(21)
ledi3 = Led(20)
nappula2 = Pin(7, Pin.IN, Pin.PULL_UP)
nappula1 = Pin(8, Pin.IN, Pin.PULL_UP)
nappula0 = Pin(9, Pin.IN, Pin.PULL_UP)
count = 0

while True:    
    if nappula2.value() == 0:
        time.sleep(0.150) #150ms estää tuplapainnallukset
        if nappula2.value() == 0:
            print("Nappulaa painettu")            
            count = count +1
            if count > 7:
                count = 0
            print(count)
            ledi1.off(), ledi2.off(), ledi3.off()
            if (count & 1):  	#ones
                ledi1.on()                
            if (count & 2):
                ledi2.on()		#twos
            if (count & 4):
                ledi3.on()		#fours
            
            
            