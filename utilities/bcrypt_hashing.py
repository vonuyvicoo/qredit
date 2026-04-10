from time import time
from random import randint
from passlib.context import CryptContext

from config import config

CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")


class HashingUtils:
    @staticmethod
    def hash(password: str) -> str:
        return CONTEXT.hash(password + config.HASH_SALT)

    @staticmethod
    def validate(plain_password: str, hashed_password: str) -> bool:
        try:
            return CONTEXT.verify(plain_password + config.HASH_SALT, hashed_password)
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def random_hash() -> str:
        timestamp = time()
        random_number = randint(0, 999999)
        return CONTEXT.hash(f"{timestamp} {random_number} {config.HASH_SALT}")
