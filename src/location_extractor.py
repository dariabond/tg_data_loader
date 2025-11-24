import re
from geopy.geocoders import Nominatim

class LocationExtractor: 
    def __init__(self):
        self.geolocator = Nominatim(user_agent="telegram_scraper_v1")

        # на сході Чернігівщини
        # на межі Харківської, Сумської, Полтавської областей
        # східної межі Потавщини
        # до Одеси
        # курсом на Одесу/Чорноморськ
        # на Запоріжжі
        # на південь Сумщини
        # на Житомирщині, Рівненщині та Волинь
        # УВАГА! Київ!
        # на південному заході Харківщини
        # м.Київ
        # напрямку на/повз Чернігів
        # в напрямку Києва
        # по межі Миколаївщини
        # в напрямку Києва, Черкас, Полтави
        # південніше Павлограду
        # на північ Харківщини
        # повз Печеніги
        self.location_patterns = [
            r'на\s+([A-Z][a-zA-Z\s]{2,20})'
        ]

    def get_location(self, text):
        print(f'Extracting location from message :{text}')
        potential_locations = []
        
        for pattern in self.location_patterns:
            matches = re.findall(pattern, text)
            potential_locations.extend(matches)

        print(potential_locations)
