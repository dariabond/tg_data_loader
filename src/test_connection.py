import asyncio
from telethon import TelegramClient
import os
from dotenv import load_dotenv
from location_extractor import LocationExtractor

load_dotenv()

api_id = os.getenv('TELEGRAM_API_ID')
api_hash = os.getenv('TELEGRAM_API_HASH')
phone = os.getenv('TELEGRAM_PHONE')

async def test_telegram():
    client = TelegramClient('sessions/test_session', api_id, api_hash)
    
    await client.start(phone=phone)
    print("✓ Connected to Telegram!")
    
    channel_username = os.getenv('TG_CHANNEL')

    location_extractor = LocationExtractor()
    
    try:
        channel = await client.get_entity(channel_username)
        
        async for message in client.iter_messages(channel, limit=10):
            print(f"\n  Date: {message.date}")
            print(f"  Text: {message.text if message.text else '[No text]'}")
            message_location = location_extractor.get_location(message.text)
            
    except Exception as e:
        print(f"✗ Error: {e}")
    
    await client.disconnect()

if __name__ == '__main__':
    asyncio.run(test_telegram())

    """
    # create tables: event, settlement, threat_type(or as a field of event)
    # identify one or multiple threats  
    # region(oblast) should be stored in file as a static data
     
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