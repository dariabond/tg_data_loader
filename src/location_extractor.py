import re
from geopy.geocoders import Nominatim

class LocationExtractor: 
    def __init__(self):
        self.geolocator = Nominatim(user_agent="telegram_scraper_v1")

        # TODO create location patterns
        # на сході Чернігівщини
        # на межі Харківської, Сумської, Полтавської областей
        # східної межі Потавщини
        # до Одеси
        # курсом на Одесу/Чорноморськ
        # на Запоріжжі
        # на південь Сумщини
        self.locationPatterns = []

    def get_location(self, message):
        print(f'Extracting location from message :{message}')
