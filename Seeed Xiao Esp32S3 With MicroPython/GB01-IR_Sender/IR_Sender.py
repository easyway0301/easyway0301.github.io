from machine import Pin, PWM          # 從 machine 模組匯入 Pin（腳位）與 PWM（硬體 PWM）
import time                           # 匯入 time 模組，用來做微秒延遲

# =========================
# NEC IR 發射器（單檔版）
# =========================

class IRSender:                       # 定義一個紅外線發射類別
    def __init__(self, pin=1, freq=38000):  # 建構子，設定輸出腳位與載波頻率
        self.pwm = PWM(               # 建立 PWM 物件
            Pin(pin),                 # 指定 PWM 使用的 GPIO 腳位
            freq=freq,                # 設定 PWM 頻率為 38kHz（NEC 標準）
            duty=0                    # 初始 duty 設為 0（不發射）
        )

    def send(self, pulses):            # 定義發射紅外線的方法
        """
        pulses: [mark, space, mark, space ...] 單位 us
        """
        if not pulses:                # 如果 pulses 是空的
            print("❌ pulses 為空")   # 印出錯誤訊息
            return False              # 回傳 False 表示發射失敗

        for i, duration in enumerate(pulses):  # 逐筆讀取脈衝索引與時間長度
            if i % 2 == 0:             # 偶數 index → mark（紅外線 ON）
                self.pwm.duty(512)     # 設定 duty 約 50%，輸出 38kHz 載波
            else:                      # 奇數 index → space（紅外線 OFF）
                self.pwm.duty(0)       # 將 duty 設為 0，關閉紅外線

            time.sleep_us(duration)    # 延遲指定的微秒數，維持脈衝寬度

        self.pwm.duty(0)               # 發射完成後，確保紅外線關閉
        return True                    # 回傳 True 表示發射成功


# =========================
# NEC 測試碼（67 pulses）
# =========================

NEC_PULSES = [                         # 定義一組 NEC 協議的紅外線脈衝資料
    9000, 4500,                        # Header：9ms mark + 4.5ms space
    560, 560, 560, 560, 560, 560, 560, 1690,   # 資料位（0 與 1）
    560, 560, 560, 560, 560, 560, 560, 560,    # 資料位
    560, 560, 560, 1690, 560, 1690, 560, 560,  # 資料位
    560, 1690, 560, 1690, 560, 1690, 560, 1690,# 資料位
    560, 1690, 560, 560, 560, 1690, 560, 560,  # 資料位
    560, 560, 560, 560, 560, 1690, 560, 560,   # 資料位
    560, 560, 560, 1690, 560, 560, 560, 1690,  # 資料位
    560, 1690, 560, 1690, 560, 560, 560, 1690  # 資料位（結尾）
]

# =========================
# 直接執行（無 main）
# =========================

ir = IRSender()                        # 建立 IRSender 物件（使用預設腳位與頻率）

print("📡 發射 NEC")                  # 印出開始發射提示
ir.send(NEC_PULSES)                   # 呼叫 send 方法發射 NEC 紅外線
print("📡 發射完畢")                  # 印出發射完成提示
