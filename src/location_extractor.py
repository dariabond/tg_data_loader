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
        postpositions = '|'.join(LOCATION_CONFIG['postpos'])

        self.patterns.extend([
            LOCATION_CONFIG['pattern_prepos'].format(
                prepositions=prepositions
            ),
            LOCATION_CONFIG['pattern_postpos']
        ]
        )
        print(LOCATION_CONFIG)


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