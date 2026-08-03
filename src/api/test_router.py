from fastapi import APIRouter, status
from src.api.test_create_api import TestApi
from src.utils.deps import session_dep
from src.tests.test_values import TestValues

router = APIRouter(tags=["Testing / Seeding"])

@router.post("/seed/test-data", status_code=status.HTTP_201_CREATED)
async def seed_test_data(session: session_dep):
    user = await TestApi.create_user(TestValues.get_test_user(), session)
    admin = await TestApi.create_admin(TestValues.get_test_admin(), session)

    return {
        "status": "success",
        "message": "Test users initialized",
        "user_email": user.email if user else None,
        "admin_email": admin.email if admin else None,
    }