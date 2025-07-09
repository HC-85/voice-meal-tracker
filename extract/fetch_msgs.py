import logging
from datetime import datetime
from os import getenv

from dotenv import load_dotenv
from pymongo import ASCENDING, MongoClient
from pymongo.collection import Collection

from .schemas import MessageRecord, TwilioCredentials
from .utils import get_twilio_client

load_dotenv()

MONGO_URI = getenv("MONGO_URI")
MONGO_DB_NAME = getenv("MONGO_DB_NAME")
MONGO_COLLECTION_NAME = getenv("MONGO_COLLECTION_NAME")

logger = logging.getLogger(__name__)


def get_mongo_collection() -> Collection:
    client = MongoClient(getenv("MONGO_URI"))
    db = client[getenv("MONGO_DB_NAME")]
    collection = db[getenv("MONGO_COLLECTION_NAME")]
    collection.create_index([("sid", ASCENDING)], unique=True)
    return collection


def fetch_messages_from_date(credentials: TwilioCredentials, date: datetime) -> dict[str, int]:
    twilio_client = get_twilio_client(credentials)
    collection = get_mongo_collection()
    message_iter = twilio_client.messages.stream(date_sent=date.date())
    stats: dict[str, int] = dict()
    for message in message_iter:
        try:
            message_record = MessageRecord(**message.__dict__)
            doc = message_record.model_dump(by_alias=False)
            doc["partition_date"] = date.date().isoformat()
            collection.update_one(
                {"_id": doc["sid"]},
                {"$set": doc},
                upsert=True,
            )
            logger.info(f"Sucessfully stored message: {message.sid}")
            stats["success_count"] = stats.get("success_count", 0) + 1
        except Exception as e:
            logger.warning(f"Failed to store {message.sid}: {e}")
            stats["fail_count"] = stats.get("fail_count", 0) + 1
    return stats


def fetch_all(credentials: TwilioCredentials) -> None:
    twilio_client = get_twilio_client(credentials)
    collection = get_mongo_collection()
    message_iter = twilio_client.messages.stream()
    for message in message_iter:
        message_record = MessageRecord(**message.__dict__)
        doc = message_record.model_dump(by_alias=False)
        collection.update_one(
            {"_id": doc["sid"]},
            {"$set": doc},
            upsert=True,
        )


if __name__ == "__main__":
    pass
    # fetch_messages_from_date(get_twilio_creds(), datetime.)
