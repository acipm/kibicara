# Copyright (C) 2020 by Thomas Lindner <tom@dl6tom.de>
# Copyright (C) 2020 by Martin Rey <martin.rey@mailbox.org>
#
# SPDX-License-Identifier: 0BSD

from ormantic import ForeignKey, Integer, Model

from kibicara.model import Hood, Mapping


class Test(Model):
    id: Integer(primary_key=True) = None
    hood: ForeignKey(Hood)

    class Mapping(Mapping):
        table_name = 'testapi'
