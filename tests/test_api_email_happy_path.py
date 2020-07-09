# Copyright (C) 2020 by Maike <maike@systemli.org>
#
# SPDX-License-Identifier: 0BSD

from fastapi import status
from logging import getLogger, INFO, WARNING, Handler


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


def test_email_subscribe(client, hood_id, auth_header):
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


# def test_email_subscribe_confirm
# def test_email_send_mda -> call kibicara_mda.py like an MDA would
# def test_email_message -> write directly to API
# def test_email_delete