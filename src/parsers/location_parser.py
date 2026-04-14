import re
from geopy.geocoders import Nominatim
from .parser_config import PARSER_CONFIG
from .models import Location
import time

class LocationParser: 
    def __init__(self):

        # Direction patterns
        self.direction_pattern = re.compile(
            r'(?:на|з|із|зі|від|у напрямку|курс)\s+'
            r'(північ(?:н[а-я]+)?|схід(?:н[а-я]+)?|південь|південн[а-я]+|'
            r'захід(?:н[а-я]+)?|західн[а-я]+|'
            r'північно-східн[а-я]+|південно-східн[а-я]+|'
            r'північно-західн[а-я]+|південно-західн[а-я]+)',
            re.IGNORECASE
        )


        # Oblast pattern 
        # Matches: Сумщині, Харківщині, Дніпропетровщині, etc.
        self.oblast_pattern = re.compile(
            r'\b([А-ЯІЇЄҐ][а-яіїєґ]+(?:ськ|цьк|зьк)?(?:щин|ччин)[іаиуюї]?)\b'
        )


        # Full oblast pattern
        # Matches: Сумська область, Харківська область
        self.oblast_full_pattern = re.compile(
            r'\b([А-ЯІЇЄҐ][а-яіїєґ]+(?:ська|цька|зька)) область\b'
        )

        # City patterns 
        # Matches: на Суми, на Охтирку, на Дніпро
        self.city_on_pattern = re.compile(
            r'\bна\s+([А-ЯІЇЄҐ][а-яіїєґ\']+(?:(?:-[А-ЯІЇЄҐ][а-яіїєґ]+)|(?:ськ[а-яіїєґ]*)|(?:цьк[а-яіїєґ]*))?[а-яіїєґу]?)\b'
        )


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
        locations = set()

        # parse oblast 
        for match in self.oblast_pattern.finditer(text): 
            oblast = match.group(1)
            locations.add(oblast)

        for match in self.oblast_full_pattern.finditer(text): 
            oblast = match.group(1)
            locations.add(oblast)

        # parse city
        for match in self.city_on_pattern.finditer(text): 
            city = match.group(1)
            locations.add(city)

        print(locations)

        return list(locations)
