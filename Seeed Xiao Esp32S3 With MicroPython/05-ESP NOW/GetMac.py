import network
# 匯入 network 模組，用來控制 ESP32 的 Wi-Fi 功能

wlan = network.WLAN(network.STA_IF)
# 建立一個 Wi-Fi 物件，並設定為「STA（Station，用戶端）」模式

wlan.active(True)
# 啟用 Wi-Fi（一定要先啟用，才能使用 Wi-Fi / ESP-NOW 等功能）

print(wlan.config('mac'))
# 讀取並印出目前 Wi-Fi 介面的 MAC 位址（bytes 格式）
# 這個 MAC 位址常用在 ESP-NOW 當作 peer_mac
