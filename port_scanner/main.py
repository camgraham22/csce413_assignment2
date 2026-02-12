#!/usr/bin/env python3
"""
Port Scanner - Starter Template for Students
Assignment 2: Network Security

This is a STARTER TEMPLATE to help you get started.
You should expand and improve upon this basic implementation.

TODO for students:
1. Implement multi-threading for faster scans
2. Add banner grabbing to detect services
3. Add support for CIDR notation (e.g., 192.168.1.0/24)
4. Add different scan types (SYN scan, UDP scan, etc.)
5. Add output formatting (JSON, CSV, etc.)
6. Implement timeout and error handling
7. Add progress indicators
8. Add service fingerprinting
"""

import socket
import time
import sys
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed 

def scan_port(target, port, timeout=1.0):
    """
    Scan a single port on the target host

    Args:
        target (str): IP address or hostname to scan
        port (int): Port number to scan
        timeout (float): Connection timeout in seconds

    Returns:
        bool: True if port is open, False otherwise
    """
    try:
        # TODO: Create a socket
        # TODO: Set timeout
        # TODO: Try to connect to target:port
        # TODO: Close the socket
        # TODO: Return True if connection successful
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        sock.connect((target, port))
        banner = get_banner(sock)
        sock.close()
        return True, banner

        pass  # Remove this and implement

    except (socket.timeout, ConnectionRefusedError, OSError):
        return False, None

def get_banner(socket):
    try:
        banner = socket.recv(1024).decode('utf-8', errors='ignore').strip()
        if not banner:
            socket.send(b"GET / HTTP/1.1\r\nHost: localhost\r\n\r\n")
            banner = socket.recv(1024).decode().strip()
            return banner if banner else None
    except:
        return None

def scan_range(target, start_port, end_port):
    """
    Scan a range of ports on the target host

    Args:
        target (str): IP address or hostname to scan
        start_port (int): Starting port number
        end_port (int): Ending port number

    Returns:
        list: List of open ports
    """
    open_ports = []

    print(f"[*] Scanning {target} from port {start_port} to {end_port}")
    print(f"[*] This may take a while...")
    start_time = time.time()

    # TODO: Implement the scanning logic
    # Hint: Loop through port range and call scan_port()
    # Hint: Consider using threading for better performance

    total_ports_to_scan = end_port - start_port + 1
    ports_already_scanned = 0
    
    with ThreadPoolExecutor(max_workers=100) as executor:
        future_to_port = {executor.submit(scan_port, target, p): p for p in range(start_port, end_port + 1)}

        for future in as_completed(future_to_port):
            port = future_to_port[future]
            is_open, banner = future.result()
            ports_already_scanned += 1
            percent_scanned = (ports_already_scanned / total_ports_to_scan) * 100
            if is_open:
                open_ports.append((port, banner))
                if banner:
                    banner = banner[:50]
                else:
                    banner = "No banner found."
                print(f"\n[*] Port {port}: OPEN - Banner: {banner}")
            sys.stdout.write(f'\rPercentage of ports scanned: {percent_scanned:.1f}%')
            sys.stdout.flush()

    print()
    end_time = time.time()
    total_time = end_time - start_time
    print(f"Scan complete - Total Time: {total_time} seconds")

    return open_ports


def main():
    """Main function"""
    # TODO: Parse command-line arguments
    # TODO: Validate inputs
    # TODO: Call scan_range()
    # TODO: Display results

    # Example usage (you should improve this):
    if len(sys.argv) < 2:
        print("Usage: python3 port_scanner_template.py <target>")
        print("Example: python3 port_scanner_template.py 172.20.0.10")
        sys.exit(1)

    # target = sys.argv[1]
    # start_port = 1
    # end_port = 1024  # Scan first 1024 ports by default

    parser = argparse.ArgumentParser()
    parser.add_argument("--target")
    parser.add_argument("--ports")
    parser.add_argument("--output")

    args = parser.parse_args()
    target = args.target
    ports = args.ports.split('-')
    start_port = int(ports[0])
    end_port = int(ports[1])
    output = args.output

    print(f"[*] Starting port scan on {target}")


    open_ports = scan_range(target, start_port, end_port)
    output_file = None

    if output:
        try:
            output_file = open(output, "w")  
        except IOError as error:
            print(f"Error opening file: {error}")

    print(f"\n[+] Scan complete!", file=output_file)
    print(f"[+] Found {len(open_ports)} open ports:", file=output_file)
    for port, banner in open_ports:
        print(f"Port {port}: OPEN - Banner: {banner}", file=output_file)
    
    if output_file:
        output_file.close()

if __name__ == "__main__":
    main()
