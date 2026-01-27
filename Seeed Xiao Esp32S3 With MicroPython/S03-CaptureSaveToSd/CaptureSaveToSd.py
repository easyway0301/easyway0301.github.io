import machine, os, sdcard, uos
from camera import Camera, PixelFormat, FrameSize, GrabMode
import time

# 韌體下載https://github.com/cnadler86/micropython-camera-API/releases
# 務必下載v0.6.0 (mpy 1.27.x)的mpy_cam-v1.27.0-XIAO_ESP32S3.zip ，不要用最新版

'''
FrameSize    長     寬    品質
R128x128    128   128    偏綠
QQVGA       160   120    偏綠
HQVGA       240   176    偏綠
R240X240    240   240    偏綠
QVGA        320   240 
R320X320    320   320    偏綠
CIF         400   296
HVGA        480   320
VGA         640   480    偏綠
P_HD        720  1280
QCIF        720  1280
SVGA        800   600    偏綠
P_3MP       864  1536
XGA        1024   768    偏綠
HD         1280   720
SXGA       1280  1024
UXGA       1600  1200
FHD        1920  1080
P_FHD      2048  1536
QHD        2048  1536
QSXGA      2048  1536
QXGA       2048  1536
WQXGA      2048  1536
R96X96   會出錯  會出錯
'''

# MicroSD格式化Fat32，32G以上用guiformat來做格式化。
# =====================================================
# SD 卡硬體腳位設定（Seeed Studio XIAO ESP32S3 Sense）
# =====================================================
# SCK  -> GPIO 7  （SPI 時脈）
SCK_PIN  = 7
# MOSI -> GPIO 9  （主機送資料）
MOSI_PIN = 9
# MISO -> GPIO 8  （主機收資料）
MISO_PIN = 8
# CS   -> GPIO 3  （MicroSD 卡片預設 21）
CS_PIN   = 21

# MicroSD 卡掛載點（掛載後 /sd 就是 MicroSD 卡根目錄）
MOUNT_POINT = "/sd"

# =====================================================
# 初始化並掛載 MicroSD 卡
# =====================================================
"""
初始化 SPI，並將 MicroSD 卡掛載到 /sd
"""
# 建立 SPI 物件（使用 SPI(2)）
spi = machine.SPI(
    2,
    baudrate=10_000_000,     # SPI 速度，10MHz（可視穩定度調低）
    polarity=0,
    phase=0,
    sck=machine.Pin(SCK_PIN),
    mosi=machine.Pin(MOSI_PIN),
    miso=machine.Pin(MISO_PIN)
)

# MicroSD 卡 CS 腳位
cs = machine.Pin(CS_PIN, machine.Pin.OUT)

# 初始化 MicroSD 卡（SPI 模式）
sd = sdcard.SDCard(spi, cs)

# 使用 FAT 檔案系統
vfs = uos.VfsFat(sd)

# 掛載到 /sd
uos.mount(vfs, MOUNT_POINT)

print("✅ MicroSD 卡掛載成功（/sd）")

# ------------ Camera 初始化 ------------
cam = Camera(
    pixel_format=PixelFormat.JPEG,
    # 穩定尺寸
    frame_size=FrameSize.QVGA,   
    jpeg_quality=90,
    # 一定用 1 才穩定
    fb_count=1,                  
    grab_mode=GrabMode.WHEN_EMPTY
)
cam.init()
print("📷 Camera 初始化完成")

# ------------ 拍照並存檔 ------------

# 透過 Camera 物件抓取一張影像，回傳 memoryview 物件
img = cam.capture()  

if img:  # 如果成功抓到影像
    # 取得當前時間 (年, 月, 日, 時, 分, 秒, 星期, 一年中的第幾天)
    t = time.localtime()  
    
    # 產生檔名，例如：/sd/20260127-10h45m30.jpg
    # 格式: 年月日-時h分m秒.jpg
    filename = "/sd/{:04d}{:02d}{:02d}-{:02d}h{:02d}m{:02d}.jpg".format(*t[:6])
    
    # 開啟檔案以二進位寫入模式 ("wb")，將影像資料寫入 SD 卡
    with open(filename, "wb") as f:
        # 將 memoryview 的 JPEG 資料寫入檔案
        f.write(img)  

    # 提示使用者存檔成功
    print("📸 影像已存成:", filename)  

else:
    print("❌ 拍照失敗")

# ------------ 顯示 SD 卡內容 ------------
print("📁 SD 根目錄:", os.listdir(MOUNT_POINT))

