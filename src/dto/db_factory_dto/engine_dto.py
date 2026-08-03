from pydantic import BaseModel

class EngineDto(BaseModel):
    url: str
    echo: bool
    pool_size: int
    max_overflow: int