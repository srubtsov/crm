from fastapi import Form
from fastapi.security import OAuth2PasswordRequestForm


class AuthRequestForm(OAuth2PasswordRequestForm):
    def __init__(
        self,
        username: str = Form(default=...),
        password: str = Form(default=...),
    ):
        self.username = username
        self.password = password
