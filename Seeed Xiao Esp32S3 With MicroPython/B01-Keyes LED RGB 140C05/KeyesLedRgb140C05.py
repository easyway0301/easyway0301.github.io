import machine, time

# 科易KEYES LED 140C05　RGB全彩LED模組(共陽極)10mm LED 140C05

# 共陽極 RGB LED
red = machine.Pin(9, machine.Pin.OUT)
blue = machine.Pin(8, machine.Pin.OUT)
green = machine.Pin(7, machine.Pin.OUT)

# 全部關燈（共陽極：1 = 關）
red.value(1)
green.value(1)
blue.value(1)

# 顏色清單（0 = 亮）
colors = [
    (0, 1, 1),  # 紅
    (1, 0, 1),  # 綠
    (1, 1, 0),  # 藍
]

for r, g, b in colors:
    red.value(r)
    green.value(g)
    blue.value(b)
    time.sleep(1)

    # 關燈
    red.value(1)
    green.value(1)
    blue.value(1)
    time.sleep(0.5)

print("結束了")

