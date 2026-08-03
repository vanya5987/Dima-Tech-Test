from pydantic import BaseModel

class SessionDto(BaseModel):
    expire_on_commit: bool