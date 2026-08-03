from fastapi import APIRouter
from sqlalchemy import select

from src.utils.deps import session_dep
from src.database.models import Account, Payment
from src.dto.user_dto import UserMeDto
from src.dto.account_dto import AccountDto
from src.dto.payment_dto import PaymentDto
from src.security.auth_deps import current_user_dep

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me", response_model=UserMeDto)
async def get_me(current_user: current_user_dep):
    return UserMeDto.model_validate(current_user)

@router.get("/me/accounts", response_model=list[AccountDto])
async def get_my_accounts(current_user: current_user_dep, session: session_dep):
    result = await session.execute(select(Account).where(Account.user_id == current_user.id))
    accounts = result.scalars().all()

    return [AccountDto.model_validate(a) for a in accounts]

@router.get("/me/payments", response_model=list[PaymentDto])
async def get_my_payments(current_user: current_user_dep, session: session_dep):
    result = await session.execute(
        select(Payment)
        .join(Account, Payment.account_id == Account.id)
        .where(Account.user_id == current_user.id)
        .order_by(Payment.created_at.desc())
    )
    payments = result.scalars().all()
    
    return [PaymentDto.model_validate(p) for p in payments]