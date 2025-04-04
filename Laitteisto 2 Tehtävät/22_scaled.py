'''Task 2.2 
Implement a program that reads test signal from the file, scales it to range 0 – 100 and prints the scaled 
values to console. Remember to enable Plotter in Thonny to see the graph. 
Start by reading two seconds of data and find minimum and maximum values from the data. Then use 
min and max values to scale the data so that minimum value is printed as zero and maximum value as 
100. Plot 10 seconds of data with the scaling.'''

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
    #print(f"{scaled_value:>5.2f}")    
    print(scaled_value)
 
    
