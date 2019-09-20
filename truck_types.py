from models import *

class TruckType(BaseModel):
    id = IntegerField(primary_key=True)
    name = CharField()
