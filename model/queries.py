import model.logist as model
from cursach.config import CursachConf as cfg
from peewee import SqliteDatabase



class TrifonQueries():
    cfg.db.connect()

    models = [
        model.Warehouse,
        model.Premise,
        model.Carrier,
        model.Cargo,
        model.Packaging,
        model.Container,
    ]

    cfg.db.create_tables(models)


    def get_query_packed_cargos_with_type(type):
        return (model.Cargo
                .select()
                .join(model.Packaging, on=(model.Cargo.id == model.Packaging.cargo))
                .where(model.Cargo.kind == type)
                .count())

    def get_query_organisations_by_warehouse_address_ordereb_by_cargo_mass(address):
        return (model.Carrier
                .select()
                .join(model.Cargo)
                .join(model.Warehouse)
                .where(model.Warehouse.address == address)
                .order_by(model.Cargo.mass.desc())
                )

    def get_mass_cap_kind_by_country_and_volume(country, volume):

        warehouses_with_big_premises = model.Warehouse.select().join(
            model.Premise).where(
                model.Premise.heigth * model.Premise.area > volume
                and
                model.Warehouse.address % '*RU*'
            )

        containers_in_big_premises = model.Cargo.select(
            model.Cargo.mass, model.Container.capacity, model.Container.kind
        ).join(
            model.Container
        ).where(
            model.Cargo.warehouse.in_(warehouses_with_big_premises)
        )

        return containers_in_big_premises.dicts()