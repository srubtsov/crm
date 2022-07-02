from sqlalchemy import (
    ARRAY,
    BigInteger,
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
    Table,
)
from sqlalchemy.orm import relationship

from db.base import Base

user_role = Table(
    "user_role",
    Base.metadata,
    Column(
        "user_id",
        Integer,
        ForeignKey("user.id"),
    ),
    Column(
        "role.id",
        Integer,
        ForeignKey("role.id"),
    ),
)


class User(Base):
    id = Column(BigInteger, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean(), default=True)
    permissions = Column(ARRAY(String))
    roles = relationship("Role", secondary=user_role)


class Role(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
