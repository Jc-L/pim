from mimetypes import init
import os

from peewee import *

db_proxy = DatabaseProxy()  # Create a proxy for our db.
initialized = False

class Task(Model):
    label = CharField()
    description = TextField()
    created = DateField()
    updated = DateField()

    class Meta:
        database = db_proxy


def pimdata_init(config):
    database = SqliteDatabase(config.database)
    database_proxy.initialize(database)
    initialized = True