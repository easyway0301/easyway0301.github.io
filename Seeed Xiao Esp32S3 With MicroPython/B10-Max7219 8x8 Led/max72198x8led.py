from machine import Pin, SPI
import max7219
import time

# 初始化 SPI
spi = SPI(1, baudrate=10000000, polarity=0, phase=0,
          sck=Pin(7), mosi=Pin(9))
cs = Pin(8, Pin.OUT)

# 初始化 MAX7219，1 個 8x8 模組
display = max7219.Matrix8x8(spi, cs, 1)
display.brightness(5)  # 亮度 0~15
display.fill(0)
display.show()

# 簡單字母對照字典 (A~H)
letters = {
    "H": [0x42,0x42,0x42,0x7E,0x42,0x42,0x42,0x00],
    "E": [0x7E,0x40,0x40,0x7C,0x40,0x40,0x7E,0x00],
    "L": [0x40,0x40,0x40,0x40,0x40,0x40,0x7E,0x00],
    "O": [0x3C,0x42,0x42,0x42,0x42,0x42,0x3C,0x00]
}

text = "HELLO"

# 用 for 迴圈顯示文字，每個字停 0.5 秒
for char in text:
    display.fill(0)
    pattern = letters.get(char, [0]*8)
    for row in range(8):
        display.pixel(row, 0, (pattern[row] & 0x80) >> 7)
        display.pixel(row, 1, (pattern[row] & 0x40) >> 6)
        display.pixel(row, 2, (pattern[row] & 0x20) >> 5)
        display.pixel(row, 3, (pattern[row] & 0x10) >> 4)
        display.pixel(row, 4, (pattern[row] & 0x08) >> 3)
        display.pixel(row, 5, (pattern[row] & 0x04) >> 2)
        display.pixel(row, 6, (pattern[row] & 0x02) >> 1)
        display.pixel(row, 7, (pattern[row] & 0x01))
    display.show()
    time.sleep(0.5)

