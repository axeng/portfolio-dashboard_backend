from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class Account(Base):
    __tablename__ = "accounts"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    platform_id = Column(
        Integer,
        ForeignKey("platforms.id")
    )

    parent_account_id = Column(
        Integer,
        ForeignKey("accounts.id")
    )

    display_name = Column(
        String(length=64),
        nullable=False
    )

    user = relationship("User", back_populates="accounts")
    platform = relationship("Platform", back_populates="accounts")
    parent_account = relationship("Account", back_populates="child_accounts")

    transactions = relationship("Transaction", back_populates="account")
    child_accounts = relationship("Account", back_populates="parent_account")
    external_apis = relationship("ExternalAPI", back_populates="account")
