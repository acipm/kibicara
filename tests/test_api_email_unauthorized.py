# Copyright (C) 2020 by Maike <maike@systemli.org>
#
# SPDX-License-Identifier: 0BSD

from fastapi import status


def test_email_create_unauthorized(client, hood_id):
    response = client.post('/api/hoods/%d/email/' % hood_id)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_email_delete_unauthorized(client, hood_id):
    response = client.delete('/api/hoods/%d/email/' % hood_id)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_email_subscribe(client, hood_id):
    response = client.post('/api/hoods/%d/email/subscribe/' % hood_id)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_email_subscribe_confirm(client, hood_id):
    response = client.post('/api/hoods/%d/email/subscribe/confirm/asdf' % hood_id)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_email_unsubscribe(client, hood_id):
    response = client.get('/api/hoods/%d/email/unsubscribe/asdf' % hood_id)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
