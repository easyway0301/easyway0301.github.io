from machine import Pin, PWM   # 匯入 Pin 與 PWM 類別，用來控制 GPIO 與硬體 PWM
import time                    # 匯入 time 模組，用來做延遲（微秒級）

# ===== 定義 IR 發射類別 =====
class IRSender:
    def __init__(self, pin=1, freq=38000):
        # 建立 PWM 物件，控制紅外線 LED 載波
        # pin: 使用哪個 GPIO 腳位輸出
        # freq: PWM 頻率，NEC 協議通常 38kHz
        # duty=0: 初始不輸出紅外線
        self.pwm = PWM(Pin(pin), freq=freq, duty=0)

    # 發射紅外線脈衝序列
    # pulses: [mark, space, mark, space ...] 單位為微秒
    def send(self, pulses):
        if not pulses:
            return False             # 若脈衝序列為空，直接返回 False 表示發射失敗

        for i, duration in enumerate(pulses):
            if i % 2 == 0:
                self.pwm.duty(512)  # 偶數 index = mark，紅外線開啟，duty 50%
            else:
                self.pwm.duty(0)    # 奇數 index = space，紅外線關閉
            time.sleep_us(duration)  # 延遲對應微秒數，維持 mark/space 寬度

        self.pwm.duty(0)            # 發射完成後，確保紅外線關閉
        return True                 # 回傳 True 表示發射成功
