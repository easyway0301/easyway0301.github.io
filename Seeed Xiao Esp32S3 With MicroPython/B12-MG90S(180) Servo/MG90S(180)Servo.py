from machine import Pin, PWM
import time

# 黃色線接GPIO 9
# 紅外線接3V3
# 褐色線接GND
servo = PWM(Pin(9), freq=50)

# 非常保守的範圍
def set_angle(angle):
    min_duty = 0.025  # 0.5ms
    max_duty = 0.125  # 2.5ms
    duty = min_duty + (max_duty - min_duty) * (angle / 180)
    servo.duty_u16(int(65535 * duty))

# 注意不要一直轉過頭，會弄壞。
# 注意不要用手直接轉動齒輪

# 會向右轉
print("go 5")
set_angle(5)
time.sleep(2)

# 會向左轉
print("go 175")
set_angle(175)
time.sleep(2)

print("go 90")
set_angle(90)
time.sleep(2)

