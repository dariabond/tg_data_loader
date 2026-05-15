import asyncio
from telethon import TelegramClient
import os
from dotenv import load_dotenv
from pathlib import Path
import traceback
from collector import fetch_messages, write_jsonl
from processor import process_messages

load_dotenv()

api_id = os.getenv('TELEGRAM_API_ID')
api_hash = os.getenv('TELEGRAM_API_HASH')
phone = os.getenv('TELEGRAM_PHONE')
DATA_SOURCE = os.getenv('DATA_SOURCE', 'local')
BASE_DIR = Path(__file__).resolve().parent      # src/
PROJECT_ROOT = BASE_DIR.parent                  # project/
RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw_messages.jsonl"

async def main():
    client = TelegramClient('sessions/test_session', api_id, api_hash)
    await client.start(phone=phone)
    channel_username = os.getenv('TG_CHANNEL')

    try:
        raw_messages = await fetch_messages(client, channel_username)
        # print(raw_messages)
        write_jsonl(RAW_DATA_PATH, raw_messages)
        processed_messages = process_messages(RAW_DATA_PATH)
        print(processed_messages)

    except Exception as e:
        print(f"✗ Error: {e}")
        traceback.print_exc()
    finally:
        await client.disconnect()


if __name__ == '__main__':
    asyncio.run(main())


    """TODO
    # Database layer testing approach
     
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