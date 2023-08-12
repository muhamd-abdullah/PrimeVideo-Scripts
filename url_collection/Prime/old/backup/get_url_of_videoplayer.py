import requests
from bs4 import BeautifulSoup

'''
Input: URL of the title page of movie/tv title itself
Output: This returns URL of the webpage that plays the video 
'''

# Specify the URL of the movie/tv's webpage
#url = "https://www.primevideo.com/detail/0SK5HM5PYJC9H4FUBRLNJSHKHQ/ref=atv_ge_aga_c_vQHLwi_brws_1_1" # Medelin
url = "https://www.primevideo.com/detail/0TIU98O83X5MR0C6I7P1GNB2X1/ref=atv_br_def_r_br_c_unkc_1_12" # In Time

# Send a GET request to the webpage
response = requests.get(url)

# Create a BeautifulSoup object to parse the HTML content
soup = BeautifulSoup(response.text, "html.parser")

# Find all elements that have the href attribute
elements_with_href = soup.find_all(href=True)

# Extract the href attribute from each element
link_addresses = [element["href"] for element in elements_with_href]

# Print the list of link addresses
for address in link_addresses:
    if "https://www.primevideo.com/detail/" in address:
        print(address,"\n\n")
        address = address.split("/")[-1]
        print(address,"\n")
        new_url = f"https://www.primevideo.com/detail/{address}/ref=atv_hm_fcv_prime_sd_mv_resume_t1ACAAAAAA0wh0?autoplay=1&t=0"
        print(new_url)