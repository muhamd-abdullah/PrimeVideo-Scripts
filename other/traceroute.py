import subprocess
import socket
import random
import re


def traceroute(target, max_hops=30, timeout=2):
    # Attempt traceroute using different methods
    methods = ["icmp", "udp", "tcp"]
    #methods = ["tcp"]
    for method in methods:
        print(f"Traceroute using {method.upper()}:")

        # Execute the traceroute command using the selected method
        command = f"traceroute -I -w {timeout} -m {max_hops} -q 1 {target}"
        if method == "udp":
            command = f"traceroute -P udp {timeout} -m {max_hops} -q 1 {target}"
        elif method == "tcp":
            command = f"traceroute -P tcp -w {timeout} -m {max_hops} -q 1 {target}"

        try:
            output = subprocess.check_output(command.split()).decode("utf-8")
            hops_ip = []
            hops_hostname = []
            lines = output.strip().split('\n')
            
            for line in lines:
                if "*" in line:
                    hops_ip.append("*")
                    hops_hostname.append("*")
                    continue
                
                match = re.search(r'(\d+)\s+([^\s]+|\*)\s+\(([^)]+)\)', line)
                
                if match:
                    hop_number = int(match.group(1))
                    host = match.group(2)
                    ip_address = match.group(3)
                    
                    if ':' in ip_address:  # IPv6 address
                        ip_address = ip_address.split()[0]  # Remove any additional information after the address
                    hops_ip.append(ip_address)
                    hops_hostname.append(host)
            
            for i in range(len(hops_hostname)):
                print(i+1, hops_hostname[i], hops_ip[i])
            

            break  # Stop attempting other methods if successful

        except subprocess.CalledProcessError as e:
            print(f"Traceroute failed with error: {e}")
            print()

    # If none of the methods were successful, fallback to Python-based traceroute
    else:
        print("Fallback to Python-based traceroute:")

        for ttl in range(1, max_hops + 1):
            # Create a socket for the traceroute
            traceroute_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
            traceroute_socket.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)

            # Send an empty packet to get the ICMP Time Exceeded response
            packet = b""
            traceroute_socket.sendto(packet, (target, 80))

            try:
                _, addr = traceroute_socket.recvfrom(512)
                print(f"{ttl}. {addr[0]}")
                traceroute_socket.close()

                if addr[0] == target:
                    break  # Reached the target, stop the traceroute

            except socket.timeout:
                print(f"{ttl}. *")
                traceroute_socket.close()

# Example usage
target = "18.165.183.115"
#target = "52.93.42.221"
traceroute(target)
