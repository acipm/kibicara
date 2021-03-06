# Copyright (C) 2020 by Cathy Hu <cathy.hu@fau.de>
# Copyright (C) 2020 by Martin Rey <martin.rey@mailbox.org>
#
# SPDX-License-Identifier: 0BSD

from fastapi import status
from pytest import mark


@mark.parametrize('bot', [{'api_token': 'apitoken123', 'welcome_message': 'msg'}])
def test_telegram_get_bot(client, auth_header, event_loop, bot, telegram):
    response = client.get(
        '/api/hoods/{0}/telegram/{1}'.format(telegram.hood.id, telegram.id),
        headers=auth_header,
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['id'] == telegram.id
    assert response.json()['api_token'] == telegram.api_token
    assert response.json()['welcome_message'] == telegram.welcome_message


def test_telegram_get_bot_invalid_id(client, auth_header, hood_id):
    response = client.get('/api/hoods/1337/telegram/123', headers=auth_header)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    response = client.get('/api/hoods/wrong/telegram/123', headers=auth_header)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    response = client.get(
        '/api/hoods/{0}/telegram/7331'.format(hood_id), headers=auth_header
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    response = client.get(
        '/api/hoods/{0}/telegram/wrong'.format(hood_id), headers=auth_header
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@mark.parametrize('bot', [{'api_token': 'apitoken456', 'welcome_message': 'msg'}])
def test_telegram_get_bot_unauthorized(client, bot, telegram):
    response = client.get(
        '/api/hoods/{0}/telegram/{1}'.format(telegram.hood.id, telegram.id)
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
