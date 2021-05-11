import json

from app import crud
from app.database import SessionLocal

from app.schemas import AssetTypeCreate, PlatformCreate, TransactionTypeCreate, AssetCreate


def add_asset_types(db, initial_data):
    for data in initial_data:
        asset_type = crud.asset_type.get_by_name(db, data["name"])
        if asset_type:
            continue

        asset_type_in = AssetTypeCreate(**data)
        crud.asset_type.create(db, asset_type_in)


def add_platforms(db, initial_data):
    for data in initial_data:
        platform = crud.platform.get_by_name(db, data["name"])
        if platform:
            continue

        platform_in = PlatformCreate(**data)
        crud.platform.create(db, platform_in)


def add_transaction_types(db, initial_data):
    for data in initial_data:
        transaction_type = crud.transaction_type.get_by_name(db, data["name"])
        if transaction_type:
            continue

        transaction_type_in = TransactionTypeCreate(**data)
        crud.transaction_type.create(db, transaction_type_in)


def add_assets(db, initial_data):
    for data in initial_data:
        asset = crud.asset.get_by_code(db, data["code"])
        if asset:
            continue

        asset_type = crud.asset_type.get_by_name(db, data["asset_type_name"])
        if not asset_type:
            continue

        asset_in = AssetCreate(**data, asset_type_id=asset_type.id)
        crud.asset.create(db, asset_in)


def populate_database() -> None:
    db = SessionLocal()

    with open("initial_data.json") as json_file:
        initial_data = json.load(json_file)

        add_asset_types(db, initial_data["asset_types"])
        add_platforms(db, initial_data["platforms"])
        add_transaction_types(db, initial_data["transaction_types"])
        add_assets(db, initial_data["assets"])

    db.close()


def main() -> None:
    populate_database()


if __name__ == "__main__":
    main()
