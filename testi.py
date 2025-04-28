from machine import Pin
import time

pinni = Pin(6, Pin.IN)
tim = 0
while True:
    print(tim, pinni.value())
    time.sleep(1)
    tim = tim +1