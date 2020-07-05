# Copyright (C) 2020 by Cathy Hu <cathy.hu@fau.de>
#
# SPDX-License-Identifier: 0BSD

from kibicara.model import Hood, Mapping
from ormantic import Integer, ForeignKey, Model, Text


class Twitter(Model):
    id: Integer(primary_key=True) = None
    hood: ForeignKey(Hood)
    dms_since_id: Integer()
    mentions_since_id: Integer()
    access_token: Text()
    access_token_secret: Text()

    class Mapping(Mapping):
        table_name = 'twitterbots'
