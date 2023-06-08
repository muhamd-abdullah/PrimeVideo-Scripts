import subprocess
import re

def measure_latency(url):
    # Extract the domain name from the URL
    domain = re.search(r'(?<=://)([^/]+)', url).group(0)
    print(f"domain= {domain}")
    # Execute the ping command to measure latency
    ping_cmd = ['ping', '-c', '10', domain]
    ping_output = subprocess.run(ping_cmd, capture_output=True, text=True)

    # Parse the output to extract latency information
    latency_pattern = r'time=(\d+\.?\d*)'
    latency_matches = re.findall(latency_pattern, ping_output.stdout)

    if latency_matches:
        # Calculate average latency
        latency_values = [float(latency) for latency in latency_matches]
        avg_latency = sum(latency_values) / len(latency_values)
        return avg_latency
    else:
        return None



# Example usage
#s3_url = "https://example-bucket.s3.amazonaws.com/example-object"
s3_url = "https://s3-dub-ww.cf.dash.row.aiv-cdn.net/dm/2$HFfn88x79JpN7GTdPBIsZ-Gf5_8~/f9b9/09a6/4d28/40f2-979f-f7198e303dd1/f58d50df-b38c-456a-ac07-59f78a4d1a9a_video_12.mp4?amznDtid=AOAGZA014O5RE"
latency = measure_latency(s3_url)
if latency is not None:
    print(f"Average latency to {s3_url}: {latency} ms")
else:
    print(f"Unable to measure latency to {s3_url}")


'''

URL of PrimeVideo chunks = s3-dub.cf.dash.row

'''