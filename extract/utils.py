from os import getenv
from typing import cast

from dotenv import load_dotenv
from twilio.rest import Client

from .schemas import TwilioCredentials


def get_twilio_creds() -> TwilioCredentials:
    load_dotenv()
    return TwilioCredentials(
        username=cast(str, getenv("TWILIO_ACCOUNT_SID")),
        password=cast(str, getenv("TWILIO_AUTH_TOKEN")),
    )


def get_twilio_client(credentials: TwilioCredentials) -> Client:
    return Client(username=credentials.username, password=credentials.password)
    # return Client(**get_twilio_creds().model_dump()) ?
