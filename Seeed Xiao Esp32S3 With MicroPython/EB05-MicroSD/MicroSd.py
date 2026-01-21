import machine
import os
import sdcard
import uos

# MicroSD格式化Fat32，32G以以用guiformat來做格式化。
# =====================================================
# SD 卡硬體腳位設定（Seeed Studio XIAO Expansion Board ）
# =====================================================
# SCK  -> GPIO 7  （SPI 時脈）
SCK_PIN  = 7
# MOSI -> GPIO 9  （主機送資料）
MOSI_PIN = 9
# MISO -> GPIO 8  （主機收資料）
MISO_PIN = 8
# CS   -> GPIO 3  （MicroSD 卡片選擇，Expansion Board 預設 D2）
CS_PIN   = 3

# MicroSD 卡掛載點（掛載後 /sd 就是 MicroSD 卡根目錄）
MOUNT_POINT = "/sd"


# =====================================================
# 初始化並掛載 MicroSD 卡
# =====================================================
def sd_mount():
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


# =====================================================
# 顯示 MicroSD 卡容量資訊
# =====================================================
def sd_show_capacity():
    """
    顯示 MicroSD 卡總容量與剩餘容量
    """
    stat = uos.statvfs(MOUNT_POINT)

    # statvfs 回傳的結構：
    # stat[0] -> block size（每個區塊大小，byte）
    block_size = stat[0]
    # stat[2] -> 總區塊數
    total_bytes = stat[0] * stat[2]
    # stat[3] -> 可用區塊數
    free_bytes  = stat[0] * stat[3]

    print("📦 MicroSD 卡總容量: {:.2f} MB".format(total_bytes / 1024 / 1024))
    print("📦 MicroSD 卡剩餘容量: {:.2f} MB".format(free_bytes / 1024 / 1024))


# =====================================================
# 列出指定目錄內容（預設列出 MicroSD 根目錄）
# =====================================================
def sd_list(path=MOUNT_POINT):
    """
    列出指定路徑的檔案與資料夾
    """
    print("📁 目錄內容:", os.listdir(path))


# =====================================================
# 寫入檔案
# =====================================================
def sd_write(filename, content):
    """
    在 MicroSD 卡中寫入文字檔
    """
    path = MOUNT_POINT + "/" + filename
    with open(path, "w") as f:
        f.write(content)

    print("✍️ 檔案寫入完成:", filename)


# =====================================================
# 讀取檔案
# =====================================================
def sd_read(filename):
    """
    讀取 MicroSD 卡中的檔案內容
    """
    path = MOUNT_POINT + "/" + filename
    with open(path, "r") as f:
        data = f.read()

    print("📖 讀取內容：")
    print(data)
    return data


# =====================================================
# 刪除檔案
# =====================================================
def sd_delete(filename):
    """
    刪除 MicroSD 卡中的檔案
    """
    path = MOUNT_POINT + "/" + filename
    os.remove(path)

    print("🗑 已刪除檔案:", filename)


# =====================================================
# 主程式測試流程
# =====================================================
try:
    # 掛載 MicroSD 卡
    sd_mount()

    # 顯示MicroSD容量
    sd_show_capacity()

    # 列出MicroSD根目錄
    sd_list()

    # 寫入測試檔案
    sd_write("hello.txt", "Hello from XIAO ESP32S3!\n")

    # 讀取檔案
    sd_read("hello.txt")

    # 刪除檔案
    #sd_delete("hello.txt")

    # 再列一次目錄確認
    #sd_list()

except Exception as e:
    print("❌ MicroSD 卡操作錯誤:", e)

