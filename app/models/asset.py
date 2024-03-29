from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from app.database import Base
from app.models.commons import same_as


class Asset(Base):
    __tablename__ = "assets"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    code = Column(
        String(length=64),
        nullable=False
    )

    asset_type_id = Column(
        Integer,
        ForeignKey("asset_types.id"),
        nullable=False
    )

    platform_id = Column(
        Integer,
        ForeignKey("platforms.id")
    )

    parent_asset_id = Column(
        Integer,
        ForeignKey("assets.id")
    )

    display_name = Column(
        String(length=64),
        nullable=False,
        default=same_as("code")
    )

    asset_type = relationship("AssetType", back_populates="assets")
    platform = relationship("Platform", back_populates="assets")
    parent_asset = relationship("Asset", backref="child_accounts", remote_side="Asset.id")

    transactions = relationship("Transaction", back_populates="asset")

    @property
    def prices(self):
        return self.prices_base + self.prices_target

    UniqueConstraint("code", "platform_id")
