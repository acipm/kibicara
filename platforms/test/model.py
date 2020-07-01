# Copyright (C) 2020 by Thomas Lindner <tom@dl6tom.de>
#
# SPDX-License-Identifier: 0BSD

from kibicara.model import Hood, Mapping
from ormantic import Integer, ForeignKey, Model


class Test(Model):
    id: Integer(primary_key=True) = None
    hood: ForeignKey(Hood)

    class Mapping(Mapping):
        table_name = 'testapi'
