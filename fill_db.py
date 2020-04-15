from peewee import SqliteDatabase
from peewee_migrate import Router

from model.logist import Warehouse, Premise, Carrier, Cargo, Packaging, Container

import random

def fill():
    countries = ['Russia', 'China', 'France', 'America']
    capacities = [1000000,1500000, 2000000, 2500000, 3000000 ]
    warehouses = []
    containers = ['drawer', 'barrel', 'container' ]
    for country in countries:
        for capacity in capacities:
            warehouse = Warehouse.create(
                address = country,
                capacity = capacity
                )
            warehouses.append(warehouse)
            for i in range(capacity//500000):
                premise = Premise.create(
                        area = int(capacity)**(1/2),
                        heigth = int(capacity)**(1/2),
                        warehouse = warehouse
                        )
    carry_num = [1, 2, 3, 4]
    orgs = ['Best Carrier', 'Super carrier', 'Common carrier']
    products = ['Fish', 'Meat', 'Seeds']
    for org in orgs:
        for num in carry_num:
            carrier = Carrier.create(
                    organisation = org,
                    cargo = num
                    )
            for i in range(num):
                cargo = Cargo.create(
                    kind = random.choice(carry_num),
                    mass = random.randint(100, 1000),
                    carrier = carrier,
                    warehouse = random.choice(warehouses)
                    )
                for i in range(random.choice(carry_num)):
                    capacity = random.randint(100, 1000)
                    container = Container.create(
                        kind = random.choice(containers),
                        capacity = capacity,
                        cargo = cargo
                        )
                    package = Packaging.create(
                        product = random.choice(products),
                        quantity = random.randint(50, capacity),
                        cargo = cargo
                        )

if __name__ == '__main__':
    fill()
    #router = Router(SqliteDatabase('logist.db'))

    # Create migration
    #router.create('init', "models")
    #
    # # Run migration/migrations
    # router.run('init')
    #
    # # Run all unapplied migrations
    #router.run()
