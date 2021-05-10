import json

from app import crud
from app.database import SessionLocal

from app.schemas import AssetTypeCreate, PlatformCreate, TransactionTypeCreate


def add_asset_types(db, initial_data):
    for data in initial_data:
        asset_type = crud.asset_type.get_by_name(db, data["name"])
        if not asset_type:
            asset_type_in = AssetTypeCreate(**data)
            crud.asset_type.create(db, asset_type_in)


def add_platforms(db, initial_data):
    for data in initial_data:
        platform = crud.platform.get_by_name(db, data["name"])
        if not platform:
            platform_in = PlatformCreate(**data)
            crud.platform.create(db, platform_in)


def add_transaction_types(db, initial_data):
    for data in initial_data:
        transaction_type = crud.transaction_type.get_by_name(db, data["name"])
        if not transaction_type:
            transaction_type_in = TransactionTypeCreate(**data)
            crud.transaction_type.create(db, transaction_type_in)


def populate_database() -> None:
    db = SessionLocal()

    with open("initial_data.json") as json_file:
        initial_data = json.load(json_file)

        add_asset_types(db, initial_data["asset_types"])
        add_platforms(db, initial_data["platforms"])
        add_transaction_types(db, initial_data["transaction_types"])

    db.close()


def main() -> None:
    populate_database()


if __name__ == "__main__":
    main()
