from geopy.geocoders import Nominatim
from models import *
from truck_types import *
from playhouse.shortcuts import model_to_dict
import datetime
from connexion import request

class Driver(BaseModel):
    id = IntegerField(primary_key=True)
    name = CharField()
    age = IntegerField()
    gender = CharField()
    license_type = CharField()
    has_truck = BooleanField()
    truck_type = ForeignKeyField(TruckType, backref='drivers')
    loaded = BooleanField()
    origin = CharField()
    destination = CharField()
    stop_date = DateTimeField()

def read(id):
    return model_to_dict(Driver.get_or_none(id))

def list():
    return [model_to_dict(d) for d in Driver.select()]

def listNotLoaded():
    return [model_to_dict(d) for d in Driver.select().where(Driver.loaded == False)]

def countWithTruck():
    return {'count': (Driver.select().where(Driver.has_truck == True).count())}

def countLoadedByPeriod():
    today = datetime.date.today()
    weekStart = today - datetime.timedelta(days=today.weekday())
    monthStart = today - datetime.timedelta(days=(today.day - 1))
    return {
        'day': Driver.select().where(Driver.loaded == True).where(Driver.stop_date >= today).count(),
        'week': Driver.select().where(Driver.loaded == True).where(Driver.stop_date >= weekStart).count(),
        'month': Driver.select().where(Driver.loaded == True).where(Driver.stop_date >= monthStart).count(),
    }

def countOriginDestinationByTruckType():
    return [{
            'origin': d.origin,
            'destination': d.destination,
            'truck_type': d.truck_type.name,
            'count': d.count
        } for d in Driver.select(Driver.origin, Driver.destination,
        Driver.truck_type, fn.COUNT(Driver.id).alias('count')
    ).join(TruckType).group_by(Driver.origin, Driver.destination, Driver.truck_type)]

def geolocate(id):
    try:
        driver = Driver.get_or_none(id)
        if not driver:
            raise Exception('Motorista não encontrado.')

        geolocator = Nominatim(user_agent="truck_app")
        geocoded_origin = geolocator.geocode(driver.origin)
        if not geocoded_origin:
            raise Exception("Origem '%s' não encontrada." % driver.origin)
        geocoded_destination = geolocator.geocode(driver.destination)
        if not geocoded_destination:
            raise Exception("Destino '%s' não encontrado." % driver.destination)
        return {
            'origin_latitude': geocoded_origin.latitude,
            'origin_longitude': geocoded_origin.longitude,
            'destination_latitude': geocoded_destination.latitude,
            'destination_longitude': geocoded_destination.longitude
        }

    except Exception as e:
        return {'error': str(e)}

def add():
    try:
        reqJson = request.get_json()
        with db.atomic():
            truckType = TruckType.get_or_none(reqJson['truck_type'])
            if not truckType:
                raise Exception('Tipo de caminhão inválido')
            stop_date = datetime.datetime.strptime(reqJson['stop_date'], '%d/%m/%Y %H:%M:%S')

            driver = Driver.create(
                name = reqJson['name'],
                age = reqJson['age'],
                gender = reqJson['gender'],
                license_type = reqJson['license_type'],
                has_truck = reqJson['has_truck'],
                truck_type = reqJson['truck_type'],
                loaded = reqJson['loaded'],
                origin = reqJson['origin'],
                destination = reqJson['destination'],
                stop_date = stop_date)
        return model_to_dict(driver)

    except Exception as e:
        return {'error': str(e)}

def edit(id):
    try:
        reqJson = request.get_json()
        with db.atomic():
            driver = Driver.get_or_none(id)
            if not driver:
                raise Exception('Motorista não encontrado.')
            truckType = TruckType.get_or_none(reqJson['truck_type'])
            if not truckType:
                raise Exception('Tipo de caminhão inválido')
            stop_date = datetime.datetime.strptime(reqJson['stop_date'], '%d/%m/%Y %H:%M:%S')

            driver.name = reqJson['name']
            driver.age = reqJson['age']
            driver.gender = reqJson['gender']
            driver.license_type = reqJson['license_type']
            driver.has_truck = reqJson['has_truck']
            driver.truck_type = reqJson['truck_type']
            driver.loaded = reqJson['loaded']
            driver.origin = reqJson['origin']
            driver.destination = reqJson['destination']
            driver.stop_date = stop_date
            driver.save()

        return model_to_dict(driver)

    except Exception as e:
        return {'error': str(e)}

def delete(id):
    try:
        with db.atomic():
            driver = Driver.get_or_none(id)
            if not driver:
                raise Exception('Motorista não encontrado.')
        return {'success': driver.delete_instance()}

    except Exception as e:
        return {'error': str(e)}
