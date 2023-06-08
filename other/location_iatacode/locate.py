import geoip2.database
import json
 

def ip_to_location(ip_address):
    # Load the GeoIP2 database
    reader = geoip2.database.Reader('GeoLite2-City.mmdb')
    
    try:
        # Perform the IP lookup
        response = reader.city(ip_address)

        # Get the city name
        city_name = response.city.name
        country_name = response.country.name
    
    except Exception as e:
        city_name, country_name = "", ""

    # Close the GeoIP2 reader
    reader.close()
    return [city_name, country_name]


def iata_to_location(iata_code):
    iata_code = iata_code[:3]
    
    # Open the JSON file
    with open('/Users/abdullah/Documents/PrimeVideo/PrimeVideo Scripts/location_iatacode/cloudfront-edge-locations.json', 'r') as file:
        # Load the JSON data into a dictionary
        data = json.load(file)
    
    iata_to_location = {}
    for iata, info in data["nodes"].items():
        country = info["country"]
        city = info["city"]
        airport = info["airport"]
        iata_to_location[iata] = [city, country, airport]
        #print(iata, city)
    
    if iata_code in iata_to_location:
        return iata_to_location[iata_code]
    else:
        return ["","",""]


if __name__ == '__main__':
    # testing
    ip_address = '46.228.150.29x'
    location = ip_to_location(ip_address)
    print(f"{ip_address} is mapped to {location}")

    iata_code = "BNE50-P2"
    location = iata_to_location(iata_code)
    print(f"{iata_code} is mapped to {location[:2]}") # print only city and country