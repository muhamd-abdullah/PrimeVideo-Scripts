import socket
import time

def measure_latency(url):
    # Resolve the IP address of the server
    ip = socket.gethostbyname(url)
    print(f"Server IP: {ip}")

    # Create a TCP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Set a timeout value for the socket (in seconds)
    sock.settimeout(5)

    try:
        # Start the timer
        start_time = time.time()

        # Connect to the server
        sock.connect((ip, 80))

        # Stop the timer and calculate the latency
        end_time = time.time()
        latency = end_time - start_time
        print(f"Latency: {latency} seconds")
    except socket.error as e:
        print(f"Error: {e}")
    finally:
        # Close the socket
        sock.close()

# Example usage
url = "example.com"
measure_latency(url)
