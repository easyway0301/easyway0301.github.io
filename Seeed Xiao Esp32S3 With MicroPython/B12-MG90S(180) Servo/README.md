# ESP32-S3 MicroPython MG90S 180度伺服馬達教學

使用 PWM 控制角度的簡單示範，適合初學者控制舵機或機器手臂。

---

## 模組介紹

MG90S 小型伺服馬達可由 PWM 控制角度，常用於機器手臂、舵機控制或簡單旋轉裝置。

📌 注意事項：
- 不要讓馬達持續轉到極限角度，容易損壞
- 不要用手直接旋轉齒輪，避免損壞內部馬達

### 接線方式 (Seeed XIAO ESP32-S3)：
- 黃色線 → GPIO 9 (控制訊號)
- 紅色線 → 3V3
- 褐色線 → GND

---

## MicroPython 程式碼

以下程式碼可在 Thonny 上執行，控制 MG90S 轉到指定角度，每個角停 2 秒：

```python
from machine import Pin, PWM        # 匯入 Pin 與 PWM 類別
import time                         # 匯入時間模組

# === 初始化 PWM ===
servo = PWM(Pin(9), freq=50)        # 將 GPIO9 設為 PWM 輸出，頻率 50Hz

# === 設定角度函式 ===
def set_angle(angle):
    min_duty = 0.025                # 0.5ms 對應 0°
    max_duty = 0.125                # 2.5ms 對應 180°
    duty = min_duty + (max_duty - min_duty) * (angle / 180)  # 計算對應 PWM
    servo.duty_u16(int(65535 * duty))                          # 設定 PWM

# === 控制範例 ===
print("go 5")                        # 向右轉到 5°
set_angle(5)
time.sleep(2)                         # 停留 2 秒

print("go 175")                      # 向左轉到 175°
set_angle(175)
time.sleep(2)                         # 停留 2 秒

print("go 90")                       # 回到中間 90°
set_angle(90)
time.sleep(2)                         # 停留 2 秒

# === 停止 PWM ===
servo.deinit()                        # 停止 PWM
