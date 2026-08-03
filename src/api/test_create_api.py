from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Admin, User
from src.dto.admin_dto import AdminCreateRequest
from src.dto.user_dto import UserCreateRequest
from src.security.password_hasher import PasswordHasher

class TestApi:
    @staticmethod
    async def _create_entity(model_cls, payload: UserCreateRequest | AdminCreateRequest,
        session: AsyncSession,):
        result = await session.execute(
            select(model_cls).where(model_cls.email == payload.email)
        )
        existing_entity = result.scalar_one_or_none()

        if existing_entity is None:
            password_hash = await PasswordHasher.hash_password_async(
                payload.password
            )
            new_entity = model_cls(
                email=payload.email,
                password_hash=password_hash,
                full_name=payload.full_name,
            )
            session.add(new_entity)
            try:
                await session.commit()
                await session.refresh(new_entity)
                return new_entity
            except IntegrityError:
                await session.rollback()
                return None

        return existing_entity

    @classmethod
    async def create_user(cls, payload: UserCreateRequest, session: AsyncSession) -> User | None:
        return await cls._create_entity(User, payload, session)

    @classmethod
    async def create_admin(cls, payload: AdminCreateRequest, session: AsyncSession) -> Admin | None:
        return await cls._create_entity(Admin, payload, session)