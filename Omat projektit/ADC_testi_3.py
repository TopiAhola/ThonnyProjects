from machine import UART, Pin, I2C, Timer, ADC, PWM
from ssd1306 import SSD1306_I2C
from fifo import Fifo
import time, ujson
from piotimer import Piotimer


def log_data(self):
    data.append(adc1.read_u16())
    if len(data) >= 1000:
        timer1.deinit()


timer1 = Timer(mode=Timer.PERIODIC, freq=250, callback=log_data) 
#adc0 = ADC(Pin(27, Pin.IN))
adc1 = ADC(1)

sample_rate = 250
data = []

time.sleep(4.5)
print("data:",len(data),data)
new_data = []
#Noise filtering
for n in range(5,len(data),5):
    new_data.append(sum(data[n-5 : n])/5)
print("new_data:",len(new_data),new_data)
data = new_data

#find initial peaks
deltas = []
peaks = []
valleys = []
for point in range(1,len(data)):    
    delta = data[point]-data[point-1]
    print(data[point]-20000, data[point-1]-20000, delta)
    deltas.append(delta)


for index in range(1,len(deltas)): 
    if deltas[index] >= 0 and deltas[index-1] >= 0:
        pass
    elif deltas[index] >= 0 and deltas[index-1] < 0:
        #its a valley!
        valleys.append([index-1, data[index-1]])
    elif deltas[index] < 0 and deltas[index-1] < 0:
        pass
    elif deltas[index] < 0 and deltas[index-1] >= 0:        
        #its a peak!
        peaks.append([index-1, data[index-1]])     
    
    #elif deltas[index] == 0 and deltas[index-1] == 0:
     #    pass
        
    else:
        pass
        print("its a me mario!")


print("Peaks:", peaks)
print("Valleys:", valleys)

peak_intervals = []
peak_intervals_s = []
for n in range(1,len(peaks)):
    interval = peaks[n][0] - peaks[n-1][0]
    peak_intervals.append(interval)
    peak_intervals_s.append(interval/sample_rate)


print("Peak to peak intervals in samples:", peak_intervals)
print("Peak to peak intervals in seconds:", peak_intervals_s)
frequency = 1/(sum(peak_intervals_s)/len(peak_intervals_s))
print("Frequency: ",frequency)

