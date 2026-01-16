# B04 – OLED SH1106 Display 教學（ESP32-S3 + MicroPython）

本章示範如何使用 **SH1106 I2C OLED 顯示模組（128×64）**  
搭配 **Seeed XIAO ESP32-S3**，用 **MicroPython** 顯示文字。

👉 完整 SOP 教學頁：  
https://easyway0301.github.io/Seeed%20Xiao%20Esp32S3%20With%20MicroPython/B04-OLED%20SH1106%20Display/sop.html

---

## 📌 第一步：認識 SH1106 OLED 模組

SH1106 是一款常見的 **128×64 單色 OLED 顯示器**，  
通常使用 **I2C 通訊** 與主控板連接。:contentReference[oaicite:0]{index=0}

### 📍 模組特性

- 顯示解析度：128 × 64  
- 通訊方式：I2C  
- 常見 I2C 位址：`0x3C` :contentReference[oaicite:1]{index=1}

---

## 🔌 第二步：I2C 接線（Seeed XIAO ESP32-S3）

OLED 與 XIAO ESP32-S3 的連接方式如下：

| OLED | XIAO ESP32-S3 |
|------|----------------|
| VCC  | 3V3 |
| GND  | GND |
| SDA  | GPIO5 |
| SCL  | GPIO6 |

> ⚠️ 請確認 GND 共地，否則顯示會失敗。:contentReference[oaicite:2]{index=2}

---

## 🧠 第三步：MicroPython 顯示範例程式

以下程式可在 Thonny 等 MicroPython IDE 上執行，  
在 SH1106 OLED 上顯示三行文字：:contentReference[oaicite:3]{index=3}

```python
from machine import Pin, I2C     # 匯入 Pin 與 I2C 類別
import sh1106                     # 匯入 SH1106 OLED 驅動
import time                       # 匯入時間模組

# === 建立 I2C 物件 ===
# scl 使用 GPIO6
# sda 使用 GPIO5
i2c = I2C(
    scl=Pin(6),
    sda=Pin(5),
    freq=400000
)

# === 建立 OLED 顯示物件 ===
oled = sh1106.SH1106_I2C(
    128,      # 螢幕寬度 128
    64,       # 螢幕高度 64
    i2c,
    addr=0x3C
)

# === 清除畫面 ===
oled.fill(0)                     # 清空畫面

# === 顯示文字 ===
oled.text("ESP32-S3", 0, 0)      # 第一行
oled.text("MicroPython", 0, 16)  # 第二行
oled.text("SH1106 OLED", 0, 32)  # 第三行

# === 更新顯示 ===
oled.show()                     # 把緩衝區內容更新到 OLED

