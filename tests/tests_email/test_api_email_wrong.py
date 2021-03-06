# Copyright (C) 2020 by Maike <maike@systemli.org>
# Copyright (C) 2020 by Martin Rey <martin.rey@mailbox.org>
#
# SPDX-License-Identifier: 0BSD

from fastapi import status
from nacl.exceptions import CryptoError


def test_email_subscribe_empty(client, hood_id):
    response = client.post('/api/hoods/{0}/email/subscribe/'.format(hood_id))
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_email_subscribe_confirm_wrong_token(client, hood_id):
    try:
        response = client.post(
            '/api/hoods/{0}/email/subscribe/confirm/'.format(hood_id)
            + 'asdfasdfasdfasdfasdfasdfasdfasdf'
        )
        assert response.status_code is not status.HTTP_201_CREATED
    except CryptoError:
        pass


def test_email_subscribe_confirm_wrong_hood(client):
    response = client.delete(
        '/api/hoods/99999/email/unsubscribe/asdfasdfasdfasdfasdfasdfasdfasdf'
    )
    assert response.json()['detail'] == 'Not Found'


def test_email_message_wrong(client, hood_id, email_row):
    body = {
        'text': '',
        'author': 'test@localhost',
        'secret': email_row['secret'],
    }
    response = client.post('/api/hoods/{0}/email/messages/'.format(hood_id), json=body)
    assert response.status_code == status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS


def test_email_unsubscribe_wrong_token(client, hood_id):
    try:
        client.delete(
            '/api/hoods/{0}/email/unsubscribe/asdfasdfasdfasdfasdfasdfasdfasdf'.format(
                hood_id
            )
        )
    except CryptoError:
        pass


def test_email_unsubscribe_wrong_hood(client):
    response = client.delete(
        '/api/hoods/99999/email/unsubscribe/asdfasdfasdfasdfasdfasdfasdfasdf'
    )
    assert response.json()['detail'] == 'Not Found'
