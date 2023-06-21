import requests
import subprocess
import time
from datetime import datetime
from tcp_latency import measure_latency
import re
import csv
import os

def traceroute(target, max_hops=30, timeout=1):
    # if ipv6
    if ":" in target:
        command = f"traceroute6 -I -w {timeout} -m {max_hops} -q 1 {target}"
    else:
        command = f"traceroute -I -w {timeout} -m {max_hops} -q 1 {target}"
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
            
            match = re.search(r'(\d+)\s+([^\s]+)\s+(\d+\.\d+ms)', line)
            
            if match:
                hop_number = int(match.group(1))
                host = match.group(3)
                ip_address = match.group(2)
                
                if ':' in ip_address:  # IPv6 address
                    ip_address = ip_address.split()[0]  # Remove any additional information after the address
                hops_ip.append(ip_address)
                hops_hostname.append(host)
        
        return hops_ip, hops_hostname
    
    except subprocess.CalledProcessError as e:
        print(f"Traceroute failed with error: {e}")
        return [], []

traceroutes_ips = {}
traceroutes_hnames = {}

def main(url, output_filename):
    print("- "*30, "\n", output_filename, "\n", "- "*30)
    outputs = [] # it'll just store 1 result, its like that only to be given to write into csv file since it takes list of dicts as input
    keys = ['timestamp(dd-mm-yyyy hh:mm:ss:ms)', 'responseIP', 'latency(ms)', 'traceroute_ips', 'traceroute_hnames', 'hop count', 'Content-Type', 'Content-Length', 'Connection', 'Date', 'Last-Modified', 'ETag', 'x-amz-storage-class', 'x-amz-server-side-encryption', 'x-amz-meta-dv-checksum-sha-1', 'x-amz-meta-dv-checksum-md5', 'x-amz-meta-dv-checksum-sha-256', 'Accept-Ranges', 'Server', 'X-Server-IP', 'X-Cache', 'Via', 'X-Amz-Cf-Pop', 'X-Amz-Cf-Id', 'Age', 'url', 'info', "reasponseHeaders"]
    data = {key : " " for key in keys}
 
    try:
        timestamp = datetime.now().strftime("%d-%m-%Y_%H:%M:%S:%f")
        
        # Step-1: Get Server IP & HTTP Response
        headers = {'Range': 'bytes=0-'}
        response = requests.head(url, stream=True, headers=headers, allow_redirects=True)

        sever_ip = response.raw._connection.sock.getpeername()[0]
        response_headers = response.headers

        # Step-2: Measure latency
        print("measuring latency...")
        latency = min(measure_latency(host=sever_ip, port=443, runs=2, timeout=1))

        # Print server IP and latency
        print("Server IP:", sever_ip)
        print("Latency:", latency, "ms")

        # Print all HTTP response headers
        print("Response Headers:")
        for header, value in response_headers.items():
            print(f"{header}: {value}")
            if header in data:
                data[header] = value
        data["reasponseHeaders"] = response_headers
        
        # Print traceroute
        if sever_ip not in traceroutes_ips:
            print("running traceroute...\n")
            hops_ip, hops_hostname = traceroute(sever_ip)
            for hop_ip, hop_hname in zip(hops_ip, hops_hostname):
                pass
                #print(hop_ip, ",", hop_hname)
            traceroutes_ips[sever_ip] = hops_ip
            traceroutes_hnames[sever_ip] = hops_hostname
        else:
            print(f"\ntraceroute already done for {sever_ip}!!!!!!")
            hops_ip = traceroutes_ips[sever_ip]
            hops_hostname = traceroutes_hnames[sever_ip]
        hop_count = len(hops_ip)

        if "my" in output_filename:
            info = "my image hosted on CloudFront"
        else:
            info = "media provided by PrimeVideo"
        data.update({'timestamp(dd-mm-yyyy hh:mm:ss:ms)': timestamp, 'url': url, 'responseIP': sever_ip, 'latency(ms)': latency, 'info': info})
        data.update({'traceroute_ips': hops_ip, 'traceroute_hnames': hops_hostname, 'hop count': hop_count})
        outputs.append(data)

    except Exception as e:
        print(f"Error: {e}")
        outputs.append(data)
        pass
        
    with open(output_filename + ".csv", 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=keys)
        if csvfile.tell() == 0: # if csv file is empty
            writer.writeheader()  # Write the header row
        writer.writerows(outputs)  # Write the data rows
        print("D O N E.\n\n")


if __name__ == '__main__':
    
    #url_eviction_period = "https://d3hobf0i9qrmvp.cloudfront.net/eviction_period.png"
    url_eviction_period = "https://d3hobf0i9qrmvp.cloudfront.net/random_video.mp4"

    timestamp = datetime.now().strftime("%d-%m-%Y_%Hhh_%Mmm")
    print("starting the script at: ",timestamp)
    results_directory = f"/home/nal-epfl/Documents/GitHub/PrimeVideo-Scripts/eviction experiment/results1/{timestamp}/"
    if not os.path.exists(results_directory):
        os.makedirs(results_directory)
        print("result directory created.")
    else:
        print("result diretory already exists!!!")

    start_time = time.time()
    elapsed_time = 0
    current_period = 0 # in minutes
     
    while elapsed_time < 721:
        print("*"*10, f"elapsed time= {elapsed_time} min -- period= {current_period} min -- (remaining = {current_period-elapsed_time} min)", "*"*10,)
        
        if elapsed_time >= current_period: 
            # access 3 times
            print("\n")
            main(url_eviction_period, f"{results_directory}/eviction_period_{timestamp}")
            main(url_eviction_period, f"{results_directory}/eviction_period_{timestamp}")
            main(url_eviction_period, f"{results_directory}eviction_period_{timestamp}")
            start_time = time.time()
            if current_period == 0:
                current_period = 1
            else:
                current_period = current_period * 2
            print(f"\naccessed image after {elapsed_time} min. Next access after {current_period} min\n\n\n")

        current_time = time.time()
        elapsed_time = int((current_time - start_time)//60) # in minutes
        #elapsed_time = round(current_time - start_time) # in secs

        time.sleep(1)
            
    print(f"\n\n-- elapsed time= {elapsed_time} min")
    print("F I N I S H E D.")