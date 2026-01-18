# VS1838B 紅外線接收模組（IR Receiver）教學

本章示範如何使用 **VS1838B 紅外線接收模組** 搭配 **Seeed XIAO ESP32-S3 + MicroPython**  
以 **IRQ 中斷方式** 偵測是否有紅外線訊號。

👉 對應完整 SOP 教學可參考 → GitHub Pages  
https://easyway0301.github.io/Seeed%20Xiao%20Esp32S3%20With%20MicroPython/B15-Keyes%20Vs1838B%20IR%20Receiver/sop.html

---

## 📌 模組簡介

VS1838B 是一款常見的 **38kHz 紅外線接收模組**，內建解調電路，可將 38kHz 紅外線訊號轉成數位輸出。  
本範例示範在 **10 秒內偵測是否收到紅外線訊號**，並打印結果。

---

## 🔌 接線方式（Seeed XIAO ESP32-S3）

| VS1838B | ESP32-S3 |
|---------|----------|
| VCC     | 3V3      |
| GND     | GND      |
| OUT     | GPIO 9   |

📌 VS1838B 的輸出為 **Active LOW**（接收到 38kHz 紅外線時輸出變為 LOW）:contentReference[oaicite:0]{index=0}

---

## 📦 使用函式庫

- `machine`  
- `time`

---

## 🧪 範例程式碼

以下程式碼可在 Thonny 上執行，並在 10 秒內偵測是否有紅外線輸入：

```python
from machine import Pin
import time

# ========= VS1838B 紅外線接收 =========

# 將 GPIO9 設定為輸入，用來接收紅外線訊號
ir = Pin(9, Pin.IN)

# 接收狀態旗標，用來記錄是否收到紅外線
收到紅外線 = False

def ir_callback(pin):
    # 使用全域變數記錄接收狀態
    global 收到紅外線
    收到紅外線 = True

    # 偵測到紅外線時顯示提示
    print("📡 偵測到紅外線")

# 設定中斷
# VS1838B 偵測到紅外線時，OUT 腳位會變成 LOW
ir.irq(trigger=Pin.IRQ_FALLING, handler=ir_callback)

print("開始接收紅外線（10 秒）")
# 等待 10 秒接收紅外線
time.sleep(10)

# 停止中斷接收
ir.irq(handler=None)

print("接收結束")

# 根據旗標判斷結果
if 收到紅外線:
    print("✅ 10 秒內有收到紅外線")
else:
    print("❌ 10 秒內沒有收到紅外線")
