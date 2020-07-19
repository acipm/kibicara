# Copyright (C) 2020 by Cathy Hu <cathy.hu@fau.de>
#
# SPDX-License-Identifier: 0BSD

from fastapi import status
from kibicara.platforms.telegram.model import Telegram, TelegramUser
from ormantic.exceptions import NoMatch
from pytest import mark, raises


@mark.parametrize('bot', [{'api_token': 'apitoken123', 'welcome_message': 'msg'}])
def test_telegram_delete_bot(client, event_loop, bot, telegram, auth_header):
    event_loop.run_until_complete(
        TelegramUser.objects.create(user_id=1234, bot=telegram.id)
    )
    event_loop.run_until_complete(
        TelegramUser.objects.create(user_id=5678, bot=telegram.id)
    )
    response = client.delete(
        f'/api/hoods/{telegram.hood.id}/telegram/{telegram.id}', headers=auth_header
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
    response = client.delete(f'/api/hoods/{hood_id}/telegram/7331', headers=auth_header)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    response = client.delete(
        f'/api/hoods/{hood_id}/telegram/wrong', headers=auth_header
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@mark.parametrize('bot', [{'api_token': 'apitoken123', 'welcome_message': 'msg'}])
def test_telegram_delete_bot_unauthorized(client, bot, telegram):
    response = client.delete(f'/api/hoods/{telegram.hood.id}/telegram/{telegram.id}')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
