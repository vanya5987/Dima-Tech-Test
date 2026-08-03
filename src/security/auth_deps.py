from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy import select

from src.utils.deps import session_dep
from src.database.models import User, Admin
from src.security.jwt_handler import JwtHandler

_bearer_scheme = HTTPBearer()

async def get_current_user(
    session: session_dep,
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(_bearer_scheme)],
) -> User:
    token = credentials.credentials
    try:
        user_id, role = JwtHandler.decode_access_token(token)
    except ValueError as ex:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(ex),
            headers={"WWW-Authenticate": "Bearer"},
        ) from ex

    if role != "user":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User token required")

    result = await session.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    return user


async def get_current_admin(
    session: session_dep,
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(_bearer_scheme)],
) -> Admin:
    token = credentials.credentials
    try:
        admin_id, role = JwtHandler.decode_access_token(token)
    except ValueError as ex:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(ex),
            headers={"WWW-Authenticate": "Bearer"},
        ) from ex

    if role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin token required")

    result = await session.execute(select(Admin).where(Admin.id == admin_id))
    admin = result.scalars().first()

    if admin is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Admin not found")

    return admin


current_user_dep = Annotated[User, Depends(get_current_user)]
current_admin_dep = Annotated[Admin, Depends(get_current_admin)]