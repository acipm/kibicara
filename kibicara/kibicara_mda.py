# Copyright (C) 2020 by Maike <maike@systemli.org>
#
# SPDX-License-Identifier: 0BSD

import email.parser
import sys
import re
import requests
from logging import getLogger
from kibicara.platforms.email.model import Email
from kibicara.model import Hood


def main():
    logger = getLogger(__name__)

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
            if not text:
                logger.error('No suitable message body')
                exit(0)
        except Exception:
            logger.info("No Body in this message part", exc_info=True)
            exit(0)
    to = mail['To'].lower()
    hood_name = to.split('@')[0]
    hood = await Hood.objects.get(name=hood_name)
    body = {
        'text': text,
        'author': mail.get_unixfrom(),
        'secret': Email.secret,
    }
    requests.post('http://localhost/api/' + hood.id + '/email/messages/', data=body)
