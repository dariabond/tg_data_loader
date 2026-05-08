import re

#авіаційних засобів ураження
#ворожої тактичної авіації
class ThreatParser():
    def __init__(self):
        # Threat type patterns
        self.threat_patterns = {
            'БпЛА': re.compile(r'БпЛА|безпілотн|мопед', re.IGNORECASE),
            'КАБ': re.compile(r'КАБ|керован[а-я]+ авіаційн[а-я]+ бомб', re.IGNORECASE),
            'Авіація': re.compile(
                            r'авіаці[а-яіїєґ]|'
                            r'тактичн[а-яіїєґ]+ засоб[а-яіїєґ]+ авіаці[а-яіїєґ]|'
                            r'тактичн[а-яіїєґ]+ авіаці[а-яіїєґ]|'
                            r'авіаційн[а-яіїєґ]+ засоб[а-яіїєґ]+ ураження', 
                            re.IGNORECASE
                        ),
            'Ракета': re.compile(r'ракет|балістичн', re.IGNORECASE)
        }


    # Extract threat type from the message
    def get_threats(self, text: str):
        threats = set()
        for threat_type, pattern in self.threat_patterns.items():
            if pattern.search(text):
                threats.add(threat_type)

        return list(threats)