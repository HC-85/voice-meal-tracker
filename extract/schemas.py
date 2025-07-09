from datetime import datetime
from typing import Literal

from pydantic import AliasPath, BaseModel, ConfigDict, Field


class TwilioCredentials(BaseModel):
    username: str
    password: str


class MessageRecord(BaseModel):
    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True, json_encoders={datetime: lambda dt: dt.isoformat()})
    body: str | None = None
    num_segments: int
    direction: Literal["inbound", "outbound"]
    from_number: str = Field(..., alias="from_")
    to_number: str = Field(..., alias="to")
    date_updated: datetime
    price: str | None = None
    error_message: str | None = None
    uri: str
    account_sid: str
    num_media: int
    status: str  # Literal["received"]
    messaging_service_sid: str | None = None
    sid: str
    date_sent: datetime
    date_created: datetime
    error_code: int | None = None
    price_unit: str | None = None
    api_version: str | None = None
    subresource_uris_feedback: str = Field(validation_alias=AliasPath("subresource_uris", "feedback"))
    subresource_uris_media: str = Field(validation_alias=AliasPath("subresource_uris", "media"))
