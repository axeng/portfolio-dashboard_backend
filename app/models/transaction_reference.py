from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class TransactionReference(Base):
    __tablename__ = "transaction_references"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    platform_transaction_reference_id = Column(
        String(length=64)
    )

    transactions = relationship("Transaction", back_populates="transaction_reference")
