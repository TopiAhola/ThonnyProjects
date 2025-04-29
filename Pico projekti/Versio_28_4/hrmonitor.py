import time
from machine import Pin, ADC, I2C
from ssd1306 import SSD1306_I2C
from fifo import Fifo
from piotimer import Piotimer
from Button import Button
#

class HeartRateMonitor:
    def __init__(self):
        # OLED ja I2C
        self.i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
        self.oled = SSD1306_I2C(128, 64, self.i2c)

        # ADC ja FIFO
        self.adc = ADC(1)
        self.raw_fifo = Fifo(50)

        # Näytön asetukset
        self.width = 128
        self.height = 64

        # Sykeparametrit
        self.baseline_values = Fifo(50)
        self.dynamic_threshold = 35000
        self.last_beat_time = time.ticks_ms()
        self.beat_detected = False
        self.bpm_list = []
        self.intervals = []
        self.avg_bpm = 0
        #self.samples_list = []

        # Nappi
        self.button = Button(Pin(8, Pin.IN, Pin.PULL_UP))

        # Aaltomuoto
        self.show_waveform = True
        self.waveform = [self.height // 2] * self.width

        # Suodatettu signaali
        self.filtered_value = 0

    def sample(self, timer):
        try:
            raw = self.adc.read_u16()
            self.raw_fifo.put(raw)
        except RuntimeError:
            pass
    
    def draw_heart(self, x, y, size=1, filled=True):
        shape = [
            " 00 00 ",
            "0000000",
            "0000000",
            " 00000 ",
            "  000  ",
            "   0   "
        ]
        for row, line in enumerate(shape):
            for col, c in enumerate(line):
                if c == "0":
                    for dx in range(size):
                        for dy in range(size):
                            self.oled.pixel(x + col * size + dx, y + row * size + dy, 1 if filled else 0)
        

    def update_display(self):
        self.oled.fill(0)
        self.oled.text("BPM:", 0, 0)
        self.oled.text(str(self.avg_bpm), 30, 0)
        self.draw_heart(55, 0, size=1, filled=self.beat_detected)
        if self.show_waveform:
            for x in range(1, self.width):
                y1 = self.waveform[x - 1]
                y2 = self.waveform[x]
                if 0 <= y1 < self.height and 0 <= y2 < self.height:
                    self.oled.line(x - 1, y1, x, y2, 1)
        self.oled.show()
        
    def button_pressed(self):
        return self.button.get()

    def stop_measurement(self):
        # Varmistetaan, että timer deinitoi oikein
        if hasattr(self, "timer"):
            try:
                self.timer.deinit()  # Poistaa timerin käytöstä
                del self.timer  # Poistetaan timer-objekti, jos se on vielä olemassa
            except Exception as e:
                print(f"Virhe timerin poistamisessa: {e}")
        
        # Tyhjennetään puskurit
        if hasattr(self, "raw_fifo"):
            del self.raw_fifo  # Poistetaan FIFO
        if hasattr(self, "baseline_values"):
            del self.baseline_values  # Poistetaan baseline_values
        
        self.oled.fill(0)
        self.oled.text("Mittaus", 0, 20)
        self.oled.text("lopetettu", 0, 35)
        self.oled.show()
        return self.intervals

    def measure(self, duration=30):
        if not hasattr(self, "raw_fifo"):
            self.raw_fifo = Fifo(50)
        self.bpm_list = []
        self.intervals = []
        self.avg_bpm = 0
        self.last_beat_time = time.ticks_ms()
        self.beat_detected = False
        self.waveform = [self.height // 2] * self.width
        self.filtered_value = 0
        self.samples_list = []

        while hasattr(self, "timer") and self.timer:
            self.timer.deinit()
        self.timer = Piotimer(freq=100, callback=self.sample)
        print("Mittaus käynnissä...")

        alpha = 0.5 # suodattimen herkkyys
        start_time = time.ticks_ms()

        while True:
            if self.button.get():
                break
            
            elapsed_time = time.ticks_diff(time.ticks_ms(), start_time)
            if elapsed_time >= (duration * 1000):
                break
            
            read_count = 0
            while self.raw_fifo.has_data() and read_count < 5:
                raw = self.raw_fifo.get()
                self.filtered_value = (1 - alpha) * self.filtered_value + alpha * raw
                self.samples_list.append(int(self.filtered_value))
                read_count += 1
                
                print(raw, self.dynamic_threshold)
                
            if len(self.samples_list) > 50:
                self.samples_list = self.samples_list[-50:]
                
            if self.samples_list:
                sum_baseline = sum(self.samples_list)
                sum_sq_baseline = sum(x*x for x in self.samples_list)
                fifo_length = len(self.samples_list)
                
                average = sum_baseline // fifo_length
                variance = (sum_sq_baseline // fifo_length) - (average * average)
                std = int(variance ** 0.5)
                self.dynamic_threshold = average + 1.7 * std
                
            else:
                self.dynamic_threshold = 35000
                
            now = time.ticks_ms()
            
            if self.show_waveform:
                y = self.height - int((self.filtered_value / 65535) * self.height)
                self.waveform.pop(0)
                self.waveform.append(y)
                
            # Sykehuipun tunnistus
            if self.filtered_value > self.dynamic_threshold and not self.beat_detected:
                interval = time.ticks_diff(now, self.last_beat_time)
                if interval > 250:
                    bpm = int(60000 / interval)
                    self.bpm_list.append(bpm)
                    self.intervals.append(interval)
                    self.last_beat_time = now
                    self.beat_detected = True
                    print("Huippu havaittu! BPM:", bpm)

                    if len(self.bpm_list) > 10:
                        self.bpm_list.pop(0)

            elif self.filtered_value < self.dynamic_threshold:
                self.beat_detected = False

            if self.bpm_list:
                self.avg_bpm = int(sum(self.bpm_list) / len(self.bpm_list))

            self.update_display()
            time.sleep(0.001)

        return self.stop_measurement()

# Käynnistä mittaus
if __name__ == "__main__":
    monitor = HeartRateMonitor()
    ppi = monitor.measure(30)
    print("PPI-arvot:", ppi)