from machine import UART, Pin, I2C, Timer, ADC, PWM
from ssd1306 import SSD1306_I2C
from fifo import Fifo
import time, ujson


adc0 = ADC(Pin(27, Pin.IN))
adc1 = ADC(Pin(26, Pin.IN, Pin.PULL_UP))

sample_rate = 250



new_value = 12500
old_value = 12500
old_value2 = 12500
old_value3 = 12500

data = []
while len(data) < 1000:
    time.sleep(1/sample_rate)
    new_value = adc1.read_u16()
    #print(new_value-12600)
    datapoint = ((new_value +old_value +old_value2+old_value3)/4)-12600
    data.append(datapoint)
    print(datapoint)
    old_value3 = old_value2
    old_value2 = old_value
    old_value = new_value

print(data)

#find initial peaks

deltas = []
peaks = []
valleys = []
for point in range(1,len(data)):    
    delta = data[point]-data[point-1]
    print(data[point], data[point-1], delta)
    deltas.append(delta)
    
for index in range(1,len(deltas)):
    if deltas[index] > 0 and deltas[index-1] > 0:
        pass
    elif deltas[index] >= 0 and deltas[index-1] < 0:
        #its a valley!
        valleys.append([index-1, data[index-1]])
    elif deltas[index] < 0 and deltas[index-1] < 0:
        pass
    elif deltas[index] <= 0 and deltas[index-1] > 0:        
        #its a peak!
        peaks.append([index-1, data[index-1]])     
    
    elif deltas[index] == 0 and deltas[index-1] == 0:
         pass
        
    else:
        pass
        print("its a me mario!",index,deltas[index],deltas[index-1])


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
