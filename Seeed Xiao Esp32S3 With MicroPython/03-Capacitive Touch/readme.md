# ESP32-S3 MicroPython 入門教學

## Capacitive Touch（電容觸控）實作教學（GPIO1）

本教學示範如何在 **Seeed XIAO ESP32-S3** 上，使用 **MicroPython** 讀取電容觸控（TouchPad）數值，並判斷 GPIO 是否被觸碰。

👉 **完整線上教學頁（GitHub Pages）**
🔗 [https://easyway0301.github.io/Seeed%20Xiao%20Esp32S3%20With%20MicroPython/03-Capacitive%20Touch/sop.html](https://easyway0301.github.io/Seeed%20Xiao%20Esp32S3%20With%20MicroPython/03-Capacitive%20Touch/sop.html)

---

## 🧩 硬體說明

* 開發板：**Seeed XIAO ESP32-S3**
* 使用功能：**Capacitive Touch（電容觸控）**
* 觸控腳位：**GPIO 1**

> ESP32-S3 內建 TouchPad，可直接感測人體或導線接觸所造成的電容變化，不需額外感測模組。

![Pin List](Pin-List.png)

圖片來源：Seeed Studio 官方文件
[https://wiki.seeedstudio.com/xiao_esp32s3_getting_started/](https://wiki.seeedstudio.com/xiao_esp32s3_getting_started/)

---

## 🧪 觸控數值說明

實測參考數值（僅供參考，實際需依環境調整）：

* **未觸碰**：約 `17331`
* **有觸碰**：約 `147034`

因此本範例使用以下門檻值：

```python
THRESHOLD = 50000
```

---

## 🧑‍💻 MicroPython 範例程式

⚠️ 此程式為 **無限迴圈**，若要停止執行，請在 **Thonny 連續按兩次 `Ctrl + C`**。

```python
from machine import TouchPad, Pin
import time

# 使用 GPIO1 的 Touch 功能
touch = TouchPad(Pin(1))

# 根據實測數值設定門檻
# 未觸碰：約 17331
# 觸  碰：約 147034
THRESHOLD = 50000

# 進入無限迴圈
# ⚠️ 若要停止程式，需在 Thonny 按兩次 Ctrl + C
while True:
    # 讀取觸控感測值
    # ESP32-S3 TouchPad 特性：
    # - 沒碰時：數值較小
    # - 觸碰時：數值會變得很大
    val = touch.read()

    # 印出原始數值，方便觀察與校正
    print(val)

    # 判斷是否被觸碰
    if val > THRESHOLD:
        print("⚡ GPIO1 被觸碰")

    # 延遲，避免刷太快
    time.sleep(0.1)
```

---

## 🎯 教學重點整理

* 使用 `TouchPad(Pin(x))` 啟用電容觸控
* 需先 **實測數值** 再設定門檻
* 門檻值會受以下因素影響：

  * 手指 / 導線
  * 電線長度
  * 濕度與環境

---

## 🚀 延伸應用建議

* TouchPad + **LED 指示燈**
* TouchPad + **蜂鳴器**
* 多個 Touch 腳位做成 **按鍵面板**
* 電容觸控版 **互動裝置 / 教具**

---

## 📌 適合對象

* MicroPython 初學者
* ESP32-S3 入門學習者
* 國中 / 高中 / 創客教學
* 互動裝置、感測專題

---

✍️ 教學作者：EasyWay
📦 平台：ESP32 / MicroPython / Seeed Studio
