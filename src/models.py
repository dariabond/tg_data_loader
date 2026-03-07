from dataclasses import dataclass
from datetime import datetime

@dataclass
class Location:
    original_text: str
    normalized_name: str
    location_type: str
    lat: Optional[float] = None
    long: Optional[float] = None
    confidence: float = 1.0

    def to_dict(self):
        return {
            'original_text': self.original_text,
            'normalized_name': self.normalized_name,
            'location_type': self.location_type,
            'lat': self.latitude,
            'long': self.longitude,
            'confidence': self.confidence
        }

@dataclass
class Threat:
    original_text: str
    threat_type: str
    quantity: Optional[int] = None
    confidence: float = 1.0

    def to_dict(self):
        return {
            'original_text': self.original_text,
            'threat_type': self.threat_type,
            'quantity': self.quantity,
            'confidence': self.confidence
        }

@dataclass
class ParsedMessage:
    message_id: int
    message_date: datetime
    message_text: str
    locations: List[Locations]
    threats: List[Threats]