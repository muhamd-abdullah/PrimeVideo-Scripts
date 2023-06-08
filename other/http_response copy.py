import requests
import socket
import time
from tcp_latency import measure_latency

'''
def measure_xlatency(ip):
    # Create a TCP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Set a timeout value for the socket (in seconds)
    sock.settimeout(5)

    try:
        # Start the timer
        start_time = time.time()

        # Connect to the server
        sock.connect((ip, 443))

        # Stop the timer and calculate the latency
        end_time = time.time()
        latency = (end_time - start_time)*1000
        return latency
    except socket.error as e:
        print(f"Error: {e}")
        return -1
    finally:
        # Close the socket
        sock.close()
'''

def main():
    url_prime = "https://s3-dub-ww.cf.dash.row.aiv-cdn.net/dm/2$HFfn88x79JpN7GTdPBIsZ-Gf5_8~/f9b9/09a6/4d28/40f2-979f-f7198e303dd1/f58d50df-b38c-456a-ac07-59f78a4d1a9a_audio_396.mp4?amznDtid=AOAGZA014O5RE"  # Replace with your desired URL
    url_myimage ="https://d1smtvqebyyniu.cloudfront.net/screenshot" # my image

    url = url_prime

    try:
        # Step-1: Get Server IP & HTTP Response
        response = requests.get(url, stream=True)
        sever_ip, server_port = response.raw._connection.sock.getpeername()
        response_headers = response.headers

        # Step-2: Measure latency
        #latency = measure_xlatency(sever_ip)
        latency_module = measure_latency(host=sever_ip, port=443, runs=10, timeout=1)

        # Print server IP and latency
        print("Server IP:", sever_ip)
        #print("Latency:", latency, "ms", min(latency_module))
        print("Latency:", min(latency_module), "ms")
        print("\n\n")

        # Print all headers
        print("Response Headers:")
        for header, value in response_headers.items():
            print(f"{header}: {value}")

        # Print specific headers
        print("\nSpecific Headers:")
        print(f"Age: {response_headers.get('Age')}")
        print(f"Etg: {response_headers.get('Etg')}")
        print(f"Server: {response_headers.get('Server')}")
        print(f"Via: {response_headers.get('Via')}")
        print(f"X-Cache: {response_headers.get('X-Cache')}")

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")


if __name__ == '__main__':
    main()
