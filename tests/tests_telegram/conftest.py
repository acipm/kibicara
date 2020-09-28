# Copyright (C) 2020 by Cathy Hu <cathy.hu@fau.de>
# Copyright (C) 2020 by Martin Rey <martin.rey@mailbox.org>
#
# SPDX-License-Identifier: 0BSD

from kibicara.model import Hood
from kibicara.platforms.telegram.model import Telegram
from pytest import fixture


@fixture(scope='function')
def telegram(event_loop, hood_id, bot):
    hood = event_loop.run_until_complete(Hood.objects.get(id=hood_id))
    return event_loop.run_until_complete(
        Telegram.objects.create(
            hood=hood,
            api_token=bot['api_token'],
            welcome_message=bot['welcome_message'],
        )
    )
