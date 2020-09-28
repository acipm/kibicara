# Copyright (C) 2020 by Christian <c.hagenest@pm.me>
# Copyright (C) 2020 by Thomas Lindner <tom@dl6tom.de>
# Copyright (C) 2020 by Martin Rey <martin.rey@mailbox.org>
#
# SPDX-License-Identifier: 0BSD

from fastapi import status


def test_test_read_all_unauthorized(client, hood_id):
    response = client.get('/api/hoods/{0}/test/'.format(hood_id))
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_test_create_unauthorized(client, hood_id):
    response = client.post('/api/hoods/{0}/test/'.format(hood_id))
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_test_read_unauthorized(client, hood_id, test_id):
    response = client.get('/api/hoods/{0}/test/{1}'.format(hood_id, test_id))
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_test_delete_unauthorized(client, hood_id, test_id):
    response = client.delete('/api/hoods/{0}/test/{1}'.format(hood_id, test_id))
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_test_message_read_all_unauthorized(client, hood_id, test_id):
    response = client.get('/api/hoods/{0}/test/{1}/messages/'.format(hood_id, test_id))
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_test_message_create_unauthorized(client, hood_id, test_id):
    response = client.post('/api/hoods/{0}/test/{1}/messages/'.format(hood_id, test_id))
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
