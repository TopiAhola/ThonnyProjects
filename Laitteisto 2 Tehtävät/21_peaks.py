# filefifo
# self, size, typecode = 'H', name = 'data.txt', repeat = True
# metodit: put, get, has_data, empty

#get(self):"Get one item from the fifo. If repeat is set to False and file ends raises an exception and returns the last value."""
        

from filefifo import Filefifo

sample_rate = 250
data_input = Filefifo(10, name="capture_250Hz_01.txt", repeat=False)
data = []
for datapoint in range(0,1000):
    try:
       data.append(data_input.get())
    except RuntimeError:
        print("Out of data")
        break    

peaks = []
delta_positive = bool
for point in range(1,len(data)):    
    delta = data[point]-data[point-1]
    #print(data[point], data[point-1], delta)
    
    if delta>=0:
        delta_positive=True
        
    if delta_positive and delta<0:
        peaks.append([point,data[point]])                     
                     
    if delta<0:
        delta_positive=False
    
print("Peaks:",peaks)

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
