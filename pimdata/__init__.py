from mimetypes import init
import os
import logging
import datetime

from peewee import *

db_proxy = DatabaseProxy()  # Create a proxy for our db.
initialized = False

class Task(Model):
    task_id = AutoField()
    label = CharField()
    description = TextField(null = True)
    created = DateTimeField(default = datetime.datetime.now)
    # should be part of a changelog table to track changes
    updated = DateTimeField(default = datetime.datetime.now)
    class Meta:
        database = db_proxy

class People(Model):
    people_id = AutoField()
    name = CharField()
    firstname = CharField()
    location = CharField(null = True)
    class Meta:
        database = db_proxy

class PeopleRole(Model):
    peoplerole_id = AutoField()
    description = CharField(null = False)
    start = DateTimeField(null = False)
    stop = DateTimeField(default = '2099-01-01')
    class Meta:
        database = db_proxy
# When you need to refer to people through an external ID

class PeopleExternalId(Model):
    peopleexternalid_id = AutoField()
    name = CharField(null = False)
    value = CharField(null = False)
    people = ForeignKeyField(People, backref='externalids')
    class Meta:
        database = db_proxy

class Organization(Model):
    organization_id = AutoField()
    name = CharField(null = False)
    description = TextField(null = True)
    # See also http://docs.peewee-orm.com/en/latest/peewee/models.html#self-referential-foreign-keys
    parent_organization = ForeignKeyField('self', backref='child_organizations', null=True)
    class Meta:
        database = db_proxy

def pimdata_init(config):
    database = SqliteDatabase(config.DATABASE)
    db_proxy.initialize(database)
    initialized = True
    database.connect()
    database.create_tables([Task, People, PeopleRole, PeopleExternalId, Organization])