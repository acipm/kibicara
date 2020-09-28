# Copyright (C) 2020 by Cathy Hu <cathy.hu@fau.de>
# Copyright (C) 2020 by Martin Rey <martin.rey@mailbox.org>
#
# SPDX-License-Identifier: 0BSD

from fastapi import status
from kibicara.model import Hood
from kibicara.platforms.telegram.model import Telegram


def test_telegram_get_bots(client, auth_header, event_loop, hood_id):
    hood = event_loop.run_until_complete(Hood.objects.get(id=hood_id))
    telegram0 = event_loop.run_until_complete(
        Telegram.objects.create(
            hood=hood,
            api_token='api_token123',
            welcome_message='welcome_message123',
        )
    )
    telegram1 = event_loop.run_until_complete(
        Telegram.objects.create(
            hood=hood,
            api_token='api_token456',
            welcome_message='welcome_message123',
        )
    )
    response = client.get(
        '/api/hoods/{0}/telegram'.format(telegram0.hood.id), headers=auth_header
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()[0]['id'] == telegram0.id
    assert response.json()[0]['api_token'] == telegram0.api_token
    assert response.json()[1]['id'] == telegram1.id
    assert response.json()[1]['api_token'] == telegram1.api_token


def test_telegram_get_bots_invalid_id(client, auth_header, hood_id):
    response = client.get('/api/hoods/1337/telegram', headers=auth_header)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    response = client.get('/api/hoods/wrong/telegram', headers=auth_header)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_telegram_get_bots_unauthorized(client, hood_id):
    response = client.get('/api/hoods/{0}/telegram'.format(hood_id))
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
