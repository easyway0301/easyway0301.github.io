# ESP32-S3 MicroPython 入門教學 — Capacitive Touch + User LED

本章示範如何在 **Seeed XIAO ESP32-S3** 上使用 **TouchPad 電容感測功能（GPIO9）**  
結合 **User LED** 控制，做到觸碰時亮燈的互動效果。

👉 **完整線上教學頁（GitHub Pages）**  
🔗 https://easyway0301.github.io/Seeed%20Xiao%20Esp32S3%20With%20MicroPython/04-Capacitive%20Touch%20UserLed/sop.html

---

## 📌 教學重點

本範例實現以下功能：:contentReference[oaicite:2]{index=2}

- 🧠 使用 **GPIO9** 作為 TouchPad 讀取電容觸控數值  
- 🔢 讀取原始觸控感測值並比較門檻  
- 💡 若超過門檻，則 **點亮 User LED**  
- 🔁 程式持續讀值並即時反應

---

## 📷 Pin 與圖片

![Pin List for XIAO ESP32-S3](Pin-List.png)

> 圖片來源：Seeed Studio 官方文件（XIAO ESP32-S3 硬體說明）

---

## 🧑‍💻 MicroPython 範例程式

⚠️ 本程式為 **無限迴圈**，若要停止執行請在 Thonny 內連按兩次 `Ctrl + C`。

```python
from machine import TouchPad, Pin
import time

# 使用 GPIO9 的 TouchPad 觸控功能
touch = TouchPad(Pin(9))

# 設定門檻值（需依實際環境調整）
# 未觸碰：約 17331
# 觸碰：約 147034
THRESHOLD = 50000

# 設定 User LED 腳位（貼片式 LED 在 GPIO21）
UserLed = Pin(21, Pin.OUT)

def 打開UserLed():
    print("打開 UserLed")
    UserLed.value(0)  # 低電位亮燈

def 關掉UserLed():
    print("關掉 UserLed")
    UserLed.value(1)  # 高電位熄燈

# 無限讀值與控制迴圈
while True:
    # 讀取觸控原始數值
    val = touch.read()
    print(val)

    # 比較是否超過門檻
    if val > THRESHOLD:
        print("⚡ GPIO9 被觸碰！")
        打開UserLed()
    else:
        關掉UserLed()

    # 延遲避免讀值過快
    time.sleep(0.1)
