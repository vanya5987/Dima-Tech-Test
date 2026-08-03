from src.dto.db_factory_dto.session_dto import SessionDto
from src.dto.db_factory_dto.engine_dto import EngineDto

from sqlalchemy.ext.asyncio import *

class CreateEngine:
    def __init__(self, engine_dto: EngineDto, session_dto: SessionDto):
        self.__async_engine = create_async_engine(
            url=engine_dto.url,
            echo=engine_dto.echo,
            pool_size=engine_dto.pool_size,
            max_overflow=engine_dto.max_overflow,
        )

        self.__async_session = async_sessionmaker(
            bind=self.__async_engine,
            expire_on_commit=session_dto.expire_on_commit,
        )

    def session(self) -> AsyncSession:
        return self.__async_session()