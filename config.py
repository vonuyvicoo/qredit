import os
from dotenv import load_dotenv

load_dotenv(".env")


def _require(key: str) -> str:
    value = os.getenv(key)
    assert value, f"{key} environment variable is not set"
    return value


class Config:
    DATABASE_URL: str = _require("DATABASE_URL")
    HASH_SALT: str = _require("HASH_SALT")
    HASH_ALGORITHM: str = _require("HASH_ALGORITHM")
    ENCRYPTION_KEY: str = _require("ENCRYPTION_KEY")
    SUPABASE_URL: str = _require("SUPABASE_URL")
    SUPABASE_KEY: str = _require("SUPABASE_KEY")
    SUPABASE_BUCKET: str = _require("SUPABASE_BUCKET")


config = Config()
