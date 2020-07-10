# Copyright (C) 2020 by Cathy Hu <cathy.hu@fau.de>
#
# SPDX-License-Identifier: 0BSD

from kibicara.model import Hood, Mapping
from ormantic import Boolean, Integer, ForeignKey, Model, Text


class Telegram(Model):
    id: Integer(primary_key=True) = None
    hood: ForeignKey(Hood)
    api_token: Text()
    welcome_message: Text()

    class Mapping(Mapping):
        table_name = 'telegrambots'


class TelegramUser(Model):
    id: Integer(primary_key=True) = None
    user_id: Integer(unique=True)
    # TODO unique
    bot: ForeignKey(Telegram)

    class Mapping(Mapping):
        table_name = 'telegramusers'
