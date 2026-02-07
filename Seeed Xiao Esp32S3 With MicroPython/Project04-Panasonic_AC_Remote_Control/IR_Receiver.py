from machine import Pin
import time
from array import array  # ✅ 只匯入 class


RX_PIN = 6
MAX_LEN = 800  # 固定大小 array，比 append 快
IDLE_US = 500_000  # 40ms 判斷封包結束

# 使用 array 儲存脈衝
pulses = array('I', [0]*MAX_LEN)
idx = 0

_last = time.ticks_us()

def irq_handler(pin):
    global _last, pulses, idx
    now = time.ticks_us()
    diff = time.ticks_diff(now, _last)
    _last = now
    if diff < 100:   # 過短視為雜訊
        return
    if idx < MAX_LEN:
        pulses[idx] = diff
        idx += 1
    else:
        # 超過 max_len，自動停 IRQ
        pin.irq(handler=None)

# attach both edges
ir = Pin(RX_PIN, Pin.IN)

#time.sleep(5)
ir.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=irq_handler)

print("請按遙控器按鍵（保持按一秒以上）...")

start_time = time.ticks_us()
while True:
    # 如果已收到資料，並且最後一次脈衝距離現在 > IDLE_US
    if idx > 1 and time.ticks_diff(time.ticks_us(), _last) > IDLE_US:
        break
    # 避免無限等待
    if time.ticks_diff(time.ticks_us(), start_time) > 5_000_000:  # 5秒
        break

# 停掉 IRQ
ir.irq(handler=None)

print("原始pulses:",pulses)

print("收完，共", len(pulses), "脈衝")
# 映射規則函數
def map_pulse(val):
    if val >= 10000:
        return 10368
    elif 3000 <= val <= 4000:
        return 3488
    elif 1500 <= val <= 2800:
        return 1728
    elif 1000 <= val <= 1500:
        return 1296
    elif 600 <= val <= 1000:
        return 864
    elif 1 <= val <= 600:
        return 432
    else:
        return 0  # 無法判斷

# 重新整理並去掉 0
mapped_pulses = array('I', [mp for mp in (map_pulse(p) for p in pulses) if mp != 0])

print("整理後脈衝長度:", len(mapped_pulses))
print("整理後脈衝:", mapped_pulses)
