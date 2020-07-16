# Copyright (C) 2020 by Christian Hagenest <c.hagenest@pm.me>
# Copyright (C) 2020 by Thomas Lindner <tom@dl6tom.de>
#
# SPDX-License-Identifier: 0BSD

from fastapi import status


def test_hood_read_all(client):
    response = client.get('/api/hoods/')
    assert response.status_code == status.HTTP_200_OK


def test_hood_create_unauthorized(client, hood_id):
    response = client.post('/api/hoods/')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_hood_read_unauthorized(client, hood_id):
    response = client.get('/api/hoods/%d' % hood_id)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_hood_update_unauthorized(client, hood_id):
    response = client.put('/api/hoods/%d' % hood_id)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_hood_delete_unauthorized(client, hood_id):
    response = client.delete('/api/hoods/%d' % hood_id)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_trigger_read_all_unauthorized(client, hood_id):
    response = client.get('/api/hoods/%d/triggers/' % hood_id)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_trigger_create_unauthorized(client, hood_id):
    response = client.post('/api/hoods/%d/triggers/' % hood_id)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_trigger_read_unauthorized(client, hood_id, trigger_id):
    response = client.get('/api/hoods/%d/triggers/%d' % (hood_id, trigger_id))
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_trigger_update_unauthorized(client, hood_id, trigger_id):
    response = client.put('/api/hoods/%d/triggers/%d' % (hood_id, trigger_id))
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_trigger_delete_unauthorized(client, hood_id, trigger_id):
    response = client.delete('/api/hoods/%d/triggers/%d' % (hood_id, trigger_id))
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_badword_read_all_unauthorized(client, hood_id):
    response = client.get('/api/hoods/%d/badwords/' % hood_id)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_badword_create_unauthorized(client, hood_id):
    response = client.post('/api/hoods/%d/badwords/' % hood_id)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_badword_read_unauthorized(client, hood_id, badword_id):
    response = client.get('/api/hoods/%d/badwords/%d' % (hood_id, badword_id))
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_badword_update_unauthorized(client, hood_id, badword_id):
    response = client.put('/api/hoods/%d/badwords/%d' % (hood_id, badword_id))
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_badword_delete_unauthorized(client, hood_id, badword_id):
    response = client.delete('/api/hoods/%d/badwords/%d' % (hood_id, badword_id))
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
