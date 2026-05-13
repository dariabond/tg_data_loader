from datetime import datetime, timedelta, timezone
import json

def write_jsonl(path: str, records: list[dict]) -> None:
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

#TODO 
# filter out messages that were not parsed and put them in different location for further investigation