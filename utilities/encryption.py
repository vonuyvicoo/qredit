from cryptography.fernet import Fernet

from config import config

_fernet = Fernet(config.ENCRYPTION_KEY.encode())


class EncryptionUtils:
    @staticmethod
    def encrypt(text: str) -> str:
        return _fernet.encrypt(text.encode()).decode()

    @staticmethod
    def decrypt(text: str) -> str:
        return _fernet.decrypt(text.encode()).decode()
