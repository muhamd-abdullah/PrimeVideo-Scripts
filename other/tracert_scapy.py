'''
Used the scapy library in Python to implement a traceroute using TCP SYN packets. 

'''

from scapy.all import IP, TCP, sr1

def traceroute(target, max_hops=30, timeout=2):
    # Perform the traceroute
    for ttl in range(1, max_hops + 1):
        # Create the IP packet with the specified TTL
        packet = IP(dst=target, ttl=ttl) / TCP(dport=80, flags="S", options=[('Timestamp',(0,0))])

        # Send the packet and receive the response
        reply = sr1(packet, verbose=False, timeout=timeout)
        try:
            pass
            #reply.show()
        except:
            pass
        if reply is None:
            # No response received, print the timeout message
            print(f"{ttl}. *")
        else:
            # Intermediate hop, print the IP address
            print(f"{ttl}. {reply.src}")
            if reply.src == target:
                break

# Example usage
target = "18.165.183.115"
traceroute(target)


