from machine import Pin, PWM
import time

# PWM 腳位
pwm_pin = PWM(Pin(9))
pwm_pin.freq(50)  # SG90 標準 50Hz

def rotate(speed_ms):
    """
    speed_ms: PWM 脈衝寬度對應 (ms)
        1.0 ~ 2.0 ms
        1.5ms 停止
    """
    duty = int(speed_ms / 20 * 1023)  # 將 20ms 週期轉成 ESP32 10bit duty
    pwm_pin.duty(duty)

# 順時針慢速
rotate(1.7)
time.sleep(2)

# 停止
rotate(1.5)
time.sleep(1)

# 逆時針慢速
rotate(1.3)
time.sleep(2)

# 停止
rotate(1.5)
time.sleep(1)       

