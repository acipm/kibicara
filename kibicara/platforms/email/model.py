# Copyright (C) 2020 by Thomas Lindner <tom@dl6tom.de>
#
# SPDX-License-Identifier: 0BSD

from kibicara.model import Hood, Mapping
from ormantic import Integer, ForeignKey, Model, Text, DateTime


class EmailRecipients(Model):
    id: Integer(primary_key=True) = None
    hood: ForeignKey(Hood)
    email: Text()

    class Mapping(Mapping):
        table_name = 'email_recipients'

class EmailSeen(Model):
    id: Integer(primary_key=True) = None
    hood: ForeignKey(Hood)
    mail_date: DateTime()

    class Mapping(Mapping):
        table_name = 'email_seen'
