from machine import Pin, I2C
import ssd1306
import time

# =====================
# I2C 設定
# =====================
i2c = I2C(0, sda=Pin(5), scl=Pin(6), freq=400000)

# =====================
# OLED 設定（SSD1306）
# =====================
oled = ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3C)

# =====================
# RTC（PCF8563）位址
# =====================
RTC_ADDR = 0x51

# =====================
# BCD 轉十進位
# =====================
def bcd_to_dec(b):
    return (b >> 4) * 10 + (b & 0x0F)

# =====================
# 從 PCF8563 讀取時間
# =====================
def read_rtc():
    # 從暫存器 0x02 開始讀 7 bytes
    data = i2c.readfrom_mem(RTC_ADDR, 0x02, 7)

    second = bcd_to_dec(data[0] & 0x7F)
    minute = bcd_to_dec(data[1] & 0x7F)
    hour   = bcd_to_dec(data[2] & 0x3F)
    day    = bcd_to_dec(data[3] & 0x3F)
    month  = bcd_to_dec(data[5] & 0x1F)
    year   = 2000 + bcd_to_dec(data[6])

    return year, month, day, hour, minute, second

# 校時程式（只跑一次）
def dec_to_bcd(d):
    return ((d // 10) << 4) | (d % 10)

def set_rtc(year, month, day, hour, minute, second):
    i2c.writeto_mem(0x51, 0x02, bytes([
        dec_to_bcd(second),
        dec_to_bcd(minute),
        dec_to_bcd(hour),
        dec_to_bcd(day),
        0,  # 星期（可忽略）
        dec_to_bcd(month),
        dec_to_bcd(year - 2000)
    ]))

# 👇 改成現在的時間，只跑一次
# 設完後 立刻註解掉 / 刪掉這段
#否則每次開機都會被重設。

#set_rtc(2026, 1, 13, 19, 0, 0)

# =====================
# 主迴圈：每秒更新畫面
# =====================
while True:
    year, month, day, hour, minute, second = read_rtc()

    oled.fill(0)

    # 顯示日期
    oled.text("{:04d}-{:02d}-{:02d}".format(year, month, day), 0, 0)

    # 顯示時間
    oled.text("{:02d}:{:02d}:{:02d}".format(hour, minute, second), 0, 16)

    oled.show()

    time.sleep(1)
