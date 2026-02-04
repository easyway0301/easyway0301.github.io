import machine              # 匯入 machine 模組，用來控制硬體
import time                 # 匯入 time 模組，提供延遲功能
import dht                  # 匯入 MicroPython 內建的 DHT 驅動

# 建立 DHT22 物件，資料腳位接在 GPIO9
dht22 = dht.DHT22(machine.Pin(9))

try:
    dht22.measure()         # 觸發一次量測（必須先呼叫）
    
    temp = dht22.temperature()  # 讀取溫度（攝氏）
    hum = dht22.humidity()      # 讀取濕度（百分比）

    # 格式化輸出溫溼度
    print("🌡 溫度: {:.1f}°C, 💧 濕度: {:.1f}%".format(temp, hum))

except OSError as e:
    # 若感測器沒有回應，會進入例外處理
    print("讀取失敗:", e)
