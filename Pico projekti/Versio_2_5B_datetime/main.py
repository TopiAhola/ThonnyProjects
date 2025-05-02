from machine import UART, Pin, I2C, Timer, ADC, PWM, RTC
from ssd1306 import SSD1306_I2C
from fifo import Fifo
from umqtt.simple import MQTTClient
from Button import Encoder, Button
from safe2 import read_and_print_files, save_raw_data
import time, ujson, network, math, ntptime

# Display ASM class
class Display:
    # General Class methods:
    def __init__(self):
        self.state = self.fast_connect_1
        self.cursor_position = 0
        self.list_position = 0
        self.cycle_time = 0.05
        self.h_page = 0
        self.screen_time = 1
        self.last_measurement = {}
        self.measurements = []
        self.responses = []
        self.last_response = {}
        self.kubios_strings = [""]
        self.id = 0
        self.rtc = RTC()

    def get_measurements(self):
        # Tämä funktio formatoi palautusarvot oikein dictiksi.
        # Asettaan mittauksen id:n määrän perusteella.
        saved_measurements = read_and_print_files()
        for line in saved_measurements:
            dic = ujson.loads(line)
            try:
                if dic["response"]:
                    self.responses.append(dic["response"])
                    print("Lisätty response:", dic["response"])
            except:
                print("No kubios response")
            try:
                self.measurements.append(dic["measurement"])
            except:
                print("No measurement")
        self.id = len(self.measurements) + 1

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

    def reset_inputs(self):
        button.get()
        rtm_button.get()
        return_button.get()

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

    def scroll_list(self, id_list, list_name = ""):
        #scrolls a list. Alternative to update_cursor.
        visible_lines = 7
        first_index = self.list_position
        last_index = first_index + visible_lines-1
        len_list = len(id_list)
        if len(id_list) < visible_lines:
            visible_lines = len(id_list)

        enc1_input = 0
        while not enc1.fifo.empty():
            try:
                enc1_input = enc1_input + enc1.fifo.get()
            except:
                print("Fifo is empty..")
        self.cursor_position = self.cursor_position + enc1_input
        if self.cursor_position >= last_index:
            first_index = self.cursor_position-4
            last_index = self.cursor_position
        elif self.cursor_position < first_index:
            first_index = self.cursor_position
            last_index = self.cursor_position+4
        #else:
        #    first_index = self.cursor_position -2
        #    last_index = self.cursor_position +2
        self.list_position = first_index

        if first_index < 0:
            first_index = 0
            last_index = first_index + visible_lines-1
        elif last_index > len_list-1:
            last_index = len_list-1
            first_index = last_index - visible_lines+1

        if self.cursor_position > len_list-1:
            self.cursor_position = len_list-1
        if self.cursor_position < 0:
            self.cursor_position = 0

        self.render_list(id_list, first_index, last_index, list_name)
        time.sleep(self.cycle_time)


    def render_list(self, id_list, first_index, last_index, list_name = "List name"):
        # a separate listdrawing function
        #print("render_list:", id_list,self.cursor_position)
        if list_name == "Kubios results":
            oled.fill(0)
            oled.text(list_name,0,0,1)
            n = 1
            for ind in range(first_index, last_index+1):
                oled.text(f"{id_list[ind]["id"]:03}  {id_list[ind]["data"]["analysis"]["create_timestamp"]}", 8, 8 * n, 1)
                n = n + 1
            oled.text(">", 0, 8 * (1 +self.cursor_position-first_index), 1)
            oled.show()
        else:
            oled.fill(0)
            oled.text(list_name, 0, 0, 1)
            n = 1
            for ind in range(first_index, last_index + 1):
                oled.text(f"{id_list[ind]["id"]:03}", 8, 8 * n, 1)
                n = n + 1
            oled.text(">", 0, 8 * (1 + self.cursor_position - first_index), 1)
            oled.show()

    def hrv_analysis(self, ppi_list):
        # Mean Heart Rate
        mean_hr = math.floor((len(ppi_list)) / (sum(ppi_list) / 60000))

        # Mean peak-peak interval
        mean_ppi = math.floor(sum(ppi_list) / len(ppi_list))

        # Root mean square of successive differences (RMSSD):
        ppi_diff_squares = []
        for index in range(1, len(ppi_list)):
            ppi_diff = ppi_list[index] - ppi_list[index - 1]
            ppi_diff_squares.append(ppi_diff ** 2)
        mean_ppi_diff_squares = sum(ppi_diff_squares) / len(ppi_diff_squares)
        rmssd = math.sqrt(mean_ppi_diff_squares)

        # standard deviation of ppi:
        ppi_mean_diff_squares = []
        for index in range(1, len(ppi_list)):
            ppi_mean_diff_squares.append((ppi_list[index] - mean_ppi) ** 2)
        average = sum(ppi_mean_diff_squares) / (len(ppi_mean_diff_squares))
        sdnn = math.sqrt(average)

        return mean_hr, mean_ppi, rmssd, sdnn

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
        print("set nettime")
        try:
            ntptime.settime()
            #(year, month, day, weekday, hours, minutes, seconds, subseconds)
            time = self.rtc.datetime()            
            timezone = 3                   
            date_time = (time[0],time[1],time[2],time[3],time[4]+timezone,time[5],time[6],time[7])
            print(date_time)
            self.rtc.datetime(date_time)
            print("Time is:",self.rtc.datetime())
        except:
            print("Time not set!")
            self.rtc.datetime()
        self.state = self.main_menu
        self.reset_inputs() #This resets buttons pressed during intro

################################################################################
    # Main menu
    def main_menu(self):
        header: str = "Main Menu"
        print(header)
        text_lines: list[str] = [""]
        option_lines : list[str] = ["Measure HR", "Basic HRV", "Kubios HRV", "History"]
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

        if button.get():
            monitor.measure(999)
            self.state = self.main_menu

        elif rtm_button.get() or return_button.get():
            self.state = self.main_menu


        oled.fill(0)
        oled.text("Place your", 0, 0, 1)
        oled.text("finger on top of", 0, 9, 1)
        oled.text("the sensor", 0, 18, 1)
        oled.text("Press button", 0, 36, 1)
        oled.text("to start!", 0, 45, 1)

        if self.screen_time == 1:
            oled.text("-->", 92, 56, 1)
            self.screen_time += 1

        elif self.screen_time == 2:
            oled.text("-->", 104, 56, 1)
            self.screen_time -= 1

        oled.show()
        self.reset_inputs()
        time.sleep(1)


################################################################################
# Measure basic HRV menu
    def measure_basic_menu(self):
        header: str = "Measure basic HRV"
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

            if len(data) >= 0:
                self.last_measurement = { "id": self.id,"type": "PPI","data": data,"analysis": { "type": "readiness" } }
                self.measurements.append(self.last_measurement)
                save_raw_data({},self.last_measurement)
                self.id = len(self.measurements)+1
                self.show_last_measurement()
                self.state = self.main_menu
            else:
                self.state = self.measure_basic_menu_error


        elif rtm_button.get() or return_button.get():
            self.state = self.main_menu
        self.reset_inputs()
        time.sleep(self.cycle_time)

########################################
# Show basic HRV results
    def show_last_measurement(self):
        header: str = "Measurement"
        print(header)
        measurement = self.last_measurement
        mean_hr, mean_ppi, rmssd, sdnn = self.hrv_analysis(measurement["data"])
        while True:
            oled.fill(0)
            oled.text(f"Measurement {measurement["id"]}", 0, 0, 1)
            oled.text(f"", 0, 9, 1)
            oled.text(f"Mean HR: {mean_hr} /min", 0, 18, 1)
            oled.text(f"Mean PPI: {mean_ppi} ms", 0, 27, 1)
            oled.text(f"RMSSD: {rmssd:5.2f}", 0, 36, 1)
            oled.text(f"SDNN: {sdnn:5.2f}ms", 0, 45, 1)
            oled.show()

            time.sleep(self.cycle_time)

            rtm_button_input = rtm_button.get()
            return_button_input = return_button.get()
            button_input = button.get()
            if rtm_button_input:
                self.update_cursor(0)
                self.state = self.main_menu
                break
            elif button_input or return_button_input:
                self.update_cursor(0)
                self.state = self.measurement_history_menu
                break

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
            data = monitor.measure(33) # Mittaa yli 30s dataa ja palauuttaa listan.
            if len(data) >= 0:
                self.last_measurement = { "id": self.id,"type": "PPI","data": data,"analysis": { "type": "readiness" }}
                self.measurements.append(self.last_measurement)
                self.id = len(self.measurements)+1
                self.state = self.kubios_menu1
            else:
                self.state = self.measure_basic_menu_error

        elif rtm_button.get() or return_button.get():
            self.state = self.main_menu
        self.reset_inputs()
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
        self.reset_inputs()
        time.sleep(self.cycle_time)

########################################
    # Kubios menu1 sends Kubios request
    def kubios_menu1(self):
        header: str = "Kubios Menu 1"
        print(header)

        if kubios.test():
            oled.fill(0)
            oled.text("Uploading last", 0, 8, 1)
            oled.text("measurement...", 0, 16, 1)
            oled.show()
            kubios.send_request(self.last_measurement)
            self.state = self.kubios_menu2

        else:
            self.state = self.kubios_menu_error
        self.reset_inputs()
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

        elif kubios.check_response():
            self.last_response = kubios.get_response()
            self.responses.append(self.last_response)
            save_raw_data(self.last_response, self.last_measurement)
            self.state = self.show_kubios_result
        else:
            pass
        self.reset_inputs()
        time.sleep(1)

########################################
    #Shows kubios response
    def show_kubios_result(self):
        header: str = "Kubios Response:"
        print(header)

        if self.kubios_strings[0] != f"id: {self.id}":
            self.kubios_strings = self.response_string(self.last_response)

        #elif self.kubios_strings[0] == f"id: {self.id}": #
        self.update_cursor(len(self.kubios_strings)-5)
        oled.fill(0)
        oled.text("Kubios results:", 0, 0, 1)
        n = 0
        for line in self.kubios_strings[self.cursor_position: self.cursor_position+5]:
            oled.text(line, 0, 8+8*n, 1)
            n = n+1
        oled.show()

        if button.get() or rtm_button.get() or return_button.get():
            self.state = self.kubios_analysis
        self.reset_inputs()
        time.sleep(self.cycle_time)



########################################
# Shows analysis based on kubios response
    def kubios_analysis(self):
        header: str = "Kubios Analysis:"
        print(header)

        oled.fill(0)
        oled.text("This will show", 0, 0, 1)
        oled.text("Kubios analysis", 0, 9, 1)
        oled.text("results.", 0, 18, 1)
        oled.show()

        if button.get() or rtm_button.get() or return_button.get():
            self.state = self.main_menu
        self.reset_inputs()
        time.sleep(self.cycle_time)

########################################

    def kubios_menu_error(self):
        header: str = "Kubios Error"
        print(header)
        oled.fill(0)
        oled.text("Connection error", 0, 0, 1)
        oled.text("", 0, 9, 1)
        oled.text("Please wait", 0, 18, 1)
        oled.text("to retry.", 0, 27, 1)
        oled.text(" ", 0, 36, 1)
        oled.text("Press any button", 0, 45, 1)
        oled.text("to return.", 0, 54, 1)
        oled.show()

        if kubios.test():
            self.state = self.kubios_menu1
            time.sleep(1)
        elif button.get() or rtm_button.get() or return_button.get():
            self.state = self.main_menu
        else:
            kubios.connect()
            self.state = self.kubios_menu_error

        self.reset_inputs()
        time.sleep(self.cycle_time)
################################################################################
    #History menu
    def history_menu(self):
        header: str = "History Menu"
        print(header)
        text_lines: list[str] = [""]
        option_lines : list[str] = ["Kubios results","Measurements","","<-back"]
        options = [self.kubios_history_menu, self.measurement_history_menu]
        self.select_option(options)
        self.update_cursor(len(options))
        self.render_menu(header,text_lines, option_lines)


        if rtm_button.get() or return_button.get():
            self.state = self.main_menu
        self.reset_inputs()
        time.sleep(self.cycle_time)

########################################
    #Measurement history
    def measurement_history_menu(self):
        header: str = "Measurements"
        button_input = button.get()
        rtm_button_input = rtm_button.get()
        return_button_input = return_button.get()

        if len(self.measurements) > 0:
            self.scroll_list(self.measurements, "Measurements")

            button_input = button.get()
            rtm_button_input = rtm_button.get()
            return_button_input = return_button.get()

            if button_input:
                self.reset_inputs()
                self.history_show_measurement(self.cursor_position)
            elif rtm_button_input:
                self.state = self.main_menu
            elif return_button_input:
                self.state = self.history_menu
        else:
            oled.fill(0)
            oled.text("No saved", 0, 9, 1)
            oled.text("measurements.", 0, 18, 1)
            oled.show()
            if button_input or rtm_button_input or return_button_input:
                self.state = self.history_menu
        self.reset_inputs()
        time.sleep(self.cycle_time)

########################################
    # Kubios history menu
    def kubios_history_menu(self):
        header: str = "Kubios results"
        button_input = button.get()
        rtm_button_input = rtm_button.get()
        return_button_input = return_button.get()

        if len(self.responses) > 0:
            self.scroll_list(self.responses, "Kubios results")

            button_input = button.get()
            rtm_button_input = rtm_button.get()
            return_button_input = return_button.get()

            if button_input:
                self.reset_inputs()
                self.history_show_response(self.responses[self.cursor_position])
                self.reset_inputs()
                self.history_show_analysis(self.responses[self.cursor_position])
            elif rtm_button_input:
                self.state = self.main_menu
            elif return_button_input:
                self.state = self.history_menu
        else:
            oled.fill(0)
            oled.text("No saved Kubios", 0, 9, 1)
            oled.text("responses.", 0, 18, 1)
            oled.show()
            if button_input or rtm_button_input or return_button_input:
                self.state = self.history_menu
        self.reset_inputs()
        time.sleep(self.cycle_time)

########################################
    # Measurement
    def history_show_measurement(self, measurement_index):
        header: str = "Measurement"
        print(header)
        measurement = self.measurements[measurement_index]
        mean_hr, mean_ppi, rmssd, sdnn = self.hrv_analysis(measurement["data"])
        while True:
            oled.fill(0)
            oled.text(f"Measurement {measurement["id"]}", 0, 0, 1)
            oled.text(f"", 0, 9, 1)
            oled.text(f"Mean HR: {mean_hr} /min", 0, 18, 1)
            oled.text(f"Mean PPI: {mean_ppi} ms", 0, 27, 1)
            oled.text(f"RMSSD: {rmssd:5.2f}", 0, 36, 1)
            oled.text(f"SDNN: {sdnn:5.2f}ms", 0, 45, 1)
            oled.show()

            time.sleep(self.cycle_time)

            rtm_button_input = rtm_button.get()
            return_button_input = return_button.get()
            button_input = button.get()
            if rtm_button_input:
                self.update_cursor(0)
                self.state = self.main_menu
                break
            elif button_input or return_button_input:
                self.update_cursor(0)
                self.state = self.measurement_history_menu
                break

########################################
    #
    def history_show_response(self, response):
        header: str = "Response"
        print(header)
        response_strings = self.response_string(response)
        while True:
            self.update_cursor(len(response_strings) - 5)
            oled.fill(0)
            oled.text("Kubios results:", 0, 0, 1)
            n = 0
            for line in response_strings[self.cursor_position: self.cursor_position + 5]:
                oled.text(line, 0, 8 + 8 * n, 1)
                n = n + 1
            oled.show()

            time.sleep(self.cycle_time)

            rtm_button_input = rtm_button.get()
            return_button_input = return_button.get()
            button_input = button.get()
            if rtm_button_input:
                self.update_cursor(0)
                self.state = self.main_menu
                break
            elif button_input:
                self.update_cursor(0)
                self.state = self.history_menu
                break
            elif return_button_input:
                self.update_cursor(0)
                self.state = self.history_menu
                break


    def history_show_analysis(self, response):
        #Shows analysis for a stored response
        header: str = "Saved Kubios Analysis:"
        print(header)
        while True:
            oled.fill(0)
            oled.text("This will show", 0, 0, 1)
            oled.text("Kubios analysis", 0, 9, 1)
            oled.text("from history.", 0, 18, 1)
            oled.show()

            if button.get() or rtm_button.get() or return_button.get():
                self.state = self.kubios_history_menu
                self.reset_inputs()
                break
            time.sleep(self.cycle_time)



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

# Kubios definition:
from Kubios import Kubios
kubios = Kubios()

# Pulse monitor
from hrmonitor import HeartRateMonitor
monitor = HeartRateMonitor()

# Haetaan tallennetut tiedostot:
menu.get_measurements()

while True:
    Display.run(menu)
    
    
    


