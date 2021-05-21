import json

from app import crud
from app.database import SessionLocal
from app.platforms import platform_to_module
from app.platforms.commons import DataTypeEnum

from app.schemas import AssetTypeCreate, PlatformCreate, TransactionTypeCreate, AssetCreate
from app.workers.tasks.external_apis_fetch_data import external_apis_fetch_data


def add_asset_types(db, initial_data):
    name_list = []

    for data in initial_data:
        name_list.append(data["name"])

        asset_type = crud.asset_type.get_by_name(db, data["name"])
        if asset_type:
            continue

        asset_type_in = AssetTypeCreate(**data)
        crud.asset_type.create(db, asset_type_in)

    for asset_type in crud.asset_type.get_multi(db, limit=-1):
        if asset_type.name not in name_list:
            crud.asset_type.remove_obj(db, asset_type)


def add_platforms(db, initial_data):
    name_list = []

    for data in initial_data:
        name_list.append(data["name"])

        platform = crud.platform.get_by_name(db, data["name"])
        if platform:
            continue

        platform_in = PlatformCreate(**data)
        crud.platform.create(db, platform_in)

    for platform in crud.platform.get_multi(db, limit=-1):
        if platform.name not in name_list:
            crud.platform.remove_obj(platform)


def add_transaction_types(db, initial_data):
    name_list = []

    for data in initial_data:
        name_list.append(data["name"])

        transaction_type = crud.transaction_type.get_by_name(db, data["name"])
        if transaction_type:
            continue

        transaction_type_in = TransactionTypeCreate(**data)
        crud.transaction_type.create(db, transaction_type_in)

    for transaction_type in crud.transaction_type.get_multi(db, limit=-1):
        if transaction_type.name not in name_list:
            crud.transaction_type.remove_obj(transaction_type)


def add_assets(db, initial_data):
    for data in initial_data:
        platform_id = data["platform_id"] if "platform_id" in data else None

        asset = crud.asset.get_by_code(db, data["code"], platform_id)
        if asset:
            continue

        asset_type = crud.asset_type.get_by_name(db, data["asset_type_name"])
        if not asset_type:
            continue

        asset_in = AssetCreate(**data, asset_type_id=asset_type.id)
        crud.asset.create(db, asset_in)


def add_platforms_assets(db):
    for platform in crud.platform.get_multi(db, limit=-1):
        platform_module = platform_to_module[platform.name]

        if DataTypeEnum.assets not in platform_module.supported_data_types:
            continue

        # TODO use celery
        external_apis_fetch_data(DataTypeEnum.assets, platform_id=platform.id)


def populate_database() -> None:
    db = SessionLocal()

    with open("initial_data.json") as json_file:
        initial_data = json.load(json_file)

        add_asset_types(db, initial_data["asset_types"])
        add_platforms(db, initial_data["platforms"])
        add_transaction_types(db, initial_data["transaction_types"])
        add_assets(db, initial_data["assets"])

    add_platforms_assets(db)

    db.close()


def main() -> None:
    populate_database()


if __name__ == "__main__":
    main()
