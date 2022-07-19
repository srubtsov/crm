from typing import AsyncGenerator, Optional

import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from pydantic import ValidationError
from sqlalchemy.orm import Session

from ...db.models.user import User
from ...db.session import SessionLocal
from ..schema.token import TokenPayload
from .config import settings
from .exceptions import AccessDeniedError, UnAuthorizedError

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="/auth/access-token")


async def get_db() -> AsyncGenerator:
    with SessionLocal() as session:
        yield session


async def get_current_user(
    security_scopes: SecurityScopes,
    db: Session = Depends(get_db),
    token: str = Depends(reusable_oauth2),
) -> Optional[User]:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.HASH_ALGORITHM]
        )
        token_data = TokenPayload(sub=payload["sub"])
    except (jwt.PyJWTError, ValidationError, KeyError):
        raise UnAuthorizedError
    user = (
        db.query(User).filter_by(username=token_data.sub, is_active=True).one_or_none()
    )
    if not user:
        raise UnAuthorizedError

    if not user.permissions:
        raise AccessDeniedError

    if security_scopes.scopes:
        if not all(acl in user.permissions for acl in security_scopes.scopes):
            raise AccessDeniedError
    return user
