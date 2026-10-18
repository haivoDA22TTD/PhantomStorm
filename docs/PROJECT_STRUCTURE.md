# 📁 Project Structure

```
PhantomStorm/
│
├── phantom_storm.py          # 🎯 Main attack tool (v2.5 Ultimate)
│
├── README.md                 # 📖 Complete documentation
├── USAGE.md                  # 🚀 Quick usage guide
├── CHANGELOG.md              # 📋 Version history
├── PROJECT_STRUCTURE.md      # 📁 This file
│
├── demo.bat                  # 🪟 Windows demo script
├── demo.sh                   # 🐧 Linux/Mac demo script
│
├── .gitignore                # 🚫 Git ignore rules
│
└── logs/                     # 📝 Auto-generated log files
    ├── phantom_storm_20241215_143022.log
    ├── phantom_storm_20241215_150530.log
    └── ...
```

---

## File Descriptions

### Core Files

#### `phantom_storm.py` (Main Tool)
- **Size**: ~500 lines
- **Language**: Python 3.7+
- **Dependencies**: None (stdlib only)
- **Features**:
  - Layer 7 Slowloris attack
  - IP spoofing with 8 bypass headers
  - Real-time statistics dashboard
  - Comprehensive logging
  - Error tracking and analytics

**Key Classes**:
- `IPGenerator`: Smart public IP generation
- `AttackStatistics`: Thread-safe stats tracking
- `AttackWorker`: Individual thread attack logic
- `Colors`: ANSI color codes

**Key Functions**:
- `main()`: Entry point and orchestration
- `validate_target()`: Pre-attack connectivity check
- `stats_monitor()`: Real-time dashboard
- `get_user_confirmation()`: Authorization check

---

### Documentation Files

#### `README.md`
- **Purpose**: Complete project documentation
- **Sections**:
  - Legal disclaimer
  - Feature list
  - Installation guide
  - Usage instructions with examples
  - Output explanation
  - Attack mechanism details
  - Troubleshooting
  - FAQ (8 questions)
  - Roadmap
  
**Length**: ~600 lines

---

#### `USAGE.md`
- **Purpose**: Quick reference guide
- **Content**:
  - Basic syntax
  - Common use cases
  - Parameter guidelines
  - Expected output
  - Bypass headers list
  - Quick troubleshooting

**Length**: ~150 lines

---

#### `CHANGELOG.md`
- **Purpose**: Version history tracking
- **Content**:
  - v2.5 Ultimate changes
  - v2.0 Professional changes
  - v1.0 Basic features
  - Version comparison table
  - Upcoming features

**Length**: ~200 lines

---

#### `PROJECT_STRUCTURE.md` (This File)
- **Purpose**: Project organization overview
- **Content**:
  - Directory tree
  - File descriptions
  - Development workflow
  - Contribution guidelines

---

### Demo Scripts

#### `demo.bat` (Windows)
- **Purpose**: Quick test on Windows
- **Target**: localhost:8080
- **Threads**: 20
- **Spoofing**: Disabled (local test)

#### `demo.sh` (Linux/Mac)
- **Purpose**: Quick test on Unix systems
- **Target**: localhost:8080
- **Threads**: 20
- **Spoofing**: Disabled (local test)

**Usage**:
```bash
# Windows
demo.bat

# Linux/Mac
chmod +x demo.sh
./demo.sh
```

---

### Generated Files

#### `logs/` Directory
- **Auto-created**: When tool runs
- **File format**: `phantom_storm_YYYYMMDD_HHMMSS.log`
- **Content**:
  - Start time and configuration
  - Spoofing status
  - Thread count
  - Target information
  - Runtime events
  - Final statistics

**Example log entry**:
```
2024-12-15 14:30:22 - [INFO] - Starting Phantom Storm v2.5 - Target: 192.168.1.100:80
2024-12-15 14:30:22 - [INFO] - IP Spoofing: ENABLED
2024-12-15 14:30:22 - [INFO] - Spawning 200 attack threads
...
2024-12-15 14:35:45 - [INFO] - Attack completed. Final stats logged.
```

---

## Code Architecture

### v2.5 Architecture Diagram

```
┌─────────────────────────────────────────┐
│          phantom_storm.py               │
├─────────────────────────────────────────┤
│                                         │
│  ┌──────────────────────────────────┐  │
│  │   IPGenerator (Static Class)     │  │
│  ├──────────────────────────────────┤  │
│  │ - generate_public_ip()           │  │
│  │ - is_private_ip()                │  │
│  │ - generate_proxy_chain()         │  │
│  └──────────────────────────────────┘  │
│                                         │
│  ┌──────────────────────────────────┐  │
│  │   AttackStatistics (Class)       │  │
│  ├──────────────────────────────────┤  │
│  │ - connection_established()       │  │
│  │ - connection_failed()            │  │
│  │ - packet_sent()                  │  │
│  │ - get_stats()                    │  │
│  └──────────────────────────────────┘  │
│                                         │
│  ┌──────────────────────────────────┐  │
│  │   AttackWorker (Class)           │  │
│  ├──────────────────────────────────┤  │
│  │ - build_http_request()           │  │
│  │ - run()                          │  │
│  │ - stop()                         │  │
│  └──────────────────────────────────┘  │
│                                         │
│  ┌──────────────────────────────────┐  │
│  │   Main Functions                 │  │
│  ├──────────────────────────────────┤  │
│  │ - print_banner()                 │  │
│  │ - validate_target()              │  │
│  │ - get_user_confirmation()        │  │
│  │ - stats_monitor()                │  │
│  │ - main()                         │  │
│  └──────────────────────────────────┘  │
│                                         │
└─────────────────────────────────────────┘
```

### Execution Flow

```
main()
  ├─> print_banner()
  ├─> Parse arguments
  ├─> get_user_confirmation()
  ├─> setup_logging()
  ├─> validate_target()
  ├─> Create AttackStatistics instance
  ├─> Spawn N threads (AttackWorker instances)
  │   └─> Each worker:
  │       ├─> IPGenerator.generate_public_ip()
  │       ├─> build_http_request() with 8 headers
  │       ├─> Connect and send
  │       └─> Loop: send garbage headers
  ├─> Start stats_monitor thread
  ├─> Wait for Ctrl+C
  └─> Display final statistics
```

---

## Development Workflow

### Adding New Features

1. **Fork the project**
2. **Create feature branch**:
   ```bash
   git checkout -b feature/new-feature-name
   ```
3. **Make changes** to `phantom_storm.py`
4. **Test thoroughly** in lab environment
5. **Update documentation**:
   - README.md (if user-facing)
   - CHANGELOG.md (always)
   - USAGE.md (if syntax changes)
6. **Commit and push**:
   ```bash
   git add .
   git commit -m "feat: Add new feature"
   git push origin feature/new-feature-name
   ```
7. **Create Pull Request**

---

### Testing Checklist

Before committing:
- [ ] Test with spoofing enabled
- [ ] Test with `--no-spoof` flag
- [ ] Test graceful shutdown (Ctrl+C)
- [ ] Verify log file creation
- [ ] Check statistics accuracy
- [ ] Test invalid arguments handling
- [ ] Test authorization denial
- [ ] Test unreachable target handling
- [ ] Verify no Python dependencies added
- [ ] Run on both Windows and Linux

---

## File Sizes (Approximate)

| File | Lines | Size |
|------|-------|------|
| phantom_storm.py | ~500 | ~20 KB |
| README.md | ~600 | ~30 KB |
| CHANGELOG.md | ~200 | ~10 KB |
| USAGE.md | ~150 | ~6 KB |
| PROJECT_STRUCTURE.md | ~250 | ~12 KB |
| demo.bat | ~20 | ~1 KB |
| demo.sh | ~20 | ~1 KB |
| .gitignore | ~30 | ~1 KB |

**Total**: ~80 KB (excluding logs)

---

## License & Legal

- **License**: MIT (use at your own risk)
- **Disclaimer**: Tool is for authorized testing ONLY
- **Liability**: Authors not responsible for misuse

---

## Version History

| Version | Date | Key Feature |
|---------|------|-------------|
| v1.0 | 2024-XX | Basic Slowloris |
| v2.0 | 2024-XX | Professional edition |
| v2.5 | 2024-XX | IP Spoofing & Bypass |

---

**Last Updated**: 2024-12
**Maintainer**: Phantom Storm Dev Team
