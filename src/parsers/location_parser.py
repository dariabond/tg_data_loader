import re
from geopy.geocoders import Nominatim
from .parser_config import PARSER_CONFIG
from .models import Location
import time

# extract threat first and slice the text

class LocationParser: 
    def __init__(self):
        self.geolocator = Nominatim(user_agent="telegram_scraper_v1")
        self.patterns = []
        prepositions = '|'.join(PARSER_CONFIG['prepos_space'])

        self.patterns.extend([
            PARSER_CONFIG['pattern_prepos'].format(
                prepositions=prepositions
            ),
            PARSER_CONFIG['pattern_postpos']
        ])

    # this method verifies if text is real location and returns 
    # normalized settlement name, latitude, longitude
    def _geocode_location(self, text): 
        print(f'GEOCODE_LOCATION method called with text: {text}')
        try: 
            time.sleep(2)
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
        """for item in potential_locations: 
            print(f"Geocoded locations")
            print(self._geocode_location(item))"""
            

        print(potential_locations)

        return potential_locations
