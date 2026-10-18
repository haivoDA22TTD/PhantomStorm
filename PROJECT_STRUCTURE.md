# 📁 Project Structure - Phantom Storm v2.5 Ultimate

## 🎯 Overview

Phantom Storm v2.5 đã được refactor hoàn toàn sang **modular architecture** để dễ dàng maintain, test và extend.

---

## 📂 Directory Structure

```
PhantomStorm/
│
├── src/                              # 🎯 Source code chính
│   ├── __init__.py                   # Package exports
│   ├── config.py                     # Configuration constants
│   │
│   ├── core/                         # 🔥 Core attack modules
│   │   ├── __init__.py
│   │   ├── attack_worker.py         # AttackWorker class (thread logic)
│   │   ├── statistics.py            # AttackStatistics class (metrics)
│   │   └── ip_generator.py          # IPGenerator class (spoofing)
│   │
│   └── utils/                        # 🛠️ Utility modules
│       ├── __init__.py
│       ├── colors.py                # Colors class (ANSI codes)
│       └── logger.py                # setup_logging() function
│
├── phantom_storm.py                  # 🕰️ Legacy entry point (v1.0 monolithic)
├── phantom_storm_v2.py               # ⭐ New modular entry point (recommended)
│
├── docs/                             # 📚 Documentation
│   ├── README.md                     # Full documentation (Vietnamese)
│   ├── USAGE.md                      # Quick usage guide
│   ├── MONITOR.md                    # Monitoring guide for defenders
│   ├── API.md                        # Complete API reference
│   ├── CHANGELOG.md                  # Version history
│   └── PROJECT_STRUCTURE.md          # This file (in docs/)
│
├── examples/                         # 📝 Example scripts
│   ├── basic_attack.py              # Simple attack (no spoofing)
│   └── advanced_attack.py           # Advanced (with spoofing + custom config)
│
├── tests/                            # 🧪 Unit tests
│   ├── __init__.py
│   ├── test_ip_generator.py         # IPGenerator tests
│   └── test_statistics.py           # AttackStatistics tests
│
├── scripts/                          # 🔧 Helper scripts
│   ├── demo.bat                      # Windows demo
│   ├── demo.sh                       # Linux/Mac demo
│   └── test_syntax.py                # Syntax checker
│
├── logs/                             # 📝 Auto-generated log files
│   └── phantom_storm_*.log
│
├── .gitignore                        # Git ignore rules
├── README.md                         # Main README (project overview)
└── LICENSE                           # MIT License

```

---

## 📦 Module Breakdown

### 1. `src/config.py` (Configuration)

**Purpose:** Central configuration constants

**Exports:**
- `USER_AGENTS`: List of User-Agent strings
- `PRIVATE_IP_RANGES`: IP ranges to avoid
- `DEFAULT_TIMEOUT`: Socket timeout (4s)
- `DEFAULT_KEEP_ALIVE_INTERVAL`: Garbage header interval (3s)
- `STATS_UPDATE_INTERVAL`: Dashboard refresh rate (2s)
- `VERSION`, `VERSION_NAME`: Version info

**Usage:**
```python
from src import config

print(config.VERSION)  # "2.5"
timeout = config.DEFAULT_TIMEOUT
```

---

### 2. `src/core/ip_generator.py` (IP Spoofing)

**Purpose:** Smart IP generation for bypass attacks

**Class:** `IPGenerator`

**Methods:**
- `generate_public_ip() -> str`: Generate random public IP
- `is_private_ip(ip_tuple) -> bool`: Check if IP is private
- `generate_proxy_chain() -> str`: Fake Via header

**Usage:**
```python
from src.core import IPGenerator

ip = IPGenerator.generate_public_ip()
print(ip)  # "203.45.67.89"
```

---

### 3. `src/core/statistics.py` (Metrics Tracking)

**Purpose:** Thread-safe attack statistics

**Class:** `AttackStatistics`

**Methods:**
- `connection_established(spoofed_ip)`: Record success
- `connection_closed()`: Record close
- `connection_failed(error_type)`: Record failure
- `packet_sent()`: Record packet
- `get_stats() -> Dict`: Get all metrics
- `reset()`: Reset all stats

**Usage:**
```python
from src.core import AttackStatistics

stats = AttackStatistics()
stats.connection_established("203.45.67.89")
print(stats.get_stats())
```

---

### 4. `src/core/attack_worker.py` (Attack Logic)

**Purpose:** Individual thread attack implementation

**Class:** `AttackWorker`

**Constructor:**
```python
AttackWorker(
    target_ip: str,
    target_port: int,
    stats: AttackStatistics,
    worker_id: int,
    use_spoofing: bool = True,
    timeout: int = 4,
    keep_alive_interval: int = 3
)
```

**Methods:**
- `run()`: Main attack loop
- `stop()`: Graceful shutdown
- `build_http_request(spoofed_ip) -> str`: Build HTTP request

**Usage:**
```python
from src.core import AttackWorker, AttackStatistics

stats = AttackStatistics()
worker = AttackWorker("192.168.1.100", 80, stats, worker_id=1)
worker.run()  # Blocks until stopped
```

---

### 5. `src/utils/colors.py` (Terminal Colors)

**Purpose:** ANSI color codes for output

**Class:** `Colors`

**Attributes:**
- `OKGREEN`, `WARNING`, `FAIL`, `OKCYAN`, etc.
- `BOLD`, `UNDERLINE`, `ENDC`

**Methods:**
- `disable()`: Turn off colors

**Usage:**
```python
from src.utils import Colors

print(f"{Colors.OKGREEN}Success!{Colors.ENDC}")
```

---

### 6. `src/utils/logger.py` (Logging)

**Purpose:** Centralized logging setup

**Function:** `setup_logging(log_file)`

**Usage:**
```python
from src.utils import setup_logging

setup_logging("my_attack.log")
import logging
logging.info("Attack started")
```

---

## 🔄 Import Patterns

### Pattern 1: Import from src package (Recommended)

```python
from src import (
    AttackWorker,
    AttackStatistics,
    IPGenerator,
    Colors,
    setup_logging,
    config
)
```

### Pattern 2: Import specific modules

```python
from src.core import AttackWorker
from src.core.ip_generator import IPGenerator
from src.utils.colors import Colors
```

### Pattern 3: Import in tests

```python
import sys
sys.path.insert(0, '..')  # Go up one directory

from src.core import IPGenerator
```

---

## 📝 File Descriptions

| File | Lines | Purpose |
|------|-------|---------|
| `src/config.py` | ~60 | Configuration constants |
| `src/core/ip_generator.py` | ~90 | IP spoofing logic |
| `src/core/statistics.py` | ~120 | Statistics tracking |
| `src/core/attack_worker.py` | ~180 | Attack thread logic |
| `src/utils/colors.py` | ~30 | Terminal colors |
| `src/utils/logger.py` | ~40 | Logging setup |
| `phantom_storm_v2.py` | ~300 | Main entry point |
| **Total (Core)** | **~820** | Clean, modular code |

---

## 🎯 Benefits of New Structure

### ✅ Modularity
- Each module has single responsibility
- Easy to test individual components
- Can reuse modules in other projects

### ✅ Testability
- Unit tests for each module
- Mock dependencies easily
- Isolated testing

### ✅ Maintainability
- Clear code organization
- Easy to find and fix bugs
- Documentation alongside code

### ✅ Extensibility
- Add new features without touching core
- Plugin architecture possible
- Easy to customize

### ✅ Readability
- Logical file structure
- Imports show dependencies clearly
- Self-documenting code

---

## 🔧 Development Workflow

### Adding New Feature

1. **Create module:**
   ```bash
   # Add to src/core/ or src/utils/
   touch src/core/new_feature.py
   ```

2. **Write code:**
   ```python
   # src/core/new_feature.py
   class NewFeature:
       def __init__(self):
           pass
   ```

3. **Export from package:**
   ```python
   # src/__init__.py
   from .core.new_feature import NewFeature
   __all__ = [..., 'NewFeature']
   ```

4. **Write tests:**
   ```bash
   touch tests/test_new_feature.py
   ```

5. **Document:**
   - Update `docs/API.md`
   - Add example to `examples/`

---

## 🧪 Testing Structure

### Unit Tests Location

```
tests/
├── __init__.py
├── test_ip_generator.py      # Tests for IPGenerator
└── test_statistics.py         # Tests for AttackStatistics
```

### Running Tests

```bash
# Individual test
cd tests
python test_ip_generator.py

# All tests
python test_ip_generator.py && python test_statistics.py
```

---

## 📚 Documentation Structure

```
docs/
├── README.md              # Main docs (Vietnamese)
├── USAGE.md               # Quick reference
├── MONITOR.md             # Defender's guide
├── API.md                 # Complete API reference
└── CHANGELOG.md           # Version history
```

---

## 🎯 Migration Guide

### From v1.0 (Monolithic) to v2.5 (Modular)

**Old way (v1.0):**
```python
python phantom_storm.py 192.168.1.100 80 200
```

**New way (v2.5):**
```python
python phantom_storm_v2.py 192.168.1.100 80 200
```

**Custom integration (OLD - not possible):**
- Had to copy/paste code chunks
- No reusability

**Custom integration (NEW - easy!):**
```python
from src import AttackWorker, AttackStatistics

# Use modules independently!
stats = AttackStatistics()
worker = AttackWorker("192.168.1.100", 80, stats, 1)
```

---

## 📊 Code Statistics

| Category | v1.0 Monolithic | v2.5 Modular | Improvement |
|----------|-----------------|--------------|-------------|
| **Files** | 1 | 14 | +1400% |
| **Lines (Core)** | ~500 | ~820 | +64% (with features) |
| **Modules** | 0 | 6 | ∞ |
| **Tests** | 0 | 2 | ∞ |
| **Examples** | 0 | 2 | ∞ |
| **Testability** | Hard | Easy | ✅ |
| **Reusability** | None | High | ✅ |

---

## 🚀 Future Enhancements

### Phase 3 (v3.0) - Planned Features

Will be added as new modules:

```
src/
├── core/
│   ├── ... (existing)
│   ├── proxy_manager.py       # Real proxy support
│   └── ssl_handler.py          # HTTPS support
│
├── plugins/                    # NEW!
│   ├── custom_headers.py
│   └── rate_adapter.py
│
└── config/                     # NEW!
    ├── yaml_loader.py
    └── json_loader.py
```

---

## 👨‍💻 Contributing

### Code Style

- Follow PEP 8
- Use type hints
- Add docstrings
- Write tests

### Pull Request Process

1. Fork repo
2. Create feature branch
3. Add module to `src/`
4. Write tests in `tests/`
5. Update `docs/API.md`
6. Submit PR

---

## 📄 License

MIT License - See LICENSE file

---

**Last Updated:** v2.5 Ultimate Edition  
**Maintainer:** haivoDA22TTD
