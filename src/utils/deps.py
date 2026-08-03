from src.database.db_session_factory import CreateEngine
from src.dto.db_factory_dto.session_dto import SessionDto
from src.dto.db_factory_dto.engine_dto import EngineDto

from src.api.json_api.json_controller import JsonAPI
from root_file_indicator import RootPathIndicator

from typing import AsyncGenerator, Annotated
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import Depends
import os

settings = JsonAPI.read_json_file(os.path.join(RootPathIndicator.get_root_path(),
                                               "src", "binary_files", "settings.json"))

__session_dto = SessionDto(expire_on_commit=settings["session_expire_on_commit"])
__engine_dto = EngineDto(
    url=settings["db_url"],
    echo=settings["db_echo"],
    pool_size=settings["db_pool_size"],
    max_overflow=settings["db_max_overflow"],
)

engine = CreateEngine(__engine_dto, __session_dto)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with engine.session() as session:
        yield session

session_dep = Annotated[AsyncSession, Depends(get_session)]