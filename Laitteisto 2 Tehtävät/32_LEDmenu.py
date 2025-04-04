'''Task 3.2 
Implement a program that uses the rotary encoder to select an item from a menu. The menu has three 
options: LED1, LED2, LED3. Encoder turns move the selection (arrow, highlight, etc.) and pressing the 
button activates the selection. Activation turns toggles the selected LED on/off. The state of the LED 
must be updated in the menu. 
Use an interrupt for both turn detection and encoder button. The turn and press event must be sent to 
the main program through a fifo. All of the menu logic must be in the main program. 
The encoder button does not have hardware filtering so switch bounce filtering must be performed. 
Bounce filtering should be done in the interrupt handler with the help of time.ticks_XXX-functions. 
Filtering is done by taking a millisecond time stamp on each detected press and comparing that to the 
timestamp of previous press. The new press is ignored if it is too close, for example less than 50 ms 
away from the previous press.
'''





class Encoder:
    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.fifo = Fifo(30, typecode = 'i')
        self.a.irq(handler = self.handler, trigger = Pin.IRQ_RISING, hard = True)

    def handler(self, pin):
        #print("handler called")
        if self.b():
            self.fifo.put(-1)
        else:
            self.fifo.put(1)
            
class Button:
    def __init__(self, pin)
        self.fifo =  Fifo(1, typecode = 'i')
        self.pin.irq(handler = button_handler, trigger = Pin.IRQ_RISING)
        
    def button_handler(self):
        self.fifo.put(1)
        
        
        
#Encoder 
rota = Pin(10, Pin.IN, Pin.PULL_UP)
rotb = Pin(11, Pin.IN, Pin.PULL_UP)
enc1 = Encoder(rota, rotb)
#Encoder push
rot_push_pin = Pin(12, Pin.IN, Pin.PULL_UP)
rot_push = Button(rot_push_pin)
#Outputs
class PWM_LED:
    def __init__(self, pin):
        self = PWM(Pin(pin), freq = 1000, duty_u16 = 0)
        self.state = 0
        
    def toggle(self):
        if self.state == 0:
            self.state = 1
            self.duty_u16(1000)
        if self.state == 1:
            self.state = 0
            self.duty_u16(0)

led1 = PWM_LED(22)
led2 = PWM_LED(21)
led3 = PWM_LED(20)

     
#Pääohjelma
cursor_pos = 0


while True:
    time.sleep(0.050)
    
    #inputs   
    enc1_input = 0 
    while not enc1.fifo.empty():
        try:
            enc1_input = enc1_input + enc1.fifo.get()
        except:
            print("Fifo is empty..")
        print(enc1_input)
        
    rot_push_input = 0
    while not rot_push.fifo.empty():
        try:
            rot_push_input = enc1.fifo.get()
        except:
            print("Fifo is empty..")
        print(rot_push_input)

    
    
    #LED toggle
    
    
    #
    line_list = []
    
    #Menu render
    oled.fill(0)
    line_px = 0
    for line in line_list:        
        oled.text(line, 0, line_px, 1)        
        line_px = line_px + 9 #text is 8 px + 1px space for clarity
    oled.show()