# Copyright (C) 2020 by Thomas Lindner <tom@dl6tom.de>
#
# SPDX-License-Identifier: 0BSD

from fastapi import FastAPI, status
from fastapi.testclient import TestClient
from kibicara.model import Mapping
from kibicara.webapi import router
from logging import getLogger, Handler, INFO, WARNING
from pytest import fixture


@fixture(scope='module')
def client():
    Mapping.drop_all()
    Mapping.create_all()
    app = FastAPI()
    app.include_router(router, prefix='/api')
    return TestClient(app)


class CaptureHandler(Handler):
    def __init__(self):
        super().__init__()
        self.records = []

    def emit(self, record):
        self.records.append(record)


@fixture(scope='module')
def register_token(client):
    # can't use the caplog fixture, since it has only function scope
    logger = getLogger()
    capture = CaptureHandler()
    logger.setLevel(INFO)
    logger.addHandler(capture)
    client.post('/api/admin/register/', json={'email': 'user', 'password': 'pass'})
    logger.setLevel(WARNING)
    logger.removeHandler(capture)
    return capture.records[0].message


@fixture(scope='module')
def register_confirmed(client, register_token):
    response = client.post('/api/admin/confirm/%s' % register_token)
    assert response.status_code == status.HTTP_200_OK


@fixture(scope='module')
def access_token(client, register_confirmed):
    response = client.post(
        '/api/admin/login/', data={'username': 'user', 'password': 'pass'}
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
        '/api/hoods/%d/triggers/' % hood_id, json={'pattern': ''}, headers=auth_header
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
