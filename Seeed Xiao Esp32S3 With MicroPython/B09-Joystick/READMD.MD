# BXX－搖桿模組（VRX / VRY / SW）｜MicroPython（Seeed XIAO ESP32S3）

本範例示範如何使用 **類比搖桿模組**（X 軸、Y 軸與按壓按鈕），  
在 **不使用 while 迴圈** 的情況下，**執行約 10 秒鐘** 讀取方向與按鈕狀態。

---

## 一、硬體接線說明

| 搖桿模組腳位 | 接到 Seeed XIAO ESP32S3 |
|-------------|------------------------|
| GND         | GND                    |
| VCC         | 3V3                    |
| VRX (X軸)   | GPIO 9                 |
| VRY (Y軸)   | GPIO 8                 |
| SW (按鈕)   | GPIO 7                 |

📌  
- SW 為 **按下 = 0（LOW）**
- X / Y 為類比輸出（0～4095）

---

## 二、程式說明重點

- 使用 `ADC` 讀取 X / Y 軸數值  
- 設定 **死區（DEAD ZONE）**，避免中心點抖動  
- 開機先進行 **中心點校正**
- 使用 `time.ticks_ms()` 控制執行 **約 10 秒**
- **不使用 while True**

---

## 三、MicroPython 範例程式碼（含逐行註解）

```python
from machine import ADC, Pin
import time

# === X / Y 軸 ADC 腳位設定 ===
vrx = ADC(Pin(9))   # VRX 接 GPIO9（X 軸）
vry = ADC(Pin(8))   # VRY 接 GPIO8（Y 軸）

# 設定 ADC 衰減（量測 0～3.3V）
vrx.atten(ADC.ATTN_11DB)
vry.atten(ADC.ATTN_11DB)

# 設定 ADC 解析度為 12-bit（0～4095）
vrx.width(ADC.WIDTH_12BIT)
vry.width(ADC.WIDTH_12BIT)

# === 按鈕（SW）設定，按下 = 0 ===
swi = Pin(7, Pin.IN, Pin.PULL_UP)

# 中心值與死區設定
CENTER = 2048
DEAD = 400   # 死區，避免輕微晃動誤判

# === 判斷方向的函式 ===
def get_direction(x, y):
    dx = x - CENTER
    dy = y - CENTER

    # 若在死區內，視為中間
    if abs(dx) < DEAD and abs(dy) < DEAD:
        return "中間"

    # 判斷 X 或 Y 偏移較大
    if abs(dx) > abs(dy):
        return "右" if dx > 0 else "左"
    else:
        return "下" if dy > 0 else "上"

# === 中心點校正（取多次平均）===
def calibrate_center(samples=50):
    sx = 0
    sy = 0
    for _ in range(samples):
        sx += vrx.read()
        sy += vry.read()
        time.sleep(0.01)
    return sx // samples, sy // samples

# 執行中心點校正
CENTER_X, CENTER_Y = calibrate_center()
CENTER = (CENTER_X + CENTER_Y) // 2
print("中心點校正:", CENTER_X, CENTER_Y)

# === 執行約 10 秒鐘 ===
start = time.ticks_ms()

while time.ticks_diff(time.ticks_ms(), start) < 10_000:
    x = vrx.read()           # 讀取 X 軸
    y = vry.read()           # 讀取 Y 軸
    direction = get_direction(x, y)

    # 若按鈕被按下
    if swi.value() == 0:
        print("🔘 按鈕按下")

    # 輸出狀態
    print("X:", x, "Y:", y, "方向:", direction)

    time.sleep(0.2)          # 每 0.2 秒讀一次

print("✅ 10 秒測試完成")
