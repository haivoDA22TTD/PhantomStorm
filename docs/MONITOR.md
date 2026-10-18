# 📊 Hướng Dẫn Monitor Trên Ubuntu Server (Defender)

Khi Phantom Storm đang tấn công, sử dụng các lệnh sau để theo dõi trạng thái hệ thống.

---

## 🎯 Quick Commands Cheat Sheet

| Lệnh | Xem Gì | Khi Nào Dùng |
|------|--------|--------------|
| `netstat -an \| grep :80 \| grep ESTABLISHED \| wc -l` | Số connections hiện tại | Liên tục (quan trọng nhất!) |
| `sudo tail -f /var/log/nginx/access.log` | Access log real-time | Xem requests đang vào |
| `sudo tail -f /var/log/nginx/error.log` | Error log real-time | Xem nginx có chặn không |
| `sudo grep "limiting" /var/log/nginx/error.log \| tail -10` | Rate limiting logs | Kiểm tra xem nginx có block |
| `top` hoặc `htop` | CPU/Memory usage | Xem nginx có bị overload |

---

## 📝 Chi Tiết Các Lệnh Monitor

### 1. Đếm Số Connections Đang Active ⭐ QUAN TRỌNG NHẤT

```bash
watch -n 1 'netstat -an | grep :80 | grep ESTABLISHED | wc -l'
```

**Giải thích:**
- `watch -n 1`: Chạy lệnh mỗi 1 giây
- `netstat -an`: Hiển thị tất cả connections
- `grep :80`: Lọc port 80
- `grep ESTABLISHED`: Chỉ lấy connections đang active
- `wc -l`: Đếm số dòng

**Kết quả mong đợi:**
- **Trước attack:** 0-5 connections
- **Khi bị attack:** 50-200 connections (tùy số threads tool dùng)
- **Sau attack dừng:** Giảm dần về 0

**Nhấn `Ctrl+C` để thoát**

---

### 2. Xem Chi Tiết Connections Từ IP Nào

```bash
netstat -an | grep :80 | grep ESTABLISHED | awk '{print $5}' | cut -d: -f1 | sort | uniq -c | sort -rn
```

**Output mẫu:**
```
     50 192.168.1.50
      2 192.168.1.100
      1 192.168.1.1
```

**Giải thích output:**
- `50 192.168.1.50`: 50 connections từ IP attacker
- `2 192.168.1.100`: 2 connections internal
- `1 192.168.1.1`: 1 connection từ backend

---

### 3. Xem Tất Cả Connections Chi Tiết

```bash
netstat -an | grep :80 | grep ESTABLISHED
```

**Output mẫu:**
```
tcp  0  0  192.168.1.100:80  192.168.1.50:54321  ESTABLISHED
tcp  0  0  192.168.1.100:80  192.168.1.50:54322  ESTABLISHED
tcp  0  0  192.168.1.100:80  192.168.1.50:54323  ESTABLISHED
...
```

**Giải thích:**
- `192.168.1.100:80`: Server port (Ubuntu)
- `192.168.1.50:54321`: Client IP:port (Attacker)
- Thấy nhiều connections từ cùng 1 IP → Đang bị DoS

---

### 4. Monitor Dashboard Tổng Hợp (Recommended!)

```bash
watch -n 2 'echo "==================== NGINX MONITOR ====================" && \
echo "" && \
echo "[1] ACTIVE CONNECTIONS:" && \
netstat -an | grep :80 | grep ESTABLISHED | wc -l && \
echo "" && \
echo "[2] TOP 5 IPs CONNECTING:" && \
netstat -an | grep :80 | grep ESTABLISHED | awk "{print \$5}" | cut -d: -f1 | sort | uniq -c | sort -rn | head -5 && \
echo "" && \
echo "[3] LAST 5 ACCESS LOGS:" && \
sudo tail -5 /var/log/nginx/access.log && \
echo "" && \
echo "[4] RATE LIMITING STATUS:" && \
sudo grep -i "limiting" /var/log/nginx/error.log | tail -3 || echo "No rate limiting detected" && \
echo "" && \
echo "======================================================="'
```

**Dashboard tự động refresh mỗi 2 giây!**

**Output mẫu khi bị attack:**
```
==================== NGINX MONITOR ====================

[1] ACTIVE CONNECTIONS:
50

[2] TOP 5 IPs CONNECTING:
     50 192.168.1.50

[3] LAST 5 ACCESS LOGS:
192.168.1.50 - - [16/Oct/2026:15:01:06] "GET /?storm=123456"
192.168.1.50 - - [16/Oct/2026:15:01:06] "GET /?storm=789012"
...

[4] RATE LIMITING STATUS:
[error] limiting requests, excess: 5.000 by zone "mylimit"

=======================================================
```

---

### 5. Xem Nginx Access Log Real-time

```bash
sudo tail -f /var/log/nginx/access.log
```

**Giải thích:**
- Xem từng request đến nginx theo thời gian thực
- Thấy IP nguồn, request path, response code

**Nhấn `Ctrl+C` để dừng**

**Nếu muốn lọc chỉ IP attacker:**
```bash
sudo tail -f /var/log/nginx/access.log | grep 192.168.1.50
```

---

### 6. Kiểm Tra Rate Limiting Có Hoạt Động

```bash
sudo grep -i "limiting" /var/log/nginx/error.log | tail -20
```

**Nếu thấy:**
```
[error] limiting requests, excess: 5.000 by zone "mylimit", client: 192.168.1.50
[error] limiting connections by zone "addr", client: 192.168.1.50
```
→ ✅ **Nginx đang chặn thành công!**

**Nếu không thấy gì:**
→ ❌ **Rate limiting chưa trigger hoặc không hiệu quả**

---

### 7. Đếm Requests Trong Khoảng Thời Gian

**Requests trong 10 giây gần nhất:**
```bash
sudo tail -n 1000 /var/log/nginx/access.log | grep "$(date '+%d/%b/%Y:%H:%M' -d '10 seconds ago')" | wc -l
```

**Requests trong 1 phút gần nhất:**
```bash
sudo tail -n 5000 /var/log/nginx/access.log | grep "$(date '+%d/%b/%Y:%H:%M')" | wc -l
```

---

### 8. Check CPU & Memory Usage

```bash
top -b -n 1 | head -20
```

**Hoặc dùng htop (friendly hơn):**
```bash
htop
```

**Chú ý:**
- `%CPU` của nginx worker processes
- `RES` (Resident Memory) của nginx
- `load average` tổng thể hệ thống

**Nếu nginx chiếm >80% CPU hoặc memory tăng cao:**
→ Đang bị overload bởi attack

---

### 9. Xem Nginx Process Status

```bash
ps aux | grep nginx | grep -v grep
```

**Output mẫu:**
```
root      1234  0.0  0.1  nginx: master process
www-data  1235  5.0  1.2  nginx: worker process
www-data  1236  5.2  1.3  nginx: worker process
```

**Chú ý:**
- Số lượng worker processes
- %CPU và %MEM của mỗi worker
- Nếu worker process CPU >50% → Đang bị attack

---

### 10. Check Nginx Service Status

```bash
sudo systemctl status nginx
```

**Hoặc:**
```bash
sudo nginx -t  # Test config syntax
sudo systemctl reload nginx  # Reload config nếu cần
```

---

## 🔥 One-Liner Quick Check

Copy toàn bộ lệnh này để check nhanh:

```bash
echo "=== PHANTOM STORM QUICK CHECK ===" && \
echo "" && \
echo "[Connections]" && \
netstat -an | grep :80 | grep ESTABLISHED | wc -l && \
echo "" && \
echo "[Top IPs]" && \
netstat -an | grep :80 | grep ESTABLISHED | awk '{print $5}' | cut -d: -f1 | sort | uniq -c | sort -rn | head -3 && \
echo "" && \
echo "[Rate Limit Logs]" && \
sudo grep -i "limiting" /var/log/nginx/error.log | tail -2 || echo "No limiting" && \
echo "" && \
echo "[CPU Usage]" && \
top -b -n 1 | grep "Cpu(s)" && \
echo "" && \
echo "[Memory Usage]" && \
free -h | grep "Mem:"
```

---

## 📊 Baseline vs Attack Comparison

### Trước Khi Attack (Baseline):

```bash
$ netstat -an | grep :80 | grep ESTABLISHED | wc -l
2  ← Chỉ 2 connections bình thường

$ top -b -n 1 | grep "nginx"
www-data  1234  0.5  0.8  ← CPU thấp
```

### Khi Đang Bị Attack:

```bash
$ netstat -an | grep :80 | grep ESTABLISHED | wc -l
50  ← Tăng vọt lên 50!

$ top -b -n 1 | grep "nginx"
www-data  1234  45.2  3.5  ← CPU tăng mạnh!

$ sudo grep "limiting" /var/log/nginx/error.log | tail -3
[error] limiting requests, excess: 5.000 by zone "mylimit"
```

### Sau Khi Attack Dừng:

```bash
$ netstat -an | grep :80 | grep ESTABLISHED | wc -l
5  ← Giảm dần, connections đóng lại

$ top -b -n 1 | grep "nginx"
www-data  1234  1.2  0.9  ← CPU về bình thường
```

---

## 🎯 Kết Luận

### ✅ Dấu Hiệu Đang Bị Attack:
- Connections tăng đột biến (50-200)
- Nhiều connections từ cùng 1 IP
- Nginx worker processes CPU cao
- Access log requests liên tục với pattern `/?storm=`

### ✅ Dấu Hiệu Nginx Đang Chặn Thành Công:
- Thấy "limiting requests" trong error log
- Connections không tăng quá limit
- CPU vẫn ở mức chấp nhận được
- Tool báo "ConnectionRefusedError"

### ❌ Dấu Hiệu Chưa Config Đủ Mạnh:
- Connections lên 200+ mà không giảm
- Không có "limiting" logs
- CPU nginx >80%
- Website bị chậm hoặc không truy cập được

---

## 💡 Tips

1. **Mở 2-3 terminals cùng lúc:**
   - Terminal 1: `watch -n 1 'netstat ... | wc -l'`
   - Terminal 2: `sudo tail -f /var/log/nginx/error.log`
   - Terminal 3: `htop`

2. **Save logs để phân tích sau:**
   ```bash
   sudo tail -1000 /var/log/nginx/access.log > ~/attack_access.log
   sudo tail -1000 /var/log/nginx/error.log > ~/attack_error.log
   ```

3. **Nếu server bị quá tải, restart nginx:**
   ```bash
   sudo systemctl restart nginx
   ```

---

**Happy Monitoring! 🔍**
