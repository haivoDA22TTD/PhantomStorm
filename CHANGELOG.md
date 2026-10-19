# Changelog

All notable changes to Phantom Storm will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [2.5.0] - 2024-01-XX

### ✨ Added - Attack Profiles Feature (#2)

**Major Feature: Predefined Attack Profiles**
- Added 3 predefined attack profiles: Stealth, Balanced, Aggressive
- Created `src/core/attack_profiles.py` module with `AttackProfile` dataclass
- Implemented `ProfileType` enum for type-safe profile selection
- Added `AttackProfiles` factory class for profile management

**Stealth Profile:**
- 50 threads, 10s keep-alive interval
- Random HTTP methods for diversity
- Optimized for avoiding detection
- Ideal for IDS/IPS testing and bypass scenarios

**Balanced Profile:**
- 150 threads, 3s keep-alive interval
- Standard GET method
- Good mix of speed and stealth
- Recommended for general purpose testing

**Aggressive Profile:**
- 300 threads, 1s keep-alive interval
- POST method for heavier load
- Maximum resource exhaustion
- Designed for stress testing and capacity discovery

**CLI Integration:**
- Added `--profile=[stealth|balanced|aggressive]` flag to CLI
- Profile settings automatically override manual thread counts
- Seamless integration with existing flags (--method, --no-spoof)
- Profile information display on attack start

**Developer Tools:**
- `AttackProfiles.list_profiles()` - Get all predefined profiles
- `AttackProfiles.compare_profiles()` - Display comparison table
- `AttackProfiles.get_custom()` - Create custom profiles
- Convenience constants: `STEALTH`, `BALANCED`, `AGGRESSIVE`

**Documentation:**
- Created comprehensive `docs/ATTACK_PROFILES.md` (200+ lines)
- Profile selection guide and decision flowchart
- Usage examples for CLI and Python API
- Best practices and monitoring guidelines

**Examples & Tests:**
- Added `examples/attack_profiles_demo.py` - Interactive demo
- Created `tests/test_attack_profiles.py` - 20 unit tests
- Full test coverage for all profiles and functionality

**Exports:**
- Updated `src/core/__init__.py` to export profile components
- Added to public API: `AttackProfile`, `ProfileType`, `AttackProfiles`

---

## [2.5.0] - 2024-01-XX

### ✨ Added - HTTP Method Variation Feature (#1)

**Major Feature: Multiple HTTP Methods Support**
- Implemented support for 6 HTTP methods: GET, POST, HEAD, OPTIONS, PUT, DELETE
- Created `src/core/http_methods.py` module with `HTTPMethod` enum
- Added `HTTPMethodBuilder` class for generating method-specific requests

**HTTP Method Features:**
- GET: Standard requests with query parameters
- POST: Requests with auto-generated body (JSON/form-data templates)
- HEAD: Lightweight requests (headers only)
- OPTIONS: Method discovery requests
- PUT: Resource update requests with body
- DELETE: Resource deletion requests

**Random Method Mode:**
- Implemented `--random-method` flag for method randomization
- Each request uses a different random method
- Harder to detect patterns and fingerprint attacks
- Increases diversity of traffic

**CLI Integration:**
- Added `--method=[GET|POST|HEAD|OPTIONS|PUT|DELETE]` flag
- Added `--random-method` flag for randomization
- Method statistics in attack output
- Color-coded method display

**AttackWorker Updates:**
- Modified `AttackWorker` to accept `http_method` parameter
- Added `randomize_method` parameter for random mode
- Integrated `HTTPMethodBuilder` for request generation
- Per-method error handling and logging

**Documentation:**
- Created `docs/HTTP_METHODS.md` with full method documentation
- Added usage examples and method selection guide
- Documented POST body generation templates
- Performance and detection characteristics per method

**Examples & Tests:**
- Added `examples/http_methods_demo.py` - Shows all methods
- Created `tests/test_http_methods.py` - Full test coverage
- 15+ unit tests covering all methods and edge cases

---

## [2.0.0] - 2024-01-XX

### 🔄 Changed - Major Refactoring

**Architecture Redesign:**
- Migrated from monolithic `phantom_storm.py` to modular structure
- Created `src/core/` for core attack logic
- Created `src/utils/` for utilities (colors, logging, config)
- Cleaner separation of concerns
- Easier to maintain and extend

**Core Modules:**
- `src/core/attack_worker.py` - Attack logic (was inline in main)
- `src/core/statistics.py` - Statistics tracking
- `src/core/ip_generator.py` - Smart IP generation
- `src/__init__.py` - Package exports

**Utilities:**
- `src/utils/colors.py` - ANSI color constants
- `src/utils/logging_setup.py` - Logging configuration
- `src/utils/config.py` - Global configuration

**File Organization:**
```
d:\PhantomStorm\
├── src\
│   ├── core\          (core attack logic)
│   ├── utils\         (utilities)
│   └── __init__.py    (exports)
├── examples\          (usage examples)
├── tests\             (unit tests)
├── docs\              (documentation)
└── phantom_storm_v2.py (entry point)
```

### ✨ Added - IP Spoofing Enhancement

**Smart IP Generation:**
- Implemented intelligent public IP generation
- Avoids private ranges (10.x, 172.16-31.x, 192.168.x)
- Avoids reserved ranges (127.x, 224-255.x)
- Avoids localhost and broadcast addresses
- Generates realistic-looking IPs from public ranges

**Multiple Spoofing Headers:**
- `X-Forwarded-For` - Standard proxy header
- `X-Real-IP` - Nginx real IP header
- `Client-IP` - Alternative client IP header
- `X-Originating-IP` - Originating IP header
- `Via` - Proxy chain simulation
- `Forwarded` - RFC 7239 standard header
- `X-Client-IP` - Client IP variant
- `True-Client-IP` - True client IP header

**Bypass Tracking:**
- `unique_ips_used` - Count of unique IPs generated
- `bypass_attempts` - Total spoofing attempts
- `bypass_diversity` - IP diversity percentage
- Real-time statistics in attack output

**Configuration:**
- Added `--no-spoof` flag to disable spoofing
- Spoofing enabled by default
- Per-request unique IP generation
- Statistics display for spoofing effectiveness

### ✨ Added - Testing Infrastructure

**Unit Tests:**
- `tests/test_statistics.py` - Statistics module tests
- `tests/test_ip_generator.py` - IP generation tests
- Comprehensive test coverage for core functionality
- All tests passing

**Examples:**
- `examples/basic_attack.py` - Simple usage example
- `examples/advanced_attack.py` - Advanced features demo
- Python API usage demonstrations

### 📝 Added - Documentation

**Comprehensive Docs:**
- `docs/API.md` - Full API reference (400+ lines)
- `docs/MONITOR.md` - Monitoring guide
- `README.md` - Updated with new features
- Inline code documentation (docstrings)

**API Documentation Includes:**
- All classes and methods
- Parameter descriptions
- Return values
- Usage examples
- Architecture overview

### 🔧 Improved

**Code Quality:**
- Added type hints throughout codebase
- Consistent coding style
- Better error handling
- Comprehensive logging
- Clean function signatures

**Performance:**
- Optimized thread creation with staggering
- Better socket management
- Reduced memory footprint
- Faster statistics calculation

**User Experience:**
- Clearer banner and disclaimers
- Real-time statistics display
- Color-coded output for readability
- Better error messages
- Authorization confirmation prompt

**Security:**
- Added explicit authorization check
- Legal disclaimer on startup
- Logged all actions to file
- Clear usage warnings

---

## [1.0.0] - 2024-01-XX

### 🎉 Initial Release

**Core Features:**
- Layer 7 HTTP Keep-Alive / Slowloris DoS attack
- Multi-threaded architecture
- Connection keep-alive with garbage headers
- Real-time statistics display

**Basic Functionality:**
- Target IP and port specification
- Configurable thread count
- Socket-based HTTP connections
- Connection persistence mechanism

**Attack Mechanism:**
- Opens multiple HTTP connections
- Sends partial HTTP requests
- Maintains connections with periodic garbage data
- Exhausts server connection pool

**CLI:**
- Simple command-line interface
- 3 required arguments: IP, Port, Threads
- Ctrl+C to stop attack
- Basic statistics output

**Documentation:**
- Initial README.md
- Usage instructions
- Lab architecture diagram
- Mitigation guidelines (Nginx rate limiting)

---

## Version Numbering

- **Major (X.0.0)**: Breaking changes, major architecture changes
- **Minor (2.X.0)**: New features, backward compatible
- **Patch (2.5.X)**: Bug fixes, minor improvements

---

## Upgrade Path

### From v1.0 to v2.0+
1. Update imports from `phantom_storm.py` to `src` modules
2. Review new CLI flags (--no-spoof, --method, --random-method, --profile)
3. Check Python API changes (now class-based)
4. Update any custom scripts using the tool

### From v2.0 to v2.5
- No breaking changes
- New features are optional (profiles, HTTP methods)
- Existing scripts continue to work
- Consider adopting profiles for simpler usage

---

## Future Roadmap

### Planned Features (v2.6+)
- [ ] Payload customization
- [ ] Multiple target support (distributed attack)
- [ ] Auto-tuning based on target response
- [ ] TLS/SSL support (HTTPS)
- [ ] Proxy chain support
- [ ] Web UI for configuration
- [ ] Attack scheduling
- [ ] Result export (JSON, CSV)

### Under Consideration
- [ ] Integration with Metasploit
- [ ] Docker container support
- [ ] Distributed coordination (multiple attackers)
- [ ] Machine learning for evasion optimization
- [ ] Cloud deployment support (AWS, Azure)

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on:
- Reporting bugs
- Suggesting features
- Submitting pull requests
- Code style requirements

---

## License

See [LICENSE](LICENSE) for legal information.

---

**⚡ Phantom Storm - Authorized Penetration Testing Only**
