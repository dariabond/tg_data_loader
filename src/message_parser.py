from location_extractor import LocationExtractor
from models import ParsedMessage

# TODO process messages that do not contain images AND
# do not contain 'Збито/подавлено' and other patterns to avoid
# try parser with patterns for both threat + location
# test which one works better 
class MessageParser:

    def __init__(self):
        self.location_extractor = LocationExtractor()

    def parse(self, message):
        print(f"  Text: {message.text if message.text else '[No text]'}")
        
        # TODO exceptions
        locations = self.location_extractor.get_location(message.text)
        print(locations)
        return ParsedMessage(message.id, message.date, message.text, locations)
