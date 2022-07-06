""" This module is designed to define accesses to endpoints

Example:
    >>> from db.models.user import User, Role
    >>> from db.base_permissions import BaseACL
    >>> module_example_acl = BaseACL([User, Role])
    >>> module_example_acl.models  # return a list of table names
    ['user', 'role']
    >>> module_example_acl.permissions  # return an interface of permissions
    ['user:view', 'role:view', 'user:add', 'role:add',
    'user:edit', 'role:edit', 'user:delete', 'role:delete']"""

from typing import List, TypeVar

from .base import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseACL:
    __acl__ = ("view", "add", "edit", "delete")

    def __init__(self, models_: List[ModelType]):
        self.models = models_  # type: ignore
        self.permissions = []

    @property
    def models(self):
        return self._models

    @property
    def permissions(self):
        return self._perms

    @permissions.setter
    def permissions(self, value):
        self._perms = [f"{mod}:{act}" for act in self.__acl__ for mod in self._models]

    @models.setter  # type: ignore
    def models(self, value):
        if not isinstance(value, list):
            raise ValueError("Value should be a list")
        self._models = [m.__table__.name for m in value]
