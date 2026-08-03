from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload

from src.utils.deps import session_dep
from src.database.models import User
from src.dto.admin_dto import AdminMeDto
from src.dto.user_dto import UserMeDto, UserWithAccountsDto, UserCreateRequest, UserUpdateRequest
from src.security.password_hasher import PasswordHasher
from src.security.auth_deps import current_admin_dep, get_current_admin

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_current_admin)],
)

@router.get("/me", response_model=AdminMeDto)
async def get_admin_me(current_admin: current_admin_dep):
    return AdminMeDto.model_validate(current_admin)

@router.get("/users", response_model=list[UserWithAccountsDto])
async def list_users(session: session_dep):
    result = await session.execute(select(User).options(selectinload(User.accounts)))
    users = result.scalars().all()

    return [UserWithAccountsDto.model_validate(u) for u in users]

@router.post("/users", response_model=UserMeDto, status_code=status.HTTP_201_CREATED)
async def create_user(payload: UserCreateRequest, session: session_dep):
    password_hash = await PasswordHasher.hash_password_async(payload.password)

    new_user = User(
        email=payload.email,
        password_hash=password_hash,
        full_name=payload.full_name,
    )
    session.add(new_user)

    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")

    await session.refresh(new_user)
    return UserMeDto.model_validate(new_user)

@router.patch("/users/{user_id}", response_model=UserMeDto)
async def update_user(
    user_id: int,
    payload: UserUpdateRequest,
    session: session_dep,
):
    user = await session.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if payload.email is not None:
        user.email = payload.email
    if payload.full_name is not None:
        user.full_name = payload.full_name
    if payload.password is not None:
        user.password_hash = await PasswordHasher.hash_password_async(payload.password)

    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")

    await session.refresh(user)
    return UserMeDto.model_validate(user)

@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, session: session_dep):
    user = await session.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    await session.delete(user)
    await session.commit()
