import time
from machine import Pin



ledi1 = Pin(22, Pin.OUT)
ledi2 = Pin(21, Pin.OUT)
ledi4 = Pin(20, Pin.OUT)
nappula = Pin(12, Pin.IN, Pin.PULL_UP)
count = 0


while True:     
    if nappula.value() == 0:
        time.sleep(0.150) #150ms estää tuplapainnallukset
        if nappula.value() == 0:
            print("Nappulaa painettu")
            count = count +1
            if count > 7:
                count = 0
            print(count)
            ledi1.value(count & 1) #ones
            ledi2.value(count & 2) #twos
            ledi4.value(count & 4) #fours

