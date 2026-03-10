import re
from geopy.geocoders import Nominatim
from location_config import LOCATION_CONFIG
from models import Location
import time

# try Nominatim for location normalization
# add Location object
# TODO assemble all regex in separate method in LE
# extract threat first and slice text

class LocationExtractor: 
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
        print(LOCATION_CONFIG)

    # this method verifies if text is real location and returns 
    # normalized settlement name, latitude, longitude
    def _geocode_location(self, text): 
        print('GEOCODE_LOCATION method called')
        try: 
            time.sleep(1)
            location = self.geolocator.geocode(text, addressdetails=True)
            if location:
                address = location.raw.get('address', {})
                print(address.get('city'))
        
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


'''SPECIAL CASES'''
'''
    Text: 🛵 Через Сумщину БпЛА ➡️ у напрямку Чернігівщини.
    Extracting location from message :🛵 Через Сумщину БпЛА ➡️ у напрямку Чернігівщини.
    ['Сумщину БпЛА', 'Чернігівщини']

    '🛵 Дніпропетровщина: БпЛА ➡️ повз Губиниху, курсом на захід.\n🛵 Чернігівщина: БпЛА ➡️ у напрямку Мени, Сосниці.\n🛵 Полтавщина: групи БпЛА ➡️ повз Велику Багачку, курсом на південний захід.'
'''

'''
 Date: 2026-03-04 00:56:18+00:00
  Text: 🛵 Група БпЛА ➡️ у напрямку Павлограда.
🛵 Харківщина: групи БпЛА ➡️ курсом на Харків, Чугуїв, Золочів, Старий Салтів.
Extracting location from message :🛵 Група БпЛА ➡️ у напрямку Павлограда.
🛵 Харківщина: групи БпЛА ➡️ курсом на Харків, Чугуїв, Золочів, Старий Салтів.
['Павлограда', 'Харків']
'''

'''
  Date: 2026-03-04 01:31:37+00:00
  Text: 🛵 БпЛА на заході Харківщини, курсом на Полтавщину.
🛵 БпЛА на півдні Полтавщини, курсом на Дніпропетровщину.
🛵 БпЛА на межі Харківщини та Дніпропетровщини, курс західний.
🛵 БпЛА західніше Кам'янського на Дніпропетровщині, курс північний.
🛵 БпЛА на сході Харківщини, курс південний.
Extracting location from message :🛵 БпЛА на заході Харківщини, курсом на Полтавщину.
🛵 БпЛА на півдні Полтавщини, курсом на Дніпропетровщину.
🛵 БпЛА на межі Харківщини та Дніпропетровщини, курс західний.
🛵 БпЛА західніше Кам'янського на Дніпропетровщині, курс північний.
🛵 БпЛА на сході Харківщини, курс південний.
['Полтавщину', 'Полтавщини', 'Дніпропетровщину', 'Харківщини', 'Кам', 'Дніпропетровщині', 'Харківщини']
'''


'''
🛵🛸 Активність ворожих розвідувальних та ударних БпЛА на півночі Харківщини.
['Миколаєвом', 'Сумському', 'Криворізькому', 'Харківщини', 'БпЛА в Сумському', 'БпЛА в Криворізькому']
'''