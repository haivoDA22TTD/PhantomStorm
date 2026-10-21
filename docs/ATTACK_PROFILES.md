# 🎯 Attack Profiles Documentation

## Overview

Attack Profiles là tính năng cho phép bạn sử dụng các cấu hình tấn công được định sẵn (presets) thay vì phải cấu hình thủ công từng tham số. Điều này giúp:

- **Tiết kiệm thời gian** - Không cần nhớ tham số phức tạp
- **Tối ưu hiệu quả** - Mỗi profile được tune cho use case cụ thể
- **Dễ sử dụng** - Chỉ cần chọn profile phù hợp với mục tiêu

---

## 📋 Available Profiles

### 🟢 1. Stealth Profile

**Mục đích:** Tấn công chậm, khó phát hiện, bypass IDS/IPS

**Đặc điểm:**
```
Threads               : 50
Socket Timeout        : 8s
Keep-Alive Interval   : 10s
HTTP Method           : RANDOM (GET/POST/HEAD/OPTIONS)
IP Spoofing           : ENABLED
Thread Creation Delay : 0.1s
Reconnect Delay       : 2.0s

Detection Risk        : LOW ⬇️
Impact Speed          : SLOW ⏱️
Resource Usage        : LOW 💾
```

**Khi nào sử dụng:**
- ✅ Testing IDS/IPS detection capabilities
- ✅ Long-term sustained attacks
- ✅ Bypassing rate limiting systems
- ✅ Avoiding triggering alarms
- ✅ Defense effectiveness testing

**Không nên dùng khi:**
- ❌ Cần kết quả nhanh
- ❌ Testing maximum capacity
- ❌ Isolated lab với thời gian giới hạn

---

### 🟡 2. Balanced Profile

**Mục đích:** Cân bằng giữa tốc độ và stealth, phù hợp đa số trường hợp

**Đặc điểm:**
```
Threads               : 150
Socket Timeout        : 4s
Keep-Alive Interval   : 3s
HTTP Method           : GET
IP Spoofing           : ENABLED
Thread Creation Delay : 0.01s
Reconnect Delay       : 0.5s

Detection Risk        : MEDIUM ↔️
Impact Speed          : MEDIUM ⚡
Resource Usage        : MEDIUM 💾💾
```

**Khi nào sử dụng:**
- ✅ General purpose DoS testing
- ✅ Standard penetration testing scenarios
- ✅ Initial attack assessment
- ✅ Most common use cases
- ✅ When unsure which profile to use

**Không nên dùng khi:**
- ❌ Cần stealth tối đa (dùng Stealth)
- ❌ Cần impact tối đa (dùng Aggressive)

---

### 🔴 3. Aggressive Profile

**Mục đích:** Tấn công mạnh, tốc độ cao, maximum impact

**Đặc điểm:**
```
Threads               : 300
Socket Timeout        : 2s
Keep-Alive Interval   : 1s
HTTP Method           : POST (heavier than GET)
IP Spoofing           : ENABLED
Thread Creation Delay : 0.001s
Reconnect Delay       : 0.1s

Detection Risk        : HIGH ⬆️⬆️⬆️
Impact Speed          : FAST ⚡⚡⚡
Resource Usage        : HIGH 💾💾💾
```

**Khi nào sử dụng:**
- ✅ Stress testing server capacity
- ✅ Finding resource breaking points
- ✅ Maximum impact demonstration
- ✅ Quick assessment of vulnerability
- ✅ Isolated lab environments

**Không nên dùng khi:**
- ❌ Cần tránh phát hiện
- ❌ Testing IDS/IPS
- ❌ Production-like environments
- ❌ Shared infrastructure

---

## 🚀 Usage Guide

### Command Line Usage

#### Cú pháp cơ bản:
```bash
python phantom_storm_v2.py [IP] [PORT] [THREADS] --profile=[PROFILE_NAME]
```

#### Ví dụ:

**1. Stealth Attack:**
```bash
python phantom_storm_v2.py 192.168.1.100 80 50 --profile=stealth
```

**2. Balanced Attack:**
```bash
python phantom_storm_v2.py 192.168.1.100 80 150 --profile=balanced
```

**3. Aggressive Attack:**
```bash
python phantom_storm_v2.py 192.168.1.100 80 300 --profile=aggressive
```

**💡 Tip:** Khi dùng `--profile`, tham số `[THREADS]` vẫn cần nhập nhưng sẽ bị override bởi profile settings.

---

### Python API Usage

#### Import modules:
```python
from src.core import AttackProfiles, ProfileType, AttackProfile
```

#### Sử dụng predefined profiles:
```python
# Cách 1: Gọi trực tiếp
stealth = AttackProfiles.get_stealth()
balanced = AttackProfiles.get_balanced()
aggressive = AttackProfiles.get_aggressive()

# Cách 2: Qua enum
profile = AttackProfiles.get_profile(ProfileType.STEALTH)

# Cách 3: Convenience constants
from src.core import STEALTH, BALANCED, AGGRESSIVE
```

#### Xem thông tin profile:
```python
profile = AttackProfiles.get_stealth()
print(profile.display_info())
```

#### So sánh các profiles:
```python
print(AttackProfiles.compare_profiles())
```

#### Liệt kê tất cả profiles:
```python
profiles = AttackProfiles.list_profiles()
for profile in profiles:
    print(f"{profile.name}: {profile.threads} threads")
```

---

## 🛠️ Creating Custom Profiles

Ngoài 3 profiles có sẵn, bạn có thể tạo custom profile:

### Cú pháp:
```python
from src.core import AttackProfiles, HTTPMethod

custom = AttackProfiles.get_custom(
    threads=200,                          # Số luồng
    timeout=3,                            # Socket timeout (seconds)
    keep_alive_interval=5,                # Interval gửi garbage headers
    http_method=HTTPMethod.POST,          # HTTP method cụ thể
    randomize_method=False,               # True = random methods
    use_spoofing=True,                    # Bật/tắt IP spoofing
    delay_between_threads=0.05,           # Delay khi tạo threads
    delay_between_reconnect=1.0           # Delay trước khi reconnect
)

print(custom.display_info())
```

### Ví dụ Custom Profiles:

**Medium-Stealth (Vừa chậm vừa ẩn):**
```python
medium_stealth = AttackProfiles.get_custom(
    threads=100,
    timeout=6,
    keep_alive_interval=7,
    http_method=None,  # None = sẽ random
    randomize_method=True,
    use_spoofing=True,
    delay_between_threads=0.05,
    delay_between_reconnect=1.5
)
```

**Super-Aggressive (Tấn công cực mạnh):**
```python
super_aggressive = AttackProfiles.get_custom(
    threads=500,
    timeout=1,
    keep_alive_interval=0.5,
    http_method=HTTPMethod.POST,
    randomize_method=False,
    use_spoofing=True,
    delay_between_threads=0.0001,
    delay_between_reconnect=0.05
)
```

---

## 📊 Profile Comparison Table

| Feature | Stealth 🟢 | Balanced 🟡 | Aggressive 🔴 |
|---------|-----------|------------|--------------|
| **Threads** | 50 | 150 | 300 |
| **Timeout** | 8s | 4s | 2s |
| **Keep-Alive Interval** | 10s | 3s | 1s |
| **HTTP Method** | RANDOM | GET | POST |
| **IP Spoofing** | ✅ | ✅ | ✅ |
| **Thread Creation Delay** | 0.1s | 0.01s | 0.001s |
| **Reconnect Delay** | 2.0s | 0.5s | 0.1s |
| | | | |
| **Detection Risk** | LOW ⬇️ | MEDIUM ↔️ | HIGH ⬆️⬆️⬆️ |
| **Impact Speed** | SLOW ⏱️ | MEDIUM ⚡ | FAST ⚡⚡⚡ |
| **Resource Usage** | LOW 💾 | MEDIUM 💾💾 | HIGH 💾💾💾 |

---

## 🎯 Profile Selection Guide

### Chọn profile theo scenario:

| Scenario | Recommended Profile |
|----------|-------------------|
| **Testing IDS/IPS detection** | 🟢 Stealth |
| **Long-term sustained attack** | 🟢 Stealth |
| **Bypassing rate limiting** | 🟢 Stealth |
| **Avoiding triggering alarms** | 🟢 Stealth |
| | |
| **General DoS testing** | 🟡 Balanced |
| **Standard pentest scenarios** | 🟡 Balanced |
| **Quick initial assessment** | 🟡 Balanced |
| **Unknown target characteristics** | 🟡 Balanced |
| | |
| **Stress testing capacity** | 🔴 Aggressive |
| **Finding resource limits** | 🔴 Aggressive |
| **Maximum impact demo** | 🔴 Aggressive |
| **Isolated lab environment** | 🔴 Aggressive |

### Decision Flow:

```
Bắt đầu
   │
   ├─ Cần tránh phát hiện?
   │     └─ YES → 🟢 Stealth
   │
   ├─ Cần impact tối đa?
   │     └─ YES → 🔴 Aggressive
   │
   └─ Không chắc? → 🟡 Balanced (mặc định an toàn)
```

---

## 💡 Best Practices

### 1. **Luôn bắt đầu với Stealth**
```bash
# Khởi động với Stealth để khảo sát
python phantom_storm_v2.py 192.168.1.100 80 50 --profile=stealth

# Nếu không có tác dụng → Nâng cấp lên Balanced
python phantom_storm_v2.py 192.168.1.100 80 150 --profile=balanced

# Cuối cùng mới dùng Aggressive
python phantom_storm_v2.py 192.168.1.100 80 300 --profile=aggressive
```

### 2. **Monitor target trong quá trình attack**
```bash
# Trên Ubuntu target, theo dõi:
# CPU usage
top

# Memory usage
free -h

# Network connections
netstat -an | grep ESTABLISHED | wc -l

# Nginx logs
sudo tail -f /var/log/nginx/access.log
```

### 3. **Kết hợp với các flags khác**
```bash
# Stealth + No spoofing (testing without bypass)
python phantom_storm_v2.py 192.168.1.100 80 50 --profile=stealth --no-spoof

# Aggressive + Custom method
python phantom_storm_v2.py 192.168.1.100 80 300 --profile=aggressive --method=HEAD
```

⚠️ **Lưu ý:** Khi dùng `--method` hoặc `--random-method` cùng với `--profile`, các flags này sẽ override HTTP method setting của profile.

---

## 🔬 Technical Details

### Profile Architecture

```python
@dataclass
class AttackProfile:
    name: str                              # Profile name
    description: str                       # Description
    threads: int                           # Number of threads
    timeout: int                           # Socket timeout
    keep_alive_interval: int               # Keep-alive interval
    http_method: Optional[HTTPMethod]      # HTTP method (None = random)
    randomize_method: bool                 # Random method mode
    use_spoofing: bool                     # Enable IP spoofing
    delay_between_threads: float           # Thread creation delay
    delay_between_reconnect: float         # Reconnect delay
```

### How Profiles Work

1. **Profile Selection:** User chọn profile qua `--profile=stealth`
2. **Settings Override:** Profile settings override CLI arguments
3. **Worker Configuration:** AttackWorker nhận profile parameters
4. **Runtime Behavior:** Workers hoạt động theo profile characteristics

### Profile Impact on Attack Behavior

| Setting | Impact |
|---------|--------|
| `threads` | Số kết nối đồng thời → Resource exhaustion |
| `timeout` | Thời gian chờ socket → Connection stability |
| `keep_alive_interval` | Tần suất gửi garbage → Detection evasion |
| `http_method` | Request type → Server load |
| `randomize_method` | Method diversity → Pattern detection |
| `use_spoofing` | IP diversity → Rate limit bypass |
| `delay_between_threads` | Thread creation speed → Detection risk |
| `delay_between_reconnect` | Reconnect speed → Persistence |

---

## 🧪 Testing & Validation

### Running Profile Tests
```bash
# Run all profile unit tests
python tests/test_attack_profiles.py

# Expected output: 20 tests passing
```

### Testing Profiles in Lab

**Setup:**
```
[Kali Linux] → [Ubuntu Nginx] → [Windows IIS]
   (Attack)      (Defense)         (Backend)
```

**Test Sequence:**

1. **Baseline:**
```bash
# No attack - record normal metrics
```

2. **Stealth Test:**
```bash
python phantom_storm_v2.py 192.168.1.2 80 50 --profile=stealth
# Quan sát: Có bị phát hiện không? IDS/IPS trigger?
```

3. **Balanced Test:**
```bash
python phantom_storm_v2.py 192.168.1.2 80 150 --profile=balanced
# Quan sát: Impact trên server như thế nào?
```

4. **Aggressive Test:**
```bash
python phantom_storm_v2.py 192.168.1.2 80 300 --profile=aggressive
# Quan sát: Server có crash không? Resource exhaustion?
```

---

## 📈 Monitoring Impact

### Metrics để theo dõi:

**Trên máy tấn công (Kali):**
- Connections Active
- Success Rate
- Packets/Second
- Unique IPs Used

**Trên máy phòng thủ (Ubuntu):**
```bash
# CPU usage
top
# Tìm nginx process, xem %CPU

# Memory
free -h
# Xem available memory

# Network connections
netstat -an | grep :80 | wc -l
# Đếm số connections tới port 80

# Nginx rate limiting
sudo tail -f /var/log/nginx/error.log | grep "limiting"
# Xem có bị rate limit không
```

### Expected Results:

| Profile | Connection Success | Detection Risk | Server Impact |
|---------|-------------------|----------------|---------------|
| Stealth | Medium (50-70%) | Very Low | Gradual |
| Balanced | High (70-85%) | Medium | Moderate |
| Aggressive | Very High (85-95%) | High | Severe |

---

## ⚠️ Important Warnings

### Legal Compliance
- ✅ Chỉ dùng trong lab có authorization
- ✅ Có written permission trước khi test
- ❌ KHÔNG attack hệ thống production
- ❌ KHÔNG attack hệ thống không được phép

### Profile-Specific Warnings

**Stealth:**
- ⚠️ Có thể mất nhiều thời gian để thấy impact
- ⚠️ Không phù hợp với testing nhanh

**Balanced:**
- ⚠️ Có thể vẫn trigger IDS/IPS
- ⚠️ Monitor server resources cẩn thận

**Aggressive:**
- ⚠️ **CỰC KỲ NGUY HIỂM** - Có thể crash server
- ⚠️ Chỉ dùng trong isolated lab
- ⚠️ Sẵn sàng reboot target server
- ⚠️ Có backup data trước khi test

---

## 🔗 Related Documentation

- [HTTP Methods Guide](./HTTP_METHODS.md) - Chi tiết về HTTP methods
- [Monitoring Guide](./MONITOR.md) - Hướng dẫn monitoring attack
- [API Reference](./API.md) - Full API documentation
- [README](../README.md) - General overview

---

## 📝 Changelog

**v2.5.0** - Attack Profiles Feature
- ✨ Added 3 predefined profiles: Stealth, Balanced, Aggressive
- ✨ Custom profile creation support
- ✨ CLI integration with `--profile` flag
- ✨ Profile comparison and selection guide
- ✨ Full test coverage (20 unit tests)

---

## 🤝 Contributing

Nếu bạn muốn đóng góp profile mới hoặc cải thiện existing profiles:

1. Fork repository
2. Tạo custom profile trong `src/core/attack_profiles.py`
3. Thêm tests trong `tests/test_attack_profiles.py`
4. Submit pull request với documentation

---

**⚡ Phantom Storm v2.5 - Attack Profiles Edition**

*"Choose your weapon wisely - Stealth for the ninja, Balanced for the strategist, Aggressive for the warrior."*
