from fifo import Fifo
from piotimer import Piotimer
from machine import ADC, Pin
import micropython, network, time

micropython.alloc_emergency_exception_buf(200)


class Adc:
    def __init__(self, pin):        
        self.pin = pin
        self.source = ADC(Pin(self.pin, Pin.IN))
        self.log = []      
    
    def ADC_mode(self):        
        adc_value = self.source.read_u16()
        print(adc_value, adc_value / ((1 << 16) - 1) * 3.3)
        return adc_value

       
class Digital:
    def __init__(self, pin):        
        self.pin = pin
        self.source = Pin(self.pin, Pin.IN, Pin.PULL_UP)
        self.log = []     
    
    def digital_mode(self):        
        digital_value = self.source.value()
        print(digital_value)
        return digital_value
        
        
adc = Adc(27)
digital = Digital(26)

while True:
    time.sleep(0.1)
    adc.ADC_mode()
    digital.digital_mode()





