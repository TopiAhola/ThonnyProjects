
'''
Implement a program that finds positive peaks from a test signal using slope inspection. The test
signal(s) contain pure sine wave so the peaks can be found by inspecting the slope of the signal without
using a threshold. The peak is at a point where the slope turns from positive to negative.
Your program must print at least three peak-to-peak intervals both in number of samples and seconds
and to calculate the frequency of the signal.
'''

# filefifo
# self, size, typecode = 'H', name = 'data.txt', repeat = True
# metodit: put, get, has_data, empty

#get(self):"Get one item from the fifo. If repeat is set to False and file ends raises an exception and returns the last value."""


from filefifo import Filefifo

#get data
sample_rate = 250
data_input = Filefifo(10, name="capture_250Hz_01.txt", repeat=False)
data = []
for datapoint in range(0,1000):
    try:
       data.append(data_input.get())
    except RuntimeError:
        print("Out of data")
        break    

#find initial peaks
deltas = []
peaks = []
valleys = []
for point in range(1,len(data)):    
    delta = data[point]-data[point-1]
    print(data[point], data[point-1], delta)
    deltas.append(delta)
treshhold = ((max(data)+min(data))/2)
print("Treshhold:",treshhold)

for index in range(1,len(deltas)):
    if data[index] > treshhold:
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

