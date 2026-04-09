from datetime import datetime

from pydantic import BaseModel


class GetUserDto(BaseModel):
    id: int
    name: str
    email: str
    updated_at: datetime
    created_at: datetime
