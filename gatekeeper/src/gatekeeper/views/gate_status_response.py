from datetime import datetime

from pydantic import BaseModel


class GateStatusResponse(BaseModel):
    closed: bool
    last_change: datetime
    train_id: str
