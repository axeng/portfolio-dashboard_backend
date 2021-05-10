from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Platform(Base):
    __tablename__ = "platforms"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String(length=64),
        nullable=False,
        unique=True
    )

    display_name = Column(
        String(length=64),
        nullable=False
    )

    accounts = relationship("Account", back_populates="platform")
    assets = relationship("Asset", back_populates="platform")
