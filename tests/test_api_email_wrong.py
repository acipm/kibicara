# Copyright (C) 2020 by Maike <maike@systemli.org>
#
# SPDX-License-Identifier: 0BSD

from fastapi import status
from nacl.exceptions import CryptoError


def test_email_subscribe_empty(client, hood_id):
    response = client.post('/api/hoods/%d/email/subscribe/' % hood_id)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_email_subscribe_confirm_wrong_token(client, hood_id):
    try:
        client.get(
            '/api/hoods/%d/email/subscribe/confirm/asdfasdfasdfasdfasdfasdfasdfasdf'
            % hood_id
        )
    except CryptoError:
        pass


def test_email_subscribe_confirm_wrong_hood(client):
    response = client.get(
        '/api/hoods/99999/email/unsubscribe/asdfasdfasdfasdfasdfasdfasdfasdf'
    )
    assert response.json()['detail'] == 'Not Found'


def test_email_unsubscribe_wrong_token(client, hood_id):
    try:
        client.get(
            '/api/hoods/%d/email/unsubscribe/asdfasdfasdfasdfasdfasdfasdfasdf' % hood_id
        )
    except CryptoError:
        pass


def test_email_unsubscribe_wrong_hood(client):
    response = client.get(
        '/api/hoods/99999/email/unsubscribe/asdfasdfasdfasdfasdfasdfasdfasdf'
    )
    assert response.json()['detail'] == 'Not Found'
