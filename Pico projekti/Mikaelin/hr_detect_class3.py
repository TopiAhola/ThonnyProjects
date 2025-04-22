import time
from machine import Pin, ADC, I2C
from ssd1306 import SSD1306_I2C
from fifo import Fifo
from piotimer import Piotimer

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
        self.threshold = 35000
        self.last_beat_time = time.ticks_ms()
        self.beat_detected = False
        self.bpm_list = []
        self.intervals = []
        self.avg_bpm = 0

        # Nappi GP8, GP7
        self.button = Pin(8, Pin.IN, Pin.PULL_UP)
        self.button_wave = Pin(7, Pin.IN, Pin.PULL_UP)
        
        self.show_waveform = False
        self.waveform = [self.height // 2] * self.width

        # Piotimer
        self.timer = Piotimer(freq=200, callback=self.sample)

    def sample(self, timer):
        try:
            self.raw_fifo.put(self.adc.read_u16())
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

    def button_wave_pressed(self):
        if self.button_wave.value() == 0:
            time.sleep(0.1) #debounce
            if self.button_wave.value() == 0:
                while self.button_wave.value() == 0:
                    time.sleep(0.1)
                print("Button pressed")
                return True
        return False

    def update_display(self):
        self.oled.fill(0)
        self.oled.text("BPM:", 0, 0)
        self.oled.text(str(self.avg_bpm), 30, 0)
        self.draw_heart(55, 0, size=1, filled=self.beat_detected)
        if self.show_waveform:
            for x in range(self.width):
                y = self.waveform[x]
                if 0 <= y < self.height:
                    self.oled.pixel(x, y, 1)
                    if y+1 < self.height:
                        self.oled.pixel(x, y+1, 1)
        self.oled.show()

    def button_pressed(self):
        if self.button.value() == 0:
            print("button_pressed")
            time.sleep(0.05)  # debounce
            return True
        return False

    def measure(self):
        print("Mittaus käynnistetty. Paina nappia (SW_1) lopettaaksesi.")

        while True:
            if self.button_pressed():
                print("Nappi painettu. Mittaus lopetetaan.")
                break

            while self.raw_fifo.has_data():
                if self.button_pressed():
                    return self.stop_measurement()
                
                if self.button_wave_pressed():
                    self.show_waveform = not self.show_waveform
                    print("Sykekäyrä:", "päällä" if self.show_waveform else "pois")
                
                raw = self.raw_fifo.get()
                now = time.ticks_ms()
                
                if self.show_waveform:
                    y = self.height - int((raw / 65535) * self.height)
                    self.waveform.pop(0)
                    self.waveform.append(y)

                # Sykehuipun tunnistus
                if raw > self.threshold and not self.beat_detected:
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

                elif raw < self.threshold - 3000:
                    self.beat_detected = False

                if self.bpm_list:
                    self.avg_bpm = int(sum(self.bpm_list) / len(self.bpm_list))

                self.update_display()

            time.sleep(0.001)
        
        return self.stop_measurement()

    def stop_measurement(self):
        self.timer.deinit()
        self.oled.fill(0)
        self.oled.text("Mittaus", 0, 20)
        self.oled.text("lopetettu", 0, 35)
        self.oled.show()
        return self.intervals

# Käynnistä mittaus automaattisesti
monitor = HeartRateMonitor()
ppi = monitor.measure()
print("PPI-arvot:", ppi)