import requests
import subprocess
import time
from datetime import datetime
from tcp_latency import measure_latency
import re
import csv
import os

def traceroute(target, max_hops=30, timeout=1):
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
            
            match = re.search(r'(\d+)\s+([^\s]+|\*)\s+\(([^)]+)\)', line)
            
            if match:
                hop_number = int(match.group(1))
                host = match.group(2)
                ip_address = match.group(3)
                
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
        response = requests.get(url, stream=True)
        sever_ip, server_port = response.raw._connection.sock.getpeername()
        response_headers = response.headers

        # Step-2: Measure latency
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
    url_ringsofpower_aud = "https://s3-dub-ww.cf.dash.row.aiv-cdn.net/dm/2$HFfn88x79JpN7GTdPBIsZ-Gf5_8~/f9b9/09a6/4d28/40f2-979f-f7198e303dd1/f58d50df-b38c-456a-ac07-59f78a4d1a9a_audio_396.mp4?amznDtid=AOAGZA014O5RE"  # Rings of power audio chunk url
    url_ringsofpower_vid = "https://s3-dub-ww.cf.dash.row.aiv-cdn.net/dm/2$HFfn88x79JpN7GTdPBIsZ-Gf5_8~/f9b9/09a6/4d28/40f2-979f-f7198e303dd1/f58d50df-b38c-456a-ac07-59f78a4d1a9a_video_12.mp4?amznDtid=AOAGZA014O5RE" # Rings of power video chunk url
    url_myimage ="https://d1smtvqebyyniu.cloudfront.net/screenshot" # my image on CloudFront
    url_samaritan = "https://m-3913s3.ll.dash.row.aiv-cdn.net/d/2$fhwDjmfg3JB979wVP6wZdGnp7HM~/ww_dub/0a61/5108/715d/429e-8447-30b214224894/a0794990-a8b1-44cf-8616-908fabb648b1_audio_350.mp4?amznDtid=AOAGZA014O5RE"
    url_harlem = "https://s3-dub-2.cf.dash.row.aiv-cdn.net/dm/2$n5-2KPDZZdXXNaT0bPlOGblPy5M~/c37d/fc4f/1891/48a4-bec0-e447cd6378c7/435f7e61-934b-4df9-ade2-df91813dbc21_audio_186.mp4?amznDtid=AOAGZA014O5RE"
    
    timestamp = datetime.now().strftime("%d-%m-%Y_%Hhh_%Mmm")
    timestamp = "26-05-2023_02hh_41mm"
    print("starting the script at: ",timestamp)
    results_directory = f"./results/{timestamp}/"
    if not os.path.exists(results_directory):
        os.mkdir(results_directory)
        print("result directory created.")
    else:
        print("result diretory already exists!!!")

    start_time = time.time()
    elapsed_time = 0 # in minutes
    iteration = 0
    
    while elapsed_time < 201:
        print("\n"*20, "*"*20, f" iteration:{iteration} -- elapsed time= {elapsed_time} min", "*"*20,"\n\n")
        
        main(url_myimage, f"./results/{timestamp}/myimage_{timestamp}")
        main(url_ringsofpower_vid, f"./results/{timestamp}/ringsofpower_vid_{timestamp}")
        main(url_ringsofpower_aud, f"./results/{timestamp}/ringsofpower_aud_{timestamp}")
        main(url_samaritan, f"./results/{timestamp}/samaritan_{timestamp}")
        main(url_harlem, f"./results/{timestamp}/harlem_{timestamp}")
        
        time.sleep(1.1)
        current_time = time.time()
        elapsed_time = int((current_time - start_time)//60)
        iteration += 1
    
    print("\n\nF I N I S H E D.")