from machine import I2C, Pin
import time
import ustruct

# 初始化 I2C
i2c = I2C(1, scl=Pin(6), sda=Pin(5), freq=100000)
print(i2c.scan())

# BMP180 I2C 地址
BMP180_ADDR = 0x77

# 讀取校正數據
def read_calibration():
    calib = i2c.readfrom_mem(BMP180_ADDR, 0xAA, 22)
    return ustruct.unpack(">hhhHHhhhhhh", calib)

AC1, AC2, AC3, AC4, AC5, AC6, B1, B2, MB, MC, MD = read_calibration()

# 讀取原始溫度
def read_raw_temp():
    i2c.writeto_mem(BMP180_ADDR, 0xF4, b'\x2E')  # 溫度測量指令
    time.sleep_ms(5)
    raw = i2c.readfrom_mem(BMP180_ADDR, 0xF6, 2)
    return ustruct.unpack(">H", raw)[0]

# 讀取原始氣壓
def read_raw_pressure(oss=0):
    i2c.writeto_mem(BMP180_ADDR, 0xF4, bytes([0x34 + (oss << 6)]))
    time.sleep_ms(2 + 3 * (1 << oss))
    msb = i2c.readfrom_mem(BMP180_ADDR, 0xF6, 1)[0]
    lsb = i2c.readfrom_mem(BMP180_ADDR, 0xF7, 1)[0]
    xlsb = i2c.readfrom_mem(BMP180_ADDR, 0xF8, 1)[0]
    return ((msb << 16) + (lsb << 8) + xlsb) >> (8 - oss)

# 計算溫度 (°C)
def get_temperature():
    UT = read_raw_temp()
    X1 = ((UT - AC6) * AC5) >> 15
    X2 = (MC << 11) // (X1 + MD)
    B5 = X1 + X2
    T = (B5 + 8) >> 4
    return T / 10, B5

# 計算氣壓 (Pa)
def get_pressure():
    oss = 0  # oversampling
    UT, B5 = get_temperature()[0]*10, get_temperature()[1]
    UP = read_raw_pressure(oss)
    B6 = B5 - 4000
    X1 = (B2 * (B6 * B6 >> 12)) >> 11
    X2 = (AC2 * B6) >> 11
    X3 = X1 + X2
    B3 = (((AC1 * 4 + X3) << oss) + 2) >> 2
    X1 = (AC3 * B6) >> 13
    X2 = (B1 * ((B6 * B6) >> 12)) >> 16
    X3 = ((X1 + X2) + 2) >> 2
    B4 = (AC4 * (X3 + 32768)) >> 15
    B7 = (UP - B3) * (50000 >> oss)
    if B7 < 0x80000000:
        p = (B7 * 2) // B4
    else:
        p = (B7 // B4) * 2
    X1 = (p >> 8) * (p >> 8)
    X1 = (X1 * 3038) >> 16
    X2 = (-7357 * p) >> 16
    p = p + ((X1 + X2 + 3791) >> 4)
    return p

# 計算高度 (m)
def get_altitude(p, p0=101325):
    return 44330 * (1 - (p / p0) ** (1/5.255))

# 執行一次讀取
temperature, B5 = get_temperature()
pressure = get_pressure()
altitude = get_altitude(pressure)

print("溫度:", temperature, "°C")
print("氣壓:", pressure, "Pa")
print("高度:", altitude, "m")


