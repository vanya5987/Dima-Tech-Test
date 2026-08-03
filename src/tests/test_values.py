from src.dto.user_dto import UserCreateRequest
from src.dto.admin_dto import AdminCreateRequest

class TestValues:
    @staticmethod
    def get_test_user():
        return UserCreateRequest(
            email="user@example.com",
            password="password",
            full_name="Userov U. U."
        )

    @staticmethod
    def get_test_admin():
        return AdminCreateRequest(
            email="admin@example.com",
            password="password",
            full_name="Adminov A. A."
        )