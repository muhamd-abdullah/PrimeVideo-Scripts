import socket
from urllib.parse import urlparse

# get http response for a url chunk from a specific cloudfront server
def get_response(url, server_ip):
    # Step-1: Get url & hostname of video chunk
    parsed_url = urlparse(url)
    hostname = parsed_url.hostname
    rest_of_url = parsed_url.path + "?" + parsed_url.query
    print(f"\nCF_Server: {server_ip}\nchunk_hostname: {hostname}\nchuck_URL: {rest_of_url}")

    # Define the server address and port
    server_address = (server_ip, 80)

    # Create a TCP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    client_socket.connect(server_address)
    print(f"TCP connection successfully created to {server_ip}\n\n")

    # Send the GET request
    request = f"HEAD {rest_of_url} HTTP/1.1\r\nHost: {hostname}\r\nRange: bytes=0-\r\n\r\n"
    client_socket.send(request.encode())

    # Receive the response
    response = b''
    while b'\r\n\r\n' not in response:
        chunk = client_socket.recv(4096)
        if not chunk:
            break
        response += chunk

    # Decode and print the response headers
    decoded_response = response.decode('iso-8859-1')
    header_end = decoded_response.index('\r\n\r\n') + 4
    headers = decoded_response[:header_end]

    # Parse the headers into a dictionary
    header_lines = headers.split('\r\n')
    header_dict = {}
    for line in header_lines[1:-2]:  # Skip the first line and last line
        key, value = line.split(': ', 1)
        header_dict[key] = value

    # Close the socket
    client_socket.close()

    return header_dict


chunk_url = "https://s3-dub-2.cf.dash.row.aiv-cdn.net/dm/2$AK8dHqESv-DO82tl-7N52o_nnPY~/9e9f/0756/6813/43da-a37e-fe6f24499339/12ba49d3-cfc0-499a-9899-7f9d0c5ed0a3_video_8.mp4?amznDtid=AOAGZA014O5RE"
server_ip = "18.165.183.81"

response_headers = get_response(chunk_url, server_ip)

print("Response Headers:")
for header, value in response_headers.items():
    print(f"{header}: {value}")

