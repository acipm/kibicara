# Copyright (C) 2020 by Cathy Hu <cathy.hu@fau.de>
# Copyright (C) 2020 by Martin Rey <martin.rey@mailbox.org>
#
# SPDX-License-Identifier: 0BSD

from fastapi import status
from ormantic.exceptions import NoMatch
from pytest import mark, raises

from kibicara.platforms.telegram.model import Telegram, TelegramUser


@mark.parametrize('bot', [{'api_token': 'apitoken123', 'welcome_message': 'msg'}])
def test_telegram_delete_bot(client, event_loop, bot, telegram, auth_header):
    event_loop.run_until_complete(
        TelegramUser.objects.create(user_id=1234, bot=telegram.id)
    )
    event_loop.run_until_complete(
        TelegramUser.objects.create(user_id=5678, bot=telegram.id)
    )
    response = client.delete(
        '/api/hoods/{0}/telegram/{1}'.format(telegram.hood.id, telegram.id), headers=auth_header
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT
    with raises(NoMatch):
        event_loop.run_until_complete(Telegram.objects.get(id=telegram.id))
    with raises(NoMatch):
        event_loop.run_until_complete(TelegramUser.objects.get(id=telegram.id))


def test_telegram_delete_bot_invalid_id(client, auth_header, hood_id):
    response = client.delete('/api/hoods/1337/telegram/123', headers=auth_header)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    response = client.delete('/api/hoods/wrong/telegram/123', headers=auth_header)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    response = client.delete('/api/hoods/{0}/telegram/7331'.format(hood_id), headers=auth_header)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    response = client.delete(
        '/api/hoods/{0}/telegram/wrong'.format(hood_id), headers=auth_header
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@mark.parametrize('bot', [{'api_token': 'apitoken123', 'welcome_message': 'msg'}])
def test_telegram_delete_bot_unauthorized(client, bot, telegram):
    response = client.delete('/api/hoods/{0}/telegram/{1}'.format(telegram.hood.id, telegram.id))
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
