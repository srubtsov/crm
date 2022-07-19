from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ....db.models.user import User
from ...core.deps import get_db
from ...core.exceptions import UnAuthorizedError
from ...core.forms import AuthRequestForm
from ...core.security import create_access_token, verify_password

router = APIRouter()


async def authenticate(db: Session, username: str, password: str) -> Optional[User]:
    user = db.query(User).filter_by(username=username, is_active=True).one_or_none()
    if not user:
        return None
    valid_password = verify_password(password, user.hashed_password)
    if not valid_password:
        return None
    return user


@router.post("/access-token")
async def obtain_access_token(
    db: Session = Depends(get_db), form_data: AuthRequestForm = Depends()
):
    """
    OAuth2 compatible token login, get an access token for future requests
    """

    user = await authenticate(db, form_data.username, form_data.password)
    if not user:
        raise UnAuthorizedError

    access_token = create_access_token(user.username)
    return {
        "access_token": access_token,
        "token_type": "Bearer",
    }
