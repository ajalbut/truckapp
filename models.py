from peewee import *

db = SqliteDatabase('truck.app.db')

class BaseModel(Model):
    class Meta:
        database = db

