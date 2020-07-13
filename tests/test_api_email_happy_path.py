# Copyright (C) 2020 by Maike <maike@systemli.org>
#
# SPDX-License-Identifier: 0BSD

from fastapi import status
from logging import getLogger, INFO, WARNING, Handler
from kibicara.webapi.admin import to_token
import subprocess


class CaptureHandler(Handler):
    def __init__(self):
        super().__init__()
        self.records = []

    def emit(self, record):
        self.records.append(record)


def test_email_subscribe(client, hood_id, email_row):
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
    response = client.post('/api/hoods/%d/email/messages/' % hood_id, json=body)
    assert response.status_code == status.HTTP_201_CREATED


def test_email_unsubscribe(client, hood_id, email_row):
    test_email_subscribe(client, hood_id, email_row)
    token = to_token(email="user@localhost", hood=hood_id)
    response = client.get('/api/hoods/%d/email/unsubscribe/%s' % (hood_id, token))
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_email_send_mda(client, auth_header, hood_id, test_id, trigger_id, email_row):
    mail = """From test@example.com Tue Jun 16 15:33:19 2020
Return-path: <test@example.com>
Envelope-to: hood@localhost
Delivery-date: Tue, 16 Jun 2020 15:33:19 +0200
Received: from [23.143.35.123] (helo=example.com)
        by example.com with smtp (Exim 4.89)
        (envelope-from <test@example.com>)
        id 1jlC1e-0005ro-PL
        for hood@localhost; Tue, 16 Jun 2020 15:33:19 +0200
Message-ID: <B5F50812.F55DFD8B@example.com>
Date: Tue, 16 Jun 2020 06:53:19 -0700
Reply-To: "Test" <test@example.com>
From: "Test" <test@example.com>
User-Agent: Mozilla/5.0 (Windows; U; Windows NT 5.1; fr; rv:1.8.1.17) Gecko/20080914 Thunderbird/2.0.0.17
MIME-Version: 1.0
To: <hood@localhost>
Subject: Chat: test
Content-Type: multipart/mixed; boundary="AqNPlAX243a8sip3B7kXv8UKD8wuti"


--AqNPlAX243a8sip3B7kXv8UKD8wuti
Content-Type: text/plain; charset=utf-8

test

--AqNPlAX243a8sip3B7kXv8UKD8wuti--
    """
    proc = subprocess.run(
        ["kibicara_mda", "hood"], stdout=subprocess.PIPE, input=mail, encoding='ascii'
    )
    assert proc.returncode == 0
    # Check whether mail was received and accepted
    response = client.get(
        '/api/hoods/%d/test/%d/messages' % (hood_id, test_id), headers=auth_header
    )
    print(response)
    print(response.json())
    assert False
