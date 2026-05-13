import re
from .location_parser import LocationParser
from .threat_parser import ThreatParser

class MessageParser:

    def __init__(self):
        self.location_parser = LocationParser()
        self.threat_parser = ThreatParser()

    def parse(self, message):
        # leave only latin, cyrillic and digits
        clean_message = re.sub(r'[^\w\s\'\-/,.:!?]', '', message)
        clean_message = re.sub(r'\s+', ' ', clean_message).strip()

        locations = self.location_parser.get_locations(clean_message)
        threats = self.threat_parser.get_threats(clean_message)

        #TODO add timestamp
        return {
            'clean_message': clean_message,
            'oblasts': locations,
            'threats': threats
        }
