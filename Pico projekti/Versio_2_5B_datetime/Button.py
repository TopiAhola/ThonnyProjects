from machine import Pin
from fifo import Fifo
import time

# Encoder input interrupt
class Encoder:
    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.fifo = Fifo(50, typecode='i')
        self.a.irq(handler=self.handler, trigger=Pin.IRQ_RISING, hard=True)

    def handler(self, pin):
        direction = -1 if self.b() else 1
        self.fifo.put(direction)

    def get(self):
        if not self.fifo.empty():
            return self.fifo.get()
        return 0


# Encoder button input interrupt
class Button:
    def __init__(self, pin):
        self.last_press = 0
        self.pressed = False
        self.pin = Pin(pin, Pin.IN, Pin.PULL_UP)
        self.pin.irq(handler=self.button_handler, trigger=Pin.IRQ_FALLING)

    def button_handler(self, pin):
        current_time = time.ticks_ms()
        if time.ticks_diff(current_time, self.last_press) > 200:  # debounce ms
            self.pressed = True
            self.last_press = current_time

    def get(self):
        if self.pressed:
            self.pressed = False
            return True
        return False
    
if __name__ == '__main__':
    rot_push = Pin(12, Pin.IN, Pin.PULL_UP)
    rota = Pin(10, Pin.IN, Pin.PULL_UP)
    rotb = Pin(11, Pin.IN, Pin.PULL_UP)
    
    last_push = 1
    last_a = rota.value()
    
    while True:
        # Detect button press
        current_push = rot_push.value()
        if last_push == 1 and current_push == 0:
            print("Button Pressed!")
        last_push = current_push

        # Detect rotation
        current_a = rota.value()
        current_b = rotb.value()
        if current_a != last_a:
            if current_b != current_a:
                print("Rotated Right")
            else:
                print("Rotated Left")
        last_a = current_a

        time.sleep_ms(1)
        
        
