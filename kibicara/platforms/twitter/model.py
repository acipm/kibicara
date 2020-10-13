# Copyright (C) 2020 by Cathy Hu <cathy.hu@fau.de>
# Copyright (C) 2020 by Martin Rey <martin.rey@mailbox.org>
#
# SPDX-License-Identifier: 0BSD

from ormantic import Boolean, ForeignKey, Integer, Model, Text

from kibicara.model import Hood, Mapping


class Twitter(Model):
    id: Integer(primary_key=True) = None
    hood: ForeignKey(Hood)
    dms_since_id: Integer(allow_null=True) = None
    mentions_since_id: Integer(allow_null=True) = None
    access_token: Text()
    access_token_secret: Text()
    username: Text(allow_null=True) = None
    verified: Boolean() = False
    enabled: Boolean() = False

    class Mapping(Mapping):
        table_name = 'twitterbots'
