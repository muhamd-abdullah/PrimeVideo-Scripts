import requests
import subprocess
import time
from datetime import datetime
from tcp_latency import measure_latency
import re
import csv
import os
import concurrent.futures
from urllib.parse import urlparse
import http.client

url = "https://s3-dub-2.cf.dash.row.aiv-cdn.net/dm/2$JyC1qFAINAYlSyysol9B0GhrVGs~/50a2/98dd/d169/4e33-a0e3-455320593992/5b8e7a9a-7116-48c8-ad70-a535441db84d_video_8.mp4?amznDtid=AOAGZA014O5RE"
server_ip = "108.156.2.17"

# Step-1: Get url & hostname of video chunk
parsed_url = urlparse(url)
hostname = parsed_url.hostname
rest_of_url = parsed_url.path + "?" + parsed_url.query
print(f"\nCF_Server: {server_ip}\nchunk_hostname: {hostname}\nchuck_URL: {rest_of_url}")

bytes_range = "bytes=0-100000"

method = "GET"
custom_headers = {
    "Host": hostname,
    "Range": bytes_range,
}

print(f'\n\n\n\nheaders:{custom_headers}\n\n\n\n')
attempt = 1
max_attempts = 2
timeout = 3
header_dict = {}
response_time = " "
while attempt <= max_attempts:
    try:
        start_time = time.perf_counter()
        conn = http.client.HTTPConnection(server_ip, port=80, timeout=timeout)
        conn.request(method, rest_of_url, body=None, headers=custom_headers)

        # Get the response
        
        response = conn.getresponse()
        end_time = time.perf_counter()
        response_time = (end_time - start_time) * 1000

        response_content = response.read()
        response_size = len(response_content)
        
        # Print the response status code
        print("Response Status:", response.status)
        print("Response Size:", response_size)

        # Print the response headers
        #print("Response Headers:")
        for header, value in response.getheaders():
            #print(f"{header}: {value}")
            header_dict[header] = value

        # Close the connection
        conn.close()

        # Exit the loop since the request was successful
        break

    except Exception as e:
        print(f"Error: {str(e)}. Retrying... (Attempt {attempt}/{max_attempts})")
        attempt += 1
        conn.close()
else:
    print(f"Max attempts reached ({max_attempts}). Exiting...")
    conn.close()
    response_time = " "

conn.close()
