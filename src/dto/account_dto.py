from decimal import Decimal
from pydantic import BaseModel

class AccountDto(BaseModel):
    id: int
    balance: Decimal

    model_config = {"from_attributes": True}