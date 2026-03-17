import re
from .location_parser import LocationParser
from .models import ParsedMessage

# TODO process messages that do not contain images AND
# do not contain 'Збито/подавлено' and other patterns to avoid
# try parser with patterns for both threat + location
# test which one works better 
class MessageParser:

    def __init__(self):
        self.location_extractor = LocationParser()

    def parse(self, message):
        # leave only latin, cyrillic and digits
        cleaned_message = re.sub(r'[^\w\s\'\-/,.:!?]', '', message.text)

        print(f"  Text: {cleaned_message if cleaned_message else '[No text]'}")

        # TODO exceptions
        # try compound parser or if patterns not found, use separate parsers
        
        locations = self.location_extractor.get_location(cleaned_message)
        return ParsedMessage(message.id, message.date, cleaned_message, locations)
