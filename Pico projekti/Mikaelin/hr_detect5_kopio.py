import time
from machine import Pin, ADC, I2C
from ssd1306 import SSD1306_I2C
from fifo import Fifo
from piotimer import Piotimer
import ujson

# OLED & I2C
i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
oled = SSD1306_I2C(128, 64, i2c)
adc = ADC(1)

# OLED
width = 128
height = 64
center_y = height // 2

# FIFO syötteen puskurille
raw_fifo = Fifo(512)

# Graafin arvot
waveform = [center_y] * width

# HR-mittauksen muuttujat
threshold = 35000
last_beat_time = time.ticks_ms()
beat_detected = False
bpm_list = []
intervals = []
avg_bpm = 0

# Mittauksen pituus 
measurement_duration = 10000
start_time = time.ticks_ms()

# Skaalaus näytölle
def scale(value):
    return int((value / 65535) * height)

# sydän OLED:lle
def draw_heart(x, y, size=1, filled=True):
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
                        oled.pixel(x + col * size + dx, y + row * size + dy, 1 if filled else 0)

# Tallennus TXT-tiedostoon
def save_session_data(bpm_list, intervals, date_str, time_str):
    bpm_list = [int(bpm) for bpm in bpm_list]
    intervals = [int(interval) for interval in intervals]

    try:
        with open("session_data3.txt", "a") as f:
            f.write("Päivämäärä: {}\n".format(date_str))
            f.write("Aikaleima: {}\n".format(time_str))
            f.write("BPM-lista: {}\n".format(", ".join(map(str, bpm_list))))
            f.write("Väliajat (ms): {}\n".format(", ".join(map(str, intervals))))
            f.write("-" * 40 + "\n")
        print("Mittaus tallennettu tiedostoon.")
    except Exception as e:
        print("Virhe tallennuksessa:", e)


# Piotimer ottaa näytteitä
def sample(timer):
    raw = adc.read_u16()
    try:
        raw_fifo.put(raw)
    except RuntimeError:
        pass

timer = Piotimer(freq=200, callback=sample)

# Pääsilmukka
while True:
##    now = time.ticks_ms()

#     # Tallenna mittaus session lopussa
#     if time.ticks_diff(now, start_time) >= measurement_duration:
#         date_str = "2025-04-14"
#         time_str = "{:02d}:{:02d}:{:02d}".format(*time.localtime()[3:6])
# 
#         save_session_data(bpm_list, intervals, date_str, time_str)
# 
#         bpm_list.clear()
#         intervals.clear()
#         start_time = time.ticks_ms()

    # Lue FIFOsta dataa ja piirrä
    if raw_fifo.has_data():
        raw = raw_fifo.get()
        y = height - scale(raw)

        waveform.pop(0)
        waveform.append(y)

        # Huipputunnistus toimii kuten "toimivassa" versiossa
        if raw > threshold and not beat_detected:
            interval = time.ticks_diff(now, last_beat_time)

            if interval > 250:
                bpm = int(60000 / interval)
                bpm_list.append(bpm)
                intervals.append(interval)
                last_beat_time = now
                beat_detected = True
                print("Huippu havaittu! BPM:", bpm)

                if len(bpm_list) > 10:
                    bpm_list.pop(0)
        elif raw < threshold - 3000:
            beat_detected = False

        if bpm_list:
            avg_bpm = int(sum(bpm_list) / len(bpm_list))

        # OLED-piirto
        oled.fill(0)

        # Piirrä graafi
        for x in range(width):
            oled.pixel(x, waveform[x], 1)

        oled.text("BPM:", 0, 0)
        oled.text(str(avg_bpm), 30, 0)

        if beat_detected:
            draw_heart(55, 0, size=1, filled=True)
        else:
            draw_heart(55, 0, size=1, filled=False)

        oled.show()

    time.sleep(0.01)

