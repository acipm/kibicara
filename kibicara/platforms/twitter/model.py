# Copyright (C) 2020 by Cathy Hu <cathy.hu@fau.de>
#
# SPDX-License-Identifier: 0BSD

from kibicara.model import Hood, Mapping
from ormantic import Boolean, Integer, ForeignKey, Model, Text


class Twitter(Model):
    id: Integer(primary_key=True) = None
    hood: ForeignKey(Hood)
    dms_since_id: Integer(allow_null=True) = None
    mentions_since_id: Integer(allow_null=True) = None
    access_token: Text()
    access_token_secret: Text()
    successful_verified: Boolean() = False

    class Mapping(Mapping):
        table_name = 'twitterbots'
