from time import sleep_ms
from machine import I2C, Pin
from esp8266_i2c_lcd import I2cLcd

# I2C LCD 預設位址
DEFAULT_I2C_ADDR = 0x27

# 建立 I2C & LCD 物件
i2c = I2C(scl=Pin(6), sda=Pin(5), freq=100000)
lcd = I2cLcd(i2c, DEFAULT_I2C_ADDR, 2, 16)

# 清除螢幕
lcd.clear()

# 顯示固定文字
lcd.move_to(0, 0)
lcd.putstr("Hello ESP8266")

lcd.move_to(0, 1)
lcd.putstr("LCD Display OK")

# 保持顯示
while True:
    sleep_ms(1000)


