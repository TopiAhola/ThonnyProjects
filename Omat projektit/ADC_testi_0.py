#rusk oranssi violett musta rusk 137 x1 1% = 137 ohm


from fifo import Fifo
from piotimer import Piotimer
from machine import ADC, Pin
import micropython, network

micropython.alloc_emergency_exception_buf(200)


class Adc:
    def __init__(self, adc_pin):
        self.adc = ADC(Pin(adc_pin))
        self.adc_fifo = Fifo(size=500, typecode='i')
        self.tmr = Piotimer(freq=50, callback=self.adc_callback)

    def adc_callback(self, tmr):
        self.adc_fifo.put(self.adc.read_u16())
     

def adc_main(pin):
    dmm = Adc(pin)

    while True:
        while dmm.adc_fifo.has_data():
            adc_count = dmm.adc_fifo.get()
            print(adc_count, adc_count / ((1 << 16) - 1) * 3.3)
            
            

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
     
    adc_main(27)
  