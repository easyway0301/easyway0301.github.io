# ==================================================
# MicroPython XIAO ESP32 打磚塊遊戲
# 搖桿控制 + OLED 顯示 + 蜂鳴器音效
# ==================================================

from machine import ADC, Pin, I2C, PWM  # 匯入 ADC、GPIO、I2C 與 PWM
import ssd1306                        # SSD1306 OLED 驅動
import time                            # 時間模組

# ==================================================
# 蜂鳴器設定（GPIO4）
# ==================================================
buzzer = PWM(Pin(4))                    # PWM 控制無源蜂鳴器
buzzer.duty_u16(0)                      # 初始關閉蜂鳴器

# ==================================================
# OLED 設定 (XIAO Expansion Board)
# ==================================================
i2c = I2C(1, scl=Pin(6), sda=Pin(5), freq=400000)   # 初始化 I2C
oled = ssd1306.SSD1306_I2C(128, 64, i2c)            # 建立 OLED 物件

# ==================================================
# Joystick 設定
# ==================================================
vrx = ADC(Pin(9))                        # X 軸
vry = ADC(Pin(8))                        # Y 軸（目前未使用）
swi = Pin(7, Pin.IN, Pin.PULL_UP)        # 搖桿按鈕

vrx.atten(ADC.ATTN_11DB)                 # ADC 範圍擴展
vry.atten(ADC.ATTN_11DB)

# ==================================================
# Joystick 校正值（依實測調整）
# ==================================================
JOY_CENTER_X = 2762
JOY_CENTER_Y = 2751
DEAD_ZONE = 400                          # 搖桿靜止容差

# ==================================================
# 遊戲設定
# ==================================================
PADDLE_W = 20                            # 橫板寬度
PADDLE_H = 4                             # 橫板高度
paddle_x = (128 - PADDLE_W) // 2         # 初始 X 位置
paddle_y = 58                             # 固定 Y 位置

ball_x = 64                               # 球初始 X
ball_y = 40                               # 球初始 Y
ball_vx = 1                               # 球 X 速度
ball_vy = -1                              # 球 Y 速度
ball_active = False                        # 球是否發射

lives = 3                                 # 剩餘生命

# ==================================================
# 磚塊設定
# ==================================================
BRICK_W = 12
BRICK_H = 6
bricks = []

def reset_bricks():
    """初始化磚塊，4排10列，有水平和垂直間距"""
    bricks.clear()
    ROWS = 4       # 磚塊排數
    COLS = 10      # 每排磚塊數量
    H_SPACE = 2    # 水平間距
    V_SPACE = 4    # 垂直間距
    X_OFFSET = 4   # 左邊距
    Y_OFFSET = 4   # 上邊距

    for row in range(ROWS):
        for col in range(COLS):
            x = X_OFFSET + col * (BRICK_W + H_SPACE)
            y = Y_OFFSET + row * (BRICK_H + V_SPACE)
            bricks.append([x, y, True])   # [X座標, Y座標, 是否存在]

reset_bricks()

# ==================================================
# ADC 讀值安全處理
# ==================================================
def read_adc_safe(adc):
    """讀 ADC 並過濾明顯錯誤值"""
    v = adc.read()
    if v < 30 or v > 4200:
        return None
    return v

def read_adc_median(adc, n=5):
    """取多筆 ADC 中位數，減少抖動"""
    vals = []
    for _ in range(n):
        v = read_adc_safe(adc)
        if v is not None:
            vals.append(v)
        time.sleep_ms(2)
    if not vals:
        return None
    vals.sort()
    return vals[len(vals)//2]

# ==================================================
# 搖桿輸入
# ==================================================
def read_joystick():
    """讀取搖桿 X 軸，控制橫板左右"""
    global paddle_x

    x = read_adc_median(vrx)
    if x is None:
        return

    dx = x - JOY_CENTER_X

    if dx < -DEAD_ZONE:
        paddle_x -= 2
    elif dx > DEAD_ZONE:
        paddle_x += 2

    # 限制橫板在螢幕範圍內
    paddle_x = max(0, min(128 - PADDLE_W, paddle_x))

# ==================================================
# 球邏輯
# ==================================================
def reset_ball():
    """重置球到橫板上方"""
    global ball_x, ball_y, ball_vx, ball_vy, ball_active
    ball_x = paddle_x + PADDLE_W // 2
    ball_y = paddle_y - 4
    ball_vx = 1
    ball_vy = -1
    ball_active = False

reset_ball()

def move_ball():
    """移動球並處理碰撞"""
    global ball_x, ball_y, ball_vx, ball_vy, lives, ball_active

    if not ball_active:
        ball_x = paddle_x + PADDLE_W // 2
        return

    ball_x += ball_vx
    ball_y += ball_vy

    # 碰牆反彈
    if ball_x <= 0 or ball_x >= 126:
        ball_vx = -ball_vx
    if ball_y <= 0:
        ball_vy = -ball_vy

    # 碰橫板
    if (paddle_y <= ball_y <= paddle_y + PADDLE_H and
        paddle_x <= ball_x <= paddle_x + PADDLE_W):
        ball_vy = -1

    # 球掉下去
    if ball_y > 63:
        lives -= 1
        # 掉球音效
        buzzer.freq(500)
        buzzer.duty_u16(32768)
        time.sleep_ms(150)
        buzzer.duty_u16(0)
        reset_ball()

# ==================================================
# 磚塊碰撞
# ==================================================
def check_bricks():
    """檢查球與磚塊碰撞"""
    global ball_vy
    for b in bricks:
        if not b[2]:
            continue
        bx, by = b[0], b[1]
        if (bx <= ball_x <= bx + BRICK_W and
            by <= ball_y <= by + BRICK_H):
            b[2] = False           # 磚塊消失
            ball_vy = -ball_vy      # 反彈
            # 打磚塊音效
            buzzer.freq(1000)
            buzzer.duty_u16(32768)
            time.sleep_ms(50)
            buzzer.duty_u16(0)
            break

# ==================================================
# 畫面更新
# ==================================================
def draw():
    oled.fill(0)

    # 磚塊
    for b in bricks:
        if b[2]:
            oled.fb.fill_rect(b[0], b[1], BRICK_W, BRICK_H, 1)

    # 橫板
    oled.fb.fill_rect(paddle_x, paddle_y, PADDLE_W, PADDLE_H, 1)

    # 球
    oled.fb.fill_rect(ball_x, ball_y, 2, 2, 1)

    oled.show()

# ==================================================
# GAME OVER 顯示
# ==================================================
def game_over():
    """顯示 GAME OVER 並等待按鈕重置"""
    oled.fill(0)
    oled.fb.text("GAME OVER", 28, 28, 1)
    oled.show()
    while swi.value():         # 等待按鈕
        time.sleep_ms(50)
    time.sleep_ms(300)

# ==================================================
# GAME OVER 音樂
# ==================================================
def game_over_sound():
    """簡單旋律 GAME OVER 音效"""
    melody = [
        (330, 150),
        (330, 150),
        (0, 100),
        (330, 150),
        (0, 100),
        (262, 150),
        (330, 150),
        (0, 100),
        (392, 300),
    ]

    for note, dur in melody:
        if note == 0:
            buzzer.duty_u16(0)  # 靜音
        else:
            buzzer.freq(note)
            buzzer.duty_u16(32768)
        time.sleep_ms(dur)

    buzzer.duty_u16(0)

# ==================================================
# 主程式迴圈
# ==================================================
while True:
    if lives <= 0:
        game_over_sound()      # 播放 GAME OVER 音樂
        game_over()            # 顯示 GAME OVER 畫面
        lives = 3
        reset_bricks()
        reset_ball()

    read_joystick()             # 讀搖桿控制

    # 按鈕發球
    if not ball_active and not swi.value():
        ball_active = True
        time.sleep_ms(200)

    move_ball()                 # 移動球
    check_bricks()              # 碰撞檢查
    draw()                      # 畫面更新

    time.sleep_ms(30)           # 遊戲速度控制


