# Copyright (C) 2020 by Thomas Lindner <tom@dl6tom.de>
# Copyright (C) 2020 by Christian Hagenest <c.hagenest@pm.me>
#
# SPDX-License-Identifier: 0BSD

from fastapi import FastAPI, status
from fastapi.testclient import TestClient
from kibicara import email
from kibicara.model import Mapping
from kibicara.webapi import router
from pytest import fixture


@fixture(scope='module')
def client():
    Mapping.drop_all()
    Mapping.create_all()
    app = FastAPI()
    app.include_router(router, prefix='/api')
    return TestClient(app)


@fixture(scope='module')
def monkeymodule():
    from _pytest.monkeypatch import MonkeyPatch

    mpatch = MonkeyPatch()
    yield mpatch
    mpatch.undo()


@fixture(scope='module')
def receive_email(monkeymodule):
    mailbox = []

    def mock_send_email(to, subject, sender='kibicara', body=''):
        mailbox.append(dict(to=to, subject=subject, sender=sender, body=body))

    def mock_receive_email():
        return mailbox.pop()

    monkeymodule.setattr(email, 'send_email', mock_send_email)
    return mock_receive_email


@fixture(scope='module')
def register_token(client, receive_email):
    response = client.post(
        '/api/admin/register/', json={'email': 'user', 'password': 'password'}
    )
    assert response.status_code == status.HTTP_202_ACCEPTED
    return receive_email()['body']


@fixture(scope='module')
def register_confirmed(client, register_token):
    response = client.post('/api/admin/confirm/%s' % register_token)
    assert response.status_code == status.HTTP_200_OK


@fixture(scope='module')
def access_token(client, register_confirmed):
    response = client.post(
        '/api/admin/login/', data={'username': 'user', 'password': 'password'}
    )
    assert response.status_code == status.HTTP_200_OK
    return response.json()['access_token']


@fixture(scope='module')
def auth_header(access_token):
    return {'Authorization': 'Bearer %s' % access_token}


@fixture(scope='function')
def hood_id(client, auth_header):
    response = client.post('/api/hoods/', json={'name': 'hood'}, headers=auth_header)
    assert response.status_code == status.HTTP_201_CREATED
    hood_id = int(response.headers['Location'])
    yield hood_id
    client.delete('/api/hoods/%d' % hood_id, headers=auth_header)


@fixture(scope='function')
def trigger_id(client, hood_id, auth_header):
    response = client.post(
        '/api/hoods/%d/triggers/' % hood_id, json={'pattern': 'te'}, headers=auth_header
    )
    assert response.status_code == status.HTTP_201_CREATED
    trigger_id = int(response.headers['Location'])
    yield trigger_id
    client.delete(
        '/api/hoods/%d/triggers/%d' % (hood_id, trigger_id), headers=auth_header
    )


@fixture(scope='function')
def badword_id(client, hood_id, auth_header):
    response = client.post(
        '/api/hoods/%d/badwords/' % hood_id, json={'pattern': ''}, headers=auth_header
    )
    assert response.status_code == status.HTTP_201_CREATED
    badword_id = int(response.headers['Location'])
    yield badword_id
    client.delete(
        '/api/hoods/%d/badwords/%d' % (hood_id, badword_id), headers=auth_header
    )


@fixture(scope='function')
def test_id(client, hood_id, auth_header):
    response = client.post(
        '/api/hoods/%d/test/' % hood_id, json={}, headers=auth_header
    )
    assert response.status_code == status.HTTP_201_CREATED
    test_id = int(response.headers['Location'])
    yield test_id
    client.delete('/api/hoods/%d/test/%d' % (hood_id, test_id), headers=auth_header)


@fixture(scope="function")
def email_row(client, hood_id, auth_header):
    response = client.post('/api/hoods/%d/email/' % hood_id, headers=auth_header)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["hood"]["id"] == hood_id
    email_row = response.json()
    yield email_row
    # not sure if necessary; it raises problems at least
    # client.delete('/api/hoods/%d/email/' % hood_id, headers=auth_header)
