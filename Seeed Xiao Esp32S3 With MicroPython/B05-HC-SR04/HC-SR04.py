<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="UTF-8">
<title>ESP32-S3 MicroPython｜SH1106 OLED 顯示教學（10 秒測試版）</title>

<style>
body {
    font-family: Arial, "Microsoft JhengHei", sans-serif;
    background: #f5f7fa;
    color: #222;
    line-height: 1.9;
    max-width: 980px;
    margin: 40px auto;
    padding: 0 20px;
}

h1 {
    text-align: center;
    margin-bottom: 10px;
}

.subtitle {
    text-align: center;
    color: #555;
    margin-bottom: 50px;
}

section {
    background: #ffffff;
    border-radius: 14px;
    padding: 40px;
    margin-bottom: 50px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.08);
}

h2 {
    margin-top: 0;
    border-left: 6px solid #2196F3;
    padding-left: 14px;
}

.highlight {
    background: #e3f2fd;
    border-left: 6px solid #2196f3;
    padding: 16px 20px;
    border-radius: 8px;
    margin: 20px 0;
}

.code-block {
    background: #0d1117;
    color: #c9d1d9;
    border-radius: 12px;
    padding: 20px;
    margin: 30px 0;
    font-family: Consolas, monospace;
    font-size: 14px;
    overflow-x: auto;
}

pre {
    margin: 0;
}
</style>
</head>

<body>

<h1>ESP32-S3 MicroPython OLED 教學</h1>
<div class="subtitle">SH1106 I2C 顯示模組（10 秒測試版）</div>

<section>
<h2>第一步：模組說明</h2>

<p>
SH1106 是常見的 <strong>128×64 單色 OLED 顯示模組</strong>，
使用 <strong>I2C</strong> 通訊方式，非常適合狀態顯示與教學示範。
</p>

<div class="highlight">
<strong>規格重點：</strong><br>
• 解析度：128 × 64<br>
• 通訊方式：I2C<br>
• 常見位址：0x3C
</div>
</section>

<section>
<h2>第二步：接線方式（Seeed XIAO ESP32-S3）</h2>

<ul>
    <li>VCC → 3V3</li>
    <li>GND → GND</li>
    <li>SDA → GPIO 5</li>
    <li>SCL → GPIO 6</li>
</ul>

<div class="highlight">
⚠️ 請確認 GND 共地，否則 OLED 不會顯示。
</div>
</section>

<section>
<h2>第三步：MicroPython 範例（不使用 while 迴圈）</h2>

<p>
此範例<strong>不使用 while 迴圈</strong>，  
OLED 會顯示畫面 <strong>10 秒</strong>，之後自動清除。
</p>

<div class="code-block">
<pre><code>
from machine import Pin, I2C      # 匯入 Pin 與 I2C
import sh1106                     # 匯入 SH1106 OLED 驅動
import time                       # 匯入時間模組

# === 建立 I2C 物件 ===
i2c = I2C(
    scl=Pin(6),                   # I2C SCL 腳位
    sda=Pin(5),                   # I2C SDA 腳位
    freq=400000                   # I2C 通訊速度
)

# === 建立 OLED 物件 ===
oled = sh1106.SH1106_I2C(
    128,                          # 螢幕寬度
    64,                           # 螢幕高度
    i2c,
    addr=0x3C                     # I2C 位址
)

# === 清除畫面 ===
oled.fill(0)                      # 清空畫面

# === 顯示文字 ===
oled.text("ESP32-S3", 0, 0)       # 第一行文字
oled.text("MicroPython", 0, 16)   # 第二行文字
oled.text("SH1106 OLED", 0, 32)   # 第三行文字

# === 更新顯示 ===
oled.show()                       # 顯示到 OLED

# === 顯示 10 秒 ===
time.sleep(10)                    # 停留 10 秒

# === 清除畫面 ===
oled.fill(0)                      # 再次清畫面
oled.show()                       # 更新顯示
</code></pre>
</div>
</section>

<section>
<h2>執行結果</h2>

<ul>
    <li>OLED 顯示三行文字</li>
    <li>約 10 秒後自動清除畫面</li>
    <li>適合用來快速測試接線是否正確</li>
</ul>

<div class="highlight">
📌 教學重點：<br>
✔ 不使用 while 迴圈<br>
✔ 避免程式卡死<br>
✔ 適合課堂與測試用途
</div>
</section>

</body>
</html>
