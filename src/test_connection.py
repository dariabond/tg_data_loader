import asyncio
from telethon import TelegramClient
import os
from dotenv import load_dotenv

load_dotenv()

api_id = os.getenv('TELEGRAM_API_ID')
api_hash = os.getenv('TELEGRAM_API_HASH')
phone = os.getenv('TELEGRAM_PHONE')

async def test_telegram():
    client = TelegramClient('sessions/test_session', api_id, api_hash)
    
    await client.start(phone=phone)
    print("✓ Connected to Telegram!")
    
    # Test: Get your dialogs
    print("\nYour recent chats:")
    async for dialog in client.iter_dialogs(limit=5):
        print(f"  - {dialog.name}")
    
    # Test: Ask for a channel to check
    channel_username = input("\nEnter a public channel username (without @): ")
    
    try:
        channel = await client.get_entity(channel_username)
        print(f"\n✓ Found channel: {channel.title}")
        
        print("\nLast 3 messages:")
        async for message in client.iter_messages(channel, limit=3):
            print(f"\n  Date: {message.date}")
            print(f"  Text: {message.text[:100] if message.text else '[No text]'}...")
            print(f"  Views: {message.views}")
            
    except Exception as e:
        print(f"✗ Error: {e}")
    
    await client.disconnect()

if __name__ == '__main__':
    asyncio.run(test_telegram())