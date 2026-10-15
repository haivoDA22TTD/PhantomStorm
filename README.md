# ⚡ Phantom Storm v1.0

**Phantom Storm** là một công cụ kiểm thử bảo mật (Pentesting Tool) được viết bằng Python, chuyên giả lập các cuộc tấn công **Layer 7 HTTP Keep-Alive / Slowloris DoS**. Công cụ này phục vụ mục đích nghiên cứu và tối ưu hóa hạ tầng mạng phòng thủ cho các kỹ sư hệ thống.

---

## ⚠️ DISCLAIMER (TỪ CHỐI TRÁCH NHIỆM)
> **Chỉ sử dụng cho mục đích giáo dục và nghiên cứu.** Công cụ này chỉ được phép khởi chạy trong môi trường Lab nội bộ (Internal Network) được cấp phép. Tác giả hoàn toàn không chịu trách nhiệm đối với bất kỳ hành vi lạm dụng nào gây thiệt hại cho các hệ thống trên Internet.

---

## 📊 Sơ Đồ Hệ Thống Thử Nghiệm (Lab Architecture)
Công cụ này đã được thử nghiệm thành công trong mô hình mạng doanh nghiệp thu nhỏ (VirtualBox Internal Network):

```text
[ Kali Linux ] --- (Tấn công) ---> [ Ubuntu Server ] ---> (Chuyển tiếp) ---> [ Windows Server ]
(Phantom Storm)                    (Nginx Proxy)                             (IIS Web / DNS)
```

* **Attacker (Kali Linux):** Khởi chạy `Phantom Storm` đa luồng, gửi gói tin mồi để chiếm giữ tài nguyên.
* **Defender (Ubuntu Server):** Đóng vai trò Reverse Proxy gánh chịu đợt tấn công, áp dụng cấu hình **Rate Limiting** để bảo vệ vùng lõi.
* **Backend (Windows Server):** Vùng lõi an toàn lưu trữ ứng dụng Web IIS.

---

## 🛠️ Cơ Chế Hoạt Động (How it works)
Không giống như các công cụ tấn công Layer 4 làm nghẽn băng thông mạng, **Phantom Storm** tấn công vào Tầng ứng dụng (Layer 7) bằng sự tinh quái:
1. Sử dụng cơ chế đa luồng (`threading`) cực nhẹ trên máy tấn công.
2. Gửi các gói tin HTTP Request mở đầu hợp pháp nhưng cố tình **giữ kết nối (Keep-Alive)**.
3. Liên tục "bơm" thêm các dòng Header rác (`X-Garbage`) sau mỗi 3 giây nhằm đánh lừa Web Server tưởng người dùng truyền dữ liệu rất chậm.
4. Ép Web Server (Nginx/IIS) phải giữ chỗ trong bộ nhớ RAM, dẫn đến cạn kiệt tài nguyên hệ thống (Resource Exhaustion) và sập nguồn từ bên trong.

---

## 🚀 Hướng Dẫn Sử Dụng (Usage Guide)

### 1. Chuẩn bị môi trường trên Kali Linux
Đảm bảo máy Kali của bạn đã cài đặt sẵn Python 3. Tải file script về máy và di chuyển vào thư mục chứa file:
```bash
python3 --version
```

### 2. Cú pháp khởi chạy lệnh
Bạn chạy công cụ bằng lệnh `python3` kèm theo 3 tham số bắt buộc:
```bash
python3 phantom_storm.py [IP_Mục_Tiêu] [Cổng] [Số_Luồng]
```

* `IP_Mục_Tiêu`: Địa chỉ IP của máy chủ Reverse Proxy (Ubuntu).
* `Cổng`: Cổng dịch vụ đang mở của Web Server (Mặc định là cổng `80` hoặc `443`).
* `Số_Luồng`: Tổng số luồng kết nối muốn tạo ra (Khuyến nghị từ `100` đến `200` cho máy cấu hình 1GB RAM).

*Ví dụ thực tế trong bài Lab:*
```bash
python3 phantom_storm.py 192.168.1.2 80 150
```

### 3. Cách rút quân (Dừng công cụ)
Khi muốn kết thúc đợt tấn công kiểm thử, bạn chỉ cần nhấn tổ hợp phím trên bàn phím:
```bash
Ctrl + C
```

---

## 🛡️ Giải Pháp Phòng Thủ (Mitigation)
Để chống đỡ thành công **Phantom Storm**, hãy chèn 2 dòng lệnh cấu hình **Rate Limiting** sau vào file cấu hình Nginx (`/etc/nginx/sites-available/default`) của máy nạn nhân:

```nginx
# Định nghĩa vùng nhớ giới hạn tần suất 5 request / giây cho mỗi IP
limit_req_zone \$binary_remote_addr zone=mylimit:10m rate=5r/s;

server {
    listen 80;
    server_name www.labpentest.vn;

    location / {
        # Áp dụng luật chặn đứng gói tin vượt ngưỡng
        limit_req zone=mylimit burst=5 nodelay;
        proxy_pass http://my_web_cluster;
    }
}
```
