# filefifo
# self, size, typecode = 'H', name = 'data.txt', repeat = True
# metodit: put, get, has_data, empty

#get(self):"Get one item from the fifo. If repeat is set to False and file ends raises an exception and returns the last value."""
        

from filefifo import Filefifo

sample_rate = 250
data_input = Filefifo(10, name="capture_250Hz_01.txt", repeat=False)

data0 = []
for datapoint in range(0,500):
    try:
       data0.append(data_input.get())
    except RuntimeError:
        print("Out of data")
        break    
max_value = max(data0)
min_value = min(data0)
print("Max, min:",max_value,min_value)


data = []
for datapoint in range(0,2500):
    try:
       data.append(data_input.get())
    except RuntimeError:
        print("Out of data")
        break 
for point in data:    
    scaled_value = ((point-min_value)*100/(max_value-min_value))    
    print(f"{scaled_value:>5.2f}")    
    
 
    
