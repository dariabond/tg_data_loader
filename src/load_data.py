import asyncio
from telethon import TelegramClient
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
from parsers.message_parser import MessageParser
from pathlib import Path
import json
from pathlib import Path

load_dotenv()

api_id = os.getenv('TELEGRAM_API_ID')
api_hash = os.getenv('TELEGRAM_API_HASH')
phone = os.getenv('TELEGRAM_PHONE')
DATA_SOURCE = os.getenv('DATA_SOURCE', 'local')
BASE_DIR = Path(__file__).resolve().parent      # src/
PROJECT_ROOT = BASE_DIR.parent                  # project/
RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw_messages.jsonl"


async def load_local_data(): 
    path = Path("test/messages.txt")
    with open(path, encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]
    return lines


async def fetch_api_data(client, channel, hours=24, limit=20):
    cutoff_time = datetime.now() - timedelta(hours=hours)
    messages = []
    async for message in client.iter_messages(
        channel, 
        offset_date=cutoff_time,
        limit=limit,
        reverse=True
    ):
        #print(message.date.isoformat())
        messages.append(message.message)
    return messages


def get_messages(client, channel, hours, limit):
    if DATA_SOURCE == 'local':
        return load_local_data()
    elif DATA_SOURCE == 'api':
        return fetch_api_data(client, channel, hours, limit)
    else:
        raise ValueError(f"Unknown data source")


def write_jsonl(path: str, records: list[dict]) -> None:
    print(path)
    path = Path(path)

    print("Writing to:", path.resolve())

    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with open(path, "a", encoding="utf-8") as f:
            for record in records:
                f.write(json.dumps(record, ensure_ascii=False) + "\n")
    except Exception as e:
        print("WRITE FAILED:", e)


def serialize_message(msg: str) -> dict:
    return {
        "id": msg.id,
        "channel_id": getattr(msg.peer_id, "channel_id", None),
        "date": msg.date.isoformat() if msg.date else None,
        "message": msg.message,
        "ingested_at": datetime.now(timezone.utc).isoformat(),
    }


async def fetch_messages(client, channel_username: str, hours=24, limit=50) -> list:
    channel = await client.get_entity(channel_username)
    cutoff_time = datetime.now() - timedelta(hours=hours)
    messages = []
    async for message in client.iter_messages(
        channel, 
        offset_date=cutoff_time,
        limit=limit,
        reverse=True
    ):
        messages.append(serialize_message(message))
    return messages
    

async def main():
    client = TelegramClient('sessions/test_session', api_id, api_hash)
    await client.start(phone=phone)
    channel_username = os.getenv('TG_CHANNEL')

    try:
        raw_messages = await fetch_messages(client, channel_username)
        # print(raw_messages)
        write_jsonl(RAW_DATA_PATH, raw_messages)
    except Exception as e:
        print(f"✗ Error: {e}")
    finally:
        await client.disconnect()


if __name__ == '__main__':
    asyncio.run(main())


    """TODO
    # today
    # clean messages from images and odd words
    # create docker db setup and tables: event, settlement, threat_type
    
    # how to connect and manipulate data in project?

    # identify one or multiple threats and cut it off(to avoid this case 🛵🛸 Активність ворожих розвідувальних та ударних БпЛА на півночі Харківщини.
['Миколаєвом', 'Сумському', 'Криворізькому', 'Харківщини', 'БпЛА в Сумському', 'БпЛА в Криворізькому'])
    # create tests 
    # exceptions to not take into account(fe messages that have image)
    # extract settlement or region name Харкова -> Харків
    # extract quantity
    # think over the how to store settlements in db
     
    DB tables
    event
    - id PK
    - date (R)
    - threat type (каб, бпла, балістична ракета, крилата ракета, Кинджал) (R)
    - amount (2/5/group/None) (NR)
    - city_id (NR)
    - region_key (R)

    city 
    - id PK
    - name (R)
    - region_key (R)
    - lat (R)
    - long (R)
    """

    # ASK ABOUT ACCURACY!!!