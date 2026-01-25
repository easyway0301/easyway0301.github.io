# 從 machine 模組匯入 Pin（腳位控制）與 I2C（I2C 通訊）
from machine import Pin, I2C

# 匯入 SSD1306 OLED 顯示器的驅動程式
import ssd1306

# 匯入波特律動網站做的文字
from font16 import FONT16

# 建立 I2C 物件
# I2C(0)            → 使用 I2C 匯流排 0
# sda=Pin(5)        → 設定 SDA 腳位為 GPIO5（XIAO Expansion Board）
# scl=Pin(6)        → 設定 SCL 腳位為 GPIO6（你實測可用）
# freq=400000       → 設定 I2C 通訊速度為 400kHz（Fast Mode）
i2c = I2C(0, sda=Pin(5), scl=Pin(6), freq=400000)

# 掃描 I2C 匯流排上所有裝置
# 正常情況下會看到：
# 0x3C（60）→ OLED
# 0x51（81）→ Expansion Board 上的 EEPROM
print(i2c.scan())

# 建立 SSD1306 OLED 物件
# 128, 64   → OLED 解析度為 128x64
# i2c       → 使用上面建立的 I2C 物件
# addr=0x3C → 指定 OLED 的 I2C 位址為 0x3C
oled = ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3C)

# 清空整個畫面（填滿 0 = 黑色）
oled.fill(0)

# 在 (x=0, y=0) 的位置顯示文字
oled.text16("你好嗎", 0, 0)

# 將緩衝區的內容真正顯示到 OLED 螢幕上
oled.show()

