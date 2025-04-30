from machine import UART, Pin, I2C, Timer, ADC, PWM
from ssd1306 import SSD1306_I2C
from fifo import Fifo
from umqtt.simple import MQTTClient
from Button import Encoder, Button
from safe_testi import read_and_print_files, save_raw_data
import time, ujson, network

# Display ASM class
class Display:
    # General Class methods:
    def __init__(self):
        self.state = self.fast_connect_1
        self.cursor_position = 0
        self.cycle_time = 0.1
        self.h_page = 0
        self.last_measurement = {}
        self.measurements = {}
        self.responses = {}
        self.last_response = {}
        self.kubios_strings = [""]
        self.id = 6969

    def get_measurements(self):
        # Tämä funktio formatoi palautusarvot oikein dictiksi.
        # Asettaan mittauksen id:n määrän perusteella.
        saved_measurements = read_and_print_files()
        for line in saved_measurements:
            dic = ujson.loads(line)
            try:
                self.responses[dic["response"]["id"]]= dic["response"]
            except:
                print("No kubios response")
            try:
                self.measurements[dic["measurement"]["id"]] = dic["measurement"]
            except:
                print("get_measurement error")
            if self.id < int(dic["measurement"]["id"]):
                self.id = int(dic["measurement"]["id"])

        print("Measurements:", self.measurements)
        print("Responses:", self.responses)
        print("Id set:", self.id)

    def response_string(self, response):
        # Muuttaa kubios responsen listaksi stringejä näyttöä varten
        list = []
        for key, value in response.items():
            if isinstance(value, dict):
                list.append("")  # Tyhjä rivi alidictien alkuun.
                list.append(key)
                sublist = self.response_string(value)
                for sub in sublist:
                    list.append(sub)
            else:
                list.append(f"{key}: {value}")
        return list

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
  
################################################################################
    # Tutorial menus
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
                
################################################################################
    # Starting logo plays during wlan connection
    def fast_connect_1(self):
        kubios.fast_connect_wlan()
        self.state = self.starting_logo


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
        self.state = self.fast_connect_2


    def fast_connect_2(self):
        print("fast mqtt connection")
        kubios.fast_connect_mqtt()
        self.state = self.main_menu
            
  
################################################################################
    # Main menu
    def main_menu(self):
        header: str = "Main Menu"
        print(header)
        text_lines: list[str] = [""]
        option_lines : list[str] = ["Measure HR", "Basic HRV", "Kubios", "History"]
        options = [self.measure_menu, self.measure_basic_menu, self.measure_kubios_menu, self.history_menu]
        time.sleep(self.cycle_time)
        self.select_option(options)
        self.update_cursor(len(options))
        self.render_menu(header,text_lines, option_lines)
        
################################################################################
    # Measure heart rate menu
    def measure_menu(self):
        header: str = "Measure Heart Rate"
        print(header)
        
        screen_time = 1
        last_update = time.ticks_ms()
        
        while True:
            if button.get():
                monitor.measure(999)
                self.state = self.main_menu
                return
            elif rtm_button.get() or return_button.get():
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

################################################################################
# Measure basic HRV menu
    def measure_basic_menu(self):
        header: str = "Measure Kubios HRV"
        print(header)
        
        oled.fill(0)
        oled.text("Place your", 0, 0, 1)
        oled.text("finger on top of", 0, 9, 1)
        oled.text("the sensor", 0, 18, 1)
        oled.text("Press button", 0, 36, 1)
        oled.text("to start!", 0, 45, 1)      
        oled.show()

        if button.get():
            # Mittaa yli 30s dataa ja palauuttaa listan.
            data = monitor.measure(33)
            if len(data) > 10:
                self.last_measurement = { "id": self.id,"type": "PPI","data": data,"analysis": { "type": "readiness" } }
                self.measurements[self.id] = data
                save_raw_data({},self.last_measurement)
                self.id = self.id + 1
                self.state = self.basic_analysis_menu
            else:
                self.state = self.measure_basic_menu_error
            
        elif rtm_button.get() or return_button.get():
            self.state = self.main_menu
            
        time.sleep(self.cycle_time)
            

########################################

# Measure basic HRV menu
    def basic_analysis_menu(self):
        print("basic analysis TBD")
        
        oled.fill(0)
        oled.text("This will show", 0, 0, 1)
        oled.text("local analysis", 0, 9, 1)
        oled.text("results.", 0, 18, 1)
        oled.show()
        
        if button.get() or rtm_button.get() or return_button.get():
            self.state = self.main_menu

        time.sleep(self.cycle_time)

################################################################################
    # Measure Kubios menu
    def measure_kubios_menu(self):
        header: str = "Measure Kubios HRV"
        print(header)
        
        oled.fill(0)
        oled.text("Place your", 0, 0, 1)
        oled.text("finger on top of", 0, 9, 1)
        oled.text("the sensor", 0, 18, 1)
        oled.text("Press button", 0, 36, 1)
        oled.text("to start!", 0, 45, 1)      
        oled.show()

        if button.get():
            # Mittaa yli 30s dataa ja palauuttaa listan.
            data = monitor.measure(33)
            if len(data) > 10:
                self.last_measurement = { "id": self.id,"type": "PPI","data": data,"analysis": { "type": "readiness" } }
                self.measurements[self.id] = data
                save_raw_data({}, self.last_measurement)
                #self.id = self.id + 1
                self.state = self.kubios_menu1
            else:
                self.state = self.measure_basic_menu_error
            
        elif rtm_button.get() or return_button.get():
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
        
        if button.get() or rtm_button.get() or return_button.get():
            self.state = self.main_menu     
             
        time.sleep(self.cycle_time)
        
        
########################################
    # Kubios menu1 sends Kubios request
    def kubios_menu1(self):
        header: str = "Kubios Menu 1"
        print(header)
        
        # if kubios.test():
        if True:
            oled.fill(0)
            oled.text("Uploading last", 0, 8, 1)
            oled.text("measurement...", 0, 16, 1)
            oled.show()
            #kubios.send_request(self.last_measurement)
            self.state = self.kubios_menu2        
        
        else:            
            self.state = self.kubios_menu_error
        
        time.sleep(1)

########################################
    # Kubios menu2
    def kubios_menu2(self):
        header: str = "Kubios Menu 2"
        print(header)       
        
        oled.fill(0)
        oled.text("Uploading last", 0, 8, 1)
        oled.text("measurement...", 0, 16, 1)
        oled.text("Press button", 0, 32, 1)
        oled.text("to cancel.", 0, 40, 1)
        oled.show()

        if button.get() or rtm_button.get() or return_button.get():
            self.state = self.main_menu

        # elif kubios.check_response():
        elif True:
            global global_response
            self.last_response = global_response

            self.responses[self.last_response["id"]] = self.last_response
            save_raw_data(self.last_response, self.measurements[self.last_response["id"]])
            self.state = self.show_kubios_result
        else:
            pass
        
        time.sleep(1)

########################################
    #Shows kubios response
    def show_kubios_result(self):
        header: str = "Kubios Result"
        print(header)

        if self.kubios_strings[0] != f"id: {self.id}":
            self.kubios_strings = self.response_string(self.last_response)

        elif self.kubios_strings[0] == f"id: {self.id}":
            self.update_cursor(len(self.kubios_strings)-5)
            oled.fill(0)
            oled.text("Kubios results:", 0, 0, 1)
            n = 0
            for line in self.kubios_strings[self.cursor_position: self.cursor_position+5]:
                oled.text(line, 0, 8+8*n, 1)
                n = n+1
            oled.show()

            if button.get() or rtm_button.get() or return_button.get():
                self.state = self.main_menu

            time.sleep(self.cycle_time)
        else:
            print("Kubios string list error!")

########################################
        
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

        if kubios.test():
            self.state = self.kubios_menu1
            time.sleep(1)
            
        elif button.get() or rtm_button.get() or return_button.get():
            self.state = self.main_menu
            time.sleep(self.cycle_time)
        else:
            kubios.connect()
            self.state = self.kubios_menu_error
            time.sleep(self.cycle_time)
        

################################################################################
    # History menu
     #Measurement history
     #Kubios history
     #
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

# Mittauksen oletusarvot:
test_measurement = { "id": 6969,
              "type": "PPI",
                "data": [828, 836, 852, 760, 800, 796, 856, 824, 808, 776, 724, 816, 800, 812, 812, 812, 812, 756, 820, 812, 800],
                "analysis": { "type": "readiness" } }

menu.last_measurement = test_measurement

# Pulse monitor
from hrmonitor import HeartRateMonitor
monitor = HeartRateMonitor()

# Haetaan tallennetut tiedostot:
menu.get_measurements()



## TEstausta varten kubios response:
global_response = {
        'id': 6969,
        'data': {
            'status': 'ok',
            'analysis': {
                'artefact': 100,
                'mean_rr_ms': 805,
                'rmssd_ms': 42.90517,
                'freq_domain': {
                    'LF_power_prc': 21.00563,
                    'tot_power': 836.9012,
                    'HF_peak': 0.1966667,
                    'LF_power_nu': 21.41622,
                    'VLF_power': 16.04525,
                    'LF_peak': 0.15,
                    'LF_power': 175.7964,
                    'HF_power_nu': 78.4376,
                    'VLF_power_prc': 1.917222,
                    'HF_power': 643.8597,
                    'HF_power_prc': 76.93377,
                    'VLF_peak': 0.04,
                    'LF_HF_power': 0.2730352
                },
                'stress_index': 18.45491,
                'type': 'readiness',
                'mean_hr_bpm': 74.53416,
                'version': '1.5.0',
                'physiological_age': 25,
                'effective_time': 0,
                'readiness': 62.5,
                'pns_index': -0.3011305,
                'sdnn_ms': 30.65533,
                'artefact_level': 'VERY LOW',
                'sd1_ms': 31.17043,
                'effective_prc': 0,
                'sd2_ms': 31.7047,
                'respiratory_rate': None,
                'create_timestamp': '2025-04-14T06:17:18.111239+00:00',
                'analysis_segments': {
                    'analysis_length': [30],
                    'analysis_start': [0],
                    'noise_length': [16.1],
                    'noise_start': [0]
                },
                'sns_index': 1.767119
            }
        }
    }

while True:
    Display.run(menu)
    
    
    


