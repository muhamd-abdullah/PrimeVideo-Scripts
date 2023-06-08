import time
from selenium import webdriver
from selenium.webdriver.common.by import By


def measure_latency(url):
    # Configure Chrome WebDriver
    options = webdriver.ChromeOptions()
    #options.add_argument("--headless")  # Run Chrome in headless mode (without opening a visible window)
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    #options.add_argument("--user-data-dir=/Users/abdullah/Library/Application Support/Google/Chrome/Default")
    #options.add_argument("--profile-directory=Profile 1")
    driver = webdriver.Chrome(options=options)
    #time.sleep(120)
    # Start the timer
    start_time = time.time()

    # Open the Prime Video page
    driver.get(url)

    # Extract the server IP for video chunks
    server_ip_element = driver.find_element(By.CSS_SELECTOR,".playerTechInfo--techInfoUrl")
    server_ip = server_ip_element.get_attribute("innerHTML")
    print(f"Server IP: {server_ip}")

    # Stop the timer and calculate the initial latency (TCP SYN)
    end_time = time.time()
    initial_latency = end_time - start_time
    print(f"Initial Latency: {initial_latency} seconds")

    # Start playing the video
    play_button = driver.find_element_by_css_selector(".playButton")
    play_button.click()

    # Measure the latency for each video chunk
    while True:
        # Start the timer
        chunk_start_time = time.time()

        # Wait for the next video chunk to load
        time.sleep(1)  # Adjust the sleep time as needed

        # Stop the timer and calculate the latency for the video chunk
        chunk_end_time = time.time()
        chunk_latency = chunk_end_time - chunk_start_time
        print(f"Chunk Latency: {chunk_latency} seconds")

        # Check if the video playback has finished
        if is_video_finished(driver):
            break

    # Quit the WebDriver
    driver.quit()

def is_video_finished(driver):
    # Check if the video playback has finished by inspecting the UI elements
    # You may need to modify this logic based on the Prime Video UI structure
    # For example, you can check if the play/pause button is present or if the video progress bar reaches the end.
    return False

# Example usage
url = "https://www.primevideo.com/detail/0TUVXIO58IUNEPNBF8363Z7YGL/ref=atv_hm_hom_c_cjm7wb_1_2/?jic=8%7CEgNhbGw%3D"
measure_latency(url)
