import logging
from datetime import datetime
from os import getenv
from pathlib import Path
from typing import cast

import requests
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()
logger = logging.getLogger(__name__)

VOICENOTES_DIR = Path("/home/hc85/Projects/voice-meal-tracker/data/raw/voicenotes")


def extract_voicenotes_from_date(date: datetime) -> dict[str, int]:
    twilio_url = "https://api.twilio.com"
    auth = cast(tuple[str, str], (getenv("TWILIO_ACCOUNT_SID"), getenv("TWILIO_AUTH_TOKEN")))
    mongo = MongoClient(getenv("MONGO_URI"))

    stats = dict()
    messages_with_vns = mongo.voice_meal_tracker.messages.find(
        {
            "partition_date": date.date().isoformat(),
            "num_media": {"$gt": 0},
        }
    )
    stats["messages_with_voicenotes"] = 0
    stats["total_voicenotes"] = 0
    stats["successful_saves"] = 0
    stats["failed_saves"] = 0
    stats["skipped_downloads"] = 0
    for message in messages_with_vns:
        stats["messages_with_voicenotes"] += 1
        msg_media_url = f"{twilio_url}/{message.get('uri')}".replace(".json", "/Media.json")
        response = requests.get(msg_media_url, auth=auth)
        media_items = response.json().get("media_list", [])
        for media in media_items:
            stats["total_voicenotes"] += 1
            if (content_type := media.get("content_type")).startswith("audio/"):
                file_extension = content_type.split("/")[1]
                filename = f"{message.get('sid')}_{media.get('sid')}.{file_extension}"
                if not (file_path := VOICENOTES_DIR / filename).exists():
                    audio_url = f"{twilio_url}{media.get('uri').replace('.json', '')}"
                    print(f"{audio_url=}")
                    audio_response = requests.get(audio_url, auth=auth)
                    try:
                        with open(file_path, "wb") as f:
                            f.write(audio_response.content)

                        logger.info(f"File saved: {filename}")
                        stats["successful_saves"] += 1
                    except OSError as e:
                        logger.error(f"Failed to save audio to {file_path}: {e}")
                        stats["failed_saves"] += 1
                else:
                    logger.info(f"File already exists: {filename}")
                    stats["skipped_downloads"] += 1
    return stats


if __name__ == "__main__":
    stats = extract_voicenotes_from_date(datetime(2025, 6, 25))
    print(stats)
