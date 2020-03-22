import os

import pytest

from peewee import SqliteDatabase
import tempfile
import model.logist as model
from cursach.config import CursachConf as cfg


@pytest.fixture(scope='session')
def test_db():
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

    yield

    cfg.db.close()
    # os.unlink('logist.db')

    return


class TestQueries():

    def _get_query_packed_cargos_with_type(self, type):
        return (model.Cargo
                .select()
                .join(model.Packaging, on=(model.Cargo.id == model.Packaging.cargo))
                .where(model.Cargo.kind == type)
                .count())

    def _get_query_organisations_by_warehouse_address_ordereb_by_cargo_mass(self, address):
        return (model.Carrier
                .select()
                .join(model.Cargo)
                .join(model.Warehouse)
                .where(model.Warehouse.address == address)
                .order_by(model.Cargo.mass.desc())
            )

    def test_shema(self, test_db):
        wh1 = model.Warehouse.create(address="test addr1", capacity=10)
        wh1.save()
        wh2 = model.Warehouse.create(address="test addr2", capacity=100)
        wh2.save()

        prem1 = model.Premise.create(area=100, heigth=100, warehouse=wh1.id)
        prem1.save()
        prem2 = model.Premise.create(area=200, heigth=200, warehouse=wh1.id)
        prem2.save()

        carrier1 = model.Carrier.create(organisation="org1", cargo=10)
        carrier1.save()
        carrier2 = model.Carrier.create(organisation="org2", cargo=20)
        carrier2.save()

        cargo_no_pack = model.Cargo.create(kind="cargo_no_pack", mass=10, carrier=carrier1.id, warehouse=wh1.id)
        cargo_no_pack.save()
        cargo1 = model.Cargo.create(kind="cargo-kind1", mass=10, carrier=carrier1.id, warehouse=wh1.id)
        cargo1.save()
        cargo2 = model.Cargo.create(kind="cargo-kind2", mass=20, carrier=carrier2.id, warehouse=wh2.id)
        cargo2.save()

        pack1 = model.Packaging.create(product="product1", quantity=10, cargo=cargo1.id)
        pack1.save()
        pack2 = model.Packaging.create(product="product2", quantity=20, cargo=cargo2.id)
        pack2.save()

        container1 = model.Container.create(kind="cont-kind1", capacity=10, cargo=cargo1.id)
        container1.save()
        container2 = model.Container.create(kind="cont-kind2", capacity=20, cargo=cargo2.id)
        container2.save()

        # 1) Количество продуктов в упаковках вида X
        # select count(*) from cargo join packaging on (cargo.id = packaging.cargo_id) where kind = 'cargo_no_pack';

        # X = cargo-kind1
        packed_type = 'cargo-kind1'
        count = self._get_query_packed_cargos_with_type(packed_type)
        print(f"type {packed_type} count = {count}")
        assert count > 0

        # X = cargo_no_pack
        # продукты без упаковки
        packed_type = 'cargo_no_pack'
        count = self._get_query_packed_cargos_with_type(packed_type)
        print(f"type {packed_type} count = {count}")
        assert count == 0

        # 2) Названия организаций перевозчиков, работающих с грузами на складе по адресу X,
        # отсортированные по массам грузов
        print("_get_query_organisations_by_warehouse_address_ordereb_by_cargo_mass")
        for carrier in self._get_query_organisations_by_warehouse_address_ordereb_by_cargo_mass(
                "test addr1").order_by(model.Cargo.mass):
            print(carrier.organisation)

        # select carrier.organisation, cargo.mass from carrier join cargo, warehouse on
        #   ( carrier.id = cargo.carrier_id and cargo.warehouse_id = warehouse.id )
        #   where warehouse.address = 'test addr1' order by cargo.mass desc;

        # 3) Виды и вместительность контейнеров и массы грузов, хранящихся на складах с
        # помещениями объёмом больше X в стране Y (пусть форма складского помещения – цилиндр
        # или параллелепипед)

        # select cargo.id, container.id from cargo join container
        #   on (cargo.id = container.cargo_id) where cargo.warehouse_id in
        #       (
        #           select distinct warehouse.id from warehouse join premise
        #           on ( premise.warehouse_id = warehouse.id )
        #           where premise.heigth * premise.area > 10
        #       );

        warehouses_with_big_premises = model.Warehouse.select().join(
            model.Premise).where(model.Premise.heigth * model.Premise.area > 10000)

        containers_in_big_premises = model.Cargo.select(
            model.Cargo.mass, model.Container.capacity, model.Container.kind
        ).join(
            model.Container
        ).where(
            model.Cargo.warehouse.in_(warehouses_with_big_premises)
        )
        print("containers_in_big_premises")
        for row in containers_in_big_premises.dicts():
            print(row)

        return
