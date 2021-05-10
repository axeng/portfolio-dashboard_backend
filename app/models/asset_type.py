from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class AssetType(Base):
    __tablename__ = "asset_types"

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

    assets = relationship("Asset", back_populates="asset_type")
