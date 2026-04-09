import re

from pydantic import BaseModel, Field, EmailStr

password_regex = r"^(?=.*\d)(?=.*[a-zA-Z]).{8,}$"


class CreateUserDto(BaseModel):
    name: str
    email: EmailStr
    password: str = Field(default="password", pattern=re.compile(password_regex))
