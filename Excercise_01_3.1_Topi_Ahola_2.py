import time
from machine import Pin, ADC

ledi = Pin("LED", Pin.OUT)
ledi.value(1) #Testataan ledin toiminta
adc = ADC(Pin(27))

while True:
    #Viive millisekunteina 0-1000ms    
    delay = int(1000*adc.read_u16()/65535)
    print(delay)
    
    ledi.value(0)
    print("LED off")
    time.sleep_ms(delay)    
    
    ledi.value(1)
    print("LED on")
    time.sleep_ms(delay)
    
    
        

    

