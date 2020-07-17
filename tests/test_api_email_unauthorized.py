# Copyright (C) 2020 by Maike <maike@systemli.org>
# Copyright (C) 2020 by Thomas Lindner <tom@dl6tom.de>
#
# SPDX-License-Identifier: 0BSD

from fastapi import status


def test_email_create_unauthorized(client, hood_id):
    response = client.post('/api/hoods/%d/email/' % hood_id)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_email_delete_unauthorized(client, hood_id, email_row):
    response = client.delete('/api/hoods/%d/email/%d' % (hood_id, email_row['id']))
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_email_message_unauthorized(client, hood_id, email_row):
    body = {"text": "test", "author": "author", "secret": "wrong"}
    response = client.post('/api/hoods/%d/email/messages/' % hood_id, json=body)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
