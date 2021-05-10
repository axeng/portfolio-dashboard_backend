from sqlalchemy import Column, Integer, String, Numeric, TIMESTAMP, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from app.database import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    timestamp = Column(
        TIMESTAMP,
        nullable=False
    )

    transaction_type_id = Column(
        Integer,
        ForeignKey("transaction_types.id"),
        nullable=False
    )

    asset_id = Column(
        Integer,
        ForeignKey("assets.id"),
        nullable=False
    )

    amount = Column(
        Numeric,
        nullable=False
    )

    account_id = Column(
        Integer,
        ForeignKey("accounts.id"),
        nullable=False
    )

    transaction_reference_id = Column(
        Integer,
        ForeignKey("transaction_references.id"),
        nullable=False
    )

    platform_transaction_id = Column(
        String(length=64)
    )

    transaction_type = relationship("TransactionType", back_populates="transactions")
    transaction_reference = relationship("TransactionReference", back_populates="transactions")
    asset = relationship("Asset", back_populates="transactions")
    account = relationship("Account", back_populates="transactions")

    UniqueConstraint("timestamp", "asset_id", "account_id")
