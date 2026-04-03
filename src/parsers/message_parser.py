import re
from .location_parser import LocationParser
from .parser_config import PARSER_CONFIG


class MessageParser:

    def __init__(self):
        self.location_extractor = LocationParser()
        self.patterns = []
        prepositions = '|'.join(PARSER_CONFIG['prepos_space'])
        print(PARSER_CONFIG['compound_pattern'])
        print(prepositions)
        self.patterns.extend([
            PARSER_CONFIG['compound_pattern'].format(
                prepositions=prepositions
            )
        ])

    def parse(self, message):
        # leave only latin, cyrillic and digits
        clean_message = re.sub(r'[^\w\s\'\-/,.:!?]', '', message)

        print(f"  Text: {clean_message if clean_message else '[No text]'}")

        # TODO exceptions
        # try compound parser or if patterns not found, use separate parsers

        potential_matches = []

        for pattern in self.patterns:
            matches = re.findall(pattern, clean_message)
            potential_matches.extend(matches)
        
        #parsed_locations = self.location_extractor.get_location(clean_message)
        print("POTENTIAL MATCHES")
        print(potential_matches)
        ''' return {
            'clean_message': clean_message,
            'locations': parsed_locations
        }'''
