from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select

from src.utils.deps import session_dep
from src.database.models import User, Admin
from src.dto.auth_dto import LoginRequest, TokenResponse
from src.security.password_hasher import PasswordHasher
from src.security.jwt_handler import JwtHandler

router = APIRouter(prefix="/auth", tags=["auth"])

_DUMMY_PASSWORD_HASH = PasswordHasher.hash_password("dummy-password-for-timing-safety")

@router.post("/login/user", response_model=TokenResponse)
async def login_user(credentials: LoginRequest, session: session_dep):
    result = await session.execute(select(User).where(User.email == credentials.email))
    user = result.scalars().first()

    password_hash = user.password_hash if user is not None else _DUMMY_PASSWORD_HASH
    password_valid = await PasswordHasher.verify_password_async(credentials.password, password_hash)

    if user is None or not password_valid:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

    token = JwtHandler.create_access_token(subject_id=user.id, role="user")
    return TokenResponse(access_token=token)

@router.post("/login/admin", response_model=TokenResponse)
async def login_admin(credentials: LoginRequest, session: session_dep):
    result = await session.execute(select(Admin).where(Admin.email == credentials.email))
    admin = result.scalars().first()

    password_hash = admin.password_hash if admin is not None else _DUMMY_PASSWORD_HASH
    password_valid = await PasswordHasher.verify_password_async(credentials.password, password_hash)

    if admin is None or not password_valid:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

    token = JwtHandler.create_access_token(subject_id=admin.id, role="admin")
    return TokenResponse(access_token=token)
