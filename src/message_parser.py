from location_extractor import LocationExtractor
from models import ParsedMessage

# TODO create class for threat and for location
class MessageParser:

    def __init__(self):
        self.location_extractor = LocationExtractor()

    def parse(self, message):
        print(f"  Text: {message.text if message.text else '[No text]'}")
        
        # TODO exceptions
        locations = self.location_extractor.get_location(message.text)
        print(locations)
        return ParsedMessage(message.id, message.date, message.text, locations)
