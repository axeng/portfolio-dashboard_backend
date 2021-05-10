from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    keycloak_user_id = Column(
        String(length=64),
        nullable=False,
        unique=True
    )

    accounts = relationship("Account", back_populates="user")
