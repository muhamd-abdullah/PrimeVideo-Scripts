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
        print(f"Latency: {latency*1000} ms")
    except socket.error as e:
        print(f"Error: {e}")
    finally:
        # Close the socket
        sock.close()

# Example usage
url = "server-18-165-183-115.zrh55.r.cloudfront.net" # 18-165-183-115 = server IP embedded in domain name = static ip = 18.165.183.115 --> That means its different servers, not NAT or other things
#url = "https://s3-dub-ww.cf.dash.row.aiv-cdn.net/dm/2$HFfn88x79JpN7GTdPBIsZ-Gf5_8~/f9b9/09a6/4d28/40f2-979f-f7198e303dd1/f58d50df-b38c-456a-ac07-59f78a4d1a9a_audio_396.mp4?amznDtid=AOAGZA014O5RE"  # Replace with your desired URL
measure_latency(url)
