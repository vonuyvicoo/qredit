from prisma.models import User

from database.config import db


def get_users() -> list[User]:
    return db.user.find_many()


def get_by_id(id: int) -> User | None:
    return db.user.find_unique(where={"id": id})


def get_by_email(email: str) -> User | None:
    return db.user.find_unique(where={"email": email})
