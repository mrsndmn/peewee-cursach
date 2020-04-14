import os

import pytest

from peewee import SqliteDatabase
import tempfile
import model.logist as model
from cursach.config import CursachConf as cfg

from model.queries import TrifonQueries

class TestQueries():

    def test_shema(self):
        wh1 = model.Warehouse.create(address="test addr1 RU", capacity=10)
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
        count = TrifonQueries.get_query_packed_cargos_with_type(packed_type)
        print(f"type {packed_type} count = {count}")
        assert count > 0

        # X = cargo_no_pack
        # продукты без упаковки
        packed_type = 'cargo_no_pack'
        count = TrifonQueries.get_query_packed_cargos_with_type(packed_type)
        print(f"type {packed_type} count = {count}")
        assert count == 0

        # 2) Названия организаций перевозчиков, работающих с грузами на складе по адресу X,
        # отсортированные по массам грузов

        # select carrier.organisation, cargo.mass from carrier join cargo, warehouse on
        #   ( carrier.id = cargo.carrier_id and cargo.warehouse_id = warehouse.id )
        #   where warehouse.address = 'test addr1' order by cargo.mass desc;

        print("_get_query_organisations_by_warehouse_address_ordereb_by_cargo_mass")
        for carrier in TrifonQueries.get_query_organisations_by_warehouse_address_ordereb_by_cargo_mass(
                "test addr1").order_by(model.Cargo.mass):
            print(carrier.organisation)

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

        print("containers_in_big_premises")
        for row in TrifonQueries.get_mass_cap_kind_by_country_and_volume("RU", 1000):
            print(row)

        return
