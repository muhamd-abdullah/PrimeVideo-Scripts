import requests
import subprocess
import time
from datetime import datetime
from tcp_latency import measure_latency
import re
import csv
import os
'''
url_harlem = "http://s3-dub-2.cf.dash.row.aiv-cdn.net/dm/2$n5-2KPDZZdXXNaT0bPlOGblPy5M~/c37d/fc4f/1891/48a4-bec0-e447cd6378c7/435f7e61-934b-4df9-ade2-df91813dbc21_audio_186.mp4?amznDtid=AOAGZA014O5RE"
   
# Step-1: Get Server IP & HTTP Response
response = requests.head(url_harlem, stream=True, verify=False)
sever_ip, server_port = response.raw._connection.sock.getpeername()
response_headers = response.headers


# Print server IP and latency
print("Server IP:", sever_ip)


# Print all HTTP response headers
print("Response Headers:")
for header, value in response_headers.items():
    print(f"{header}: {value}")


print("\n\n\n\n\n")




# Manually provide the IP address of the server
server_ip = '54.182.219.118'
request_uri = "/dm/2$n5-2KPDZZdXXNaT0bPlOGblPy5M~/c37d/fc4f/1891/48a4-bec0-e447cd6378c7/435f7e61-934b-4df9-ade2-df91813dbc21_audio_186.mp4?amznDtid=AOAGZA014O5RE"

url = f"http://{server_ip}{request_uri}"

# Step-1: Send an HTTP HEAD request to the server IP
headers = {'Host': 's3-dub-2.cf.dash.row.aiv-cdn.net/dm/2$n5-2KPDZZdXXNaT0bPlOGblPy5M~/c37d/fc4f/1891/48a4-bec0-e447cd6378c7/435f7e61-934b-4df9-ade2-df91813dbc21_audio_186.mp4?amznDtid=AOAGZA014O5RE'}
response = requests.head('http://' + server_ip, headers=headers, stream=True, verify=False)
response_headers = response.headers
for header, value in response_headers.items():
    print(f"{header}: {value}")
'''


import http.client
import socket

url_harlem = "http://s3-dub-2.cf.dash.row.aiv-cdn.net/dm/2$n5-2KPDZZdXXNaT0bPlOGblPy5M~/c37d/fc4f/1891/48a4-bec0-e447cd6378c7/435f7e61-934b-4df9-ade2-df91813dbc21_audio_186.mp4?amznDtid=AOAGZA014O5RE"

# Make the initial request with allow_redirects=False
response1 = requests.head(url_harlem, allow_redirects=False, verify=False)

# Check if it's a redirect
if response1.status_code in (301, 302, 303, 307, 308):
    # Extract the IP address from the Location header
    location_header = response1.headers.get("Location")
    ip_address = http.client.urlsplit(location_header).netloc.split(":")[0]
    print("Redirection to", ip_address)
else:
    # Use the original URL's hostname
    ip_address = http.client.urlsplit(url_harlem).netloc.split(":")[0]
    print("No redirection to", ip_address)

ip_address = "54.182.200.119" # when i use server IP direcly, doesn't work

# Establish a connection using the IP address
conn = http.client.HTTPConnection(ip_address)

# To check if connection is successful
try:
    conn.connect()
    print(f"Connection established successfully to {ip_address}")
except http.client.HTTPException as e:
    print(f"Failed to establish connection  to {ip_address}. Error:", str(e))

# Construct the request path
path = http.client.urlsplit(url_harlem).path + "?" + http.client.urlsplit(url_harlem).query
print("PATH= ",path)

# Send the HEAD request
conn.request("HEAD", path)

# Get the response
response = conn.getresponse()
resp_ip = response.fp.raw._sock.getpeername()[0]
print(f"Response IP: {resp_ip}")

# Print the status code and headers
print("Status:", response.status)
print("Headers:")
for header, value in response.getheaders():
    print(header + ":", value)

# Close the connection
conn.close()