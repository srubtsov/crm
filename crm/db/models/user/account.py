from sqlalchemy import (
    ARRAY,
    BigInteger,
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Table,
    func,
)
from sqlalchemy.orm import relationship

from ...base import Base

user_role = Table(
    "user_role",
    Base.metadata,  # type: ignore
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
    created_at = Column(
        DateTime(),
        default=func.now(),
        nullable=False,
    )

    roles = relationship("Role", secondary=user_role, back_populates="users")


class Role(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, nullable=False)
    created_at = Column(
        DateTime(),
        default=func.now(),
        nullable=False,
    )

    users = relationship("User", secondary=user_role, back_populates="roles")
