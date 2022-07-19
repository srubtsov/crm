from datetime import datetime, timedelta
from typing import Any, Union

from jose import jwt
from passlib.context import CryptContext

from .config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(subject: Union[str, Any], exp_delta: timedelta = None) -> str:
    """
    Create access JWT token for login into the system
    """
    expire = datetime.utcnow() + timedelta(
        minutes=exp_delta
        if exp_delta
        else settings.ACCESS_TOKEN_EXPIRE_MINUTES  # type:ignore
    )
    to_encode = {
        "exp": expire,
        "sub": str(subject),
    }
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.HASH_ALGORITHM
    )
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def set_password_hash(password: str) -> str:
    return pwd_context.hash(password)
