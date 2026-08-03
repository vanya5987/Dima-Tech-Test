from decimal import Decimal
from datetime import datetime
from pydantic import BaseModel

class PaymentDto(BaseModel):
    id: str
    account_id: int
    amount: Decimal
    created_at: datetime

    model_config = {"from_attributes": True}