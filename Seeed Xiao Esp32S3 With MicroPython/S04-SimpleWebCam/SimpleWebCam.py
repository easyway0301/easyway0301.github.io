# 參考來源：https://github.com/cnadler86/micropython-camera-API/blob/master/examples/SimpleWebCam.py
# 部份修改SimpleWebCam.py範例使用
# https://github.com/cnadler86/micropython-camera-API/releases
# 下載mpy_cam-v1.27.0-XIAO_ESP32S3.zip v0.6.0 (mpy 1.27.x)，不要用最新版
# 修改第33行的SSID及36行的PASSWORD，其餘不必動。

# ==============================
# 匯入 Wi-Fi 連線模組
# ==============================
import network

# ==============================
# 匯入 Socket（HTTP Server 用）
# ==============================
import socket

# ==============================
# 匯入時間模組（延遲用）
# ==============================
import time

# ==============================
# 匯入攝影機控制模組
# ==============================
from camera import Camera, FrameSize, PixelFormat, GrabMode


# ==============================
# Wi-Fi 設定
# ==============================

# Wi-Fi 名稱
SSID = '你的SSID'

# Wi-Fi 密碼
PASSWORD = '你的WIFI密碼'


# ==============================
# 連線 Wi-Fi
# ==============================
def connect_wifi():
    
    
    # 建立 Wi-Fi 物件（STA 模式）
    station = network.WLAN(network.STA_IF)

    # 確保 STA 狀態先清空
    station.active(False)
    
    # 啟用 Wi-Fi
    station.active(True)

    # 連線到指定 Wi-Fi
    station.connect(SSID, PASSWORD)

    # 等待 Wi-Fi 連線成功
    while not station.isconnected():
        time.sleep(1)

    # 取得裝置 IP 位址
    ip = station.ifconfig()[0]

    # 顯示連線成功訊息
    print(f'Wi-Fi 已連線，IP 位址：{ip}')

    # 提示使用者瀏覽器開啟網址
    print(f'請在瀏覽器輸入：http://{ip}/stream')

    # 回傳 IP 位址
    return ip


# ==============================
# 初始化 Camera（尚未啟動）
# ==============================
def init_camera():
    # 建立 Camera 物件
    cam = Camera(
        
        # 設定輸出格式為 JPEG
        pixel_format=PixelFormat.JPEG,
        
        # 設定解析度為 VGA
        frame_size=FrameSize.HD,
        
        # JPEG 壓縮品質（70~85 最穩）
        jpeg_quality=70,    

        # Frame Buffer 數量（2 比較穩）
        fb_count=2,

        # 只有 buffer 空時才抓新畫面
        grab_mode=GrabMode.WHEN_EMPTY,

        # 延後初始化（需要串流時再 init）
        init=False
    )

    # 回傳 Camera 物件
    return cam


# ==============================
# HTML 頁面（顯示影像用）
# ==============================
HTML_PAGE = """<!DOCTYPE html>
<html>
<head>
    <title>ESP32 Camera Stream</title>
    <style>
        body {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            background-color: #f0f0f0;
        }
        .video-container {
            text-align: center;
            width: 100%;
            max-width: 1000px;
        }
        img {
            width: 100%;
            height: auto;
        }
    </style>
</head>
<body>
    <div class="video-container">
        <h1>ESP32 Camera Stream</h1>
        <img src="/stream">
    </div>
</body>
</html>
"""


# ==============================
# 處理單一 Client 連線
# ==============================
def handle_client(client, cam):
    try:
        # 讀取瀏覽器送來的 HTTP Request
        request = client.recv(1024).decode()

        # --------------------------
        # 若是影像串流請求
        # --------------------------
        if 'GET /stream' in request:
            # 回傳 MJPEG HTTP Header
            client.send(
                b'HTTP/1.1 200 OK\r\n'
                b'Content-Type: multipart/x-mixed-replace; boundary=frame\r\n\r\n'
            )

            # 初始化攝影機
            cam.init()

            # 持續串流影像
            while True:
                try:
                    # 擷取一張 JPEG 影像
                    frame = cam.capture()
                    
                    print(hex(frame[-2]), hex(frame[-1]))


                    # 若沒有影像資料則中斷
                    if not frame:
                        break

                    # 傳送一個 MJPEG frame
                    client.send(
                        b'--frame\r\n'
                        b'Content-Type: image/jpeg\r\n'
                        b'Content-Length: ' + str(len(frame)).encode() + b'\r\n\r\n'
                        + frame + b'\r\n'
                    )
                    
                    cam.free_buffer()


                # 若客戶端斷線或錯誤則跳出
                except Exception:
                    break

        # --------------------------
        # 一般首頁請求（HTML）
        # --------------------------
        else:
            # 組合 HTTP 回應內容
            response = (
                'HTTP/1.1 200 OK\r\n'
                'Content-Type: text/html\r\n\r\n'
                + HTML_PAGE
            )

            # 傳送 HTML 頁面
            client.send(response.encode())

    # 捕捉整體錯誤
    except Exception as e:
        print('Client 錯誤：', e)

    # 最後一定要關閉 Client
    finally:
        client.close()
        # ⚠️ 不在此 deinit camera，避免其他連線被中斷


# ==============================
# 啟動 HTTP Server
# ==============================
def start_server(cam):
    # 取得本機 0.0.0.0:80 的 socket 位址
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

    # 建立 socket
    s = socket.socket()

    # 允許重複使用 port（非常重要）
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # 綁定 IP 與 Port
    s.bind(addr)

    # 開始監聽（一次一個 client）
    s.listen(1)

    # 顯示 Server 啟動訊息
    print('HTTP Server 啟動，等待連線中...')

    # 不斷接受新的連線
    while True:
        # 等待 Client 連線
        client, addr = s.accept()

        # 顯示連線來源
        print('連線來源：', addr)

        # 處理 Client 請求
        handle_client(client, cam)


# ==============================
# 主程式進入點
# ==============================
def main():
    # 連線到 Wi-Fi
    connect_wifi()

    # 建立 Camera 物件
    cam = init_camera()

    # 啟動 HTTP Server
    start_server(cam)


# ==============================
# 程式開始執行
# ==============================
main()

