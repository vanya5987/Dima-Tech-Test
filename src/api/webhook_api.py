from decimal import Decimal

from fastapi import APIRouter, HTTPException, Request, status
from sqlalchemy.exc import IntegrityError

from src.utils.deps import session_dep
from src.database.models import Account, Payment, User
from src.dto.webhook_dto import PaymentWebhookRequest
from src.utils.webhook_emulator import WebhookEmulator

import os

router = APIRouter(prefix="/webhooks", tags=["webhooks"])

_SECRET_KEY: str = os.getenv("WEBHOOK_SECRET_KEY", "")

@router.post("/payment")
async def process_payment_webhook(
    payload: PaymentWebhookRequest,
    request: Request,
    session: session_dep,
):
    raw_body = await request.json()

    if not WebhookEmulator.is_signature_valid(
        raw_body["account_id"],
        raw_body["amount"],
        raw_body["transaction_id"],
        raw_body["user_id"],
        raw_body["signature"],
        _SECRET_KEY,
    ):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid signature")

    amount = Decimal(str(payload.amount))
    if amount <= 0:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Amount must be positive")

    user = await session.get(User, payload.user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    account = await session.get(Account, payload.account_id)

    if account is None:
        account = Account(id=payload.account_id, user_id=payload.user_id, balance=Decimal("0"))
        session.add(account)
        try:
            await session.flush()
        except IntegrityError:
            await session.rollback()
            account = await session.get(Account, payload.account_id)

            if account is None:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to create account",
                )

    if account.user_id != payload.user_id:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Account belongs to a different user",
        )

    payment = Payment(id=payload.transaction_id, account_id=account.id, amount=amount)
    session.add(payment)

    try:
        await session.flush()
    except IntegrityError:
        await session.rollback()
        return {"status": "already_processed", "transaction_id": payload.transaction_id}

    account.balance = account.balance + amount
    await session.commit()

    return {
        "status": "success",
        "transaction_id": payload.transaction_id,
        "account_id": account.id,
        "new_balance": str(account.balance),
    }
