# Copyright (C) 2020 by Cathy Hu <cathy.hu@fau.de>
#
# SPDX-License-Identifier: 0BSD

from kibicara.model import Hood
from kibicara.platforms.twitter.model import Twitter
from pytest import fixture


@fixture(scope='function')
def twitter(event_loop, hood_id):
    hood = event_loop.run_until_complete(Hood.objects.get(id=hood_id))
    return event_loop.run_until_complete(
        Twitter.objects.create(
            hood=hood,
            access_token='access_token123',
            access_token_secret='access_token_secret123',
        )
    )
