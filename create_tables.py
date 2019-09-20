from drivers import *
from truck_types import *

with db:
    db.drop_tables([Driver, TruckType])
    db.create_tables([Driver, TruckType])

    with db.atomic():
        TruckType.insert_many([
        {"id": 1, "name": "Caminhão 3/4"},
        {"id": 2, "name": "Caminhão Toco"},
        {"id": 3, "name": "Caminhão Truck"},
        {"id": 4, "name": "Carreta Simples"},
        {"id": 5, "name": "Carreta Eixo Estendido"},
    ]).execute()
