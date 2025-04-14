from fifo import Fifo
from piotimer import Piotimer
from machine import ADC, Pin
import micropython, network, time

micropython.alloc_emergency_exception_buf(200)


class Adc:
    def __init__(self, pin):        
        self.pin = pin
        self.source = Pin(self.pin, Pin.IN, Pin.PULL_UP)
        self.log = []      
        
    def digital_mode(self):
        self.source = Pin(self.pin, Pin.IN, Pin.PULL_UP)
        digital_value = self.source.value()
        print(digital_value)
        return digital_value
    
    def ADC_mode(self):
        self.source = ADC(Pin(self.pin, Pin.IN, Pin.PULL_UP))
        adc_value = self.source.read_u16()
        print(adc_value, adc_value / ((1 << 16) - 1) * 3.3)
        return adc_value

    def run(self):
        while True:
            self.digital_mode()
            self.ADC_mode()
            time.sleep(0.1)
       
    def log(self):
        n = 0
        while n < 10:            
            self.log.append( (self.digital_mode(), self.ADC_mode()))
            n= n+1
        time.sleep(0.1)
        
        
        
adc = Adc(27)
adc.run()




