import time
from machine import Pin, PWM, ADC


#PWM luokan objektille voi antaa attribuutit freq jaa duty_u16:

ledi1 = PWM(Pin(22), freq = 10, duty_u16 = 100)   
ledi2 = PWM(Pin(21))
ledi3 = PWM(Pin(20))
nappula2 = Pin(7, Pin.IN, Pin.PULL_UP)
nappula1 = Pin(8, Pin.IN, Pin.PULL_UP)
nappula0 = Pin(9, Pin.IN, Pin.PULL_UP)

count = 0

#ledi1.freq(1000)
ledi2.freq(1000)
ledi3.freq(1000)



while True:
    
    
    if nappula2.value() == 0:
        time.sleep(0.150) #150ms estää tuplapainnallukset
        if nappula2.value() == 0:
            print("Nappulaa painettu")
            ledi1.freq(1000)
            count = count +1
            if count > 7:
                count = 0
            print(count)
            ledi1.duty_u16(100* (count & 1)) #ones
            ledi2.duty_u16(100* (count & 2)) #twos
            ledi3.duty_u16(100* (count & 4)) #fours