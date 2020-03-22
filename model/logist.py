from peewee import *

from cursach.config import CursachConf as cfg


class LigistModel(Model):
    class Meta:
        database = cfg.db  # This model uses the "people.db" database.


class Warehouse(LigistModel):
    """
    Склад
    """
    address = TextField()
    capacity = IntegerField()


class Premise(LigistModel):
    """
    Помещение
    """
    area = IntegerField()
    heigth = IntegerField()
    warehouse = ForeignKeyField(Warehouse, backref='premise')


class Carrier(LigistModel):
    """
    Перевозчик
    """
    organisation = TextField()
    cargo = IntegerField()  # todo wat?! почему не FareignKey?


class Cargo(LigistModel):
    """
    Груз
    """
    kind = TextField()
    mass = IntegerField()
    carrier = ForeignKeyField(Carrier, backref='cargo_obj')
    warehouse = ForeignKeyField(Warehouse, backref='cargo_obj')


class Packaging(LigistModel):
    """
    Класс упаковки
    """
    product = TextField()
    quantity = IntegerField()
    cargo = ForeignKeyField(Cargo, backref='pack')


class Container(LigistModel):
    """
    Класс контейнера
    """
    kind = TextField()
    capacity = IntegerField()
    cargo = ForeignKeyField(Cargo, backref='conteainer')
