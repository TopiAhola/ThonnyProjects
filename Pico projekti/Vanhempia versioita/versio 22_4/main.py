from machine import UART, Pin, I2C, Timer, ADC, PWM
from ssd1306 import SSD1306_I2C
from fifo import Fifo
from umqtt.simple import MQTTClient
from Button import Encoder, Button
import time, ujson, random, network


# Measurement history
class Measurement_history:
    def __init__(self):
        self.measurements = []

    def add_measurement(self, time_str, mean_hr, mean_ppi, rmssd, sdnn, sns, pns):
        measurement = {
            "time": time_str,
            "mean_hr": mean_hr,
            "mean_ppi": mean_ppi,
            "rmssd": rmssd,
            "sdnn": sdnn,
            "sns": sns,
            "pns": pns
        }
        self.measurements.append(measurement)

    def get_measurement(self, index):
        if 0 <= index < len(self.measurements):
            return self.measurements[index]
        else:
            return None

    def get_all(self):
        return self.measurements

    def count(self):
        return len(self.measurements)    

# Display ASM class
class Display:
    # General Class methods:
    def __init__(self):
        self.state = self.starting_logo
        self.cursor_position = 0
        self.cycle_time = 0.1
        self.last_measurement = []
        self.h_page = 0        
        self.last_measurement = {}
        self.last_response = {}

    def run(self):
        self.state()

    def update_cursor(self, len_options):
        enc1_input = 0
        while not enc1.fifo.empty():
            try:
                enc1_input = enc1_input + enc1.fifo.get()
            except:
                print("Fifo is empty..")
        self.cursor_position = self.cursor_position + enc1_input
        if self.cursor_position > len_options-1:
            self.cursor_position = len_options-1
        if self.cursor_position < 0:
            self.cursor_position = 0


    def select_option(self, options):
        button_input = button.get()  
        if button_input:
            self.state = options[self.cursor_position]
            self.cursor_position = 0

    # Render functions to draw menus
    def render_menu(self, header, text_lines, option_lines):
        oled.fill(0)
        oled.text(header, 0, 0, 1)
        n=1
        if len(text_lines) != 0:
            for line in text_lines:            
                oled.text(line, 0, 9*n, 1)
                n = n+1
        for line in option_lines:
            oled.text(line, 8, 9*n, 1)
            n = n+1
        oled.text(">",0,9*(1+len(text_lines)+self.cursor_position),1)
        oled.show()
        
        rtm_button_input = rtm_button.get()
        if rtm_button_input:
            self.update_cursor(0)
            self.state = self.main_menu
  
########################################
    # Tutorial choosing page
    def choose(self):
        header: str = "Choose menu"
        print(header)
        
        screen_time = 1
        
        while True:
            button_input = button.get()
            rtm_button_input = rtm_button.get()
            
            oled.fill(0)
            oled.text("Skip hints", 40, 8, 1)
            oled.text("press SW_2", 0, 17, 1)
            oled.text("Press button", 0, 47, 1)
            oled.text("to start!", 0, 56, 1)
            if button_input:
                self.state = self.tutorial1
                return
            elif rtm_button_input:
                self.state = self.starting_logo
                return
            
            if screen_time == 1:
                oled.text("<--", 12, 8, 1)
                oled.text("-->", 92, 56, 1)
                screen_time += 1
                
            elif screen_time == 2:
                oled.text("<--", 0, 8, 1)
                oled.text("-->", 104, 56, 1)
                screen_time -= 1
                
            time.sleep(1)
            oled.show()

    # Tutorial page 1
    def tutorial1(self):
        header: str = "Tutorial 1"
        print(header)
        
        screen_time = 1
        
        while True:
            button_input = button.get()
            rtm_button_input = rtm_button.get()
            if button_input:
                self.state = self.tutorial2
                return
            elif rtm_button_input:
                self.state = self.main_menu
                return
            
            if screen_time == 1:
                oled.fill(0)
                oled.text("Turn button -> |", 0, 17, 1)
                oled.text("to scroll   | <-", 0, 26, 1)
                oled.text("Press button", 0, 47, 1)
                oled.text("to select", 0, 56, 1)
                oled.text("-->", 92, 56, 1)
                
                screen_time += 1
            
            elif screen_time == 2:
                oled.fill(0)
                oled.text("Turn button | <-", 0, 17, 1)
                oled.text("to scroll   -> |", 0, 26, 1)
                oled.text("Press button", 0, 47, 1)
                oled.text("to select", 0, 56, 1)
                oled.text("-->", 104, 56, 1)
                
                screen_time -= 1
                
            oled.show()
            time.sleep(1)
                
    # Tutorial page 2
    def tutorial2(self):
        header: str = "Tutorial 2"
        print(header)
        
        screen_time = 1
        
        while True:
            button_input = button.get()
            rtm_button_input = rtm_button.get()
            
            oled.fill(0)
            oled.text("Press SW_2", 40, 8, 1)
            oled.text("Return to menu", 0, 17, 1)
            oled.text("Previous page", 0, 47, 1)
            oled.text("Press SW_0", 40, 56, 1)
            
            if button_input:
                self.state = self.tutorial2
                return
            elif rtm_button_input:
                self.state = self.starting_logo
                return
            
            if screen_time == 1:
                oled.text("<--", 12, 8, 1)
                oled.text("<--", 12, 56, 1)
                
                screen_time += 1
            
            elif screen_time == 2:
                oled.text("<--", 0, 8, 1)
                oled.text("<--", 0, 56, 1)
                
                screen_time -= 1
                
            oled.show()
            time.sleep(1)
                
########################################
    # Starting logo
    def starting_logo(self):
        header: str = "Starting"
        print(header)
        
        message = "HeartBeatZ"
        x = 24 
        y = 28  

        oled.fill(0)  
        
        for i in range(3):
            oled.text(".", x , y)
            oled.show()
            time.sleep(0.4)
            oled.fill(0)
            oled.show()
            time.sleep(0.4)

        for char in message:
            oled.text(char, x, y)
            oled.show()
            x += 8
            time.sleep(0.1)  
            
        time.sleep(0.8)
        
        for i in range(2):
            oled.fill(0)
            oled.text("HEARTBEATZ", 24, 28)
            oled.show()
            time.sleep(0.1)
            oled.fill(0)
            oled.text("HeartBeatZ", 24, 28)
            oled.show()
            time.sleep(0.15)
            
        time.sleep(1)
        self.state = self.main_menu
            
  
########################################
    # Menu states with sleep timers:
    def main_menu(self):
        header: str = "Main Menu"
        print(header)
        text_lines: list[str] = [""]
        option_lines : list[str] = ["Measure HR", "Basic HRV", "Kubios", "History"]
        options = [self.measure_menu, self.measure_basic_menu, self.kubios_menu1, self.history_menu]
        time.sleep(self.cycle_time)
        self.select_option(options)
        self.update_cursor(len(options))
        self.render_menu(header,text_lines, option_lines)
        
########################################
    # Measure heart rate menu
    def measure_menu(self):
        header: str = "Measure Heart Rate"
        print(header)
        
        screen_time = 1
        last_update = time.ticks_ms()
        
        while True:
            button_input = button.get()
            rtm_button_input = rtm_button.get()
            return_button_input = return_button.get()
            
            if button_input:
                self.last_measurement = monitor.measure()
                self.state = self.main_menu
                return
            elif rtm_button_input or return_button_input:
                self.state = self.main_menu
                return
            
            oled.fill(0)
            oled.text("Place your", 0, 0, 1)
            oled.text("finger on top of", 0, 9, 1)
            oled.text("the sensor", 0, 18, 1)
            oled.text("Press button", 0, 36, 1)
            oled.text("to start!", 0, 45, 1)
            
            if screen_time == 1:
                oled.text("-->", 92, 56, 1)
                screen_time += 1
            
            elif screen_time == 2:
                oled.text("-->", 104, 56, 1)
                screen_time -= 1
                
            oled.show()
            time.sleep(1)

########################################
    # Measure basic HRV menu
    def measure_basic_menu(self):
        header: str = "Measure Basic HRV"
        print(header)
        
        oled.fill(0)
        oled.text("Place your", 0, 0, 1)
        oled.text("finger on top of", 0, 9, 1)
        oled.text("the sensor", 0, 18, 1)
        oled.text("Press button", 0, 36, 1)
        oled.text("to start!", 0, 45, 1)      
        oled.show()
                
        button_input = button.get()
        rtm_button_input = rtm_button.get()
        return_button_input = return_button.get()
        
        if button_input:
            # Mittaa yli 30s dataa ja palauuttaa listan.
            data = monitor.measure(850)
            if len(data) > 10:
                self.last_measurement = { "id": 1,
          "type": "PPI",
            "data": data,
            "analysis": { "type": "readiness" } }
                self.state = self.kubios_menu1
            else:
                self.state = self.measure_basic_menu_error
            
        elif rtm_button_input or return_button_input:
            self.state = self.main_menu
            
        time.sleep(self.cycle_time)
            
########################################
    # Measurement Error menu
    def measure_basic_menu_error(self):
        header: str = "Measurement error menu"
        print(header)
        
        oled.fill(0)
        oled.text("Pulse signal was", 0, 16, 1)
        oled.text("not good enough", 0, 24, 1)
        oled.show()
        
        if button_input or rtm_button_input or return_button_input:
            self.state = self.main_menu     
             
        time.sleep(self.sycle_time)
        
        
########################################
    # Kubios menu
    def kubios_menu1(self):
        header: str = "Kubios Menu 1"
        print(header)
        
        if kubios.test():    
        
            oled.fill(0)
            oled.text("Uploading last", 0, 32, 1)
            oled.text("measurement...", 0, 40, 1)
            oled.show()
            kubios.send_request(self.last_measurement)
            self.state = self.kubios_menu2        
        
        else:            
            self.state = self.kubios_menu_error
        
        time.sleep(1)
        
        
        
        
    def kubios_menu2(self):
        header: str = "Kubios Menu 2"
        print(header)       
        
        oled.fill(0)
        oled.text("Uploading last", 0, 24, 1)
        oled.text("measurement...", 0, 32, 1)
        oled.text("<--cancel", 0, 40, 1)
        oled.show()
        
        button_input = button.get()
        if button_input:
            self.state = self.main_menu
                
        elif kubios.check_response():
            self.last_response = kubios.get_response()
            self.state = self.show_kubios_result
        else:
            pass
        
        time.sleep(1)
        
    def show_kubios_result(self):
        header: str = "Kubios Result"
        print(header)
        
        oled.fill(0)
        oled.text("Kubios analysis:", 0, 0, 1)
        oled.text(f"id: {self.last_response["id"]}", 0, 8, 1)
        oled.text(f"stress: {self.last_response["data"]["analysis"]["stress_index"]}", 0, 16, 1)
        oled.text(f"mean HR: {self.last_response["data"]["analysis"]["mean_hr_bpm"]}", 0, 24, 1)
        oled.text(f"p-Age: {self.last_response["data"]["analysis"]["physiological_age"]}", 0, 32, 1)
        oled.text(f"Time: {self.last_response["data"]["analysis"]["create_timestamp"]}", 0, 40, 1)
        oled.show()
        
        button_input = button.get()
        if button_input:
            self.state = self.main_menu
        
        time.sleep(self.cycle_time)
       

        
    def kubios_menu_error(self):
        header: str = "Kubios Error"
        print(header)
        oled.fill(0)
        oled.text("Error sending", 0, 0, 1)
        oled.text("data!", 0, 9, 1)
        oled.text("Please wait", 0, 18, 1)
        oled.text("to retry.", 0, 27, 1)
        oled.text(" ", 0, 36, 1)
        oled.text("Press cancel", 0, 45, 1)
        oled.text("to return.", 0, 54, 1)
        oled.show()
        
        button_input = button.get()        
        if kubios.test():
            self.state = self.kubios_menu1
            time.sleep(1)
            
        elif button_input:
            self.state = self.main_menu
            time.sleep(self.cycle_time)
        else:
            kubios.connect()
            self.state = self.kubios_menu_error
            time.sleep(self.cycle_time)
        
        
        
        
########################################
    # Hardcoded history !Delete afterr
    history = Measurement_history()
    history.add_measurement("2025-04-11 19:20", 79, 765, 24, 22, 1.385, -1.012)
    history.add_measurement("2025-04-11 19:30", 85, 710, 26, 24, 1.612, -1.205)
    history.add_measurement("2025-04-11 19:40", 77, 730, 23, 21, 1.472, -0.982)
    history.add_measurement("2025-04-11 19:20", 79, 765, 24, 22, 1.385, -1.012)
    history.add_measurement("2025-04-11 19:30", 85, 710, 26, 24, 1.612, -1.205)
    history.add_measurement("2025-04-11 19:40", 77, 730, 23, 21, 1.472, -0.982)
    history.add_measurement("2025-04-11 19:20", 79, 765, 24, 22, 1.385, -1.012)
    history.add_measurement("2025-04-11 19:30", 85, 710, 26, 24, 1.612, -1.205)
    history.add_measurement("2025-04-11 19:40", 77, 730, 23, 21, 1.472, -0.982)
    history.add_measurement("2025-04-11 19:20", 79, 765, 24, 22, 1.385, -1.012)
    history.add_measurement("2025-04-11 19:30", 85, 710, 26, 24, 1.612, -1.205)
    history.add_measurement("2025-04-11 19:40", 77, 730, 23, 21, 1.472, -0.982)

    # History menu
    def history_menu(self):
        header: str = "History Menu"
        print(header)
        text_lines: list[str] = [""]
        count = self.history.count()
        
        options_per_page = 4
        start_index = self.h_page * options_per_page
        end_index = start_index + options_per_page
        measurements_on_page = self.history.get_all()[start_index:end_index]

        if count == 0:
            option_lines = ["No data"]
            options = [lambda: None] # Builds a dummy function that returns nothing
        else:
            option_lines = [f"Measurement {start_index + i + 1}" for i in range(len(measurements_on_page))]
            
            options = [
                # Creates list of lambda functions that call 'self.measurement'
                lambda i=i: self.measurement(self.history.get_measurement(start_index + i))
                for i in range(len(measurements_on_page))
            ]
            
            if end_index < count:
                option_lines.append("Next Page")
                options.append(lambda: self.show_next_page())

        self.render_menu(header, text_lines, option_lines)
        time.sleep(self.cycle_time)
        self.select_option(options)
        self.update_cursor(len(options))
        
        rtm_button_input = rtm_button.get()
        return_button_input = return_button.get()
        if rtm_button_input:
            self.update_cursor(0)
            self.state = self.main_menu
            self.h_page = 0
        elif return_button_input and self.h_page > 0:
            self.update_cursor(0)
            self.h_page -= 1
            self.state = self.history_menu
    
    def show_next_page(self):
        self.h_page += 1
        time.sleep(self.cycle_time)
        self.state = self.history_menu
        
    # Measurement
    def measurement(self, data):
        header: str = "Measurement"
        print(header)
        oled.fill(0)
        oled.text(data["time"], 0, 0, 1)
        oled.text(f"Mean HR: {data['mean_hr']}", 0, 9, 1)
        oled.text(f"Mean PPI: {data['mean_ppi']}", 0, 18, 1)
        oled.text(f"RMSSD: {data['rmssd']}", 0, 27, 1)
        oled.text(f"SDNN: {data['sdnn']}", 0, 36, 1)
        oled.text(f"SNS: {data['sns']}", 0, 45, 1)
        oled.text(f"PNS: {data['pns']}", 0, 54, 1)
        oled.show()
        
        time.sleep(self.cycle_time)
        
        rtm_button_input = rtm_button.get()
        return_button_input = return_button.get()
        button_input = button.get()
        if rtm_button_input:
            self.update_cursor(0)
            self.state = self.main_menu
        elif button_input:
            self.update_cursor(0)
            self.state = self.history_menu
        elif return_button_input:
            self.update_cursor(0)
            self.state = self.history_menu
        
####################################################################################
# Main program
# Globals

# Init menu object
menu = Display()

# Display definitions
i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
oled_width = 128
oled_height = 64
oled = SSD1306_I2C(oled_width, oled_height, i2c)

# Input Pins
adc1 = ADC(Pin(27))
rot_push = Pin(12, Pin.IN, Pin.PULL_UP)
rota = Pin(10, Pin.IN, Pin.PULL_UP)
rotb = Pin(11, Pin.IN, Pin.PULL_UP)

#Tactile switches
sw2 = Pin(7, Pin.IN, Pin.PULL_UP)
sw1 = Pin(8, Pin.IN, Pin.PULL_UP)
sw0 = Pin(9, Pin.IN, Pin.PULL_UP)

# Encoder definition
enc1 = Encoder(rota, rotb)

# Button definition
button = Button(rot_push)
rtm_button = Button(sw2) # return to menu
return_button = Button(sw0)

## Kubios definition:
from Kubios import Kubios
kubios = Kubios()
kubios.connect()
if kubios.test():
    print("Kubios is working")    
else:
    print("Kubios is not working!")
    
test_measurement = { "id": 666,
              "type": "PPI",
                "data": [828, 836, 852, 760, 800, 796, 856, 824, 808, 776, 724, 816, 800, 812, 812, 812, 812, 756, 820, 812, 800],
                "analysis": { "type": "readiness" } }
menu.last_measurement = test_measurement

# Pulse monitor
from hrmonitor import HeartRateMonitor
monitor = HeartRateMonitor()


while True:
    Display.run(menu)
    
    
    


