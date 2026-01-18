from machine import UART, Pin
import time

# UART 設定 (TX=9, RX=8, 9600 bps)
uart = UART(2, baudrate=9600, tx=9, rx=8)
# TXD要接在8，RXD接在9，跟上面相反！！！

# 儲存接收到的訊號
ir_codes = []

print("開始接收紅外線訊號...按 Ctrl+C 停止接收")

try:
    while True:
        if uart.any():  # UART 有資料
            data = uart.read()
            if data:
                # 將接收到的 bytes 轉成 hex string
                code = data.hex()
                print("接收到 IR code:", code)
                ir_codes.append(code)
        time.sleep(0.05)

except KeyboardInterrupt:
    print("接收結束，共儲存", len(ir_codes), "筆訊號")

# 發射儲存的訊號
print("開始發射儲存的紅外線訊號...")
for code in ir_codes:
    # 將 hex string 轉回 bytes
    uart.write(bytes.fromhex(code))
    print("已發射:", code)
    time.sleep(0.5)

print("全部訊號發射完成")

