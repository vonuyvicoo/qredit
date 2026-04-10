from pydantic import BaseModel


class LoginDto(BaseModel):
    client_id: str
    secret: str
