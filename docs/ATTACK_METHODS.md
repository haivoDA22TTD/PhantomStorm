# Phantom Storm - Attack Methods Documentation

## Overview

Phantom Storm supports multiple Layer 7 DoS attack methods. Each method has different characteristics and is effective against different types of targets.

---

## Attack Types

### 1. **Slowloris** (Default)
**Status:** ✅ Fully Implemented

**Description:**  
Classic Keep-Alive exhaustion attack. Sends incomplete HTTP headers and keeps connections alive by periodically sending garbage headers.

**How it works:**
1. Opens connection to target
2. Sends partial HTTP headers (no final `\r\n\r\n`)
3. Periodically sends additional headers to keep connection alive
4. Server keeps connection open waiting for complete request
5. Multiple connections → server exhaustion

**Best targets:**
- Apache HTTP Server
- Nginx (with certain configurations)
- IIS
- Generic web servers with limited connection pools

**Effectiveness:**
- ✅ Very effective on servers with limited connection pools
- ✅ Low bandwidth requirement
- ✅ Works with IP spoofing for bypass
- ⚠️ May be blocked by modern WAFs
- ⚠️ Ineffective against async servers (Node.js, Go)

**Usage:**
```bash
# Default attack (Slowloris)
python phantom_storm_v2.py 192.168.1.2 80 200

# Explicit Slowloris
python phantom_storm_v2.py 192.168.1.2 80 200 --attack-type=slowloris
```

---

### 2. **Slow POST** (R-U-Dead-Yet)
**Status:** ✅ Fully Implemented

**Description:**  
Send POST request body extremely slowly (byte-by-byte) to exhaust server's upload handler connections.

**How it works:**
1. Sends complete HTTP POST headers with large `Content-Length`
2. Sends body data byte-by-byte with configurable delays
3. Server must wait for complete body → connection held open
4. Multiple slow uploads → server resource exhaustion

**Best targets:**
- Upload endpoints (`/upload`, `/api/upload`, `/file/upload`)
- Form submission endpoints (`/contact`, `/register`, `/login`)
- API endpoints accepting POST data
- Comment/feedback forms
- Any endpoint that processes POST body data

**Effectiveness:**
- ✅ Very effective against upload handlers
- ✅ Bypasses many timeout defenses (server receives data)
- ✅ Works well with low bandwidth
- ✅ Hard to detect (looks like slow client upload)
- ✅ Low resource usage on attacker side
- ✅ Works with HTTPS/TLS
- ✅ Effective against both sync and async servers

**Parameters:**
- `--content-length`: Declared body size in bytes (default: 1,000,000)
- `--post-delay`: Delay between bytes in seconds (default: 10.0)

**Attack Duration:**
```
Duration = content_length × post_delay

Examples:
- 100,000 bytes × 5s  = 500,000s (5.7 days per connection!)
- 500,000 bytes × 10s = 5,000,000s (57.8 days per connection!)
- 1,000,000 bytes × 10s = 10,000,000s (115.7 days per connection!)
```

**Usage Examples:**

```bash
# Basic slow POST
python phantom_storm_v2.py 192.168.1.2 80 100 --attack-type=slow-post

# Custom parameters (faster attack)
python phantom_storm_v2.py 192.168.1.2 80 100 \
  --attack-type=slow-post \
  --content-length=500000 \
  --post-delay=5.0

# HTTPS target
python phantom_storm_v2.py 192.168.1.2 443 100 \
  --attack-type=slow-post \
  --https

# Aggressive (200 threads, fast bytes)
python phantom_storm_v2.py 192.168.1.2 80 200 \
  --attack-type=slow-post \
  --content-length=100000 \
  --post-delay=1.0

# Stealth (slow, hard to detect)
python phantom_storm_v2.py 192.168.1.2 80 50 \
  --attack-type=slow-post \
  --content-length=1000000 \
  --post-delay=30.0
```

**Recommended Parameters by Target:**

| Target Strength | Threads | Content-Length | Byte Delay | Duration/conn |
|----------------|---------|----------------|------------|---------------|
| **Weak** (small server) | 50 | 100,000 | 5s | 5.7 days |
| **Medium** (typical server) | 100 | 500,000 | 10s | 57.8 days |
| **Strong** (enterprise) | 200 | 1,000,000 | 15s | 173.6 days |

**Defense Bypass:**
- ✅ IP spoofing enabled by default (unique IP per connection)
- ✅ Works with `X-Forwarded-For`, `X-Real-IP` headers
- ✅ Bypasses rate limiting (each connection = different IP)
- ✅ Hard to fingerprint (looks like legitimate slow upload)

**Target Selection Tips:**
1. Look for endpoints that accept POST data
2. Upload forms are ideal targets
3. API endpoints with JSON/XML body parsing
4. Login/registration pages
5. Contact/feedback forms

---

### 3. **Slow Read**
**Status:** 🚧 Not Yet Implemented

**Description:**  
Read server response extremely slowly to exhaust server memory/buffers.

**How it works:**
1. Send normal HTTP request
2. Set very small TCP receive window
3. Read response data extremely slowly
4. Server's send buffer fills up → connection held open
5. Multiple connections → server memory exhaustion

**Best targets:**
- Servers serving large files
- Streaming endpoints
- Servers with limited send buffers

**Planned Implementation:** Future version

---

### 4. **Range Header** (Apache Killer)
**Status:** 🚧 Not Yet Implemented

**Description:**  
Request multiple byte ranges to spike CPU usage during range processing.

**How it works:**
1. Send HTTP request with multiple byte ranges
2. Server must process and merge ranges → CPU intensive
3. Multiple requests → CPU exhaustion

**Best targets:**
- Apache HTTP Server (vulnerable versions)
- Servers supporting byte range requests
- CDNs with range support

**Planned Implementation:** Future version

---

### 5. **Cache Bypass**
**Status:** 🚧 Not Yet Implemented

**Description:**  
Add random query parameters to bypass cache and hit backend directly.

**How it works:**
1. Send requests with random parameters
2. Cache can't serve → backend must process
3. High request rate → backend overload

**Best targets:**
- Sites with aggressive caching
- CDN-protected sites
- Reverse proxy configurations

**Planned Implementation:** Future version

---

## Comparison Table

| Attack Type | Bandwidth | Effectiveness | Stealth | Bypass Capability | Status |
|-------------|-----------|---------------|---------|-------------------|--------|
| **Slowloris** | Very Low | High | Medium | High (with IP spoof) | ✅ |
| **Slow POST** | Very Low | Very High | High | Very High | ✅ |
| **Slow Read** | Low | High | High | High | 🚧 |
| **Range Header** | Medium | High | Low | Medium | 🚧 |
| **Cache Bypass** | High | Medium | Low | High | 🚧 |

---

## General Tips

### 1. Start Conservative
- Begin with 50-100 threads
- Monitor target behavior
- Increase gradually if needed

### 2. Use IP Spoofing
- Enabled by default
- Each connection uses unique spoofed IP
- Bypasses most rate limiting
- Disable with `--no-spoof` if needed

### 3. HTTPS Testing
- Add `--https` flag for HTTPS targets
- Use `--sni=hostname` for SNI
- Use `--verify-ssl` to verify certificates

### 4. Combine with Profiles
```bash
# Stealth profile + Slow POST
python phantom_storm_v2.py 192.168.1.2 80 50 \
  --profile=stealth \
  --attack-type=slow-post
```

### 5. Monitor & Adjust
- Watch target server resources
- Adjust thread count based on effect
- Adjust delays for slow POST
- Check logs for errors

---

## Legal Notice

⚠️ **IMPORTANT:** These attack methods are for **AUTHORIZED TESTING ONLY**.

You **MUST** have:
- Explicit written permission to test the target
- Proper authorization documentation
- Understanding of legal consequences

Unauthorized use is **ILLEGAL** and may result in criminal prosecution.

---

## References

- **Slowloris:** Original by RSnake (2009)
- **Slow POST (R.U.D.Y.):** Raviv Raz (2010)
- **Apache Killer:** Range header attack (2011)

---

**Last Updated:** Feature #4 Implementation (Slow POST)  
**Version:** Phantom Storm v2.5 Ultimate
