from machine import Pin, I2C          # 從 machine 模組匯入 Pin 與 I2C 類別，用來控制 GPIO 與 I2C 通訊
import ssd1306                        # 匯入 SSD1306 OLED 顯示驅動模組

# === 初始化 I2C ===
i2c = I2C(1, scl=Pin(6), sda=Pin(5), freq=400000)  # 建立 I2C 物件，使用 I2C1，SCL 接 GPIO6，SDA 接 GPIO5，頻率 400kHz
oled = ssd1306.SSD1306_I2C(128, 64, i2c)          # 建立 OLED 物件，解析度 128x64，透過上面建立的 I2C 物件控制

# === 顯示文字函式 ===
def show(*lines):                # 定義 show 函式，可傳入多行文字參數
    oled.fill(0)                  # 將 OLED 畫面填滿黑色（清空畫面）
    y = 0                         # 初始 y 座標為 0，用來控制文字行位置
    for line in lines:            # 逐行讀取傳入的文字
        oled.text(line, 0, y)    # 在 OLED 畫面指定 x=0, y 位置顯示文字
        y += 15                   # y 座標增加 15 像素，為下一行文字預留空間
    oled.show()                   # 將畫面更新到 OLED，實際顯示文字
