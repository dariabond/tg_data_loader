import re
from geopy.geocoders import Nominatim
from location_config import LOCATION_CONFIG

# TODO assemble all regex in separate method
# are there private methods in Py?
# extract threat first
# extract only from those that have length <40
class LocationExtractor: 
    def __init__(self):
        self.geolocator = Nominatim(user_agent="telegram_scraper_v1")
        self.patterns = []
        prepositions = '|'.join(LOCATION_CONFIG['prepos_space'])
        self.patterns.append(LOCATION_CONFIG['pattern'].format(
            prepositions=prepositions
        ))


    def get_location(self, text):
        print(f'Extracting location from message :{text}')
        potential_locations = []

        for pattern in self.patterns:
            matches = re.findall(pattern, text)
            potential_locations.extend(matches)

        print(potential_locations)


'''SPECIAL CASES'''
'''
    Text: 🛵 Через Сумщину БпЛА ➡️ у напрямку Чернігівщини.
    Extracting location from message :🛵 Через Сумщину БпЛА ➡️ у напрямку Чернігівщини.
    ['Сумщину БпЛА', 'Чернігівщини']
'''