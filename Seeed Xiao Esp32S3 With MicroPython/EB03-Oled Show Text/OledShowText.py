
from machine import Pin, I2C       # 匯入 I2C 類別
import ssd1306                     # 匯入 SSD1306 顯示驅動
import time                        # 匯入時間

# === 初始化 I2C ===
# scl 使用 GPIO6
# sda 使用 GPIO5
i2c = I2C(1, scl=Pin(6), sda=Pin(5), freq=400000)

# === 建立 OLED 物件 ===
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# === 清除畫面 ===
oled.fill(0)                      # 填滿黑色
oled.show()                       # 顯示更新

# === 顯示文字 ===
oled.text("Hello ESP32-S3", 0, 0) # 第一行
oled.text("OLED Text OK!", 0, 15) # 第二行
oled.show()                       # 推送到 OLED

# === 保持顯示 5 秒 ===
time.sleep(5)

# === 清除畫面 ===
oled.fill(0)                      # 填滿黑色
oled.show()                       # 顯示更新
