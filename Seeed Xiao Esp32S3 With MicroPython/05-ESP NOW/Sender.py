import network
# 匯入 network 模組，用來控制 ESP32 的 Wi-Fi 功能

import espnow
# 匯入 ESP-NOW 模組，用來做 ESP32 之間的無線點對點通訊

import time
# 匯入 time 模組，用來做延遲（sleep）

# -------------------------------------------------
# 啟動 Wi-Fi STA（Station，用戶端）模式
# -------------------------------------------------
sta = network.WLAN(network.STA_IF)
# 建立 Wi-Fi 物件，設定為 STA 模式（ESP-NOW 需要）

sta.active(True)
# 啟用 Wi-Fi（不需要連上基地台）

sta.disconnect()
# 中斷任何自動連線的 Wi-Fi AP
# 避免被 AP 綁定 Channel，導致 ESP-NOW 收不到資料

# -------------------------------------------------
# 初始化 ESP-NOW
# -------------------------------------------------
espSender = espnow.ESPNow()
# 建立 ESP-NOW 物件

espSender.active(True)
# 啟用 ESP-NOW 功能

# -------------------------------------------------
# 設定接收端（對方）ESP32 的 MAC 位址
# -------------------------------------------------
peer_mac = b'\x90pi\x0b\xe28'
# 對方 ESP32 的 MAC 位址（bytes 格式）
# 可用 wlan.config('mac') 在對方板子上查詢

espSender.add_peer(peer_mac)
# 將對方加入 ESP-NOW 的通訊對象（peer）

# -------------------------------------------------
# 開始傳送資料
# -------------------------------------------------
print("Start sending...")
# 顯示開始傳送訊息

# -------------------------------------------------
# 傳送「打開 User LED」指令
# -------------------------------------------------
espSender.send(peer_mac, "打開UserLed".encode("utf-8"))
# 將中文字串轉成 UTF-8 bytes 後送出
# ESP-NOW 只能傳送 bytes 資料

time.sleep(2)
# 等待 2 秒，讓接收端有時間處理第一個指令

# -------------------------------------------------
# 傳送「關掉 User LED」指令
# -------------------------------------------------
espSender.send(peer_mac, "關掉UserLed".encode("utf-8"))
# 再次送出 UTF-8 編碼的中文指令

print("傳送完成")
# 傳送完成

