import re
from geopy.geocoders import Nominatim
from .location_config import LOCATION_CONFIG
from .models import Location
import time

# add Location object
# TODO assemble all regex in separate method in LE
# extract threat first and slice text

class LocationParser: 
    def __init__(self):
        self.geolocator = Nominatim(user_agent="telegram_scraper_v1")
        self.patterns = []
        prepositions = '|'.join(LOCATION_CONFIG['prepos_space'])
        postpositions = '|'.join(LOCATION_CONFIG['postpos'])

        self.patterns.extend([
            LOCATION_CONFIG['pattern_prepos'].format(
                prepositions=prepositions
            ),
            LOCATION_CONFIG['pattern_postpos']
        ]
        )

    # this method verifies if text is real location and returns 
    # normalized settlement name, latitude, longitude
    def _geocode_location(self, text): 
        print(f'GEOCODE_LOCATION method called with text: {text}')
        try: 
            time.sleep(1)
            location = self.geolocator.geocode(text)
            if location:
                address = location.raw.get("address", {})
                print(f'RAW ADDRESS {address}')
                city = address.get("city") or address.get("town") or address.get("village") or address.get("state")
                print(f'CITY: {city}')
            else: 
                print('Location not found')
        
        except (GeocoderTimedOut, GeocoderServiceError) as e:
            print(f"Geocoding error for '{location_name}': {e}")
        except Exception as e:
            print(f"Unexpected error for '{location_name}': {e}")
        
        return None

    def get_location(self, text):
        print(f'Extracting location from message :{text}')
        potential_locations = []

        for pattern in self.patterns:
            matches = re.findall(pattern, text)
            potential_locations.extend(matches)

        locations = []
        for item in potential_locations: 
            self._geocode_location(item)

        print(potential_locations)

        return potential_locations
