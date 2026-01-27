import network
import socket
import time
from machine import Pin
import time

# ===== Wi-Fi 設定 =====
SSID = "你的WiFi名稱"
PASSWORD = "你的WiFi密碼"

# 啟動 STA
sta = network.WLAN(network.STA_IF)
sta.active(True)
sta.connect(SSID, PASSWORD)

# 等待連線
while not sta.isconnected():
    time.sleep(1)

ip = sta.ifconfig()[0]
print("IP:", ip)

# ===== HTTP Server =====
addr = socket.getaddrinfo("0.0.0.0", 80)[0][-1]
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(addr)
s.listen(1)

# ===== 先前控制LED的範例TurnOnUserLed.py =====
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

print("HTTP Server Ready")
print("打開UserLed：http://" + ip + "/turnOn")
print("關掉UserLed：http://" + ip + "/turnOff")

while True:
    cl, addr = s.accept()
    print("Client:", addr)

    req = cl.recv(1024).decode()
    print("REQ:")
    print(req)

    # 👉 只判斷一個 REQ
    if "GET /turnOn " in req:
        print("✅ 收到 打開UserLed 請求")
        打開UserLed()
        response = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: text/html; charset=utf-8\r\n"
            "\r\n"
            "打開UserLed OK"
        )

        
    if "GET /turnOff " in req:
        print("✅ 收到 關掉UserLed 請求")
        關掉UserLed()
        response = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: text/html; charset=utf-8\r\n"
            "\r\n"
            "關掉UserLed OK"
        )

    cl.send(response.encode())
    cl.close()

