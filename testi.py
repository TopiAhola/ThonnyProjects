import Led from /led.py
import Pin, PWM


#Led(self, pin, mode = Pin.OUT, brightness = 1, value = None)

ledi1 = Led(22)
ledi2 = Led(21)
ledi3 ) Led(20)
nappula2 = Pin(7, Pin.IN, Pin.PULL_UP)
nappula1 = Pin(8, Pin.IN, Pin.PULL_UP)
nappula0 = Pin(9, Pin.IN, Pin.PULL_UP)

#Rotary encoder
rot_push = Pin(12, Pin.IN, Pin.PULL_UP)
rota = Pin(14, Pin.IN, Pin.PULL_UP) #clock signal
rotb = Pin(15, Pin.IN, Pin.PULL_UP) #clockwise rot =



while True:    
    if nappula2.value() == 0:
        time.sleep(0.150) #150ms estää tuplapainnallukset
        if nappula2.value() == 0:
            print("Nappulaa painettu")            
            count = count +1
            if count > 7:
                count = 0
            print(count)
            if (count & 1):                 #ones
                ledi1.on()
            if (count & 2):
                ledi2.on()		#twos
            if (count & 4):
                ledi3.on		#fours
            
            
            