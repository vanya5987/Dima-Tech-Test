from src.database.db_session_factory import CreateEngine
from src.dto.db_factory_dto.session_dto import SessionDto
from src.dto.db_factory_dto.engine_dto import EngineDto

from typing import AsyncGenerator, Annotated
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import Depends
import os

from dotenv import load_dotenv
load_dotenv()

__expire_flag: bool = os.getenv("SESSION_EXPIRE_TO_COMMIT", "false").lower() == "true"
__url: str = os.getenv("DB_URL", "")
__db_echo: bool = os.getenv("DB_ECHO", "false").lower() == "true"
__pool_size: int = int(os.getenv("DB_POOL_SIZE", 20))
__max_overflow: int = int(os.getenv("DB_MAX_OVERFLOW", 10))

__session_dto = SessionDto(expire_on_commit=__expire_flag)
__engine_dto = EngineDto(
    url=__url,
    echo=__db_echo,
    pool_size=__pool_size,
    max_overflow=__max_overflow,
)

engine = CreateEngine(__engine_dto, __session_dto)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with engine.session() as session:
        yield session

session_dep = Annotated[AsyncSession, Depends(get_session)]