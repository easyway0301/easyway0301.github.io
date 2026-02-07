from machine import Pin            # 從 machine 模組匯入 Pin，用來操作 GPIO
import time                        # 匯入 time 模組，用來取得微秒時間

ir = Pin(6, Pin.IN)                # 將 GPIO6 設定為輸入腳位，接紅外線接收器輸出腳

pulses = []                        # 建立一個 list，用來儲存每一段脈衝的時間長度
last = time.ticks_us()             # 紀錄上一次中斷發生的時間（微秒）

def irq(pin):                      # 定義 GPIO 中斷處理函式
    global last, pulses             # 使用全域變數 last 與 pulses
    now = time.ticks_us()           # 取得目前時間（微秒）
    pulses.append(                 # 將兩次中斷之間的時間差加入 pulses
        time.ticks_diff(now, last)  # 計算 now 與 last 的差值（避免溢位）
    )
    last = now                     # 更新 last 為本次中斷時間

ir.irq(                            # 設定 GPIO 中斷
    trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING,  # 上升沿與下降沿都觸發
    handler=irq                    # 指定中斷處理函式
)

print("📡 IR Receiver ready")      # 提示紅外線接收器已就緒

while True:
    time.sleep(0.1)  # 100ms 檢查一次

    # 如果已經有資料，而且 50ms 沒再收到新脈衝
    if pulses and time.ticks_diff(time.ticks_us(), last) > 50_000:
        print("📥 pulses 數量 =", len(pulses))
        print("📥 pulses =", pulses)
        pulses = []   # 只在「真的結束」後才清空
        