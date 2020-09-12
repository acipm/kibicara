# Copyright (C) 2020 by Cathy Hu <cathy.hu@fau.de>
#
# SPDX-License-Identifier: 0BSD

from fastapi import status
from kibicara.platforms import telegram
from kibicara.platforms.telegram.model import Telegram
from pytest import fixture, mark


@fixture(scope='function')
def disable_spawner(monkeypatch):
    class DoNothing:
        def start(self, bot):
            assert bot is not None

    monkeypatch.setattr(telegram.webapi, 'spawner', DoNothing())


@mark.parametrize('body', [{'api_token': 'string', 'welcome_message': 'string'}])
def test_telegram_create_bot(
    event_loop,
    client,
    disable_spawner,
    hood_id,
    auth_header,
    monkeypatch,
    body,
):
    def check_token_mock(token):
        return True

    monkeypatch.setattr(telegram.webapi, 'check_token', check_token_mock)

    response = client.post(
        f'/api/hoods/{hood_id}/telegram/',
        json=body,
        headers=auth_header,
    )
    assert response.status_code == status.HTTP_201_CREATED
    bot_id = response.json()['id']
    telegram_obj = event_loop.run_until_complete(Telegram.objects.get(id=bot_id))
    assert response.json()['api_token'] == body['api_token'] == telegram_obj.api_token
    assert (
        response.json()['welcome_message']
        == body['welcome_message']
        == telegram_obj.welcome_message
    )
    assert response.json()['hood']['id'] == telegram_obj.hood.id
    assert telegram_obj.enabled


@mark.parametrize('body', [{'api_token': 'string', 'welcome_message': 'string'}])
def test_telegram_invalid_api_token(
    event_loop,
    client,
    disable_spawner,
    hood_id,
    auth_header,
    monkeypatch,
    body,
):
    response = client.post(
        f'/api/hoods/{hood_id}/telegram/',
        json=body,
        headers=auth_header,
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_telegram_create_telegram_invalid_id(client, auth_header):
    response = client.post('/api/hoods/1337/telegram/', headers=auth_header)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    response = client.post('/api/hoods/wrong/telegram/', headers=auth_header)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_telegram_create_unauthorized(client, hood_id):
    response = client.post('/api/hoods/{hood_id}/telegram/')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
