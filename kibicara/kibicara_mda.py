# Copyright (C) 2020 by Maike <maike@systemli.org>
#
# SPDX-License-Identifier: 0BSD

import email.parser
import sys
import re
import requests
from logging import getLogger
from kibicara.model import Hood
from kibicara.platforms.email.webapi import get_email
import argparse


async def main():
    logger = getLogger(__name__)

    # the MDA passes the recipient address as command line argument
    parser = argparse.ArgumentParser()
    parser.add_argument("recipient_address")
    args = parser.parse_args()

    # read mail from STDIN
    mailbytes = bytes(sys.stdin.read())

    # parse plaintext to email.EmailMessage object
    myparser = email.parser.BytesParser()
    mail = myparser.parsebytes(mailbytes)

    # extract relevant data from mail
    for part in mail.walk():
        try:
            text = part.get_body(('plain',))
            if not text:
                text = re.sub(r'<[^>]*>', '', part.get_body(('html',)))
        except Exception:
            logger.info("No Body in this message part", exc_info=True)
    if not text:
        logger.error('No suitable message body')
        exit(0)
    # extract hood name from the envelope recipient address
    hood_name = args.recipient_address.split('@')[0]
    hood = await Hood.objects.get(name=hood_name)
    email_row = await get_email(hood=hood.id)
    body = {
        'text': text,
        'author': mail.get_unixfrom(),
        'secret': email_row.secret,
    }
    requests.post('http://localhost:8000/api/hoods/%d/email/messages/' % (hood.id), data=body)
