from machine import Pin
import neopixel
import time

pin = Pin(9, Pin.OUT)
# WS2812 4顆LED燈
np = neopixel.NeoPixel(pin, 4)

for i in range(4):
    np.fill((0, 0, 0))   # 全滅
    np[i] = (0, 0, 255) # 藍色
    np.write()
    time.sleep(0.3)
    
np.fill((0, 0, 0))   # 全滅
np.write()
