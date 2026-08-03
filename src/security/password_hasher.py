import asyncio

from passlib.context import CryptContext

_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class PasswordHasher:
    @staticmethod
    def hash_password(plain_password: str) -> str:
        return _pwd_context.hash(plain_password)

    @staticmethod
    def verify_password(plain_password: str, password_hash: str) -> bool:
        return _pwd_context.verify(plain_password, password_hash)

    @staticmethod
    async def hash_password_async(plain_password: str) -> str:
        return await asyncio.to_thread(_pwd_context.hash, plain_password)

    @staticmethod
    async def verify_password_async(plain_password: str, password_hash: str) -> bool:
        return await asyncio.to_thread(_pwd_context.verify, plain_password, password_hash)
