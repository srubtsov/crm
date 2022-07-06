from ...base_permissions import BaseACL
from .account import Role, User

account_acl = BaseACL(
    [
        Role,
        User,
    ]
)  # type: ignore
