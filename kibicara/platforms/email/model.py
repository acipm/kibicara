# Copyright (C) 2020 by Maike <maike@systemli.org>
# Copyright (C) 2020 by Cathy Hu <cathy.hu@fau.de>
# Copyright (C) 2020 by Thomas Lindner <tom@dl6tom.de>
#
# SPDX-License-Identifier: 0BSD

from kibicara.model import Hood, Mapping
from ormantic import Integer, ForeignKey, Model, Text


class Email(Model):
    """ This table is used to track the names. It also stores the token secret. """

    id: Integer(primary_key=True) = None
    hood: ForeignKey(Hood)
    name: Text(unique=True)
    secret: Text()

    class Mapping(Mapping):
        table_name = 'email'


class EmailSubscribers(Model):
    """ This table stores all subscribers, who want to receive messages via email. """

    id: Integer(primary_key=True) = None
    hood: ForeignKey(Hood)
    email: Text(unique=True)

    class Mapping(Mapping):
        table_name = 'email_subscribers'
