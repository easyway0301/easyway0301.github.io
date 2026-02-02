from machine import I2C, Pin  # 從 machine 模組匯入 I2C 和 Pin 類別，用來控制 I2C 通訊與腳位
import time  # 匯入 time 模組，用來延遲等待或計時

# 初始化 I2C（SHT31 的 Grove 介面用 GPIO5 / GPIO6）
i2c = I2C(0, scl=Pin(6), sda=Pin(5), freq=100000)  
# I2C(0)：使用 I2C 匯流排 0
# scl=Pin(6)：指定 SCL（時鐘線）接到 GPIO6
# sda=Pin(5)：指定 SDA（資料線）接到 GPIO5
# freq=100000：設定通訊頻率為 100kHz（標準模式）

SHT31_ADDR = 0x44  # SHT31 預設 I2C 位址為 0x44（十六進位表示）

def read_sht31():  # 定義函式 read_sht31()，用來讀取 SHT31 溫濕度感測器資料
    # 發送測量命令：高重複性模式
    i2c.writeto(SHT31_ADDR, b'\x24\x00')  
    # writeto：向指定 I2C 位址寫入資料
    # b'\x24\x00'：SHT31 高精度測量命令（資料表指定）

    time.sleep(0.015)  # 等感測器測量完成，約 15ms

    data = i2c.readfrom(SHT31_ADDR, 6)  
    # 從 SHT31 讀取 6 個位元組（2 byte 溫度 + 1 byte CRC + 2 byte 濕度 + 1 byte CRC）
    # data[0], data[1] → 溫度原始值
    # data[3], data[4] → 濕度原始值

    # 溫度計算公式（依資料表）
    temp_raw = data[0] << 8 | data[1]  
    # 將高位元組左移 8 位元，再與低位元組做 OR 運算，得到 16-bit 原始溫度數值
    temperature = -45 + (175 * temp_raw / 65535)  
    # SHT31 資料表公式：T = -45 + 175 * (temp_raw / 65535)
    # 將原始值轉換成攝氏溫度

    # 濕度計算公式（依資料表）
    humidity_raw = data[3] << 8 | data[4]  
    # 將高位元組左移 8 位元，再與低位元組做 OR 運算，得到 16-bit 原始濕度數值
    humidity = 100 * humidity_raw / 65535  
    # SHT31 資料表公式：RH = 100 * (humidity_raw / 65535)
    # 將原始值轉換成相對濕度百分比

    return temperature, humidity  # 回傳溫度與濕度

# 主程式測試
t, h = read_sht31()  # 呼叫函式讀取 SHT31 溫濕度
print("溫度: {:.2f} °C, 濕度: {:.2f} %".format(t, h))  
# 印出測得的溫度與濕度，保留小數點兩位

