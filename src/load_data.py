import asyncio
from telethon import TelegramClient
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from parsers.message_parser import MessageParser
from pathlib import Path

load_dotenv()

api_id = os.getenv('TELEGRAM_API_ID')
api_hash = os.getenv('TELEGRAM_API_HASH')
phone = os.getenv('TELEGRAM_PHONE')
DATA_SOURCE = os.getenv('DATA_SOURCE', 'local')


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
        messages.append(message.message)
    return messages


def get_messages(client, channel, hours):
    if DATA_SOURCE == 'local':
        return load_local_data()
    elif DATA_SOURCE == 'api':
        return fetch_api_data(client, channel, hours)
    else:
        raise ValueError(f"Unknown data source")


async def test_telegram():
    client = TelegramClient('sessions/test_session', api_id, api_hash)
    await client.start(phone=phone)
    channel_username = os.getenv('TG_CHANNEL')
    parser = MessageParser()

    try:
        channel = await client.get_entity(channel_username)
        cutoff_time = datetime.now() - timedelta(hours=8)
        
        messages = await get_messages(client, channel, hours=24)
        for message in messages:
            res = parser.parse(message)
            print()
            print(
                f"Raw: {message}\n"
                f"Clean: {res['clean_message']}\n"
                f"Locations: {', '.join(res['locations'])}"
            )
            
    except Exception as e:
        print(f"✗ Error: {e}")
    
    await client.disconnect()


if __name__ == '__main__':
    asyncio.run(test_telegram())

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