# Copyright (C) 2020 by Thomas Lindner <tom@dl6tom.de>
# Copyright (C) 2020 by Cathy Hu <cathy.hu@fau.de>
#
# SPDX-License-Identifier: 0BSD

""" ORM Models for core. """

from databases import Database
from kibicara.config import config
from ormantic import Boolean, Integer, ForeignKey, Model, Text
from sqlalchemy import create_engine, MetaData


class Mapping:
    database = Database(config['database_connection'])
    metadata = MetaData()

    @classmethod
    def create_all(cls):
        engine = create_engine(str(cls.database.url))
        cls.metadata.create_all(engine)

    @classmethod
    def drop_all(cls):
        engine = create_engine(str(cls.database.url))
        cls.metadata.drop_all(engine)


class Admin(Model):
    id: Integer(primary_key=True) = None
    email: Text(unique=True)
    passhash: Text()

    class Mapping(Mapping):
        table_name = 'admins'


class Hood(Model):
    id: Integer(primary_key=True) = None
    name: Text(unique=True)
    landingpage: Text()
    email_enabled: Boolean() = True

    class Mapping(Mapping):
        table_name = 'hoods'


class AdminHoodRelation(Model):
    id: Integer(primary_key=True) = None
    admin: ForeignKey(Admin)
    hood: ForeignKey(Hood)

    class Mapping(Mapping):
        table_name = 'admin_hood_relations'


class Trigger(Model):
    id: Integer(primary_key=True) = None
    hood: ForeignKey(Hood)
    pattern: Text()

    class Mapping(Mapping):
        table_name = 'triggers'


class BadWord(Model):
    id: Integer(primary_key=True) = None
    hood: ForeignKey(Hood)
    pattern: Text()

    class Mapping(Mapping):
        table_name = 'badwords'
