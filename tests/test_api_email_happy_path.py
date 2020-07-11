# Copyright (C) 2020 by Maike <maike@systemli.org>
#
# SPDX-License-Identifier: 0BSD

from fastapi import status
from logging import getLogger, INFO, WARNING, Handler
from kibicara.webapi.admin import to_token


class CaptureHandler(Handler):
    def __init__(self):
        super().__init__()
        self.records = []

    def emit(self, record):
        self.records.append(record)


def test_email_create(client, hood_id, auth_header):
    response = client.post('/api/hoods/%d/email/' % hood_id, headers=auth_header)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["hood"]["id"] == hood_id
    # response = client.post('/api/hoods/%d/email/' % hood_id, headers=auth_header)
    # assert response.status_code == status.HTTP_409_CONFLICT


def test_email_subscribe(client, hood_id):
    logger = getLogger()
    capture = CaptureHandler()
    logger.setLevel(INFO)
    logger.addHandler(capture)
    response = client.post(
        '/api/hoods/%d/email/subscribe/' % hood_id, json={'email': 'test@localhost'}
    )
    logger.setLevel(WARNING)
    logger.removeHandler(capture)
    assert response.status_code == status.HTTP_502_BAD_GATEWAY
    token = capture.records[0].message
    response = client.get('/api/hoods/%d/email/subscribe/confirm/%s' % (hood_id, token))
    assert response.status_code == status.HTTP_201_CREATED
    # response = client.get('/api/hoods/%d/email/subscribe/confirm/%s' % (hood_id, token))
    # assert response.status_code == status.HTTP_409_CONFLICT


def test_email_message(client, hood_id, trigger_id, email_row):
    body = {
        'text': "test",
        'author': "test@localhost",
        'secret': email_row['secret'],
    }
    response = client.post(
        '/api/hoods/%d/email/messages/%d' % (hood_id, email_row['id']), json=body
    )
    assert response.status_code == status.HTTP_201_CREATED


def test_email_unsubscribe(client, hood_id):
    test_email_subscribe(client, hood_id)
    token = to_token(email="user@localhost", hood=hood_id)
    response = client.get('/api/hoods/%d/email/unsubscribe/%s' % (hood_id, token))
    assert response.status_code == status.HTTP_200_OK


# def test_email_send_mda -> call kibicara_mda.py like an MDA would
# def test_email_delete
