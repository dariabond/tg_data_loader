import re
from geopy.geocoders import Nominatim
import time
import json

# TODO 
# create oblast config to normalize oblast
# cut off oblast and try to catch settlement name
# return array: [{oblast: ..., settlement: ...}]
# handle multiple matchesof settlements i.e. Бпла в напрямку Бахмача, БпЛА на півдні Полтавщини
# handle errors 
# settlememt/oblast name normalization
class LocationParser: 
    def __init__(self):

        prepositions = [
            'на', 'у', 'в', 'до', 'від', 'поблизу', 'біля', 'коло', 'під', 'через',
            'на н.п.', 'над н.п.', 'поблизу н.п.', 'в районі н.п.', 'в районі', 'в напрямку н.п.',
            'повз', 'межі', 'в напрямку', 'в напрямі', 'над', 'на сході', 'на півночі',
            'на півдні', 'на північ', 'на південь', 'на захід',
            'на схід', 'південніше', 'північніше', 'східніше', 'західніше', 'на/повз', 'у бік',
            'півночі', 'півдня', 'сходу', 'заходу'
        ]

        # Direction patterns
        self.direction_pattern = re.compile(
            r'(?:на|з|із|зі|від|у напрямку|курс|курс на)\s+'
            r'(північ(?:н[а-я]+)?|схід(?:н[а-я]+)?|південь|південн[а-я]+|'
            r'захід(?:н[а-я]+)?|західн[а-я]+|'
            r'північно-східн[а-я]+|південно-східн[а-я]+|'
            r'північно-західн[а-я]+|південно-західн[а-я]+)',
            re.IGNORECASE
        )

        prepositions_sorted = sorted(prepositions, key=len, reverse=True)
        prepositions_pattern = '|'.join(re.escape(prep) for prep in prepositions_sorted)

        # Threat + settlement/region/oblast
        self.threat_location_pattern = re.compile(
            r'(бпла|БпЛА|Каб|КАБ|керованих авіаційних бомб)(?:\s+[\u0400-\u04FF]{{1,30}}){{0,3}}\s+(?:{prepositions})\s+([\u0410-\u042F][\u0400-\u04FF]+(?:\s+[\u0410-\u042F][\u0400-\u04FF]+)*)(?:\s+(?:обл\.|область|області|район|районі|р-н|р-ні|р-н\.))'
        )

        # Generic preposition and settlement pattern
        # Matches: повз Київ/на Харків
        self.direction_settlement_pattern = re.compile(
            rf'(?:{prepositions_pattern})\s+([\u0410-\u042F][\u0400-\u04FF]+(?:\s+[\u0410-\u042F][\u0400-\u04FF]+)*)'
        )

        # Full oblast/region pattern
        # Matches: Сумська область, Харківська область, Білоцерківському районі
        self.oblast_full_pattern = re.compile(
            r'([\u0410-\u042F][\u0400-\u04FF\s]{2,30})\s+(?:обл.|область|області|район|районі|р-н|р-ні|р-н)'
        )

        # Oblast pattern 
        # Matches: Сумщині, Харківщині, Дніпропетровщині, etc.
        self.oblast_pattern = re.compile(
            r'\b([А-ЯІЇЄҐ][а-яіїєґ]+(?:ськ|цьк|зьк)?(?:щин|ччин)[іаиуюї]?)\b'
        )

        # City patterns 
        # Matches: на Суми, на Охтирку, на Дніпро
        self.city_on_pattern = re.compile(
            r'\bна\s+([А-ЯІЇЄҐ][а-яіїєґ\']+(?:(?:-[А-ЯІЇЄҐ][а-яіїєґ]+)|(?:ськ[а-яіїєґ]*)|(?:цьк[а-яіїєґ]*))?[а-яіїєґу]?)\b'
        )

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


    # takes text that represents location(oblast/settlement) and returns corresponding normalized
    # oblast i.e. харківщині -> kharkiv or київ -> kyiv as a capital is a special case
    # TODO what about '
    # should I change representation of the json here? 
    def _normalize_location(self, text: str, oblast_config: dict) -> str|None: 
        text = text.lower()

        for obl_key, obl_data in oblast_config.items():
            stems = obl_data.get("relat_stems", [])
            for stem in stems:
                if stem in text:
                    return obl_key
        return None


    def get_locations(self, text):
        locations = set()
        oblasts = set()

        # parse settlement
        matches = self.direction_settlement_pattern.findall(text)
        locations.update(matches)
        
        # parse oblast 
        for match in self.oblast_pattern.finditer(text): 
            oblast = match.group(1)
            locations.add(oblast)

        if not locations:
            return []

        oblast_config = {}
        with open("src/parsers/oblast_config.json", encoding="utf-8") as f:
            oblast_config = json.load(f)

        # map settlement/oblast to normalized oblast name
        for location in locations: 
            oblast = self._normalize_location(location, oblast_config)
            if oblast is not None:
                oblasts.add(oblast)

        return list(oblasts)
