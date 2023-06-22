import http.client
import time

rest_of_url = "/myvideo-milan.mp4"
hostname = "dm6nckdz08do7.cloudfront.net"
server_ip = "18.66.196.124" # Milan

method = "HEAD"
custom_headers = {
    "Host": hostname,
    "Range": "bytes=0-"
}

attempt = 1
max_attempts = 3
timeout = 3
header_dict = {}

while attempt <= max_attempts:
    try:
        conn = http.client.HTTPConnection(server_ip, port=80, timeout=timeout)
        conn.request(method, rest_of_url, body=None, headers=custom_headers)

        # Get the response
        start_time = time.time()
        response = conn.getresponse()
        end_time = time.time()
        response_time = (end_time - start_time) * 1000
        print(f"latency:{response_time}")

        # Print the response status code
        print("Response Status:", response.status)

        # Print the response headers
        print("Response Headers:")
        for header, value in response.getheaders():
            print(f"{header}: {value}")
            header_dict[header] = value

        # Close the connection
        conn.close()

        # Exit the loop since the request was successful
        break

    except Exception as e:
        print(f"Error: {str(e)}. Retrying... (Attempt {attempt}/{max_attempts})")
        attempt += 1
else:
    print(f"Max attempts reached ({max_attempts}). Exiting...")