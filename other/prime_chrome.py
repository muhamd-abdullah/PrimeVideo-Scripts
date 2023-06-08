from selenium import webdriver
import time
import socket

def measure_latency(url):
    # Set up Chrome WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run Chrome in headless mode (no GUI)
    driver = webdriver.Chrome(options=options)

    try:
        # Open Prime Video in Chrome
        driver.get(url)

        # Wait for the video to load
        time.sleep(5)

        # Find the video source element
        video_element = driver.find_element("tag", "video")

        # Retrieve the source URL of the video
        video_src = video_element.get_attribute("src")

        # Resolve the IP address of the video server
        video_server_ip = socket.gethostbyname(socket.gethostbyname(video_src.split("//")[1].split("/")[0]))
        print(f"Video Server IP: {video_server_ip}")

        # Measure latency for each video chunk
        chunks = driver.execute_script(
            """
            const video = arguments[0];
            const currentTime = video.currentTime;
            const buffered = video.buffered;

            let chunks = [];

            for (let i = 0; i < buffered.length; i++) {
                const start = buffered.start(i);
                const end = buffered.end(i);
                const duration = end - start;

                const chunk = {
                    start: start,
                    end: end,
                    duration: duration
                };

                chunks.push(chunk);
            }

            return chunks;
            """,
            video_element
        )

        for i, chunk in enumerate(chunks):
            # Start the timer
            start_time = time.time()

            # Seek to the start of the chunk
            driver.execute_script("arguments[0].currentTime = arguments[1];", video_element, chunk["start"])

            # Wait for the chunk to load
            time.sleep(chunk["duration"])

            # Stop the timer and calculate the latency
            end_time = time.time()
            latency = end_time - start_time
            print(f"Chunk {i+1} Latency: {latency} seconds")

    finally:
        # Quit the WebDriver
        driver.quit()

# Example usage
#url = "https://www.amazon.com/your-prime-video-url"  # Replace with your Prime Video URL
url = "https://www.primevideo.com/detail/0TUVXIO58IUNEPNBF8363Z7YGL/ref=atv_hm_hom_c_cjm7wb_1_2/?jic=8%7CEgNhbGw%3D"
measure_latency(url)