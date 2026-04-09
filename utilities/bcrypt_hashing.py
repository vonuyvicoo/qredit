from time import time
from random import randint
import os
from dotenv import load_dotenv
from passlib.context import CryptContext

CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")

load_dotenv('.env')

salt = os.getenv("HASH_SALT")

class HashingUtils:
    @staticmethod
    def hash(password: str) -> str:
        to_hash = password + salt
        return CONTEXT.hash(to_hash)

    @staticmethod
    def validate(plain_password: str, hashed_password: str) -> bool:
        try:
            to_verify = plain_password + salt
            return CONTEXT.verify(to_verify, hashed_password)
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def random_hash() -> str:
        timestamp = time()
        random_number = randint(0, 999999)
        return CONTEXT.hash(f"{timestamp} {random_number} {salt}")

