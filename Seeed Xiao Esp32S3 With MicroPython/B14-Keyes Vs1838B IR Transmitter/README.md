# Bxx－紅外線發射模組（IR Transmitter）

## 📌 模組說明
紅外線發射模組可發送 **38kHz 紅外線載波訊號**，  
常用於電視、冷氣、音響等遙控器應用。

本範例使用 **Seeed XIAO ESP32S3 + MicroPython**，  
示範「**單次發射紅外線訊號（不使用 while 迴圈）**」。

---

## 🔌 接線方式

| 紅外線模組 | ESP32S3 |
|-----------|--------|
| VCC       | 3V3    |
| GND       | GND    |
| SIG       | GPIO 9 |

📌 建議紅外線 LED 串接 **限流電阻（100Ω～220Ω）**

---

## 📦 使用模組 / 函式庫
- `machine`
- `time`

---

## 🧪 範例程式碼（單次發射）

```python
from machine import Pin, PWM
import time

# ========= 紅外線發射設定 =========

# 建立 PWM 物件
# GPIO 9：紅外線輸出腳位
# freq=38000：38kHz 紅外線載波
# duty=0：初始為關閉
ir = PWM(Pin(9), freq=38000, duty=0)

def 發射紅外線(duration_ms):
    # 開啟紅外線（輸出 38kHz PWM）
    ir.duty(512)          # 約 50% duty
    
    # 維持指定時間（毫秒）
    time.sleep_ms(duration_ms)
    
    # 關閉紅外線
    ir.duty(0)

print("開始發射紅外線")

# 發射 500 ms（0.5 秒）
發射紅外線(500)

print("發射完成")
