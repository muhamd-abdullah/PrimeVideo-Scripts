import subprocess
import time
from datetime import datetime
from tcp_latency import measure_latency
import re
import csv
import os
import concurrent.futures
from urllib.parse import urlparse
from urllib.parse import urlparse
import http.client


pop_ips ={
'FRA51-M1' : '54.182.218.101',
'FRA54-M3' : '54.182.220.122',
'FRA52-M2' : '54.182.219.121',
'SFO50-M3' : '54.240.131.114',
'SFO5-M1' : '54.240.129.122',
'SFO20-M2' : '54.240.130.99',
'AMS51-M1' : '54.182.215.109',
'AMS52-M2' : '54.182.216.113',
'AMS53-M3' : '54.182.217.120',
'LHR50-M1' : '54.182.235.102',
'LHR61-M2' : '54.182.171.116',
'LHR62-M3' : '54.182.190.119',
'LHR51-M2' : '54.182.199.108',
'LHR52-M3' : '54.182.200.122',
'LHR4-M1' : '54.182.198.104',
'ZRH55-P1' : '18.165.183.115',
'MXP64-P2' : '108.138.199.35',
'MXP63-P1' : '18.66.196.124',
'MXP63-P2' : '18.66.212.34',
'MRS52-P4' : '18.161.111.71',
'MRS52-P3' : '18.161.94.90',
'VIE50-P1' : '18.66.26.26',
'MXP53-P3' : '3.160.212.5',
'MXP64-C2' : '99.86.159.35',
'ZRH50-C1' : '13.224.103.115',
}


# create snapshot file
def create_snapshot_file(timestamp):
    keys = ["content"] + list(pop_ips.keys())
    outputs = []

    for file_name in os.listdir(f"./snapshots/{timestamp}/"):
        if file_name.endswith('.csv') and "0_snapshot" not in file_name:
            print(file_name)
            with open(f"./snapshots/{timestamp}/"+ file_name, 'r') as csv_file:
                data = {key : " " for key in keys}
                data["content"] = file_name.replace(".csv", "")
                #print(f"\n\n\n\n\n{file_name}:\n")
                csv_reader = csv.DictReader(csv_file)
                for row in csv_reader:
                    pop = row["X-Amz-Cf-Pop"]
                    age = row["Age"]
                    hit_miss = row["X-Cache"].lower()
                    if "hit" in hit_miss:
                        data[pop] = 1
                    elif "miss" in hit_miss:
                        data[pop] = 0
                    #print(f"POP:{pop}\nStatus:{hit_miss}\nAge:{age}\n")
                outputs.append(data)
    
    with open(f"./snapshots/{timestamp}/0_snapshot_{timestamp}.csv", 'w', newline='') as csvfile2:
        writer = csv.DictWriter(csvfile2, fieldnames=keys)
        if csvfile2.tell() == 0: # if csv file is empty
            writer.writeheader()  # Write the header row
        writer.writerows(outputs)  # Write the data rows
        print("\n\n\n\nSnapshot created.\n\n")


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
        if error and "hops max" not in error: # in mac, error returns the first line of output
            raise Exception(f"traceroute command failed")
        
        hops_ip = []
        hops_hostname = []
        lines = output.strip().split('\n')
        if "hops max" not in error: # in mac, we dont need to skip the first line
            lines = lines[1:] # skip the first line if ubuntu
        
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
            #print(f"traceroute incomplete for {target} !\n")
            return hops_ip, []
        return hops_ip, hops_hostname
    
    except Exception as e:
        #print(f"traceroute failed with error: {e}")
        return [], []


# get http response for a url chunk from a specific cloudfront server
def get_http_response(url, server_ip, input_hostname):
    # Step-1: Get url & hostname of video chunk
    parsed_url = urlparse(url)
    if "ga.video.cdn.pbs.org" in url or "d2ufudlfb4rsg4" in url:
        hostname = input_hostname
    else:
        hostname = parsed_url.hostname
    rest_of_url = parsed_url.path + "?" + parsed_url.query
    print(f"\nCF_Server: {server_ip}\nchunk_hostname: {hostname}\nchuck_URL: {rest_of_url}")

    method = "HEAD"
    custom_headers = {
        "Host": hostname,
        "Range": "bytes=0-"
    }

    attempt = 1
    max_attempts = 2
    timeout = 3
    header_dict = {}

    while attempt <= max_attempts:
        try:
            conn = http.client.HTTPConnection(server_ip, port=80, timeout=timeout)
            conn.request(method, rest_of_url, body=None, headers=custom_headers)

            # Get the response
            response = conn.getresponse()

            # Print the response status code
            print("Response Status:", response.status)

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
    conn.close()
    return header_dict


traceroutes_ips = {}
traceroutes_hnames = {}

def main(url, output_filename, server_ip, hostname):
    print("- "*30, "\n", output_filename, "\n", "- "*30)
    outputs = [] # it'll just store 1 result, its like that only to be given to write into csv file since it takes list of dicts as input
    keys = ['timestamp(dd-mm-yyyy hh:mm:ss:ms)', 'responseIP', 'latency(ms)', 'traceroute_ips', 'traceroute_hnames', 'hop count', 'Content-Type', 'Content-Length', 'Connection', 'Date', 'Last-Modified', 'ETag', 'x-amz-storage-class', 'x-amz-server-side-encryption', 'x-amz-meta-dv-checksum-sha-1', 'x-amz-meta-dv-checksum-md5', 'x-amz-meta-dv-checksum-sha-256', 'Accept-Ranges', 'Server', 'X-Server-IP', 'X-Server-IP_hops', 'X-Server-IP_hnames', 'X-Server-IP_hopcount','X-Cache', 'Via', 'X-Amz-Cf-Pop', 'X-Amz-Cf-Id', 'Age', 'url', 'info', "reasponseHeaders"]
    data = {key : " " for key in keys}
    data.update({'responseIP': server_ip})
    data.update({'url': url})
    timestamp = datetime.now().strftime("%d-%m-%Y_%H:%M:%S:%f")
    data.update({'timestamp(dd-mm-yyyy hh:mm:ss:ms)': timestamp})

    try:
        # Step-1: Get HTTP Response
        response_headers = get_http_response(url, server_ip, hostname)

        # Step-2: Measure latency
        #print("measuring latency...")
        latency = measure_latency(host=server_ip, port=443, runs=5, timeout=1)
        if latency:
            latency = min(latency)
        else:
            latency = " "
        data.update({'latency(ms)': latency})

        # print server IP and latency
        #print("Server IP:", server_ip)
        #print("Latency:", latency, "ms")

        # print all HTTP response headers
        #print("Response Headers:")
        for header, value in response_headers.items():
            #print(f"{header}: {value}")
            if header in data:
                data[header] = value
        data["reasponseHeaders"] = response_headers

        # Step-3: Traceroute for response IP
        hops_ip, hops_hostname = [], []
        hop_count = 0
        if server_ip not in traceroutes_ips:
            #print(f"running traceroute for response IP: {server_ip} ....\n")
            hops_ip, hops_hostname = traceroute(server_ip)
            traceroutes_ips[server_ip] = hops_ip
            traceroutes_hnames[server_ip] = hops_hostname
        else:
            #print(f"\ntraceroute already done for {server_ip}!!!!!!")
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
                #print(f"running traceroute for X-server: {x_server_ip} ....\n")
                hops_ip, hops_hostname = traceroute(x_server_ip)
                traceroutes_ips[x_server_ip] = hops_ip
                traceroutes_hnames[x_server_ip] = hops_hostname
            else:
                #print(f"\ntraceroute already done for X-Server-IP {server_ip}!!!!!!")
                hops_ip = traceroutes_ips[x_server_ip]
                hops_hostname = traceroutes_hnames[x_server_ip]
        
            hop_count = len(hops_hostname)
        
        data.update({'X-Server-IP_hops':hops_ip, 'X-Server-IP_hnames':hops_hostname, 'X-Server-IP_hopcount':hop_count})

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
      
    with open(output_filename + ".csv", 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=keys)
        if csvfile.tell() == 0: # if csv file is empty
            writer.writeheader()  # Write the header row
        writer.writerows(outputs)  # Write the data rows
        print(f"{output_filename} D O N E.\n\n")


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
        #new_url = re.sub(r"_\d{5}\.ts$", lambda match: f"_{replace_with:05d}.ts", url)
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
    print("starting the script at: ",timestamp)
    
    results_directory = f"./snapshots/{timestamp}/"
    if not os.path.exists(results_directory):
        os.makedirs(results_directory)
        print("result directory created.")
    else:
        print("result diretory already exists!!!")

    start_time = time.time()
    elapsed_time = 0 # in minutes
    
    url_dicts_list = get_url_dicts_from_csv("urls_pbs_haystack_prime_my.csv")
  
    for pop, server_ip in pop_ips.items():
        print("\n"*20, "*"*20, f" POP: {pop} -- elapsed time= {elapsed_time} min", "*"*20,"\n\n")
        
        # Number of urls to process in parallel
        chunk_size = 125    

        # Create a ThreadPoolExecutor with max_workers set to the chunk size
        with concurrent.futures.ThreadPoolExecutor(max_workers=chunk_size) as executor:
            # Create a list to store the future objects
            futures = []

            # Iterate over the strings in chunks
            for i in range(0, len(url_dicts_list), chunk_size):
                # Get the chunk of strings
                print(f"\n\n\n\n\n\n\n********* CHUNK: {i} to {i+chunk_size} **********")
                chunk = url_dicts_list[i:i+chunk_size]

                # Submit the process_string function to the executor for each string in the chunk
                for url_data in chunk:
                    url = url_data["url_chunk"]
                    #print(f"old url:\n{url}\n")
                    prime_replace_with = 2
                    pbs_replace_with = 22
                    url = modify_url(url, f"{prime_replace_with}", f"{pbs_replace_with}")
                    with open(f"./snapshots/{timestamp}/0_metadata_{timestamp}.txt", "w") as file:
                        file.write(f"url = modify_url(url, \"{prime_replace_with}\", \"{pbs_replace_with}\")\n")
                    #print(f"new url:\n{url}\n")
                    name = url_data["name"]
                    content = url_data["content"]
                    hostname = url_data["hostname"]
                    futures.append(executor.submit(main, url, f"./snapshots/{timestamp}/{name}_{content}", server_ip, hostname))

            # Wait for all the futures to complete
            concurrent.futures.wait(futures)
            print("\n"*20,f"POP:{pop} COMPLETED" ,"*"*20, "\n"*20)

        current_time = time.time()
        elapsed_time = int((current_time - start_time)//60)
        print(f"sleeping for 1 sec ..... (elapsed:{elapsed_time})\n\n")          
        time.sleep(1)
    
    print(f"\n\nelapsed time= {elapsed_time} min\n")
    print("F I N I S H E D.")
    
    # Step-5: Create snapshot for all content
    pop_ips ={
    'FRA51-M1' : '54.182.218.101',
    'FRA54-M3' : '54.182.220.122',
    'FRA52-M2' : '54.182.219.121',
    'SFO50-M3' : '54.240.131.114',
    'SFO5-M1' : '54.240.129.122',
    'SFO20-M2' : '54.240.130.99',
    'AMS51-M1' : '54.182.215.109',
    'AMS52-M2' : '54.182.216.113',
    'AMS53-M3' : '54.182.217.120',
    'LHR50-M1' : '54.182.235.102',
    'LHR61-M2' : '54.182.171.116',
    'LHR62-M3' : '54.182.190.119',
    'LHR51-M2' : '54.182.199.108',
    'LHR52-M3' : '54.182.200.122',
    'LHR4-M1' : '54.182.198.104',
    'ZRH55-P1' : '18.165.183.115',
    'MXP64-P2' : '108.138.199.35',
    'MXP63-P1' : '18.66.196.124',
    'MXP63-P2' : '18.66.212.34',
    'MRS52-P4' : '18.161.111.71',
    'MRS52-P3' : '18.161.94.90',
    'VIE50-P1' : '18.66.26.26',
    'MXP53-P3' : '3.160.212.5',
    'MXP64-C2' : '99.86.159.35',
    'ZRH50-C1' : '13.224.103.115',
    }
    print("creating snapshot...")
    time.sleep(1)
    create_snapshot_file(timestamp)
    print("snapshot created.")