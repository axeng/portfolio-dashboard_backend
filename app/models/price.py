from sqlalchemy import Column, Integer, Numeric, TIMESTAMP, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from app.database import Base


class Price(Base):
    __tablename__ = "prices"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    timestamp = Column(
        TIMESTAMP,
        nullable=False
    )

    base_asset_id = Column(
        Integer,
        ForeignKey("assets.id"),
        nullable=False
    )

    target_asset_id = Column(
        Integer,
        ForeignKey("assets.id"),
        nullable=False
    )

    price = Column(
        Numeric,
        nullable=False
    )

    base_asset = relationship("Asset", foreign_keys=[base_asset_id], backref="prices_base")
    target_asset = relationship("Asset", foreign_keys=[target_asset_id], backref="prices_target")

    UniqueConstraint("timestamp", "base_asset_id", "target_asset_id")
