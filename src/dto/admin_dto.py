from pydantic import BaseModel, EmailStr

class AdminMeDto(BaseModel):
    id: int
    email: str
    full_name: str

    model_config = {"from_attributes": True}

class AdminCreateRequest(BaseModel):
    email: EmailStr
    password: str
    full_name: str