from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class TransactionType(Base):
    __tablename__ = "transaction_types"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    display_name = Column(
        String(length=64),
        nullable=False,
        unique=True
    )

    transactions = relationship("Transaction", back_populates="transaction_type")
