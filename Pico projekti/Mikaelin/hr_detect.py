import time
from machine import Pin, ADC, I2C, UART, Timer, PWM
from ssd1306 import SSD1306_I2C

i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
oled = SSD1306_I2C(128, 64, i2c)

adc = ADC(1)

# oled
width = 128
height = 64

# käyrän keskitys
center_y = height // 2

# skaalataan jotta käyrä mahtuu näytölle
def scale(value):
    return int((value / 65535) * height)

# bufferi aikasemmille arvoille
waveform = [center_y] * width

# hr variables
threshold = 36000
last_beat_time = time.ticks_ms()
beat_detected = False
bpm_list = []
avg_bpm = 0

# sydän
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

while True:
    # lukee sensorin arvon ja skaalataan
    raw = adc.read_u16()
    #print("ADC:", raw)
    y = height - scale(raw)  # käännetään y-akseli, jotta käyrät näkyy ylöspäin

    # jatkuva tulostus
    waveform.pop(0)
    waveform.append(y)
    
    now = time.ticks_ms()
    
    if raw > threshold and not beat_detected:
        beat_detected = True
        interval = time.ticks_diff(now, last_beat_time)
        
        if interval > 250:
            bpm = int (60000 / interval)
            bpm_list.append(bpm)
            last_beat_time = now
            
            if len(bpm_list) > 10:
                bpm_list.pop(0)
            
    elif raw < threshold - 3000:
        beat_detected = False
    if bpm_list:
        avg_bpm = int(sum(bpm_list) / len(bpm_list))
    
    # tyhjennetään näyttö
    oled.fill(0)

    # piirretään käyrä
    for x in range(width):
        oled.pixel(x, waveform[x], 1)
        
    oled.text("BPM:", 0, 0)
    oled.text(str(avg_bpm), 30, 0)
    
    if beat_detected:
        draw_heart(55, 0, size = 1, filled = True)
    else:
        draw_heart(55, 0, size = 1, filled = False)

    oled.show()
    time.sleep(0.001)
