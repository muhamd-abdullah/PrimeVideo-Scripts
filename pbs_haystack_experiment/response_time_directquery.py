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

server_ip = "13.224.103.115" # ZRH50-C1 


def traceroute(target, max_hops=30, timeout=1):
    ipv6 = False
    # if ipv6
    if ":" in target:
        command = ['traceroute6', '-I', '-w', str(timeout), '-m', str(max_hops), '-q', '1', str(target)]
        ipv6 = True
    else:
        command = ['traceroute', '-I', '-w', str(timeout), '-m', str(max_hops), '-q', '1', str(target)]
    try:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        output, error = process.communicate()
        if error:
            raise Exception(f"traceroute command failed")
        
        hops_ip = []
        hops_hostname = []
        lines = output.strip().split('\n')
        lines = lines[1:] # skip first line
        
        for line in lines:
            ip_address = ""
            if ipv6:
                ip_address = line.split()[1]
                if "*" in line:
                    host_name = "*"
                else:
                    host_name = line.split()[2]
                if ":" in host_name:
                    temp = ip_address
                    ip_address = host_name.replace("(", "").replace(")", "")
                    host_name = temp
            
            else:
                match = re.search(r'(\b(?:\d{1,3}\.){3}\d{1,3}\b|\*)', line)
                if match:
                    ip_address = match.group(0)
                    host_name = ip_address
            
            hops_ip.append(ip_address)
            hops_hostname.append(host_name)

        if "*" in hops_ip[-1] and len(hops_ip) == 30:
            print(f"traceroute incomplete for {target} !\n")
            return hops_ip, []
        return hops_ip, hops_hostname
    
    except Exception as e:
        print(f"traceroute failed with error: {e}")
        return [], []





# get http response for a url chunk from a specific cloudfront server
def get_http_response(url, server_ip, input_hostname, bytes_range):
    # Step-1: Get url & hostname of video chunk
    parsed_url = urlparse(url)
    if "ga.video.cdn.pbs.org" in url or "d2ufudlfb4rsg4" in url:
        hostname = input_hostname
    else:
        hostname = parsed_url.hostname
    rest_of_url = parsed_url.path + "?" + parsed_url.query
    print(f"\nCF_Server: {server_ip}\nchunk_hostname: {hostname}\nchuck_URL: {rest_of_url}")


    bytes_range_new = "bytes=0-100000"
    print(f"\n\nbytes_range:{[bytes_range]}\nbytes_range_new:{[bytes_range_new]}\n")

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
    return header_dict, response_time


traceroutes_ips = {}
traceroutes_hnames = {}

prime_bytes = {}
bytes_step =  100000


def main(url, output_filename, server_ip, hostname):
    print("- "*30, "\n", output_filename, "\n", "- "*30)
    outputs = [] # it'll just store 1 result, its like that only to be given to write into csv file since it takes list of dicts as input
    keys = ['timestamp(dd-mm-yyyy hh:mm:ss:ms)', 'responseIP', 'response_time(ms)','latency(ms)', 'traceroute_ips', 'traceroute_hnames', 'hop count', 'Content-Type', 'Content-Length', 'Connection', 'Date', 'Last-Modified', 'ETag', 'x-amz-storage-class', 'x-amz-server-side-encryption', 'x-amz-meta-dv-checksum-sha-1', 'x-amz-meta-dv-checksum-md5', 'x-amz-meta-dv-checksum-sha-256', 'Accept-Ranges', 'Server', 'X-Server-IP', 'X-Server-IP_hops', 'X-Server-IP_hnames', 'X-Server-IP_hopcount','X-Cache', 'Via', 'X-Amz-Cf-Pop', 'X-Amz-Cf-Id', 'Age', 'url', 'info', "reasponseHeaders"]
    data = {key : " " for key in keys}

    try:
        timestamp = datetime.now().strftime("%d-%m-%Y_%H:%M:%S:%f")
        
        # Step-1: Get Server IP & HTTP Response
        if "dash.row" in url: # Prime's url
            print("PRIME")
            if url not in prime_bytes:
                prime_bytes[url] = {"start":0, "end":bytes_step}
            prime_bytes_start = prime_bytes[url]["start"]
            prime_bytes_end = prime_bytes[url]["end"]
            range = f'bytes={prime_bytes_start}-{prime_bytes_end}'
            prime_bytes[url] = {"start":prime_bytes_end+1, "end":prime_bytes_end+bytes_step}
            
            response_headers, response_time = get_http_response(url, server_ip, hostname, range)
            data.update({'timestamp(dd-mm-yyyy hh:mm:ss:ms)': timestamp, 'url': url, 'responseIP': server_ip, 'response_time(ms)':response_time})
        else:
            print("PBS/Haystack")
            response_headers, response_time = get_http_response(url, server_ip, hostname, f'bytes=0-{bytes_step}')

            data.update({'timestamp(dd-mm-yyyy hh:mm:ss:ms)': timestamp, 'url': url, 'responseIP': server_ip, 'response_time(ms)':response_time})

        # Step-2: Measure latency
        print("measuring latency...")
        #latency = measure_latency(host=server_ip, port=443, runs=5, timeout=1)
        latency = " "
        if latency:
            latency = min(latency)
        else:
            latency = " "
        data.update({'latency(ms)': latency})

        # print server IP and latency
        print("Server IP:", server_ip)
        print("Latency:", latency, "ms")
        print("Response Time:", response_time, "ms")

        # print all HTTP response headers
        print("Response Headers:")
        for header, value in response_headers.items():
            print(f"{header}: {value}")
            if header in data:
                data[header] = value
        data["reasponseHeaders"] = response_headers
        
        '''
        # Step-3: Traceroute for response IP
        hops_ip, hops_hostname = [], []
        hop_count = 0
        if server_ip not in traceroutes_ips:
            print(f"running traceroute for response IP: {server_ip} ....\n")
            hops_ip, hops_hostname = traceroute(server_ip)
            traceroutes_ips[server_ip] = hops_ip
            traceroutes_hnames[server_ip] = hops_hostname
        else:
            print(f"\ntraceroute already done for {server_ip}!!!!!!")
            hops_ip = traceroutes_ips[server_ip]
            hops_hostname = traceroutes_hnames[server_ip]
        
        hop_count = len(hops_hostname)
        data.update({'traceroute_ips': hops_ip, 'traceroute_hnames': hops_hostname, 'hop count': hop_count})
        

        # Step-4: Traceroute for X-Server-IP
        hops_ip, hops_hostname = [], []
        hop_count = 0
        x_server_ip = data['X-Server-IP']
        if x_server_ip != " ":
            if x_server_ip not in traceroutes_ips:
                print(f"running traceroute for X-server: {x_server_ip} ....\n")
                hops_ip, hops_hostname = traceroute(x_server_ip)
                traceroutes_ips[x_server_ip] = hops_ip
                traceroutes_hnames[x_server_ip] = hops_hostname
            else:
                print(f"\ntraceroute already done for X-Server-IP {server_ip}!!!!!!")
                hops_ip = traceroutes_ips[x_server_ip]
                hops_hostname = traceroutes_hnames[x_server_ip]
        
            hop_count = len(hops_hostname)

        data.update({'X-Server-IP_hops':hops_ip, 'X-Server-IP_hnames':hops_hostname, 'X-Server-IP_hopcount':hop_count})
        '''

        if "my" in output_filename:
            info = "my content hosted on CloudFront"
        else:
            info = "media provided by PrimeVideo"
        data.update({'info': info})
        
        outputs.append(data)

    except Exception as e:
        print(f"Error: {e}")
        outputs.append(data)
        pass
    
    if "Error" not in data['X-Cache']:
        with open(output_filename + ".csv", 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=keys)
            writer.writerows(outputs)  # Write the data rows
            print("D O N E.\n\n")
    
    result = outputs[0]
    return result['X-Cache']


def get_url_dicts_from_csv(filename):
    result = []
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            result.append(row)
    return result


def modify_url(url, replace_with, replace_with_pbc):
    new_url = url
    if "ga.video.cdn.pbs.org" in url or "d2ufudlfb4rsg4" in url:    
        new_url = re.sub(r"_\d{5}\.ts$", lambda match: f"_{int(replace_with_pbc):05d}.ts", url)
        return new_url
    else:
        new_url = url
        for i in range(6,10):
            url_to_check = f"video_{i}.mp4"
            if url_to_check in url:
                new_url = url.replace(url_to_check, f"video_{replace_with}.mp4")
                break
        return new_url






if __name__ == '__main__':
    timestamp = datetime.now().strftime("%d-%m-%Y_%Hhh_%Mmm")
    timestamp = timestamp + server_ip.replace(".","-")
    print("starting the script at: ",timestamp)
    
    results_directory = f"./testing/{timestamp}/"
    if not os.path.exists(results_directory):
        os.makedirs(results_directory)
        print("result directory created.")
    else:
        print("result diretory already exists!!!")

    url_dicts_list = get_url_dicts_from_csv("urls_pbs_haystack_prime_my.csv")

    start_time = time.time()
    elapsed_time = 0 # in minutes
    iteration = 1

    # RESPONSE TIMES FOR ALL
    for k, content_data in  enumerate(url_dicts_list):
        print("\n"*20, "*"*20, f" name:{content_data['name']} ({k/len(url_dicts_list)}) -- elapsed time= {elapsed_time} sec", "*"*20,"\n\n")
        content_type = content_data["content"]
        
        if "pbs" in content_type or "haystack" in content_type: # pbs, haystack
            chunk_range = range(500) 
        elif "my_content" in content_type: # my content
            continue
        else:
            chunk_range = range(500) # this is no. of MBs prime will go through
        
        current_url_dicts_list = []
        for chunk_i in chunk_range:
            temp_content_data = dict(content_data)
            url = content_data["url_chunk"]
            prime_replace_with = 1 # video quality
            pbs_replace_with = chunk_i + 1
            new_url = modify_url(url, f"{prime_replace_with}", f"{pbs_replace_with}")
            temp_content_data["url_chunk"] = new_url
            if "pbs" not in content_type and "haystack" not in content_type:
                pass
                #temp_content_data["url_chunk"] = content_data['url_chunk'] # keep the url same for Prime
            current_url_dicts_list.append(temp_content_data)

        # create csv for the result
        keys = ['timestamp(dd-mm-yyyy hh:mm:ss:ms)', 'responseIP', 'response_time(ms)','latency(ms)', 'traceroute_ips', 'traceroute_hnames', 'hop count', 'Content-Type', 'Content-Length', 'Connection', 'Date', 'Last-Modified', 'ETag', 'x-amz-storage-class', 'x-amz-server-side-encryption', 'x-amz-meta-dv-checksum-sha-1', 'x-amz-meta-dv-checksum-md5', 'x-amz-meta-dv-checksum-sha-256', 'Accept-Ranges', 'Server', 'X-Server-IP', 'X-Server-IP_hops', 'X-Server-IP_hnames', 'X-Server-IP_hopcount','X-Cache', 'Via', 'X-Amz-Cf-Pop', 'X-Amz-Cf-Id', 'Age', 'url', 'info', "reasponseHeaders"]
        with open(f"./testing/{timestamp}/{content_data['name']}_{content_data['content']}" + ".csv", 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=keys)
            if csvfile.tell() == 0: # if csv file is empty
                writer.writeheader()  # Write the header row
        
   
        # go through all video chunks of the content
        for url_data in current_url_dicts_list:
            url = url_data["url_chunk"]
            name = url_data["name"]
            content = url_data["content"]
            hostname = url_data["hostname"]
            status = main(url, f"./testing/{timestamp}/{name}_{content}", server_ip, hostname)
            if "Error" in status:
                print("\n\n\nFound Error from Cloudfront ---> STOPPING!!!!!!\n\n\n")
                break

        time.sleep(0.1)
        current_time = time.time()
        elapsed_time = int((current_time - start_time)//60)

    
    
    print(f"\n\nelapsed time= {elapsed_time} min")
    print("F I N I S H E D.")