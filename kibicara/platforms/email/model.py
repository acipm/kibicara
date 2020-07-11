# Copyright (C) 2020 by Maike <tom@dl6tom.de>
#
# SPDX-License-Identifier: 0BSD

from kibicara.model import Hood, Mapping
from ormantic import Integer, ForeignKey, Model, Text


class EmailSubscribers(Model):
    """ This table stores all subscribers, who want to receive messages via email. """

    id: Integer(primary_key=True) = None
    hood: ForeignKey(Hood)
    email: Text()

    class Mapping(Mapping):
        table_name = 'email_subscribers'


class Email(Model):
    """ This table is used to track the hood ID. It also stores the token secret. """

    id: Integer(primary_key=True) = None
    hood: ForeignKey(Hood)  # this is supposed to be unique - dl6tom/ormantic/pulls/1
    secret: Text()

    class Mapping(Mapping):
        table_name = 'email'
