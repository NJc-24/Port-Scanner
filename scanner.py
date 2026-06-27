"""
Simple Port Scanner
A clean, multi-threaded TCP port scanner built for learning network reconnaissance.
"""

import pyfiglet
import socket
import threading
import argparse
from datetime import datetime
import sys

#Display ASCII banner.
def print_banner():
    print(pyfiglet.figlet_format("PORT SCANNER"))
    print("=" * 60)

#Scan a single port and add to open_ports list if successful.
def scan_port(target: str, port: int, open_ports: list, timeout: float = 1.0):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            if sock.connect_ex((target, port)) == 0:
                open_ports.append(port)
    except:
        pass

def main():
    print_banner()

    parser = argparse.ArgumentParser(description="Fast & Clean TCP Port Scanner")
    parser.add_argument("target", help="Target IP address or hostname")
    parser.add_argument("-p", "--ports", default="1-1000",
                        help="Port range to scan (default: 1-1000)")
    parser.add_argument("-t", "--threads", type=int, default=200,
                        help="Number of concurrent threads (default: 200)")
    parser.add_argument("-T", "--timeout", type=float, default=1.0,
                        help="Connection timeout in seconds (default: 1.0)")

    args = parser.parse_args()

# Resolve target
    try:
        target_ip = socket.gethostbyname(args.target)
    except socket.gaierror:
        print("[-] Error: Hostname could not be resolved.")
        sys.exit(1)

    print(f"[+] Target: {args.target} ({target_ip})")
    print(f"[+] Scan started at: {datetime.now()}")
    print("-" * 60)

    open_ports = []
    threads = []

    start, end = map(int, args.ports.split("-"))

    for port in range(start, end + 1):
        thread = threading.Thread(
            target=scan_port,
            args=(target_ip, port, open_ports, args.timeout)
        )
        threads.append(thread)
        thread.start()

# Control thread count
        if len(threads) >= args.threads:
            for t in threads:
                t.join()
            threads = []

# Wait for remaining threads
    for t in threads:
        t.join()

# Results
    print(f"\n[+] Scan completed at: {datetime.now()}")
    if open_ports:
        print(f"\n[+] Found {len(open_ports)} open port(s):")
        for port in sorted(open_ports):
            try:
                service = socket.getservbyport(port)
                print(f"    • Port {port:<5} → OPEN ({service})")
            except:
                print(f"    • Port {port:<5} → OPEN")
    else:
        print("[-] No open ports found in the given range.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Scan interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n[!] Unexpected error: {e}")