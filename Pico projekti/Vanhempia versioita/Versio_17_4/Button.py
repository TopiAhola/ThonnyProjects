class Button:
    def __init__(self, pin):
        self.press_times = Fifo(50, typecode='i')
        self.pressed = False
        self.pin = Pin(pin, Pin.IN, Pin.PULL_UP)
        self.pin.irq(handler=self.button_handler, trigger=Pin.IRQ_FALLING)

    def button_handler(self, pin):
        current_time = time.ticks_ms()
        if not self.press_times.empty():
            previous_time = self.press_times.get()
            diff = time.ticks_diff(current_time, previous_time)
            # print(diff)
            if diff < 50:
                pass
            else:
                self.pressed = True
        else:
            self.press_times.put(current_time)

    def get(self):
        return_value = self.pressed
        self.pressed = False
        return return_value


if __name__ == '__main__':
    rot_push = Pin(12, Pin.IN, Pin.PULL_UP)
    rota = Pin(10, Pin.IN, Pin.PULL_UP)
    rotb = Pin(11, Pin.IN, Pin.PULL_UP)

    rot_push = Button(rot_push)
    rot_a = Button(rota)
    rot_b = Button(rotb)

    while True:
        if rot_push.get():
            print("rot_push")