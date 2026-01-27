import network  # 匯入網路模組，用來控制 Wi-Fi
import socket   # 匯入 socket 模組，用來建立 TCP/UDP server
import time     # 匯入時間模組，可以用 sleep 延遲

# ---------- AP 設定 ----------
SSID = "ESP32_AP"        # Wi-Fi 熱點名稱
PASSWORD = "12345678"    # Wi-Fi 密碼（至少 8 個字元）

# 建立 AP 物件（ESP32 當 Wi-Fi 熱點）
ap = network.WLAN(network.AP_IF)

# 如果 AP 已經啟動，先停掉舊 AP，確保可以重複 bind
if ap.active():
    ap.active(False)
    print("已停掉舊的 AP")

# 啟動 AP
ap.active(True)
# 設定 SSID、密碼、加密模式 authmode=3 → WPA2
ap.config(essid=SSID, password=PASSWORD, authmode=3)
print("AP 已啟動")
print("SSID:", SSID)
print("密碼:", PASSWORD)
# 印出 AP 的 IP
print("IP:", ap.ifconfig()[0])

# 建立 TCP server
# getaddrinfo 取得監聽位址 0.0.0.0 表示所有網路介面，port 80
addr = socket.getaddrinfo("0.0.0.0", 80)[0][-1]
s = socket.socket()  # 建立 TCP socket
# ✅ 設定 socket 可重複使用位址，避免端口衝突
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(addr)         # 綁定 IP 與 port
s.listen(1)          # 開始監聽，最多 1 個 client 等待
print("TCP Server 已建立，port 6666")

try:
    while True:  # 無限迴圈，持續監聽 client
        try:
            cl, addr = s.accept()  # 接受 client 連線
            print("Client 連線:", addr)  # 印出 client 位址
            data = cl.recv(1024).decode()  # 接收最多 1024 bytes，並解碼成字串
            print("收到:", data)  # 印出收到的資料

            # 回傳簡單訊息給 Client（HTTP response）
            cl.send("HTTP/1.1 200 OK\r\n\r\nHello ESP32".encode())
            cl.close()  # 關閉 client socket
        except Exception as e:
            print("Client error:", e)  # 捕捉 client 錯誤，不停止 server
except KeyboardInterrupt:
    print("停止 AP 與 TCP Server")  # 按 Ctrl+C 停止程式
finally:
    s.close()        # 關閉 server socket
    ap.active(False) # 停用 AP 模式

