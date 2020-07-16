# Copyright (C) 2020 by Maike <maike@systemli.org>
#
# SPDX-License-Identifier: 0BSD

from fastapi import status
from kibicara.webapi.admin import to_token
import subprocess
from pytest import skip
from re import findall
from urllib.parse import urlparse


def test_email_subscribe_unsubscribe(client, hood_id, receive_email):
    response = client.post(
        '/api/hoods/%d/email/subscribe/' % hood_id, json={'email': 'test@localhost'}
    )
    assert response.status_code == status.HTTP_202_ACCEPTED
    mail = receive_email()
    body = mail['body']
    confirm_url = findall(
        'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
        body,
    )[0]
    print(urlparse(confirm_url).path)
    response = client.post(urlparse(confirm_url).path)
    assert response.status_code == status.HTTP_201_CREATED
    response = client.post(urlparse(confirm_url).path)
    assert response.status_code == status.HTTP_409_CONFLICT
    token = to_token(email=mail['to'], hood=hood_id)
    response = client.delete('/api/hoods/%d/email/unsubscribe/%s' % (hood_id, token))
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_email_message(client, hood_id, trigger_id, email_row):
    body = {
        'text': "test",
        'author': "test@localhost",
        'secret': email_row['secret'],
    }
    response = client.post('/api/hoods/%d/email/messages/' % hood_id, json=body)
    assert response.status_code == status.HTTP_201_CREATED


def test_email_send_mda(trigger_id, email_row):
    skip('Only works if kibicara is listening on port 8000, and only sometimes')
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
