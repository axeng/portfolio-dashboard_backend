from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class ExternalAPI(Base):
    __tablename__ = "external_apis"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    account_id = Column(
        Integer,
        ForeignKey("accounts.id"),
        nullable=False
    )

    authentication_data = Column(
        String,
        nullable=False
    )

    display_name = Column(
        String(length=64),
        nullable=False
    )

    account = relationship("Account", back_populates="external_apis")
