import json
from typing import Generator
from parsers.message_parser import MessageParser

def read_jsonl(path: str) -> Generator[dict, None, None]:
    with open(path, "r", encoding="utf-8") as f: 
        for line in f:
            if line.strip():
                yield json.loads(line)


def process_messages(path):
    parser = MessageParser()
    processed_messages = []
    for record in read_jsonl(path):
        parsed_message = parser.parse(record['message'])
        processed_messages.append({
            'id': record['id'],
            'channel_id': record['channel_id'], 
            'date': record['date'],
            'clean_message': parsed_message['clean_message'],
            'oblasts': parsed_message['oblasts'],
            'threats': parsed_message['threats']
        })
    return processed_messages




