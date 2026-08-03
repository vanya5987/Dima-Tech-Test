from src.utils.deps import settings

from datetime import datetime, timedelta, timezone

import jwt

_SECRET_KEY: str = settings["jwt_secret"]
_ALGORITHM: str = settings.get("jwt_algorithm", "HS256")
_EXPIRE_MINUTES: int = settings.get("jwt_expire_minutes", 60)


class JwtHandler:
    @staticmethod
    def create_access_token(subject_id: int, role: str) -> str:
        expire = datetime.now(timezone.utc) + timedelta(minutes=_EXPIRE_MINUTES)
        payload = {
            "sub": str(subject_id),
            "role": role,
            "exp": expire,
        }
        return jwt.encode(payload, _SECRET_KEY, algorithm=_ALGORITHM)

    @staticmethod
    def decode_access_token(token: str) -> tuple[int, str]:
        try:
            payload = jwt.decode(token, _SECRET_KEY, algorithms=[_ALGORITHM])
        except jwt.ExpiredSignatureError as ex:
            raise ValueError("Token has expired") from ex
        except jwt.PyJWTError as ex:
            raise ValueError("Invalid token") from ex

        try:
            return int(payload["sub"]), payload["role"]
        except (KeyError, ValueError) as ex:
            raise ValueError("Malformed token payload") from ex