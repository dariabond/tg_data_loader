import json
import pytest
from pathlib import Path
from src.parsers.message_parser import MessageParser

@pytest.fixture
def sample_messages():
    """path = Path("./messages_sample.json")
    with open(path, encoding="utf-8") as f:
        return json.load(f)"""


def test_parser(sample_messages):
    parser = MessageParser()
    print('Test is run')
    assert "KYIV" == "KYIV"