# 🚦 ESP32-S3 紅綠燈 LED 模組教學（MicroPython）

本教學示範如何使用 **Seeed XIAO ESP32-S3** 搭配 **紅綠燈 LED 模組（共陰極）**，
透過 **MicroPython + Timer 定時器** 實作一個不使用 `while True + sleep()` 的交通號誌系統。

👉 **適合對象**：

* ESP32 / MicroPython 初學者
* 想理解 Timer、非阻塞程式設計的人
* 教學展示交通號誌 / 狀態切換範例

---

## 📦 使用模組說明

### 模組名稱（常見）

* 紅綠燈模組（Traffic Light LED Module）
* 三色 LED 紅綠燈模組
* LED Traffic Light Module

### 電氣特性

* **類型**：共陰極（Common Cathode）
* **控制邏輯**：

  * GPIO = `1` → LED 亮
  * GPIO = `0` → LED 滅

---

## 🔌 硬體接線說明

| LED 顏色 | ESP32-S3 GPIO |
| ------ | ------------- |
| 🔴 紅燈  | GPIO 9        |
| 🟡 黃燈  | GPIO 8        |
| 🟢 綠燈  | GPIO 7        |
| 共用腳    | GND           |

> ⚠️ 請確認模組為 **共陰極**，若是共陽極，控制邏輯需反轉。

---

## 🧠 程式設計概念

* 使用 `Timer` 週期性執行 callback
* 每 1 秒切換一次燈號
* 燈號順序：

  1. 紅燈
  2. 綠燈
  3. 黃燈

這種寫法不會阻塞主程式，適合進階專案使用。

---

## 💻 MicroPython 範例程式碼

```python
from machine import Pin, Timer

# === LED 腳位設定（共陰極：GPIO=1 亮） ===
red = Pin(9, Pin.OUT)
yellow = Pin(8, Pin.OUT)
green = Pin(7, Pin.OUT)

# === 燈號狀態表 ===
# (紅, 綠, 黃)
states = [
    (1, 0, 0),  # 紅燈
    (0, 1, 0),  # 綠燈
    (0, 0, 1),  # 黃燈
]

state_index = 0

def update_led(timer):
    global state_index

    r, g, y = states[state_index]
    red.value(r)
    green.value(g)
    yellow.value(y)

    state_index = (state_index + 1) % len(states)

# === 設定定時器 ===
tim = Timer(0)
tim.init(
    period=1000,              # 1 秒
    mode=Timer.PERIODIC,
    callback=update_led
)
```

---


