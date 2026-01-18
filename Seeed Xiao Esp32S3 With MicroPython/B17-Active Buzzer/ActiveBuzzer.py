from machine import Pin
import time

# 有源蜂鳴器Active Buzzer
# 蜂鳴器正極接在GPIO 9，負極接GND
buzzer = Pin(9, Pin.OUT)

for i in range(10):
    buzzer.value(1)
    time.sleep(0.2)
    buzzer.value(0)
    time.sleep(0.2)
