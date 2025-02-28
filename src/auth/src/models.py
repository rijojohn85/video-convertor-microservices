from src.db_connection import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import (
    Column,
    text,
    String,
    LargeBinary,
    CheckConstraint,
    UniqueConstraint,
)


class User(Base):
    __tablename__ = "users"

    id: str = Column(
        UUID(as_uuid=True),
        nullable=False,
        primary_key=True,
        unique=True,
        server_default=text("uuid_generate_v4()"),
    )
    username: str = Column(String(100), nullable=False, unique=True)
    hashed_password: bytes = Column(LargeBinary, nullable=False)

    __table_args__ = (
        CheckConstraint("LENGTH(username)>0", name="username_length_min_check"),
        CheckConstraint("LENGTH(username)<100", name="username_length_max_check"),
        UniqueConstraint("username", name="username_level_unique"),
    )
