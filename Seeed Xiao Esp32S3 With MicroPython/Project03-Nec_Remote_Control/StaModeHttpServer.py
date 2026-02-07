import socket  # 匯入 socket 模組，用來建立網路連線（HTTP Server）

# ===== 建立 HTTP Server =====
def start_server():
    addr = socket.getaddrinfo("0.0.0.0", 80)[0][-1]  # 取得 0.0.0.0:80 的地址資訊（監聽所有網卡）
    s = socket.socket()                               # 建立 TCP socket 物件
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # 設定 socket 選項，允許重複使用同一個地址
    s.bind(addr)                                     # 綁定 socket 到指定地址（IP + port）
    s.listen(1)                                      # 開始監聽，最多排隊 1 個連線
    s.settimeout(0.1)                                # 設定 accept() 最多等待 0.1 秒，不會阻塞主程式
    return s                                         # 回傳建立好的 socket 物件

# ===== 處理 HTTP Client =====
def handle_client(server, on_request):
    try:
        cl, addr = server.accept()                  # 嘗試接受 client 連線，cl 為 client socket，addr 為 client 地址
    except:
        return                                     # 若沒有連線或超時，直接回傳，不做任何處理

    try:
        on_request(cl)                              # 呼叫傳入的處理函式 on_request()，由使用者定義如何處理 HTTP 請求
    except Exception as e:
        print("處理 client 發生錯誤:", e)           # 捕捉錯誤並印出
    finally:
        cl.close()                                  # 不論是否出錯，都關閉 client socket，釋放資源
