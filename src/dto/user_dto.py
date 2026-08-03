from typing import Optional
from pydantic import BaseModel, EmailStr

from src.dto.account_dto import AccountDto

class UserMeDto(BaseModel):
    id: int
    email: str
    full_name: str

    model_config = {"from_attributes": True}

class UserWithAccountsDto(UserMeDto):
    accounts: list[AccountDto] = []

class UserCreateRequest(BaseModel):
    email: EmailStr
    password: str
    full_name: str

class UserUpdateRequest(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    full_name: Optional[str] = None