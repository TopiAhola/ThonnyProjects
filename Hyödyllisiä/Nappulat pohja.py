from machine import Pin, PWM
import time

#PWM tekee valoista himmeitä
ledi1 = PWM(Pin(22), freq = 2000, duty_u16 = 50)   
ledi2 = PWM(Pin(21), freq = 1000, duty_u16 = 50)
ledi3 = PWM(Pin(20), freq = 1000, duty_u16 = 50)
nappula2 = Pin(7, Pin.IN, Pin.PULL_UP)
nappula1 = Pin(8, Pin.IN, Pin.PULL_UP)
nappula0 = Pin(9, Pin.IN, Pin.PULL_UP)
nappula_knob = Pin(12, Pin.IN, Pin.PULL_UP)

while True:
    if nappula0.value() == 0:
        time.sleep(0.100) #100ms estää tuplapainnallukset
        if nappula0.value() == 0:
            print("Nappulaa 0 painettu")
            ledi1.duty_u16(1000)

    elif nappula1.value() == 0:
        time.sleep(0.100) #100ms estää tuplapainnallukset
        if nappula1.value() == 0:
            print("Nappulaa 1 painettu")
            ledi2.duty_u16(1000)
            
    elif nappula2.value() == 0:
        time.sleep(0.100) #100ms estää tuplapainnallukset
        if nappula2.value() == 0:
            print("Nappulaa 2 painettu")                 
            ledi3.duty_u16(1000)
            
    elif nappula_knob.value() == 0:
            time.sleep(0.100) #100ms estää tuplapainnallukset
            if nappula_knob.value() == 0:
                print("Kääntönappulaa painettu")

    else:
        ledi1.duty_u16(0)
        ledi2.duty_u16(0)
        ledi3.duty_u16(0)