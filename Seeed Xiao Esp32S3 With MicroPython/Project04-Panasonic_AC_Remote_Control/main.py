import network
import time
import ure

import StaModeHttpServer as http
import OledShowText as oled
from IR_Sender import IRSender
import IR_Codes

# ===== WiFi =====
SSID = "您家的SSID"
PASSWORD = "您家的PASSWORD"

sta = network.WLAN(network.STA_IF)
if sta.active():
    sta.active(False)
time.sleep(0.5)
sta.active(True)
sta.connect(SSID, PASSWORD)

oled.show("WiFi Connecting...")
while not sta.isconnected():
    time.sleep(0.5)

ip = sta.ifconfig()[0]
oled.show("WiFi OK", "IP:", ip)
print("IP:", ip)

# ===== IR =====
ir = IRSender(pin=1)

def send_ir(code_name):
    pulses = IR_Codes.CODES.get(code_name)
    if pulses:
        ir.send(pulses)
        print("IR pulses:", pulses)  
        print("IR 發射:", code_name)  

# ===== HTTP =====
server = http.start_server()
oled.show("HTTP Server Ready", ip)  # OLED 只顯示 IP

def on_request(cl):
    req = cl.recv(1024).decode()
    #print("REQ:", req)

    # 直接用 if 判斷 URL，對應 IR
    for url, code_name in IR_Codes.CODES.items():
        if f"GET /{url} " in req:
            send_ir(url)
            response_body = f"{url} 發射完成"
            break
    else:
        response_body = "未知指令"

    response = (
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: text/plain; charset=utf-8\r\n\r\n"
        + response_body
    )
    cl.send(response.encode('utf-8'))

# ===== 主迴圈 =====
while True:
    http.handle_client(server, on_request)
    time.sleep_ms(10)

