# Copyright (C) 2020 by Maike <maike@systemli.org>
#
# SPDX-License-Identifier: 0BSD

import email.parser
from email.policy import default
import email.message
import sys
import re
import requests
from logging import getLogger
from kibicara.model import Hood
from kibicara.platforms.email.model import Email
import argparse
from asyncio import run
from fastapi import status
from ormantic import NoMatch


async def async_main(mail=None, hood_name=None):
    logger = getLogger(__name__)

    # the MDA passes the recipient address as command line argument
    parser = argparse.ArgumentParser()
    if hood_name is None:
        parser.add_argument("recipient_address")
        args = parser.parse_args()
        # extract hood name from the envelope recipient address
        hood_name = args.recipient_address.split('@')[0].lower()

    if mail is None:
        # read mail from STDIN
        mail = bytes(sys.stdin.read(), encoding='ascii')
        # parse plaintext to email.EmailMessage object
        mail = email.parser.BytesParser(policy=default).parsebytes(mail)
    else:
        mail = email.parser.Parser(policy=default).parsestr(mail)

    assert type(mail) == email.message.EmailMessage

    # extract relevant data from mail
    body = mail.get_body(preferencelist=('plain', 'html'))
    if body['content-type'].subtype == 'plain':
        text = str(body.get_content())
    elif body['content-type'].subtype == 'html':
        text = re.sub(r'<[^>]*>', '', body.get_content())

    try:
        text = str(text)
    except UnboundLocalError:
        print('No suitable message body')
        exit(1)
    try:
        hood = await Hood.objects.get(name=hood_name)
    except NoMatch:
        print('No hood with this name')
        exit(1)
    email_row = await Email.objects.get(hood=hood)
    body = {
        'text': text,
        'author': mail.get_unixfrom(),
        'secret': email_row.secret,
    }
    response = requests.post(
        'http://localhost:8000/api/hoods/%d/email/messages/' % hood.id, json=body
    )
    print("Request sent:")
    if response.status_code == status.HTTP_201_CREATED:
        exit(0)
    elif response.status_code == status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS:
        print("Message was't accepted: " + text)
    elif response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY:
        print("Malformed request: " + str(response.json()))
    elif response.status_code == status.HTTP_401_UNAUTHORIZED:
        logger.error('Wrong API secret. kibicara_mda seems to be misconfigured')
    else:
        print(str(response.status_code))
    exit(1)


def main():
    run(async_main())


if __name__.endswith('kibicara_mda'):
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
    run(async_main(mail=mail, hood_name='hood'))
