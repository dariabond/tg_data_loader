import re
from .location_parser import LocationParser

class MessageParser:

    def __init__(self):
        self.location_extractor = LocationParser()

    def parse(self, message):
        # leave only latin, cyrillic and digits
        clean_message = re.sub(r'[^\w\s\'\-/,.:!?]', '', message)
        clean_message = re.sub(r'\s+', ' ', clean_message).strip()

        # TODO here we should filter invalid messages. but In this case what is to be returned?

        parsed_locations = self.location_extractor.get_location(clean_message)
        return {
            'clean_message': clean_message,
            'locations': parsed_locations
        }
