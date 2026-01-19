# https://easyway0301.github.io/Seeed Xiao Esp32S3 With MicroPython/02-TurnOn UserLed/sop.html
# 以下為02-TurnOn UserLed範例
from machine import Pin
import time

# 本範例適用Seeed XIAO Esp32S3開發板
# TYPEC插頭朝上，UserLed燈在右邊，打開是黃燈。

# 設定 LED 腳位
# 貼片式LED燈焊在GPIO 21 
UserLed = Pin(21, Pin.OUT)

def 打開UserLed():
    print("打開UserLed")
    # LED 亮燈
    UserLed.value(0)
    #UserLed.off() # 注意如果要用off，它會亮燈

def 關掉UserLed():
    print("關掉UserLed")
    # LED 熄燈
    UserLed.value(1)
    #UserLed.on() # 注意如果要用on，它會關燈
# 以上為02-TurnOn UserLed範例

import network
# 匯入 network 模組，用來控制 ESP32 的 Wi-Fi 功能

import espnow
# 匯入 ESP-NOW 模組，用來進行點對點無線通訊

# -------------------------------------------------
# 啟動 Wi-Fi STA（Station，用戶端）模式
# -------------------------------------------------
sta = network.WLAN(network.STA_IF)
# 建立 Wi-Fi 物件，設定為 STA 模式

sta.active(True)
# 啟用 Wi-Fi 功能（ESP-NOW 需要 Wi-Fi 介面 active）

sta.disconnect()
# 避免自動連線到 Wi-Fi AP，確保 ESP-NOW 收發穩定

# -------------------------------------------------
# 初始化 ESP-NOW
# -------------------------------------------------
espReceiver = espnow.ESPNow()
# 建立 ESP-NOW 物件

espReceiver.active(True)
# 啟用 ESP-NOW 功能

# -------------------------------------------------
# 等待接收資料
# -------------------------------------------------
print("等待接收資料...")
while True:
    host, msg = espReceiver.recv()  # 阻塞等待接收 ESP-NOW 資料

    if msg:
        text = msg.decode("utf-8")  # 將 bytes 轉成 UTF-8 字串
        # 中文指令必須 decode 才能比對

        if text == "打開UserLed":
            print("收到開燈指令")
            打開UserLed()  # 呼叫函式開啟 User LED

        elif text == "關掉UserLed":
            print("收到關燈指令")
            關掉UserLed()  # 呼叫函式關閉 User LED
