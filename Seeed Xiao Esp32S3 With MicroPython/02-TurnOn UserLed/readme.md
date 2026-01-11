# ESP32-S3 MicroPython 入門教學

本教學以 **Seeed XIAO ESP32-S3** 為例，帶你從零開始認識開發板、設定 MicroPython，並完成第一個 LED 控制程式。內容適合初學者與教學使用。

---

## 📌 教學資源

👉 **請從這裡開始閱讀完整教學：**

* 🌐 **GitHub Pages（圖文版）**
  [https://easyway0301.github.io/Seeed%20Xiao%20Esp32S3%20With%20MicroPython/01-Flash%20MicroPython%20onto%20the%20Board/sop.html](https://easyway0301.github.io/Seeed%20Xiao%20Esp32S3%20With%20MicroPython/01-Flash%20MicroPython%20onto%20the%20Board/sop.html)

* 🎥 **YouTube（影片教學）**
  [https://youtu.be/c7OXmXeBEP4](https://youtu.be/c7OXmXeBEP4)

---

## 🧩 第一部分：認識 ESP32-S3 開發板

在開始之前，先來認識 **ESP32-S3 開發板上的 User LED**。

**面向板子正面（USB 接口朝上）時：**

* 💡 **User LED 位於 BOOT 按鈕下方**
* 💛 **亮燈顏色為黃色**

![XIAO ESP32-S3 Front](front-indication.png)

> 圖片來源：Seeed Studio 官方文件
> [https://wiki.seeedstudio.com/xiao_esp32s3_getting_started/](https://wiki.seeedstudio.com/xiao_esp32s3_getting_started/)

---

## 🧰 第二部分：開啟 Thonny 並測試 LED

以下範例為 **MicroPython** 程式，可直接貼到 **Thonny** 執行。

### 🔁 LED 開關測試程式

```python
from machine import Pin
import time

# 本範例適用：Seeed XIAO ESP32-S3 開發板
# TYPE-C 插頭朝上時，User LED 位於右側
# LED 亮燈時為「黃色」

# 設定 LED 腳位（GPIO 21）
UserLed = Pin(21, Pin.OUT)

def 打開UserLed():
    print("打開 UserLed")
    UserLed.value(0)  # 低電位亮燈

def 關掉UserLed():
    print("關掉 UserLed")
    UserLed.value(1)  # 高電位熄燈

打開UserLed()
print("暫停 2 秒")
time.sleep(2)
關掉UserLed()
```

📌 **說明：**

* ESP32-S3 的 User LED 為「**低電位亮燈**」
* `GPIO21` 為 XIAO ESP32-S3 內建 LED 腳位

---

## 🎬 完整操作影片

點擊下方圖片即可觀看完整教學影片（新分頁開啟）：

[![完整操作影片](http://img.youtube.com/vi/t7Ce9VMCXps/0.jpg)](https://youtu.be/t7Ce9VMCXps)

---

## ✅ 適合對象

* MicroPython 初學者
* ESP32 / XIAO 系列入門
* 教學 / 課堂示範 / 自學

---

## 📄 授權與使用

本教學內容可自由用於 **學習與教學**，如需轉載或改作，請註明來源。

---

✍️ 教學作者：ESP32 / MicroPython 教學創作者
🔧 使用開發板：Seeed XIAO ESP32-S3
