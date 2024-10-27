import numpy as np
from geopy.geocoders import Nominatim
from sklearn.cluster import KMeans
import time
import random
import json
from typing import List, Dict
from geopy.exc import GeocoderTimedOut

class SimpleDeliveryClusterer:
    def __init__(self):
        """Initialize the clusterer with Nominatim geocoder."""
        self.geolocator = Nominatim(user_agent="delivery_clusterer", timeout=10)
        
    def geocode_address(self, address: str) -> tuple:
        """Convert a single address to coordinates with retries."""
        retries = 3
        for i in range(retries):
            try:
                time.sleep(1)  # Respect rate limiting
                location = self.geolocator.geocode(address)
                if location:
                    return {
                        "location": address,
                        "stopover": True,
                        "coords": (location.latitude, location.longitude)
                    }
            except GeocoderTimedOut:
                if i < retries - 1:
                    wait_time = (2 ** i) + random.uniform(0, 1)
                    time.sleep(wait_time)
                else:
                    return None
            except Exception:
                return None
        return None

    def cluster_addresses(self, addresses: List[str], num_drivers: int) -> Dict:
        """Cluster addresses and return JSON-formatted results."""
        # Convert addresses to coordinates
        location_data = []
        for addr in addresses:
            location = self.geocode_address(addr)
            if location:
                location_data.append(location)

        if len(location_data) < num_drivers:
            raise ValueError(f"Not enough valid addresses ({len(location_data)}) for {num_drivers} drivers")

        # Extract coordinates for clustering
        coordinates = [loc["coords"] for loc in location_data]

        # Perform clustering
        kmeans = KMeans(n_clusters=num_drivers, random_state=42)
        clusters = kmeans.fit_predict(coordinates)

        # Organize results by driver
        driver_routes = {}
        for i, cluster_id in enumerate(clusters):
            driver_id = f"driver_{cluster_id + 1}"
            if driver_id not in driver_routes:
                driver_routes[driver_id] = {
                    "waypoints": []
                }
            driver_routes[driver_id]["waypoints"].append({
                "location": location_data[i]["location"],
                "stopover": True
            })

        return driver_routes

def main():
    # Sample addresses
    addresses = [
        "15277 Castle Downs Rd NW, Edmonton, AB",   
        "11920 129 Ave NW, Edmonton, AB",          
        "15178 127 St NW, Edmonton, AB",          
        "11320 132 Ave NW, Edmonton, AB",
        "4501 30 Ave NW, Edmonton, AB", 
        "10408 124 St NW, Edmonton, AB", 
        "10363 Jasper Ave NW, Edmonton, AB", 
        "4225 118 Ave NW, Edmonton, AB", 
        "2007 138 Ave NW, Edmonton, AB",
        "10025 102A Ave NW, Edmonton, AB T5J 2Z2",
    ]
    
    num_drivers = int(input(f"Enter number of drivers (2-{len(addresses)}): "))
    
    clusterer = SimpleDeliveryClusterer()
    try:
        routes = clusterer.cluster_addresses(addresses, num_drivers)
        
        # Export to JSON file
        with open('driver_routes.json', 'w') as f:
            json.dump(routes, f, indent=2)
            
        print("Routes exported to driver_routes.json")

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
